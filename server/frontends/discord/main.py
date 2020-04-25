from .config import bot
import discord
from server.shellman import ShellmanCore
import asyncio

client = discord.Client()
guild = None


class ShellmanFrontend:


    def __init__(self):
        self.TOKEN = bot["token"]
        loop = asyncio.get_event_loop()
        loop.create_task(client.start(bot["token"]))



    ##CORE HOOKS
    #######################################
    async def on_connection(self, connection_id):
        print(f"Discordbot: connection {connection_id} received, listening")
        await self.createChannel(connection_id)
        ShellmanCore().add_frontend_to_connection(connection_id, self)

    async def on_read(self, conn_id, data):
        print(f'example_frontend: received data from connection {conn_id}: {data} - sending back the same')
        await ShellmanCore().write_to_connection(conn_id, data, self)

    async def on_disconnect(self, conn_id):
        print(f'example_frontend: {conn_id} disconnected :(')

    async def on_write_by_other(self, conn_id, data):
        print(f'example_frontend: another frontend wrote {data} to {conn_id}')





    ##DISCORD HOOKS
    #######################################

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
        
        
        
        if(message.content=='!shinit'):
            global guild
            guild = message.guild
            for category in message.guild.categories:
                if(category.name=='shells'):
                    for channel in category.channels:
                        await channel.delete()
                    await category.delete()
                    break
            await message.guild.create_category('shells')


        if(message.channel.category.name=='shells'):
            print(message.channel.name)

    async def createChannel(self,name):
        print(guild)
        print(guild.categories)
        category = discord.utils.get(guild.categories, name="shells")
        print(category)
        await guild.create_text_channel(name, category=category)
        
        pass

