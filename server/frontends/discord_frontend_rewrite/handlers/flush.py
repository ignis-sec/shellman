async def handler(message, match, shell, shellman_frontend):
    shell.buffer = ''
    shell.write_task.cancel()
    shell.write_task = None
    await message.channel.send('Flushed read buffer.')
