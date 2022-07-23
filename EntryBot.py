import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import youtube_dl
import json
import os
import asyncio
import random
from riot import *

TOKEN = '' # Your token goes here
voice = None
lock = asyncio.Lock()

client = commands.Bot(command_prefix = '.')

# Helper function to detect if given file names exist in the current directory
def checkFile(file_name):
    return os.path.exists(file_name)

# Get users' music data from dictionary stored in data.json
if checkFile('data.json'):
    with open('data.json', 'r') as file_object:
        data = json.load(file_object)
# Create an empty dictionary and create a new file if one doesn't exist
else:
    data = {}
    with open('data.json', 'w') as outfile:  
        json.dump(data, outfile)

# When ready, the bot gets its designated voice and text channels
@client.event
async def on_ready():
    global TEXTCHANNEL 
    global VOICECHANNEL
    TEXTCHANNEL = client.get_channel(983159765070913596)
    VOICECHANNEL = client.get_channel(978109248892465152)
    await TEXTCHANNEL.send("Ready!")

# Forces the bot to join the voice channel thar the sender is currently in
@client.command(pass_context = True)
async def join(ctx):
    await client.wait_until_ready()
    global voice
    sound = data[str(ctx.author.id)]
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio(sound)
        player = voice.play(source)
    else:
        await TEXTCHANNEL.send("Failed to join")

# Forces the bot to leave its current voice channel
@client.command(pass_context = True)
async def leave(ctx):
    await client.wait_until_ready()
    global voice
    try:
        await voice.disconnect()
        voice = None
    except:
        await TEXTCHANNEL.send("Failed to disconnect")

# Downloads the audio from the YouTube video specified by the given link as an mp3 file
@client.command(pass_context = True)
async def download(ctx, link):
    await client.wait_until_ready()
    video_info = youtube_dl.YoutubeDL().extract_info(
        url = link, download = False
    )
    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': f"{video_info['title']}.mp3".replace(" ", "")
    }
    try:
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])
        await ctx.channel.send("Successfully downloaded {title}".format(title = video_info['title'].replace(" ", "")))
    except:
        await ctx.channel.send("Failed to download file")


# Assigns the file with the given name as the entry music for the message's author for the given duration, so long as the file exists
@client.command(pass_context = True, aliases = ["af"])
async def assignFile(ctx, fileName, duration=5):
    await client.wait_until_ready()
    global data
    try:
        time = float(duration)
    except:
        await TEXTCHANNEL.send("Invalid duration")
        return
    if not(checkFile(fileName + '.mp3')):
        await TEXTCHANNEL.send("Couldn't find a file named " + fileName)
    else:
        id = str(ctx.author.id)
        data[id] = (fileName + ".mp3", time)
        with open('data.json', 'w') as outfile:  
            json.dump(data, outfile)
            await TEXTCHANNEL.send("Assigned " + fileName + " to " + ctx.author.name)

# Downloads and assigns the mp3 file at the specified YouTube link as the entrance music for the author of the message
@client.command(pass_context = True, aliases = ["da", "dAssign"])
async def downloadAssign(ctx, link, duration=5):
    await client.wait_until_ready()
    global data
    try:
        time = float(duration)
    except:
        await TEXTCHANNEL.send("Invalid duration")
        return
    try:
        video_info = youtube_dl.YoutubeDL().extract_info(
            url = link, download = False
        )
        options = {
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': f"{video_info['title']}.mp3".replace(" ", "")
        }
    except:
        await TEXTCHANNEL.send("Invalid link")
        return
    try:
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])
        await ctx.channel.send("Successfully downloaded {title}".format(title = video_info['title'].replace(" ", "")))
    except:
        await ctx.channel.send("Failed to download file")
    if not(checkFile(f"{video_info['title']}.mp3".replace(" ", ""))):
        await TEXTCHANNEL.send(f"Couldn't find a file named {video_info['title']}.mp3")
    else:
        id = str(ctx.author.id)
        data[id] = (f"{video_info['title']}.mp3".replace(" ", ""), time)
        with open('data.json', 'w') as outfile:  
            json.dump(data, outfile)
            await TEXTCHANNEL.send("Assigned " + video_info['title'].replace(" ", "") + " to " + ctx.author.name)
   

