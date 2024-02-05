import openai
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import pytz
from datetime import datetime, timedelta
from gm_logger import create_logger
from gavebot_dj import GavebotDJ
from dallegavebot import DalleGavebot
from gavebot_preacher import GavebotPreacher
import site
import pytube
import asyncio
import traceback
logger = create_logger('gavebot')

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
target_channel_id = int(os.getenv('GAVE_DIGITAL_POTD_ID'))


sitesite= pytube.__file__


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
preacher = GavebotPreacher()
dj = GavebotDJ()
dalle = DalleGavebot()
@bot.event 
async def on_message(message):
    
    if message.author == bot.user:
        return

    if message.content.startswith('!img'):
        try:
            prompt = message.content[len('!img'):]
            response = dalle.get_image(prompt)
            await message.channel.send(response)
        except openai.BadRequestError as e:
            await message.channel.send("This prompt is too toxic according to sam altman.")
        except Exception as e:
            await message.channel.send(f"ERROR : {e} ")
        
    if message.content.startswith('!preach'):
        try:
            prompt = message.content[len('!preach'):]
            response = preacher.preach_to_user(prompt)
            to_user = message.author.mention
            message_content = f"{to_user}, {response}"
            # Join the voice channel of the user who issued the command
            if message.author.voice:
                voice_channel = message.author.voice.channel
                speechName = preacher.get_text_to_speech(response)
                voice_client = discord.utils.get(bot.voice_clients, guild=message.guild)
                if voice_channel and voice_client is None:
                    await voice_channel.connect()
                    voice_client = discord.utils.get(bot.voice_clients, guild=message.guild)
                    await preacher.playPreach(voice_client, voice_channel, speechName)
                    
                elif voice_channel and voice_client:
                   await message.channel.send("the pastor is cooking and will preach soon!")
                
            else:
                
                char_limit = 2000
                if len(message_content) > char_limit:
                    for chunk in [message_content[i:i+char_limit] for i in range(0, len(message_content), char_limit)]:
                        await message.channel.send(chunk)# Combining text and image URL
                else:
                    await message.channel.send(message_content)
        except Exception as e:
            traceback.print_exc()
            await message.channel.send(f"ERROR : {e.args}")

    if message.content.startswith('!play'):
        voice_channel = message.author.voice.channel
        voice_client = discord.utils.get(bot.voice_clients, guild=message.guild)
        if voice_channel and voice_client is None:
            await voice_channel.connect()
            voice_client = discord.utils.get(bot.voice_clients, guild=message.guild)
            dj.add_to_queue(message.content[len('!play '):])
            await dj.play_queue(voice_client, message.channel)
        elif voice_channel and voice_client:
            dj.add_to_queue(message.content[len('!play '):])
            await message.channel.send("Added to queue position: " + str(len(dj.queue)))
    if message.content.startswith("!skip"):
        voice_channel = message.author.voice.channel
        voice_client = discord.utils.get(bot.voice_clients, guild=message.guild)
        if voice_channel and voice_client:
            skipped = dj.skip_song(voice_client)
            if skipped:
                await message.channel.send("Skipping....")
            else:
                await message.channel.send("No song to skip...")

@bot.event
async def on_ready():
    logger.debug('Bot is ready and logged in')
    logger.debug(str(sitesite))   
 #get discord channel by channel id
    
    

print(token)
bot.run(token)
