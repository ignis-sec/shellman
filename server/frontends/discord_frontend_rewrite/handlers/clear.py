from ....config import Config


async def handler(message, shell, shellman_frontend):
    if not Config()['discord_frontend'].getboolean('admin_mode'):
        message.channel.send('Cannot clear in non-admin mode.')  # TODO: implement deleting messages instead
        return
    await shell.channel.delete()
    await shellman_frontend.create_shell_channel(shell)
