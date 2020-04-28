from ....shellman import ShellmanCore


async def handle(message, match, discord_client):
    host = match.group(2)
    port = match.group(3)
    ssl = match.group(4)

    if not (host and port):
        await message.channel.send(help())
        return

    await ShellmanCore().connect_to_bind_shell(host, port, ssl is not None)


def help():
    return "`!connect <HOST> <PORT> [SSL]` - Connects to a bind shell at HOST:PORT. " \
                                            "Connects with SSL if SSL is specified."
