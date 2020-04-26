import asyncio

from ....shellman import ShellmanCore


async def handler(message, match, discord_client):
    loop = asyncio.get_event_loop()

    print(match.groups())

    loop.create_task(ShellmanCore().start_listening(host, port))