from ....config import Config


async def handler(message, match, discord_client):
    if not Config()['discord_frontend'].getboolean('admin_mode'):
        message.channel.send('Cannot reset category in non-admin mode.')
        return
    for channel in discord_client.category.channels:
        await channel.delete()