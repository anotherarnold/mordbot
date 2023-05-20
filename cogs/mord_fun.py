import random
import re
import sys
from discord.ext import commands
sys.path.append("..")
from mord_globals import excluded
from cogs.mord_trivia import trivia_list

class FunStuff(commands.Cog, name="Fun Stuff"):
    def __init__(self, bot):
        self.bot = bot

    #return ranom fact from the Wikipedia article on common misconceptions
    @commands.command(name="trivia", help="Learn some random trivia")
    @commands.check(excluded)
    async def trivia(self, ctx):
        await ctx.send(random.choice(trivia_list))

    #Returns random numbers after parsing with regex 
    @commands.command(name="roll", help="Roll dice! Format as XdY, XdY+Z, or XdY-Z.")
    @commands.check(excluded)
    async def roll(self, ctx, roll):
        dice_pattern = "(\d+)d(\d+)([\+\-]\d+)?"
        if re.match(dice_pattern, roll):
            x = re.split(dice_pattern, roll)
            dice_mod = 0
            if x[3] != None:
                dice_mod = int(x[3])
            if int(x[2]) < 1:
                await ctx.send("A die can't have 0 sides!")
                return 
            if int(x[1]) > 70 or int(x[2]) > 1000 or abs(dice_mod) > 9999999999999:
                await ctx.send("Woah there pilgrim, don't roll so big.")
                return        
            rolls = [
                random.choice(range(1, int(x[2]) + 1))
                for _ in range(int(x[1]))
            ]
            rolls_formatted = ["[**" + str(y) + "**]" if y == int(x[2]) else "[" + str(y) + "]" for y in rolls]
            dice_mod_print = ""
            if dice_mod != 0:
                dice_mod_print = " Modifier: [" + str(dice_mod) + "]"

            await ctx.send('Roll results: ' + ' '.join([i for i in rolls_formatted]) + dice_mod_print + " Total: **" + str(sum(rolls) + dice_mod) + "**")
        else:
            await ctx.send("Please enter a roll in the form of XdY+Z.")

    @roll.error
    async def missing_roll(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a roll in the form of XdY+Z.")
        elif isinstance(error, commands.UserInputError):
            await ctx.send("There was a problem with that command.")

    @commands.command(name="whale", help = "Have the bot discuss whaling with you.")
    @commands.check(excluded)
    async def whale(self, ctx):
        await ctx.send(self.bot.TEXT_MODELS['moby_dick'].make_sentence(tries=100))
