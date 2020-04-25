from .config import bot
import discord
from server.shellman import ShellmanCore
import asyncio
import threading

client = discord.Client()
guild = None

timer = None
delayCallId=0

writeBuffer = {}
def retriggerableDelay(delay, callback, id):
    global timer
    if(writeBuffer[id]["timer"]):
        writeBuffer[id]["timer"].cancel()
    
    t = asyncio.get_event_loop().create_task(sendToShellChannel(id,delay))
    writeBuffer[id]["timer"] = t



async def sendToShellChannel(id,delay):
    print("Callback called")
    asyncio.sleep(delay)
    print("Delay finished")
    data = f'```{writeBuffer[id]["buf"]}```'
    channel = discord.utils.get(guild.channels, name=str(id))
    await channel.send(data)
    writeBuffer[id]["buf"]="\n"
    writeBuffer[id]["timer"] = None



class ShellmanFrontend:


    def __init__(self):
        self.TOKEN = bot["token"]
        loop = asyncio.get_event_loop()
        loop.set_debug(True)
        loop.create_task(client.start(bot["token"]))


    ##CORE HOOKS
    #######################################
    async def on_connection(self, connection):
        print(f"Discordbot: connection {connection} received, listening")
        await self.createChannel(connection.id)
        connection.add_frontend(self)
        writeBuffer[connection.id] = {"timer": None, "buf": "\n"}

    async def on_read(self, connection, data):
        print(f'discord: received data from connection {connection.id}: {data}')
        writeBuffer[connection.id]["buf"] = writeBuffer[connection.id]["buf"] + data.decode()
        retriggerableDelay(0.5, sendToShellChannel, connection.id)

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
            await ShellmanCore().write(int(message.channel.name), (message.content + "\n").encode(), "discord" )
 
    async def createChannel(self,name):
        category = discord.utils.get(guild.categories, name="shells")
        await guild.create_text_channel(name, category=category)


