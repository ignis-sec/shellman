import asyncio

from ...config import Config
from .shell import Shell
from .discord_client import DiscordClient


class ShellmanFrontend:
    discord_client = None
    shells = {}

    def __init__(self):
        loop = asyncio.get_event_loop()
        loop.set_debug(True)  # TODO: remove this
        try:
            Config()['discord_frontend']
        except KeyError:
            # TODO: replace this with a wizard?
            print('discord_frontend cannot run without the discord token set in the config')
        self.discord_client = DiscordClient(shellman_frontend=self)
        loop.create_task(self.discord_client.start(Config()['discord_frontend']['token']))

    async def on_connection(self, connection):
        print(f"discord_frontend: connection {connection.id} received")
        if Config()['discord_frontend']['admin_mode']:
            channel = None  # TODO: create channel, set this to Channel object - naming may have options
            connection.add_frontend(self)
            self.shells[connection.id] = Shell(connection=connection, channel=channel)
        else:
            # TODO: let user know about new connection in configured channel
            # TODO: do admin mode steps 2 and 3 if user runs ?listen <id> <channel>
            pass

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
        # TODO: if admin mode, lock the chat or otherwise indicate it's disconnected

    async def on_write_by_other(self, connection, data):
        shell = self.shells[connection.id]
        async with shell.buffer_lock:
            shell.buffer += f'o> {data}\n'

    async def shutdown(self):
        await self.discord_client.logout()
