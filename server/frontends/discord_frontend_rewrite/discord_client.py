import discord

from ...config import Config


class DiscordClient(discord.Client):
    def __init__(self, shellman_frontend):
        self.shellman_frontend = shellman_frontend
        super().__init__()

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if message.channel.id == Config()['discord_frontend']['channel']:
            # TODO: implement main channel commands (listen shell, listen port?, list shells)
            pass

        for shell in self.shellman_frontend.shells:
            if message.channel == shell.channel:
                # TODO: implement shell specific commands (^C, flush, clear)
                await shell.connection.write(f'{message.content}\n'.encode(), self.shellman_frontend)
                break
