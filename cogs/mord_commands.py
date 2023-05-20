import discord
import sys
from discord.ext import commands
sys.path.append("..")
import mord_globals

#List of hardcoded commands not to be overwritten
default_commands = ["!channelid", "!refresh", "!silence", "!silencechannel", "!unsilence", 
                    "!unsilencechannel", "!add", "!remove", "!commands", "!roll", "!trivia", 
                    "!addrole", "!getrole", "!listroles", "!loserole", "!reactrole", 
                    "!removerole", "!help", "!whale", "!enablechatbot", "!disablechatbot", 
                    "!bulkaddroles", "!markovsave", "!bulkremoveroles", "!mutechannel", 
                    "!unmutechannel", "!mute", "!unmute"]

class MordbotCommands(commands.Cog, name = "Custom Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='add', help="Add a command to the bot. Enter a name for the command, then either a piece of text, a link, or an attachment. Multiple attachments are possible but may look bad.")
    @commands.has_permissions(kick_members=True)
    async def add_command(self, ctx, *args):
        arguments = list(args)
        #arguments.pop(0)
        try:
            test = arguments[0][0]
        except:
            await ctx.send("Command not added; Enter a keyword and a value.") 
            return 
        if len(arguments) == 1:
            if arguments[0][0] == '!':
                key = arguments[0]
            else:
                key = '!' + arguments[0]
            if key not in default_commands:
                if str(ctx.message.guild.id) not in mord_globals.added_commands:
                    mord_globals.added_commands[str(ctx.message.guild.id)] = {"!hi":"Hello! This is a default command!"}
                try:
                    mord_globals.added_commands[str(ctx.message.guild.id)][key] = " ".join([_.url for _ in ctx.message.attachments])
                    #mord_globals.added_commands[str(ctx.message.guild.id)][key] = ctx.message.attachments[0].url
                except:
                    await ctx.send("Command not added; Enter a keyword and a value.")
                    return
                try:                     
                    mord_globals.save_commands(mord_globals.added_commands)
                    await ctx.send("Command " + key + " added.")
                except:
                    await ctx.send("Something went wrong! Changes may not be saved. Contact the bot admin if problems persist.")   
            else:
                await ctx.send("Command not added; default commands cannot be overwritten.")
        elif len(arguments) > 1:
            if arguments[0][0] == '!':
                key = arguments[0]
            else:
                key = '!' + arguments[0]
            command = " ".join(arguments[1:])
            if key not in default_commands:
                if str(ctx.message.guild.id) not in mord_globals.added_commands:
                    mord_globals.added_commands[str(ctx.message.guild.id)] = {"!hi":"Hello! This is a default command!"}
                try:           
                    mord_globals.added_commands[str(ctx.message.guild.id)][key] = command
                    mord_globals.save_commands(mord_globals.added_commands)
                    await ctx.send("Command " + key + " added.")
                except:
                    await ctx.send("Something went wrong! Changes may not be saved. Contact the bot admin if problems persist.")   
            else:
                await ctx.send("Command not added; default commands cannot be overwritten.")
        else:
            await ctx.send("Command not added; Enter a keyword and a value.") 
    
    @add_command.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a command to add.")
        elif isinstance(error, commands.UserInputError):
            await ctx.send("There was a problem with that command.")

    @commands.command(name='remove', help="Remove a given command from the bot.")
    @commands.has_permissions(kick_members=True)
    async def remove_command(self, ctx, command : str = commands.parameter(description = "Command to remove from the bot.")):
        if str(ctx.message.guild.id) in mord_globals.added_commands:
            if command[0] != "!":
                command = "!" + command
            if command in mord_globals.added_commands[str(ctx.message.guild.id)]:
                try:
                    mord_globals.added_commands[str(ctx.message.guild.id)].pop(command)
                    mord_globals.save_commands(mord_globals.added_commands)
                    await ctx.send("Command " + command + " removed.")   
                except:                    
                    await ctx.send("Something went wrong! Changes may not be saved. Contact the bot admin if problems persist.")     
            else:
                await ctx.send("Command not found.")
        else:
            await ctx.send("Command not found.")

    @remove_command.error
    async def remove_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a command to remove.")
        elif isinstance(error, commands.UserInputError):
            await ctx.send("There was a problem with that command.")

    @commands.command(name='commands', help="List all custom commands.")
    @commands.check(mord_globals.excluded)
    async def list_commands(self, ctx):
        response = discord.Embed(
            title=self.bot.user.name + " knows how to:",
            color = discord.Colour.red()
        )
        if str(ctx.message.guild.id) in mord_globals.added_commands:
            if len(mord_globals.added_commands[str(ctx.message.guild.id)]) > 0:
                for key in mord_globals.added_commands[str(ctx.message.guild.id)]:
                    response.add_field(
                        name=str(key), value=""
                    )
            else:
                response.add_field(name="No commands here...", value="Add some with !add")
        else:
            response.add_field(name="No commands here...", value="Add some with !add")
        await ctx.send(embed=response)
