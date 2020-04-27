from ....config import Config


async def handle(message, match, shell, shellman_frontend):
    if not Config()['discord_frontend'].getboolean('admin_mode'):
        await message.channel.send('Cannot rename in non-admin mode.')
        return

    new_name = match.group(2)
    if not new_name:
        new_name = shellman_frontend.get_default_channel_name(shell)

    shell.name = new_name
    await message.channel.edit(name=new_name)
    await message.channel.send(f'This shell is now called {new_name}')


def help():
    return "`!rename [NEW_NAME]` - Renames shell channel to NEW_NAME if specified, " \
                                  "otherwise to the default name as specified in the config. Admin mode only."
