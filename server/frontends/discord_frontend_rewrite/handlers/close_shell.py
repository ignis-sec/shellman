from ....shellman import ShellmanCore


async def handle(message, match, shell, shellman_frontend):
    id = shell.connection.id
    ShellmanCore().connections[id].remove_frontend(shellman_frontend)
    del shellman_frontend.shells[id]

    await message.channel.send(f'No longer listening connection {id}.')


def help():
    return "`!close` - Stops listening to the shell (the connection will be kept available - " \
                      "you can `!listen` it back from the main channel.)"
