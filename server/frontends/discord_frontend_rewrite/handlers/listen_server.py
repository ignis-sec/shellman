from ....shellman import ShellmanCore


async def handle(message, match, discord_client):
    host = match.group(2)
    port = match.group(3)

    if not (host and port):
        await message.channel.send(help())
        return

    if await ShellmanCore().start_listening(host, port):
        await message.channel.send(f'Started listening {host}:{port}')
    else:
        await message.channel.send(f'Could not start listening {host}:{port}')


def help():
    return "`!serverlisten <HOST> <PORT>` - Starts listening a new HOST:PORT pair."
