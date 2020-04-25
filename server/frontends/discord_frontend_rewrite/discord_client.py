import discord

from ...config import Config
from .commands import handle_main_channel_command, handle_shell_command


class DiscordClient(discord.Client):
    def __init__(self, shellman_frontend):
        self.shellman_frontend = shellman_frontend
        super().__init__()

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if message.channel.id == Config()['discord_frontend']['channel']:
            await handle_main_channel_command(message)

        for shell in self.shellman_frontend.shells:
            if message.channel == shell.channel:
                await handle_shell_command(message, shell, self.shellman_frontend)
                break