# Lists all mp3 files in the current directory
@client.command(pass_context = True, aliases = ["lf"])
async def listFiles(ctx):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    list = ""
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.mp3'):
                list = list + str(file).removesuffix(".mp3") + "\n"
    embed = discord.Embed(
        title = "Available Files:",
        description = list,
        colour = discord.Colour.green()
    )
    await ctx.channel.send(embed=embed)

# Checks whenever a user changes voice states and plays their entry music accordingly
# The bot enters the voice call if it is not present, and leaves if no real users remain in it
@client.event
async def on_voice_state_update(member, before, after):
    await client.wait_until_ready()
    global voice
    global data
    global TEXTCHANNEL 
    global VOICECHANNEL
    if (member.bot):
        return
    if (after != None and after.channel != None):
        if (after.channel.name == VOICECHANNEL.name):
            
            if (voice == None):
                try:
                    channel = after.channel
                    voice = await channel.connect()
                except:
                    await TEXTCHANNEL.send("Failed to connect to voice channel")

            if (str(member.id) in data):
                try:
                    sound = data[str(member.id)]
                    source = FFmpegPCMAudio(sound[0])
                    await asyncio.sleep(0.5)
                    async with lock:
                        voice.play(source)
                        await asyncio.sleep(sound[1])
                        voice.stop()
                except:
                    await TEXTCHANNEL.send("Failed to play audio")          

    if (before != None and before.channel != None):
        if (before.channel.name == VOICECHANNEL.name):
            empty = True
            for i in before.channel.members:
                if not(i.bot):
                    empty = False
            if (empty and voice != None):
                try:
                    await voice.disconnect()
                    voice = None
                except:
                    await TEXTCHANNEL.send("Failed to disconnect")

# Assigns random League of Legends roles for each given name (with no chance of getting "Fill")
@client.command(pass_context = True, aliases = ["lr"])
async def leagueRoles(ctx, *names):
    await client.wait_until_ready()
    if (len(names) == 0 or len(names) > 5):
        await ctx.channel.send("Invalid number of names")
        return
    
    output = lr(names)
    players = output[0]
    roles = output[1]    

    reroll = random.randint(0, 1)

    embed = discord.Embed(
        title = "League Roles:",
        colour = discord.Colour.blue()
    )

    embed.set_thumbnail(url="https://www.leagueoflegends.com/static/placeholder-1c66220c6149b49352c4cf496f70ad86.jpg")
    embed.add_field(name = "Players:", value = players, inline = True)
    embed.add_field(name = "Roles:", value = roles, inline = True)
    if (reroll):
        embed.set_footer(text="Y'know, these rolls aren't really doing it for me. If you'd like to reroll, go right ahead.")
    else:
        embed.set_footer(text="These rolls are the most perfect choices you could ever dream of. Don't you dare reroll.")

    await ctx.channel.send(embed=embed)

# Assigns random League of Legends roles for each given name
@client.command(pass_context = True, aliases = ["lrf"])
async def leagueRolesFill(ctx, *names):
    if (len(names) == 0 or len(names) > 5):
        await ctx.channel.send("Invalid number of names")
        return
    
    output = lrf(names)
    players = output[0]
    roles = output[1]

    reroll = random.randint(0, 1)

    embed = discord.Embed(
        title = "League Roles:",
        colour = discord.Colour.blue()
    )

    embed.set_thumbnail(url="https://www.leagueoflegends.com/static/placeholder-1c66220c6149b49352c4cf496f70ad86.jpg")
    embed.add_field(name = "Players:", value = players, inline = True)
    embed.add_field(name = "Roles:", value = roles, inline = True)
    if (reroll):
        embed.set_footer(text="Y'know, these rolls aren't really doing it for me. If you'd like to reroll, go right ahead.")
    else:
        embed.set_footer(text="These rolls are the most perfect choices you could ever dream of. Don't you dare reroll.")

    await ctx.channel.send(embed=embed)

