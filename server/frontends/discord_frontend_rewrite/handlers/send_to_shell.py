async def handle(message, match, shell, shellman_frontend):
    await shell.connection.write(f'{message.content}\n'.encode(), shellman_frontend)


def help():
    return "Any message you send to a shell channel will be sent to the correspondent shell as a command."
