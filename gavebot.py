import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import pytz
from datetime import datetime, timedelta
from gm_logger import create_logger




logger = create_logger('gavebot')

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
target_channel_id = int(os.getenv('GAVE_DIGITAL_POTD_ID'))


bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())



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
        await message_channel.send("gm @everyone")
    
    elif day_of_week == 1 and current_time_est >= est_tuesday and current_time_est - timedelta(hours=4) < est_tuesday:
        logger.debug("Tuesday")
        message_channel = bot.get_channel(target_channel_id)
        logger.debug(f"Got channel {message_channel}")
        logger.debug("tuesday message sent @ " + str(current_time_est))
        await message_channel.send("get a bag or kill yourself @everyone https://www.youtube.com/watch?v=mm9_v4idmJo ")
    
    elif day_of_week == 2 and current_time_est >= est_wednesday and current_time_est - timedelta(hours=4) < est_wednesday:
        logger.debug("Wednesday")
        message_channel = bot.get_channel(target_channel_id)
        logger.debug(f"Got channel {message_channel}")
        logger.debug("wednesday message sent @ " + str(current_time_est))
        await message_channel.send("gm @everyone im wetttt affff for wet wednesdayss https://images-ext-2.discordapp.net/external/pNbIuq9ee5QCjHRYs-jLZKltevEIRpValp0nP3gzEDM/https/media.tenor.com/UfeLRq2_tr4AAAPo/wednesday-humpday.mp4 ")
    
    elif day_of_week == 3 and current_time_est >= est_thursday and current_time_est - timedelta(hours=4) < est_thursday:
        logger.debug("Thursday")
        message_channel = bot.get_channel(target_channel_id)
        logger.debug(f"Got channel {message_channel}")
        logger.debug("thursday message sent @ " + str(current_time_est))
        await message_channel.send("gm @everyone")

    elif day_of_week == 4 and current_time_est >= est_friday and current_time_est - timedelta(hours=4) < est_friday:
        logger.debug("Friday")
        message_channel = bot.get_channel(target_channel_id)
        logger.debug(f"Got channel {message_channel}")
        logger.debug("friday message sent @ " + str(current_time_est))
        await message_channel.send("happy bmf @everyone https://tenor.com/view/walking-gif-25278075")

    elif day_of_week == 5 and current_time_est >= est_saturday and current_time_est - timedelta(hours=4) < est_saturday:
        logger.debug("Saturday")
        message_channel = bot.get_channel(target_channel_id)
        logger.debug(f"Got channel {message_channel}")
        logger.debug("saturday message sent @ " + str(current_time_est))
        await message_channel.send("gm @everyone ITS SLUTTY SATURDAY https://tenor.com/view/beurk-sexy-dance-funny-gif-13733130")

    elif day_of_week == 6 and current_time_est >= est_sunday and current_time_est - timedelta(hours=4) < est_sunday:
        logger.debug("Sunday")
        message_channel = bot.get_channel(target_channel_id)
        logger.debug(f"Got channel {message_channel}")
        logger.debug("sunday message sent @ " + str(current_time_est))
        await message_channel.send("gm @everyone and happy sunday https://tenor.com/view/its-sunday-bitches-gif-13992837")



@gmEveryone.before_loop
async def before():
    logger.debug("wating for bot....")
    await bot.wait_until_ready()


@bot.event
async def on_ready():
    logger.debug('Bot is ready and logged in')
    gmEveryone.start()
bot.run(token)