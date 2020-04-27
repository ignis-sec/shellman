async def handle(message, match, shell, shellman_frontend):
    await shell.connection.write('\x03\n'.encode(), shellman_frontend)


def help():
    return "`!C` or `^C` - Tries to emulate a Ctrl-c in the shell by sending \\x03, " \
                          "will not work unless you have a pty."
