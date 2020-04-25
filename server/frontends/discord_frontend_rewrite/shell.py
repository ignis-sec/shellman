import asyncio


class Shell:
    __slots__ = ['write_task', 'buffer', 'buffer_lock', 'channel', 'connection']

    def __init__(self, connection, channel):
        self.connection = connection
        self.channel = channel
        self.buffer_lock = asyncio.Lock()