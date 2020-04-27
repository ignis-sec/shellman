async def handle(message, match, shell, shellman_frontend):
    shell.buffer = ''
    shell.write_task.cancel()
    shell.write_task = None
    await message.channel.send('Flushed read buffer.')


def help():
    return "`!flush` - Clears the buffer of data that is currently being sent to the channel."
