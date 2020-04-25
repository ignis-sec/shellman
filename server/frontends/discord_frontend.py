import asyncio

import discord

from ..shellman import ShellmanCore
from ..config import Config

client = discord.Client()
guild = None

writeBuffer = {}


class ShellmanFrontend:
    def __init__(self):
        loop = asyncio.get_event_loop()
        loop.set_debug(True)  # TODO: remove this
        loop.create_task(client.start(Config['discord_frontend']["token"]))

    async def on_connection(self, connection):
        print(f"Discordbot: connection {connection} received, listening")
        await create_channel(connection.id)
        connection.add_frontend(self)
        writeBuffer[connection.id] = {"timer": None, "buf": "\n"}

    async def on_read(self, connection, data):
        print(f'discord: received data from connection {connection.id}: {data}')
        writeBuffer[connection.id]["buf"] = writeBuffer[connection.id]["buf"] + data.decode()

        write_task = writeBuffer[connection.id]["timer"]
        if write_task:
            write_task.cancel()

        new_write_task = asyncio.get_event_loop().create_task(send_buffer_to_channel_with_delay(id, 0.5))
        writeBuffer[id]["timer"] = new_write_task

    async def on_disconnect(self, conn_id):
        print(f'discord_frontend: {conn_id} disconnected :(')

    async def on_write_by_other(self, conn_id, data):
        print(f'discord_frontend: another frontend wrote {data} to {conn_id}')


# DISCORD HOOKS
@client.event
async def on_ready():
    global guild
    guild = client.guilds[0]
    print(guild)
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!shinit':
        global guild
        guild = message.guild
        for category in message.guild.categories:
            if category.name == 'shells':
                for channel in category.channels:
                    await channel.delete()
                await category.delete()
                break
        await message.guild.create_category('shells')

    if message.channel.category.name == 'shells':
        await ShellmanCore().write(int(message.channel.name), (message.content + "\n").encode(), "discord")


async def send_buffer_to_channel_with_delay(id, delay):
    print("Callback called")
    await asyncio.sleep(delay)
    print("Delay finished")
    data = f'```{writeBuffer[id]["buf"]}```'
    channel = discord.utils.get(guild.channels, name=str(id))
    await channel.send(data)
    writeBuffer[id]["buf"] = "\n"
    writeBuffer[id]["timer"] = None


async def create_channel(name):
    category = discord.utils.get(guild.categories, name="shells")
    await guild.create_text_channel(name, category=category)