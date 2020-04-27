async def handle(message, match, discord_client):
    ret = 'Main channel commands:\n'
    from ..commands import shell_commands
    for _, handler in shell_commands.items():
        ret += f'{handler.help()}\n'
    ret += 'Please note that there are some commands specific to shell channels. ' \
           'To get a list of those, type `!help` in a shell channel.'
    await message.channel.send(ret)


def help():
    return "`!help` - Shows you this help text."
