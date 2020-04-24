from server.shellman import ShellmanCore


class ShellmanFrontend:
    def __init__(self):
        pass

    async def new_connection(self, connection_id):
        print(f"example_frontend: connection {connection_id} received, listening")
        ShellmanCore().add_frontend_to_connection(connection_id, self)
