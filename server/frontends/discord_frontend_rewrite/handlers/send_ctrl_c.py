async def handler(message, match, shell, shellman_frontend):
    await shell.connection.write('\x03\n'.encode(), shellman_frontend)
