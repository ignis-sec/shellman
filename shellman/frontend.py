from abc import ABC, abstractmethod


class ShellmanFrontend(ABC):
    @abstractmethod
    async def on_connection(self, connection):
        pass

    @abstractmethod
    async def on_read(self, connection, data):
        pass

    @abstractmethod
    async def on_disconnect(self, connection):
        pass

    @abstractmethod
    async def on_write_by_other(self, connection, data):
        pass

    @abstractmethod
    async def shutdown(self):
        pass
