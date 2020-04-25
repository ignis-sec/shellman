import asyncio


class Connection:
    def __init__(self, reader, writer, id):
        self.reader = reader
        self.writer = writer
        self.id = id
        self.listening_frontends = []
        self.read_task = asyncio.get_event_loop().create_task(self.read_loop())
        self.write_lock = asyncio.Lock()

    def add_frontend(self, frontend):
        self.listening_frontends.append(frontend)

    def remove_frontend(self, frontend):
        self.listening_frontends.remove(frontend)

    async def write(self, data, writer):
        for frontend in self.listening_frontends:
            if frontend != writer:
                await frontend.on_write_by_other(self, data)
        async with self.write_lock:
            self.writer.write(data)
            await self.writer.drain()

    async def read_loop(self):
        while True:
            data = await self.reader.readline()
            if data == b'':
                await self.disconnected()
                break
            for frontend in self.listening_frontends:
                await frontend.on_read(self, data)

    async def disconnected(self):
        for frontend in self.listening_frontends:
            await frontend.on_disconnect(self)

        from .shellman import ShellmanCore
        ShellmanCore().connections[self.id] = None
