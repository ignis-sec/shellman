from ....config import Config


async def handle(message, match, discord_client):
    if not Config()['discord_frontend'].getboolean('admin_mode'):
        await message.channel.send('Cannot reset category in non-admin mode.')
        return
    for channel in discord_client.category.channels:
        await channel.delete()


def help():
    return "`!catreset` - Deletes all the channels in the shell category (chosen in config). Admin mode only."
