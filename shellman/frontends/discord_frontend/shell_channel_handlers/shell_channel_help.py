async def handle(message, match, shell, shellman_frontend):
    ret = 'Shell channel commands:\n'
    from ..commands import shell_channel_commands
    for _, handler in shell_channel_commands.items():
        ret += f'{handler.help()}\n'
    ret += 'Please note that there are some commands specific to the main channel ' \
           f'(<#{shellman_frontend.discord_client.main_channel.id}>). ' \
           'To get a list of those, type `!help` in the main channel.'
    await message.channel.send(ret)


def help():
    return "`!help` - Shows you this help text."
