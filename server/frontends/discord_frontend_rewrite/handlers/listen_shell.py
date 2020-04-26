from ....shellman import ShellmanCore
from ..shell import Shell


async def handler(message, match, discord_client):
    id = int(match.group(2))
    channel = int(match.group(3))

    try:
        assert(ShellmanCore().connections[id] is not None)
    except (IndexError, AssertionError):
        await message.channel.send(f'No connection with id {id}.')
        return

    discord_client.shellman_frontend.shells[id] = Shell(connection=ShellmanCore().connections[id])
    discord_client.shellman_frontend.shells[id].channel = discord_client.guild.get_channel(channel)

    if discord_client.shellman_frontend.shells[id].channel is None:
        await message.channel.send(f'No such channel.')
        discord_client.shellman_frontend.shells[id] = None
        return

    ShellmanCore().connections[id].add_frontend(discord_client.shellman_frontend)
    await message.channel.send(f'Successfully started listening connection {id} in channel <#{channel}>.')