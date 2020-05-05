from shellman.shellman import ShellmanCore


async def handle(message, match, shell, shellman_frontend):
    id = shell.connection.id
    ShellmanCore().connections[id].writer.close()
    await ShellmanCore().connections[id].disconnected()


def help():
    return "`!disconnect` - Disconnects from the shell."
