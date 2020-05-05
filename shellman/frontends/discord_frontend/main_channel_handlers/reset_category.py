from ....config import Config


async def handle(message, match, discord_client):
    if not Config()['discord_frontend'].getboolean('admin_mode'):
        await message.channel.send('Cannot reset category in non-admin mode.')
        return
    for channel in discord_client.category.channels:
        active = None
        for index, shell in discord_client.shellman_frontend.shells.items():
            if active := shell.channel == channel:
                break
        if active:
            continue
        await channel.delete()


def help():
    return "`!catreset` - Deletes all the channels in the shell category (chosen in config). Admin mode only."
