from ....config import Config


async def handle(message, match, shell, shellman_frontend):
    if not Config()['discord_frontend'].getboolean('admin_mode'):
        await message.channel.send('Cannot clear in non-admin mode.')
        return
    await shell.channel.delete()
    await shellman_frontend.create_shell_channel(shell)


def help():
    return "`!clear` - \"Clears\" channel by deleting and re-creating it. Admin mode only."
