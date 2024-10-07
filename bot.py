from secret import *
import discord
import json
import datetime
from discord.ext import tasks
import zoneinfo

tz = zoneinfo.ZoneInfo('America/Los_Angeles')
time = datetime.time(hour=8, minute=30, tzinfo=tz)

client = discord.Client(intents=discord.Intents.all())

@tasks.loop(time=time)
async def refresh_threads():
    for guild in client.guilds:
        print(guild)
        for channel in guild.channels:
            if channel.name == "to-do-list":
                for thread in channel.threads:
                    dead_channels = json.load(open("dead_channels.json"))["dead_channels"]
                    if thread.id not in dead_channels:
                        if thread.archived:
                            pass
                        else:
                            print("refreshing thread: ", thread.name)
                            await thread.send(content = "not archived!", delete_after = 3)
        print("****")

@client.event
async def on_ready():
    print("I'm in")
    print(client.user)
    await refresh_threads()
    refresh_threads.start()

async def kill_channel(channel):
    dead_channels = json.load(open("dead_channels.json"))["dead_channels"]
    dead_channels.append(channel.id)
    json.dump({"dead_channels": dead_channels}, open("dead_channels.json", "w"))

@client.event
async def on_message(message):
    if message.content.lower() == "/done":
        await kill_channel(message.channel)

client.run(token)
