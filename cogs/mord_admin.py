from discord.ext import commands
import sys
import re
import markovify
sys.path.append("..")
import mord_globals

class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot            

    @commands.command(name="serverid", hidden=True)
    @commands.has_permissions(kick_members=True)
    async def serverid(self, ctx):
        await ctx.send("server id: " + str(ctx.message.guild.id))

    @commands.command(name="channelid", hidden=True)
    @commands.has_permissions(kick_members=True)
    async def channelid(self, ctx):
        await ctx.send("channel id: " + str(ctx.message.channel.id))

    @commands.command(name="silence", help="Disables most commands and chatbot activity temporarily in all channels in the server." +
                       " Use !unsilencechannel to enable bot in just those channels. Moderator commands will still work under silence.")
    @commands.has_permissions(kick_members=True)
    async def silence(self, ctx):
        for channel in ctx.message.guild.channels:
            mord_globals.excluded_channels.add(channel.id)
        mord_globals.save_excluded(mord_globals.excluded_channels)
        await ctx.send("Going silent!")

    @commands.command(name="unsilence", help="Undoes the silence command, enabling bot activities in all channels in the server.")
    @commands.has_permissions(kick_members=True)
    async def unsilence(self, ctx):
        tracker = False
        for channel in ctx.message.guild.channels:
            if channel.id in mord_globals.excluded_channels:
                mord_globals.excluded_channels.remove(channel.id)
                tracker = True
        if (tracker):
            mord_globals.save_excluded(mord_globals.excluded_channels)
            await ctx.send("Activities resuming in all channels.")
        else:
            await ctx.send("No channels were silent.")

    @commands.command(name="silencechannel", help="Temporarily disables bot activity in the channel the command is used. Moderator commands will still function.")
    @commands.has_permissions(kick_members=True)
    async def silence_channel(self, ctx):
        if ctx.message.channel.id not in mord_globals.excluded_channels:
            mord_globals.excluded_channels.add(ctx.message.channel.id)
            mord_globals.save_excluded(mord_globals.excluded_channels)
            await ctx.send("Going silent!")
        else:
            await ctx.send("Channel already silent.")

    @commands.command(name="unsilencechannel", help="Enables bot activities in the channel the command is used.")
    @commands.has_permissions(kick_members=True)
    async def unsilence_channel(self, ctx):
        if ctx.message.channel.id in mord_globals.excluded_channels:
            mord_globals.excluded_channels.remove(ctx.message.channel.id)
            mord_globals.save_excluded(mord_globals.excluded_channels)
            await ctx.send("Resuming activities.")
        else:
            await ctx.send("Silence mode not active.")
    
    #This was used in debugging but could probably be cut.
    @commands.command(name="refresh", hidden = True)
    @commands.is_owner()
    async def refresh(self, ctx):
        try:
            mord_globals.refresh()
            await ctx.send("Settings refreshed.") 
        except:
            await ctx.send("Something went wrong! I may have had trouble accessing some files. Contact the bot admin if problems persist.") 
    
    @commands.command(name="enablechatbot", help = "Enables the chatbot in your server, letting it learn from what people are saying. It can take a minute to process.")
    @commands.has_permissions(administrator = True)
    async def enablechatbot(self, ctx):
        print(f"enablechatbot called by {ctx.author} in {ctx.guild}#{ctx.channel}")
        working_history = [message async for message in ctx.channel.history(limit=5000)]
        fulltext = ''
        for m in working_history:
            if re.match(self.bot.RE_MESSAGE_MATCH, m.content) and len(m.content.split()) > 3 and m.content[0] != "!" and not m.author == self.bot.user:
                fulltext += m.content + '\n'
        if (str(ctx.message.guild.id)) in self.bot.TEXT_RAW:
            self.bot.TEXT_RAW[str(ctx.message.guild.id)] = self.bot.TEXT_RAW[str(ctx.message.guild.id)] + fulltext
        else:
            self.bot.TEXT_RAW[str(ctx.message.guild.id)] = fulltext            
        self.bot.TEXT_MODELS[str(ctx.message.guild.id)] = markovify.NewlineText(self.bot.TEXT_RAW[str(ctx.message.guild.id)], state_size=2, retain_original=False)
        await ctx.send("Markov chatbot model for this server generated successfully!")
    
    @commands.command(name="disablechatbot", help="Disables the chatbot in your server. If you want to retrain the bot's vocabulary, run this, then re-enable it!")
    @commands.has_permissions(administrator=True)
    async def disablechatbot(self, ctx):
        print(f"disablechatbot called by {ctx.author} in {ctx.guild}#{ctx.channel}")
        if (str(ctx.message.guild.id)) in self.bot.TEXT_RAW:
            self.bot.TEXT_RAW.pop(str(ctx.message.guild.id))
            mord_globals.deletemarkovfile(str(ctx.message.guild.id) + '.txt')
            if str(ctx.message.guild.id) in self.bot.TEXT_MODELS:
                self.bot.TEXT_MODELS.pop(str(ctx.message.guild.id))
            await ctx.send("Markov chatbot for this server has been disabled.")
        else:
            await ctx.send("No chatbot stuff found. Is there a problem?")

    @commands.command(name="mutechannel", help="Temporarily disables chatbot functionality in the channel the command is used, leaving other bot commands enabled.")
    @commands.has_permissions(kick_members=True)
    async def chatter_silence(self, ctx):
        if ctx.message.channel.id not in mord_globals.bot_chatter_excluded:
            mord_globals.bot_chatter_excluded.add(ctx.message.channel.id)
            mord_globals.save_bot_chatter_excluded(mord_globals.bot_chatter_excluded)
            await ctx.send("Chatbot disabled in this channel.")
        else:
            await ctx.send("Chatbot already disabled in this channel.")

    @commands.command(name="unmutechannel", help="Enables chatbot activities in the channel the command is used.")
    @commands.has_permissions(kick_members=True)
    async def chatter_unsilence(self, ctx):
        if ctx.message.channel.id in mord_globals.bot_chatter_excluded:
            mord_globals.bot_chatter_excluded.remove(ctx.message.channel.id)
            mord_globals.save_bot_chatter_excluded(mord_globals.bot_chatter_excluded)
            await ctx.send("Resuming chatbot activities.")
        else:
            await ctx.send("Chatter silence mode not active.")
    
    @commands.command(name="mute", help="Temporarily disables chatbot across all server channels without deleting" +
                       " the chatbot functionality or disabling other bot commands.")
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx):
        for channel in ctx.message.guild.channels:
            mord_globals.bot_chatter_excluded.add(channel.id)
        mord_globals.save_bot_chatter_excluded(mord_globals.bot_chatter_excluded)
        await ctx.send("Muting chatbot across server!")

    @commands.command(name="unmute", help="Re-enables chatbot across all server channels if the chatbot function has been enabled with !enablechatbot.")
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx):
        tracker = False
        for channel in ctx.message.guild.channels:
            if channel.id in mord_globals.bot_chatter_excluded:
                mord_globals.bot_chatter_excluded.remove(channel.id)
                tracker = True
        if (tracker):
            mord_globals.save_bot_chatter_excluded(mord_globals.bot_chatter_excluded)
            await ctx.send("Chatbot activities resuming in all channels.")
        else:
            await ctx.send("No channels were muted.")
