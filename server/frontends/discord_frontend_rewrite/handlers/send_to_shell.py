async def handler(message, shell, shellman_frontend):
    await shell.connection.write(f'{message.content}\n'.encode(), shellman_frontend)