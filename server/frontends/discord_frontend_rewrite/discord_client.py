import discord

from ...config import Config
from .commands import handle_main_channel_command, handle_shell_command


class DiscordClient(discord.Client):
    def __init__(self, shellman_frontend):
        self.shellman_frontend = shellman_frontend
        self.guild = None
        self.main_channel = None
        super().__init__()

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        self.guild = self.get_guild(Config()['discord_frontend'].getint('guild'))
        self.main_channel = self.guild.get_channel(Config()['discord_frontend'].getint('channel'))

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.channel == self.main_channel:
            await handle_main_channel_command(message)

        for index, shell in self.shellman_frontend.shells.items():
            if message.channel == shell.channel:
                await handle_shell_command(message, shell, self.shellman_frontend)
                break