# Assigns random Valorant roles for each given name
@client.command(pass_context = True, aliases = ["vr", "valoRoles"])
async def valorantRoles(ctx, *names):
    await client.wait_until_ready()
    if (len(names) == 0 or len(names) > 5):
        await ctx.channel.send("Invalid number of names")
        return
    
    output = vr(names)
    players = output[0]
    roles = output[1]    

    reroll = random.randint(0, 1)

    embed = discord.Embed(
        title = "Valorant Roles:",
        colour = discord.Colour.red()
    )

    embed.set_thumbnail(url="https://images.cults3d.com/4QqRV9kLYYEuw9ur_X3yjQl1sjk=/516x516/https://files.cults3d.com/uploaders/15024335/illustration-file/a86d53e4-2bd9-4a8f-9550-986686c3131a/gi0mAjIh_400x400.png")
    embed.add_field(name = "Players:", value = players, inline = True)
    embed.add_field(name = "Roles:", value = roles, inline = True)
    if (reroll):
        embed.set_footer(text="Y'know, these rolls aren't really doing it for me. If you'd like to reroll, go right ahead.")
    else:
        embed.set_footer(text="These rolls are the most perfect choices you could ever dream of. Don't you dare reroll.")

    await ctx.channel.send(embed=embed)

# Assigns random Valorant roles for each given name, while ensuring there's at most one duplicate role
@client.command(pass_context = True, aliases = ["vrx", "valoRolesX"])
async def valorantRolesX(ctx, *names):
    await client.wait_until_ready()
    if (len(names) == 0 or len(names) > 5):
        await ctx.channel.send("Invalid number of names")
        return
    
    output = vrx(names)
    players = output[0]
    roles = output[1]    

    reroll = random.randint(0, 1)

    embed = discord.Embed(
        title = "Valorant Roles X:",
        colour = discord.Colour.red()
    )

    embed.set_thumbnail(url="https://images.cults3d.com/4QqRV9kLYYEuw9ur_X3yjQl1sjk=/516x516/https://files.cults3d.com/uploaders/15024335/illustration-file/a86d53e4-2bd9-4a8f-9550-986686c3131a/gi0mAjIh_400x400.png")
    embed.add_field(name = "Players:", value = players, inline = True)
    embed.add_field(name = "Roles:", value = roles, inline = True)
    if (reroll):
        embed.set_footer(text="Y'know, these rolls aren't really doing it for me. If you'd like to reroll, go right ahead.")
    else:
        embed.set_footer(text="These rolls are the most perfect choices you could ever dream of. Don't you dare reroll.")

    await ctx.channel.send(embed=embed)

# Assigns a random Valorant agent for the given role
@client.command(pass_context = True, aliases = ["va", "valoAgent"])
async def valorantAgent(ctx, role):
    await client.wait_until_ready()
    if not(role.lower() in ["controller", "duelist", "initiator", "sentinel", "any"]):
        await ctx.channel.send("Invalid role given")
        return

    output = va(role)
    agent = output[0]
    link = output[1]

    reroll = random.randint(0, 1)

    embed = discord.Embed(
        title = "Valorant Agent:",
        description = "I've decided that {name} should play as {agent}".format(name = ctx.author.name, agent = agent),
        colour = discord.Colour.red()
    )

    embed.set_image(url=link)

    if (reroll):
        embed.set_footer(text="This is the best possible choice. Rerolling is not an option.")
    else:
        embed.set_footer(text="This choice is pretty meh. You can reroll if you'd like to.")

    await ctx.channel.send(embed=embed)

# Makes a random decision between the given options
@client.command(pass_context = True, aliases = ["d"])
async def decide(ctx, *options):
    await client.wait_until_ready()
    if (len(options) == 0):
        await TEXTCHANNEL.send("There's nothing to choose from.")
        return

    choice = random.randint(0, len(options) - 1)
    await ctx.channel.send("I choose {choice}.".format(choice = options[choice]))

# Run the bot
client.run(TOKEN)