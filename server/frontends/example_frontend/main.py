from server.shellman import ShellmanCore


class ShellmanFrontend:
    def __init__(self):
        pass

    async def on_connection(self, connection_id):
        print(f"example_frontend: connection {connection_id} received, listening")
        ShellmanCore().add_frontend_to_connection(connection_id, self)

    async def on_read(self, conn_id, data):
        print(f'example_frontend: received data from connection {conn_id}: {data} - sending back the same')
        await ShellmanCore().write_to_connection(conn_id, data, self)

    async def on_disconnect(self, conn_id):
        print(f'example_frontend: {conn_id} disconnected :(')

    async def on_write_by_other(self, conn_id, data):
        print(f'example_frontend: another frontend wrote {data} to {conn_id}')
