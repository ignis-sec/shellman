from ....shellman import ShellmanCore


async def handle(message, match, discord_client):
    host = match.group(2)
    port = match.group(3)

    if not (host and port):
        await message.channel.send(help())
        return

    if await ShellmanCore().stop_listening(host, port):
        await message.channel.send(f'Stopped listening {host}:{port}')
    else:
        await message.channel.send(f'Could not stop listening {host}:{port} - '
                                   f'maybe we weren\'t listening it in the first place?')


def help():
    return "`!serverclose <HOST> <PORT>` - Stops listening a HOST:PORT pair."
