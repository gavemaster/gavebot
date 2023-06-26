import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import pytz
from datetime import datetime, timedelta
from gavemaster_langchain import gavebot_simple_sequential, gavebot_stocks_and_sports, run_agent, run_chain, wikiBacked_gavebot
from gm_logger import create_logger
from gavemaster_open_ai import gavebot_character, gavebot_character_morning


logger = create_logger('gavebot')

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
target_channel_id = int(os.getenv('GAVE_DIGITAL_POTD_ID'))


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
gavebot_chain = gavebot_simple_sequential(1.2)
sport_stocks_agent =gavebot_stocks_and_sports(1.2)
wiki_gavebot = wikiBacked_gavebot(1.2)

@bot.event 
async def on_message(message):
    
    if message.author == bot.user:
        return
    
    if message.content.startswith('!ask'):
        logger.debug("asking gavebot a question")

        response = await run_agent(sport_stocks_agent, message.content)

        await message.channel.send(response)

    if bot.user.mentioned_in(message) or "gavebot" in message.content.lower():
        formatted_message = await format_message(message)

        logger.debug(formatted_message)
    
        #store author @ name for response
        author = message.author.mention


        response = await run_chain(wiki_gavebot, formatted_message, 'wiki')
       
        #check to see if response it too long for discord message
        
        await message.channel.send(response)


@tasks.loop(hours=4)
async def gmEveryone():
    
    logger.debug("starting morning function")
    est_tz = pytz.timezone('US/Eastern')
    current_time_est = datetime.now(est_tz)
    day_of_week = current_time_est.weekday()
    est_monday = current_time_est.replace(hour=5, minute=45, second=0, microsecond=0) + timedelta(days=(0 - current_time_est.weekday()) % 7)
    est_tuesday = current_time_est.replace(hour=5, minute=45, second=0, microsecond=0) + timedelta(days=(1 - current_time_est.weekday()) % 7)
    est_wednesday = current_time_est.replace(hour=5, minute=45, second=0, microsecond=0) + timedelta(days=(2 - current_time_est.weekday()) % 7)
    est_thursday = current_time_est.replace(hour=5, minute=45, second=0, microsecond=0) + timedelta(days=(3 - current_time_est.weekday()) % 7)
    est_friday = current_time_est.replace(hour=5, minute=45, second=0, microsecond=0) + timedelta(days=(4 - current_time_est.weekday()) % 7)
    est_saturday = current_time_est.replace(hour=5, minute=45, second=0, microsecond=0) + timedelta(days=(5 - current_time_est.weekday()) % 7)
    est_sunday = current_time_est.replace(hour=5, minute=45, second=0, microsecond=0) + timedelta(days=(6 - current_time_est.weekday()) % 7)
    
    
    if day_of_week == 0 and current_time_est >= est_monday and current_time_est - timedelta(hours=4) < est_monday:
        logger.debug("Monday")
        message_channel = bot.get_channel(target_channel_id)
        logger.debug(f"Got channel {message_channel}")
        logger.debug("monday message sent @ " + str(current_time_est))
        morning_message = gavebot_character_morning("Monday")
        await message_channel.send(morning_message)
    
    elif day_of_week == 1 and current_time_est >= est_tuesday and current_time_est - timedelta(hours=4) < est_tuesday:
        logger.debug("Tuesday")
        message_channel = bot.get_channel(target_channel_id)
        logger.debug(f"Got channel {message_channel}")
        logger.debug("tuesday message sent @ " + str(current_time_est))
        morning_message = gavebot_character_morning("Tuesday")
        await message_channel.send(morning_message + " get a bag or kill yourself @everyone https://www.youtube.com/watch?v=mm9_v4idmJo ")
    
    elif day_of_week == 2 and current_time_est >= est_wednesday and current_time_est - timedelta(hours=4) < est_wednesday:
        logger.debug("Wednesday")
        message_channel = bot.get_channel(target_channel_id)
        logger.debug(f"Got channel {message_channel}")
        logger.debug("wednesday message sent @ " + str(current_time_est))
        morning_message = gavebot_character_morning("Wednesday")
        await message_channel.send(morning_message)
    
    elif day_of_week == 3 and current_time_est >= est_thursday and current_time_est - timedelta(hours=4) < est_thursday:
        logger.debug("Thursday")
        message_channel = bot.get_channel(target_channel_id)
        logger.debug(f"Got channel {message_channel}")
        logger.debug("thursday message sent @ " + str(current_time_est))
        morning_message = gavebot_character_morning("Thursday")
        await message_channel.send(morning_message)

    elif day_of_week == 4 and current_time_est >= est_friday and current_time_est - timedelta(hours=4) < est_friday:
        logger.debug("Friday")
        message_channel = bot.get_channel(target_channel_id)
        logger.debug(f"Got channel {message_channel}")
        logger.debug("friday message sent @ " + str(current_time_est))
        morning_message = gavebot_character_morning("Friday")
        await message_channel.send("happy bmf @everyone https://tenor.com/view/walking-gif-25278075 " + morning_message)

    elif day_of_week == 5 and current_time_est >= est_saturday and current_time_est - timedelta(hours=4) < est_saturday:
        logger.debug("Saturday")
        message_channel = bot.get_channel(target_channel_id)
        logger.debug(f"Got channel {message_channel}")
        logger.debug("saturday message sent @ " + str(current_time_est))
        morning_message = gavebot_character_morning("Saturday")
        await message_channel.send(morning_message)

    elif day_of_week == 6 and current_time_est >= est_sunday and current_time_est - timedelta(hours=4) < est_sunday:
        logger.debug("Sunday")
        message_channel = bot.get_channel(target_channel_id)
        logger.debug(f"Got channel {message_channel}")
        logger.debug("sunday message sent @ " + str(current_time_est))
        morning_message = gavebot_character_morning("Sunday")
        await message_channel.send(morning_message + " https://tenor.com/view/its-sunday-bitches-gif-13992837")


async def get_gavebot_response(user, current_time, message):
    response = gavebot_character(current_time, message)
    return user + ' ' + response




async def format_message(message):

    #get the current time in eastern standard time in format "DAYOFWEEK, MONTH-DAY-YEAR , HH:MM" 
   
    est_tz = pytz.timezone('US/Eastern')
    current_time = datetime.now(est_tz)
    current_time = current_time.strftime("%A, %B-%d-%Y , %H:%M")

    if bot.user.mentioned_in(message):
        message_content = message.content.replace(bot.user.mention, "gavebot")
    else:
        message_content = message.content

    response = "( " + str(current_time) + " ) " + message.author.name + ": " + message_content
    print(response)
    return response

@gmEveryone.before_loop
async def before():
    logger.debug("wating for bot....")
    await bot.wait_until_ready()


@bot.event
async def on_ready():
    logger.debug('Bot is ready and logged in')
    #await target_channel_id.send("new gavebot version is here..... use '!ask' to ask gavebot a question... currently has data on current stocks and sports gamesS")
    gmEveryone.start()
    

bot.run(token)