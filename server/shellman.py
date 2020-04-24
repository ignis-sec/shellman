import socket
import asyncio

from singleton import singleton
from config import Config
from wizard import shellman_wizard


@singleton
class ShellmanCore:
    connections = []
    ssl_ctx = None

    def __init__(self):
        # set up ssl context
        # import modules

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.create_task(self.start_listening(Config()['connection']['port']))
        loop.create_task(self.start_listening(12111))
        loop.run_forever()
        # start checking connections' readers for updates

    async def start_listening(self, port):
        server = await asyncio.start_server(self.client_connected, Config()['connection']['host'],
                                   port, family=socket.AF_INET, ssl=self.ssl_ctx, start_serving=True)
        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

    async def client_connected(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peername = writer.get_extra_info('peername')
        print('Connection from %s:%s' % peername)
        self.connections.append((reader, writer))
        # notify frontends that a new connection is available


if __name__ == '__main__':
    # check if config exists
    try:
        Config()['shellman']
    except KeyError:
        shellman_wizard()
    ShellmanCore()
