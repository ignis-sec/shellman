import asyncio

from ...config import Config
from .shell import Shell
from .discord_client import DiscordClient
from ...wizard import prompt_configs, check_config
from ...frontend import ShellmanFrontend
from .config import config_dict


class DiscordFrontend(ShellmanFrontend):
    discord_client = None
    shells = {}
    guild = None

    def __init__(self):
        if not check_config(config_dict):
            prompt_configs(config_dict)
            Config().write()

        self.discord_client = DiscordClient(shellman_frontend=self)
        asyncio.get_event_loop().create_task(self.discord_client.start(Config()['discord_frontend']['token']))

    async def on_connection(self, connection):
        if Config()['discord_frontend'].getboolean('admin_mode'):
            connection.add_frontend(self)
            self.shells[connection.id] = shell = Shell(connection=connection)
            shell.name = self.get_default_channel_name(shell)
            await self.create_shell_channel(shell)
        else:
            await self.discord_client.main_channel.send(f'New connection {connection.id} available!')

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

    async def on_disconnect(self, connection):
        await self.shells[connection.id].channel.send('Disconnected :(')
        del self.shells[connection.id]

    async def on_write_by_other(self, connection, data):
        shell = self.shells[connection.id]
        async with shell.buffer_lock:
            shell.buffer += f'o> {data}\n'

    async def shutdown(self):
        await self.discord_client.logout()

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

    async def create_shell_channel(self, shell):
        shell.channel = await self.discord_client.guild.create_text_channel(name=shell.name,
                                                                            category=self.discord_client.category)

    @staticmethod
    def get_default_channel_name(shell):
        return eval(
            "f'{}'".format(Config()['discord_frontend']['channel_scheme']),
            {'shell': shell}
        )