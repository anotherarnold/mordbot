import discord
import sys
from discord.ext import commands
sys.path.append("..")
import mord_globals

class MordbotRoles(commands.Cog, name="Role Management"):
    def __init__(self, bot):
        self.bot = bot
    
    #Listener for reactrole, applies role when specific emojies are applied to specific messages
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return    
        if str(payload.channel_id) in mord_globals.role_mess and str(payload.message_id) in mord_globals.role_mess[str(payload.channel_id)]:
            if str(payload.emoji) in mord_globals.react_role[str(payload.guild_id)].values():
                role = list(filter(lambda x: mord_globals.react_role[str(payload.guild_id)][x] == str(payload.emoji), mord_globals.react_role[str(payload.guild_id)]))[0]
                guild = self.bot.get_guild(payload.guild_id)
                role_list = [i.name for i in list(guild.roles)]
                if role in role_list:
                    new_role = discord.utils.get(guild.roles,  name=role)
                    await payload.member.add_roles(new_role)
            else:
                user = self.bot.get_user(payload.user_id)
                channel = self.bot.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                await message.remove_reaction(payload.emoji, user)

    #Listener for reactrole, removes role when specific emojies are removed from specific messages
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if str(payload.channel_id) in mord_globals.role_mess and str(payload.message_id) in mord_globals.role_mess[str(payload.channel_id)]:
            if str(payload.emoji) in mord_globals.react_role[str(payload.guild_id)].values():
                role = list(filter(lambda x: mord_globals.react_role[str(payload.guild_id)][x] == str(payload.emoji), mord_globals.react_role[str(payload.guild_id)]))[0]
                guild = self.bot.get_guild(payload.guild_id)
                if role in [i.name for i in list(guild.roles)]:
                    old_role = discord.utils.get(guild.roles,  name=role)
                    member = await(guild.fetch_member(payload.user_id))
                    if member is not None:
                        await member.remove_roles(old_role)

    #Sets up a react role message, where users can react to that message with specific emojis to be given roles
    #Roles can then be removed by unselecting the emojis
    @commands.command(name="reactrole", help="Set up reaction roles. The bot will react to your message with your set up role-emoji pairs; users can react to" + 
                                            " that message to receive or remove those roles. Message can be edited without problems. Just use !reactrole to have" +
                                            " the bot react with every role you have set up, or list every role you want the bot to react to your message with." +
                                            " If reactrole has problems, move the bot role higher in the server's roles than the roles you want it to add." +
                                            " Don't move it above mod/admin roles!")
    @commands.has_permissions(manage_roles = True)
    async def reactrole(self, ctx):
        args = ctx.message.content.split()
        args.pop(0)
        if str(ctx.message.guild.id) in mord_globals.react_role:
            mord_globals.role_mess[str(ctx.message.channel.id)] = str(ctx.message.id)
            role_list = [i.name for i in list(ctx.guild.roles)]
            try:
                mord_globals.save_role_mess(mord_globals.role_mess)
            except:
                await ctx.send("Something went wrong! I may have had trouble accessing some files. Try again and contact your admin if problems persist.")
                return
            if len(args) == 0:
                for role in mord_globals.react_role[str(ctx.message.guild.id)]:
                    if role in role_list:
                        #This should raise a NotFound or TypeError exception if it tries to apply an illegal emoji
                        #but it doesn't seem to. Since the exception causes no crashes or seemingly doesn't interrupt
                        #the operation of the API, I'm not sure how to handle it. 
                        #try:
                        #    await ctx.message.add_reaction(mord_globals.react_role[str(ctx.message.guild.id)][role])
                        #except:
                        #    print("error")
                        #    await ctx.send(f"The emoji for the following role was not found: {role}")
                        try:
                            await ctx.message.add_reaction(mord_globals.react_role[str(ctx.message.guild.id)][role])
                        except:
                            await ctx.send("Unable to react with role: " + role + " but I'll keep going!")
            else:
                roles = []
                for arg in args:
                    if arg in mord_globals.react_role[str(ctx.message.guild.id)]:
                        roles.append(arg)
                    elif arg in mord_globals.react_role[str(ctx.message.guild.id)].values():
                        roles.append([key for key in mord_globals.react_role[str(ctx.message.guild.id)] if mord_globals.react_role[str(ctx.message.guild.id)][key]==arg][0])
                if len(roles) == 0:
                    await ctx.send("None of the roles listed matched what I have down. Were they listed correctly? You can list the emojis for the roles if that's simpler!")
                    return
                for role in mord_globals.react_role[str(ctx.message.guild.id)]:
                    if role in roles and role in role_list:
                        try:
                            await ctx.message.add_reaction(mord_globals.react_role[str(ctx.message.guild.id)][role])
                        except:
                            await ctx.send("Unable to react with role: " + role + " but I'll keep going!")
        else:
            await ctx.send("Roles aren't set up for this server. Try adding some roles with the addrole command.")        
            try:
                del mord_globals.role_mess[str(ctx.message.channel.id)]
                mord_globals.save_role_mess(mord_globals.role_mess)
            except:
                return

    @commands.command(name='addrole', help="Add a role-emoji pair. Put roles with spaces in their names in quotes. Don't add mod/admin roles!")
    @commands.has_permissions(manage_roles = True)
    async def add_role(self, ctx, role : str = commands.parameter(description = "Role to add. Put roles with spaces in their names in quotes."), 
                       emoji : str = commands.parameter(description = "Emoji to pair w/ role. The bot can't tell if it's an emoji or not.")):
        if str(ctx.message.guild.id) not in mord_globals.react_role.keys():
            mord_globals.react_role[str(ctx.message.guild.id)] = {}
        if emoji not in list(mord_globals.react_role[str(ctx.message.guild.id)].values()):
            try:
                mord_globals.react_role[str(ctx.message.guild.id)][role] = emoji
                mord_globals.save_roles(mord_globals.react_role)
                await ctx.send("Role " + role + " added.")
            except:
                await ctx.send("Something went wrong! I may have had trouble accessing some files. Try again and contact your admin if problems persist.")
        else:
            await ctx.send("Role not added; either message was formatted incorrectly or emoji already in use for a role.")  

    @add_role.error
    async def role_add_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a role to add and paired emoji.")
        elif isinstance(error, commands.UserInputError):
            await ctx.send("There was a problem with that command.")

    @commands.command(name='bulkaddroles', help="Add role-emoji pairs in bulk. List pairs of roles and emojis to add them all at once.")
    @commands.has_permissions(manage_roles = True)
    async def bulk_add_roles(self, ctx, *args):
        arguments = list(args)
        pairs_added = []
        if len(arguments) == 0:
            await ctx.send("Please enter a list of role-emoji pairs.")
            return
        if len(arguments) % 2 != 0:
            await ctx.send("Please ensure each role is paired with an emoji.")
            return
        if str(ctx.message.guild.id) not in mord_globals.react_role.keys():
            mord_globals.react_role[str(ctx.message.guild.id)] = {}
        while len(arguments) != 0:
            role = arguments.pop(0)
            emoji = arguments.pop(0)
            if emoji not in list(mord_globals.react_role[str(ctx.message.guild.id)].values()):
                try:
                    mord_globals.react_role[str(ctx.message.guild.id)][role] = emoji
                    mord_globals.save_roles(mord_globals.react_role)
                    pairs_added.append(role + ": " + emoji)
                except:
                    await ctx.send("Something went wrong! I may have had trouble accessing some files. Try again and contact your admin if problems persist.")
                    return
        await ctx.send("Pairs added: " + " ".join(pairs_added))

    @commands.command(name='removerole', help="Remove a role-emoji pair from the bot's archive.")
    @commands.has_permissions(manage_roles = True)
    async def remove_role(self, ctx, command : str = commands.parameter(description = "Role name or role emoji to remove")):
        if command in mord_globals.react_role[str(ctx.message.guild.id)]:
            try:
                mord_globals.react_role[str(ctx.message.guild.id)].pop(command)
                if len(mord_globals.react_role[str(ctx.message.guild.id)]) == 0:
                    del mord_globals.react_role[str(ctx.message.guild.id)]
                mord_globals.save_roles(mord_globals.react_role)
                await ctx.send("Role " + command + " removed.")
            except:
                await ctx.send("Something went wrong! I may have had trouble accessing some files. Try again and contact your admin if problems persist.")  
                return
        elif command in list(mord_globals.react_role[str(ctx.message.guild.id)].values()):
            role_to_remove = [key for key in mord_globals.react_role[str(ctx.message.guild.id)] if mord_globals.react_role[str(ctx.message.guild.id)][key]==command][0]
            try:
                mord_globals.react_role[str(ctx.message.guild.id)].pop(role_to_remove)
                if len(mord_globals.react_role[str(ctx.message.guild.id)]) == 0:
                    del mord_globals.react_role[str(ctx.message.guild.id)]
                mord_globals.save_roles(mord_globals.react_role)
                await ctx.send("Role " + role_to_remove + " removed.")
            except:
                await ctx.send("Something went wrong! I may have had trouble accessing some files. Try again and contact your admin if problems persist.")  
                return
        else:
            await ctx.send("Role not found. You may need to put it in quotes if the name has spaces.")

    @remove_role.error
    async def role_remove_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a role to remove.")
        elif isinstance(error, commands.UserInputError):
            await ctx.send("There was a problem with that command.")

    @commands.command(name='bulkremoveroles', help="Remove role-emoji pairs in bulk. List roles or emojis to remove them all at once.")
    @commands.has_permissions(manage_roles = True)
    async def bulk_remove_roles(self, ctx, *args):
        arguments = list(args)
        roles_removed = []
        for command in arguments:
            if command in mord_globals.react_role[str(ctx.message.guild.id)]:
                try:
                    mord_globals.react_role[str(ctx.message.guild.id)].pop(command)
                    if len(mord_globals.react_role[str(ctx.message.guild.id)]) == 0:
                        del mord_globals.react_role[str(ctx.message.guild.id)]
                    mord_globals.save_roles(mord_globals.react_role)
                    roles_removed.append(command)
                except:
                    await ctx.send("Something went wrong! I may have had trouble accessing some files. Try again and contact your admin if problems persist.")  
                    return
            elif command in list(mord_globals.react_role[str(ctx.message.guild.id)].values()):
                role_to_remove = [key for key in mord_globals.react_role[str(ctx.message.guild.id)] if mord_globals.react_role[str(ctx.message.guild.id)][key]==command][0]
                try:
                    mord_globals.react_role[str(ctx.message.guild.id)].pop(role_to_remove)
                    if len(mord_globals.react_role[str(ctx.message.guild.id)]) == 0:
                        del mord_globals.react_role[str(ctx.message.guild.id)]
                    mord_globals.save_roles(mord_globals.react_role)
                    roles_removed.append(role_to_remove)
                except:
                    await ctx.send("Something went wrong! I may have had trouble accessing some files. Try again and contact your admin if problems persist.")  
                    return
        if len(roles_removed) == 0:
            await ctx.send("No roles removed; were they entered correctly?")
        else:
            await ctx.send("Roles removed: " + " ".join(roles_removed))       

    @commands.command(name='listroles', help="List all role-emoji pairs.")
    @commands.check(mord_globals.excluded)
    async def list_roles(self, ctx):
        response = discord.Embed(
            title=self.bot.user.name +  " knows these roles:",
            color = discord.Colour.red()
        )
        if str(ctx.message.guild.id) in mord_globals.react_role:
            if len(mord_globals.react_role[str(ctx.message.guild.id)]) > 0:
                for key in mord_globals.react_role[str(ctx.message.guild.id)]:
                    response.add_field(
                        name=str(key), value=mord_globals.react_role[str(ctx.message.guild.id)][key]
                    )
            else:
                response.add_field(name="No roles to be found...", value="Add some with !addrole")
        else:
            response.add_field(name="No roles to be found...", value="Add some with !addrole")
        await ctx.send(embed=response)

    @commands.command(name="getrole", help="Have the bot give you a role.")
    @commands.check(mord_globals.excluded)
    async def get_role(self, ctx, command : str = commands.parameter(description = "Role name or emoji to recieve.")):
        role_list = [i.name for i in list(ctx.guild.roles)]
        user = ctx.author
        if command in mord_globals.react_role[str(ctx.message.guild.id)]:
            if command in role_list:
                role = discord.utils.get(ctx.guild.roles, name=command)
                await user.add_roles(role)
            else:
                await ctx.channel.send("Role not in server.")
        elif command in list(mord_globals.react_role[str(ctx.message.guild.id)].values()):
            role_to_add = [key for key in mord_globals.react_role[str(ctx.message.guild.id)] if mord_globals.react_role[str(ctx.message.guild.id)][key]==command][0]
            if role_to_add in role_list:
                role = discord.utils.get(ctx.guild.roles,  name=role_to_add)
                await user.add_roles(role)
            else:
                await ctx.channel.send("Role not in server.")
        else:
            await ctx.channel.send("Role not in role list. You may need to put it in quotes if the name has spaces.")

    @get_role.error
    async def get_role_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a role to recieve.")
        elif isinstance(error, commands.UserInputError):
            await ctx.send("There was a problem with that command.")

    @commands.command(name="loserole", help="Have the bot remove a role from you.")
    @commands.check(mord_globals.excluded)
    async def lose_role(self, ctx, command : str = commands.parameter(description = "Role name or emoji to have the bot remove from you.")):
        role_list = [i.name for i in list(ctx.guild.roles)]
        user = ctx.author
        if command in mord_globals.react_role[str(ctx.message.guild.id)]:
            if command in role_list:
                role = discord.utils.get(ctx.guild.roles, name=command)
                await user.remove_roles(role)
            else:
                await ctx.channel.send("Role not in server.")
        elif command in list(mord_globals.react_role[str(ctx.message.guild.id)].values()):
            role_to_add = [key for key in mord_globals.react_role[str(ctx.message.guild.id)] if mord_globals.react_role[str(ctx.message.guild.id)][key]==command][0]
            if role_to_add in role_list:
                role = discord.utils.get(ctx.guild.roles,  name=role_to_add)
                await user.remove_roles(role)
            else:
                await ctx.channel.send("Role not in server.")
        else:
            await ctx.channel.send("Role not in role list. You may need to put it in quotes if the name has spaces.")

    @lose_role.error
    async def lose_role_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a role to remove.")
        elif isinstance(error, commands.UserInputError):
            await ctx.send("There was a problem with that command.")