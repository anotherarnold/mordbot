# CJA
# Discord Bot

import os
import discord
import logging
import sys
import re
import random
import markovify
import mord_globals
from cogs import mord_admin, mord_fun, mord_commands, mord_roles, mord_task
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(os.path.realpath(sys.executable))
elif __file__:
    application_path = os.path.dirname(__file__)  

#the API token is loaded through the .env file.
#if the token is ever changed or needs to be reset, this file can be edited.
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command = commands.DefaultHelpCommand(no_category = 'Other'))

bot.TEXT_MODELS = {}
bot.TEXT_RAW = {}
texts = [_ for _ in os.listdir(application_path + '/data/corpus/') if _[-4:] == '.txt']
for t in texts:
    f = open(application_path + '/data/corpus/' + t, 'r', encoding="utf-8")
    bot.TEXT_RAW[t[:-4]] = f.read()

bot.RE_MESSAGE_MATCH = '^[a-zA-Z0-9\s\.,&*\-“”!\?\/\(\)]+$'

mord_globals.initialize()

#Simple prevention of multiple bot instances by keeping an empty file open.
locker_path = mord_globals.application_path + '//data/locker.txt'

if os.path.exists(locker_path):
    try:
        os.rename(locker_path, locker_path)
    except OSError as e:
        exit(1)
else:
    file_lock = open(locker_path, 'w')

file_lock = open(locker_path, 'w')

handler = logging.FileHandler(filename='mordbot.log', encoding='utf-8', mode='w')

#Bot announces wakeup and loads cogs

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.add_cog(mord_admin.Administration(bot))
    await bot.add_cog(mord_fun.FunStuff(bot))
    await bot.add_cog(mord_commands.MordbotCommands(bot))
    await bot.add_cog(mord_roles.MordbotRoles(bot))
    await bot.add_cog(mord_task.TaskCog(bot))

#Listener for custom commands and chatbot function
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    elif str(message.guild.id) in mord_globals.added_commands and message.content in mord_globals.added_commands[str(message.guild.id)]:
        if message.channel.id in mord_globals.excluded_channels:
            return
        answer = mord_globals.added_commands[str(message.guild.id)][message.content]
        await message.channel.send(answer)
    elif len (str(message.content)) > 0 and str(message.content)[0] != "!":
        if (str(message.guild.id)) in bot.TEXT_RAW:
            if len(message.content.split()) > 3 and message.content.split()[0].upper() != "MORDBOT" and re.match(bot.RE_MESSAGE_MATCH, message.content):            
                if len(bot.TEXT_RAW[str(message.guild.id)].splitlines()) < 10000:
                    bot.TEXT_RAW[str(message.guild.id)] = bot.TEXT_RAW[str(message.guild.id)] + message.content + '\n'      
            if message.channel.id not in mord_globals.excluded_channels and message.channel.id not in mord_globals.bot_chatter_excluded and (str(message.guild.id)) in bot.TEXT_MODELS:
                if re.search("MORDBOT", str(message.content.upper())):
                    try:    
                        imitation = bot.TEXT_MODELS[str(message.guild.id)].make_sentence_with_start(random.choice([word for word in message.content.split() if word not in ["mordbot", "Mordbot", "the", "The", "and", "And", "a", "A", "an", "An"]]), strict=False, tries=100)
                    except:
                        imitation = bot.TEXT_MODELS[str(message.guild.id)].make_sentence(tries=100)
                    if imitation:
                        await message.channel.send(imitation) 
                    else:
                        print(f"mordbot tried to speak in {message.guild}#{message.channel} but got confused.")               
    else:
        await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if type(error) != discord.ext.commands.errors.CommandNotFound:
        if isinstance(error, commands.UserInputError):
            #handled per command
            return
        if isinstance(error, commands.MissingRequiredArgument):
            #handled per command
            return
        logging.error(f"{error}: called by {ctx.author} in {ctx.guild}#{ctx.channel}")

bot.run(TOKEN, log_handler = handler, log_level = logging.INFO)