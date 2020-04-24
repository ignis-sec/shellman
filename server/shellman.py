import socket
import asyncio
import ssl
import os

from singleton import singleton
from config import Config
from wizard import shellman_wizard


@singleton
class ShellmanCore:
    connections = {}
    connection_id_ctr = 0
    frontends = []
    ssl_ctx = None

    def __init__(self):
        # set up ssl context
        self.ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

        with open("./cert.pem", "w") as cert:
            cert.write(Config()['tls']['cert'])
        with open("./private.key", "w") as cert:
            cert.write(Config()['tls']['key'])

        self.ssl_ctx.load_cert_chain('./cert.pem', './private.key')

        os.remove('./cert.pem')
        os.remove('./private.key')

        # import frontends
        self.frontends = []

        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)

        loop.create_task(self.start_listening(Config()['connection']['port']))
        # loop.create_task(self.start_listening(12111))
        loop.run_forever()
        # start checking connections' readers for updates

    async def start_listening(self, port):
        server = await asyncio.start_server(self.client_connected, Config()['connection']['host'],
                                            port, family=socket.AF_INET, ssl=self.ssl_ctx)
        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

    async def client_connected(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peername: (str, int) = writer.get_extra_info('peername')
        connection_id = self.connection_id_ctr
        self.connection_id_ctr += 1

        print('Connection %s from %s:%s' % (connection_id, *peername))
        self.connections[connection_id] = (reader, writer, [])

        for frontend in self.frontends:
            frontend.new_connection(id=connection_id)
        # notify frontends that a new connection is available


if __name__ == '__main__':
    # check if config exists
    try:
        Config()['shellman']
    except KeyError:
        shellman_wizard()
    ShellmanCore()
