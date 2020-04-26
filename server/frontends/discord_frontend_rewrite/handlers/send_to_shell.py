async def handler(message, match, shell, shellman_frontend):
    await shell.connection.write(f'{message.content}\n'.encode(), shellman_frontend)
