import asyncio


class Shell:
    __slots__ = ['write_task', 'buffer', 'buffer_lock', 'channel', 'connection']

    def __init__(self, connection):
        self.connection = connection
        self.buffer_lock = asyncio.Lock()
        self.channel = None
        self.buffer = ''
        self.write_task = None
