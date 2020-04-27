from ....shellman import ShellmanCore


async def handle(message, match, discord_client):
    ret = '```\nListening on\n============\n'
    for server in ShellmanCore().servers:
        host, port = server.sockets[0].getsockname()
        ret += f'{host}:{port}\n'
    ret += '```'
    await message.channel.send(ret)


def help():
    return "`!servers` - Gives a list of HOST:PORT pairs we are currently listening"
