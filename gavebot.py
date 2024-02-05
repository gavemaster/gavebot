import openai
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import pytz
from datetime import datetime, timedelta
from gavemaster_langchain import gavebot_simple_sequential, gavebot_stocks_and_sports, run_agent, run_chain, wikiBacked_gavebot
from gm_logger import create_logger
from gavemaster_open_ai import gavebot_character, gavebot_character_morning
from dallegavebot import get_image, get_prompt_from_ai, extract_text_and_image_from_message, get_image_from_variation_dalle
from gavebot_dj import GavebotDJ
import site
import pytube
logger = create_logger('gavebot')

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
target_channel_id = int(os.getenv('GAVE_DIGITAL_POTD_ID'))


sitesite= pytube.__file__


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
gavebot_chain = gavebot_simple_sequential(1.2)
sport_stocks_agent =gavebot_stocks_and_sports(1.2)
wiki_gavebot = wikiBacked_gavebot(1.2)
dj = GavebotDJ()
@bot.event 
async def on_message(message):
    
    if message.author == bot.user:
        return

    if message.content.startswith('!img'):
        try:
            prompt = message.content[len('!img'):]
            response = get_image(prompt)
            await message.channel.send(response)
        except openai.BadRequestError as e:
            await message.channel.send("This prompt is too toxic according to sam altman.")
        except Exception as e:
            await message.channel.send(f"ERROR : {e} ")


    if message.content.startswith('!pic'):
        try:
            prompt = message.content[len('!pic'):]
            image_prompt = get_prompt_from_ai(prompt)
            logger.debug(f"{image_prompt}")
            response = get_image(image_prompt)
            await message.channel.send(image_prompt)
            await message.channel.send(response)
        except openai.BadRequestError as e:
            await message.channel.send("This prompt is too toxic according to sam altman")
        except Exception as e:
            await message.channel.send(f"ERROR:  {e}")
    
    if message.content.startswith('!remix'):
        try:
            image_stream = extract_text_and_image_from_message(message)
            image = get_image_from_variation_dalle( image_stream)
            await message.channel.send(image)
        except openai.BadRequestError as e:
            await message.channel.send("This prompt is too toxic according to sam altman")
        except Exception as e:
            await message.channel.send(f"ERROR: {e}")  
    

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
    
    


bot.run(token)
