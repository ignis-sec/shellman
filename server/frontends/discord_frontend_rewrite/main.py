import asyncio

from ...config import Config
from .shell import Shell
from .discord_client import DiscordClient


class ShellmanFrontend:
    discord_client = None
    shells = {}
    guild = None

    def __init__(self):
        loop = asyncio.get_event_loop()
        try:
            Config()['discord_frontend']
        except KeyError:
            # TODO: replace this with a wizard?
            print('discord_frontend cannot run without config')
        self.discord_client = DiscordClient(shellman_frontend=self)
        loop.create_task(self.discord_client.start(Config()['discord_frontend']['token']))

    async def on_connection(self, connection):
        print(f"discord_frontend: connection {connection.id} received")
        if Config()['discord_frontend'].getboolean('admin_mode'):
            connection.add_frontend(self)
            self.shells[connection.id] = shell = Shell(connection=connection)
            shell.name = self.get_default_channel_name(shell)
            await self.create_shell_channel(shell)
        else:
            await self.discord_client.main_channel.send(f'New connection {connection.id} available!')

    def get_default_channel_name(self, shell):
        return eval(
            "f'{}'".format(Config()['discord_frontend']['channel_scheme']),
            {'shell': shell}
        )


    async def create_shell_channel(self, shell):
        shell.channel = await self.discord_client.guild.create_text_channel(name=shell.name,
                                                                            category=self.discord_client.category)

    async def on_read(self, connection, data):
        shell = self.shells[connection.id]

        async with shell.buffer_lock:
            shell.buffer += data.decode()

        if shell.write_task:
            shell.write_task.cancel()

        new_write_task = asyncio.get_event_loop().create_task(
            self.send_buffer_to_channel_with_delay(connection, 0.5)
        )

        shell.write_task = new_write_task

    async def send_buffer_to_channel_with_delay(self, connection, delay):
        await asyncio.sleep(delay)

        shell = self.shells[connection.id]
        channel = shell.channel

        data = '```\n'
        for line in shell.buffer.splitlines():
            if len(data) + len(line) <= 1996:
                data += f'{line}\n'
            else:
                await channel.send(f'{data}```')
                data = f'```\n{line}\n'
        if data:
            await channel.send(f'{data}```')

        shell.buffer = ''
        shell.write_task = None

    async def on_disconnect(self, connection):
        await self.shells[connection.id].channel.send('Disconnected :(')
        del self.shells[connection.id]

    async def on_write_by_other(self, connection, data):
        shell = self.shells[connection.id]
        async with shell.buffer_lock:
            shell.buffer += f'o> {data}\n'

    async def shutdown(self):
        await self.discord_client.logout()
