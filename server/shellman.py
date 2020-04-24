import importlib
import socket
import asyncio
import ssl
import os

from .singleton import singleton
from .config import Config


@singleton
class ShellmanCore:
    connections = {}
    connection_id_ctr = 0
    frontends = []
    ssl_ctx = None
    loop = None

    def __init__(self):
        print("Initializing ShellmanCore")
        # set up ssl context
        self.ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

        with open("./cert.pem", "w") as cert:
            cert.write(Config()['tls']['cert'])
        with open("./private.key", "w") as cert:
            cert.write(Config()['tls']['key'])

        self.ssl_ctx.load_cert_chain('./cert.pem', './private.key')

        os.remove('./cert.pem')
        os.remove('./private.key')

        self.loop = asyncio.get_event_loop()

        self.loop.create_task(self.start_listening(Config()['connection']['port']))
        # loop.create_task(self.read_loop())
        # start checking connections' readers for updates

    async def start_listening(self, port):
        server = await asyncio.start_server(self.client_connected, Config()['connection']['host'],
                                            port, family=socket.AF_INET, ssl=self.ssl_ctx)
        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr[0]}:{addr[1]}')

    async def client_connected(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peername: (str, int) = writer.get_extra_info('peername')
        connection_id = self.connection_id_ctr
        self.connection_id_ctr += 1

        print(f'Connection {connection_id} from {peername[0]}:{peername[1]}')

        self.connections[connection_id] = (
            reader, writer, [], self.loop.create_task(self.read_loop(connection_id)), asyncio.Lock()
        )

        # notify frontends that a new connection is available
        for frontend in self.frontends:
            await frontend.on_connection(connection_id=connection_id)

    async def write_to_connection(self, connection_id, data, writer):
        conn = self.connections[connection_id]
        for frontend in conn[2]:
            if frontend != writer:
                await frontend.on_write_by_other(connection_id, data)
        async with conn[4]:
            conn[1].write(data)

    async def read_loop(self, connection_id):
        conn = self.connections[connection_id]
        while True:
            data = await conn[0].readline()
            if data == b'':
                await self.disconnected(connection_id)
                break
            for frontend in conn[2]:
                await frontend.on_read(connection_id, data)

    async def disconnected(self, connection_id):
        conn = self.connections[connection_id]
        for frontend in conn[2]:
            await frontend.on_disconnect(connection_id)

        del self.connections[connection_id]

    def import_frontends(self):
        frontend_file_list = os.listdir(f'{os.path.dirname(__file__)}/frontends/')
        for file in frontend_file_list:
            if file in ['.', '..']:
                continue

            try:
                # import module from the module folder
                module = importlib.import_module(f'..frontends.{file}', __name__)
                print(f'Imported frontend: {module.__name__}')

                # add it to the list to iterate later
                self.frontends.append(module.ShellmanFrontend())
            except Exception as e:
                print(f"Failed to import frontend at {file}")
                print(e)

    def add_frontend_to_connection(self, connection_id, frontend):
        self.connections[connection_id][2].append(frontend)
