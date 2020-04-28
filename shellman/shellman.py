import importlib
import socket
import asyncio
import ssl
import os

from .singleton import singleton
from .config import Config
from .connection import Connection


@singleton
class ShellmanCore:
    connection_id_ctr = 0
    frontends = []
    connections = []
    servers = []
    ssl_ctx = None

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

    async def start_listening(self, host, port):
        try:
            server = await asyncio.start_server(self.client_connected, host,
                                                port, family=socket.AF_INET, ssl=self.ssl_ctx)
        except (OSError, socket.gaierror) as e:
            print(e)
            return False

        self.servers.append(server)
        return True

    async def stop_listening(self, host, port):
        success = False
        for server in self.servers.copy():
            if success := server.sockets[0].getsockname() == (host, int(port)):
                server.close()
                await server.wait_closed()
                self.servers.remove(server)
                break
        return success

    async def connect_to_bind_shell(self, host, port, ssl=True):
        await self.client_connected(*(await asyncio.open_connection(host, port, ssl=ssl)))

    async def client_connected(self, reader, writer):
        peername: (str, int) = writer.get_extra_info('peername')
        connection_id = self.connection_id_ctr
        self.connection_id_ctr += 1

        print(f'Connection {connection_id} from {peername[0]}:{peername[1]}')

        connection = Connection(reader, writer, connection_id)
        self.connections.append(connection)

        # notify frontends that a new connection is available
        for frontend in self.frontends:
            await frontend.on_connection(connection)

    def import_frontends(self):
        frontend_file_list = os.listdir(f'{os.path.dirname(__file__)}/frontends/')
        for file in frontend_file_list:
            if file.startswith('.') or file == '__pycache__':
                continue
            if file.endswith('.py'):
                file = file[:-3]
            try:
                # import module from the module folder
                module = importlib.import_module(f'..frontends.{file}', __name__)
                print(f'Imported frontend: {module.__name__}')

                # add it to the list to iterate later
                self.frontends.append(module.ShellmanFrontend())
            except Exception as e:
                print(f"Failed to import frontend at {file}")
                print(e)

    async def write(self, connection_id, data, writer):
        await self.connections[connection_id].write(data, writer)

    async def shutdown(self):
        for connection in self.connections:
            connection.writer.close()
            await connection.writer.wait_closed()
        for frontend in self.frontends:
            await frontend.shutdown()
