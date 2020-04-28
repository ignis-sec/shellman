from ....shellman import ShellmanCore


async def handle(message, match, discord_client):
    ret = '```\nID: IP Address\n==============\n'
    for connection in ShellmanCore().connections:
        ret += f'{connection.id}: {connection.writer.get_extra_info("peername")[0]}'
    ret += '```'
    await message.channel.send(ret)


def help():
    return "`!shells` - Gives a list of currently available shells."
