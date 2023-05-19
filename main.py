import json
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

bot = commands.Bot(command_prefix=":")

try:
    with open('sets.json') as setsfile:
        sets = json.load(setsfile)
except Exception:
        sets = {}

def set_save():
    with open('sets.json', "w+") as setsfile:
        json.dump(sets, setsfile, indent=4)

@bot.command(name="set.create", aliases=["create","s.create", "set_create", "s_create"])
@has_permissions(manage_roles=True)
async def set_create(ctx, setname):
    guild = ctx.guild
    id = ctx.guild.id

    if id not in sets:
        sets[id] = {}
    
    if setname not in sets[id]:
        sets[id][setname] = []
        set_save()
        await ctx.send(embed=discord.Embed(title=f":white_check_mark: `{setname}` set created.",color=discord.Color.green()))
    else:
        await ctx.send(embed=discord.Embed(title=f":x: A set named `{setname}` already exists.",color=discord.Color.red()))

@set_create.error
async def create_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title=":x: Missing permissions", color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.command(name="set.list", aliases=["list","s.list", "set_list", "s_list"])
@has_permissions(manage_roles=True)
async def set_list(ctx):
    guild = ctx.guild
    id = ctx.guild.id

    if id not in sets:
        await ctx.send(embed=discord.Embed(title=":x: There are no sets in this guild.", color=discord.Color.red()))
    else:
        listembed = discord.Embed(title=f"Guild Sets", description='\n'.join(sets.get(id)), color=discord.Color.blurple())
        listembed.set_footer(text=guild, icon_url=guild.icon_url)
        await ctx.send(embed=listembed)

@set_list.error
async def list_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title=":x: Missing permissions", color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.command(name="set.get", aliases=["get","s.get", "set_get", "s_get"])
@has_permissions(manage_roles=True)
async def set_get(ctx, setname):
    guild = ctx.guild
    id = ctx.guild.id

    if id not in sets:
        sets[id] = {}

    if setname not in sets[id]:
        await ctx.send(embed=discord.Embed(title=f":x: There is no set named `{setname}`.",color=discord.Color.red()))
    else:
        if sets[id].get(setname) == []:
            await ctx.send(embed=discord.Embed(title=f":x: Set `{setname}` has no roles attatched.",color=discord.Color.red()))
        else:
            getembed = discord.Embed(title=f"{setname} Set", color=discord.Color.blurple())
            getembed.add_field(name="Contents:", value=', '.join(sets[id].get(setname)))
            getembed.set_footer(text=guild, icon_url=guild.icon_url)
            await ctx.send(embed=getembed)

@set_get.error
async def get_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title=":x: Missing permissions", color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.command(name="set.add", aliases=["add","s.add", "set_add", "s_add"])
@has_permissions(manage_roles=True)
async def set_add(ctx, setname, setcontents):
    guild = ctx.guild
    id = ctx.guild.id

    if id not in sets:
        sets[id] = {}
    
    if setname not in sets[id]:
        await ctx.send(embed=discord.Embed(title=f":x: There is no set named `{setname}`.", color=discord.Color.red()))
    else:
        if setcontents not in sets[id][setname]:
            sets[id][setname] += [setcontents]
            set_save()
            await ctx.send(embed=discord.Embed(title=f":white_check_mark: Added `{setcontents}` to `{setname}` set.", color=discord.Color.green()))
        else:
            await ctx.send(embed=discord.Embed(title=f":x: `{setcontents}` is already in `{setname}`.", color=discord.Color.red()))

@set_add.error
async def add_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title=":x: Missing permissions", color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.command(name="set.remove", aliases=["remove", "s.remove", "set_remove", "s_remove", "set.rem", "s.rem", "set_rem", "s_rem"])
@has_permissions(manage_roles=True)
async def set_remove(ctx, setname, setcontents):
    guild = ctx.guild
    id = ctx.guild.id

    if id not in sets:
        sets[id] = {}
    
    if setname not in sets[id]:
        await ctx.send(embed=discord.Embed(title=f":x: There is no set named `{setname}`.", color=discord.Color.red()))
    else:
        if setcontents in sets[id][setname]:
            contents = sets[id].get(setname)
            contents.remove(setcontents)
            sets[id][setname] = contents
            set_save()
            await ctx.send(embed=discord.Embed(title=f":white_check_mark: Removed `{setcontents}` from `{setname}`", color=discord.Color.green()))
        else:
            await ctx.send(embed=discord.Embed(title=f":x: `{setcontents}` is not in `{setname}`", color=discord.Color.red()))

@set_remove.error
async def remove_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title=":x: Missing permissions", color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.command(aliases=["promote", "set.op", "s.op", "set_op", "s_op"])
@has_permissions(manage_roles=True)
async def op(ctx, user:discord.Member, setname):
    sent = False
    guild = ctx.guild
    id = ctx.guild.id
	
    if id not in sets:
        sets[id] = {}
        set_save()
    if setname not in sets[id]:
        await ctx.send(embed=discord.Embed(title=f":x: There are no sets named `{setname}`.", color=discord.Color.red()))
    else:
        contents = sets[id].get(setname)
        for check in contents:
            if discord.utils.get(ctx.guild.roles, name=check):
                role = discord.utils.get(ctx.guild.roles, name=check)
                await user.add_roles(role)
                if sent != True:
                    await ctx.send(embed=discord.Embed(title=f":white_check_mark: Oped `{user}` to roles in `{setname}` set.", color = discord.Color.green()))
                    sent = True
            else:
                await ctx.send(embed=discord.Embed(title=f":x: There are no role with the name `{check}`.", color=discord.Color.red()))

@op.error
async def op_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title=":x: Missing permissions", color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.command(aliases=["demote", "set.deop", "s.deop", "set_deop", "s_deop"])
@has_permissions(manage_roles=True)
async def deop(ctx, user:discord.Member, setname):
    sent = False
    guild = ctx.guild
    id = ctx.guild.id
	
    if id not in sets:
        sets[id] = {}
        set_save()
    if setname not in sets[id]:
        await ctx.send(embed=discord.Embed(title=f":x: There are no sets named `{setname}`.", color=discord.Color.red()))
    else:
        contents = sets[id].get(setname)
        for check in contents:
            if discord.utils.get(ctx.guild.roles, name=check):
                role = discord.utils.get(ctx.guild.roles, name=check)
                await user.remove_roles(role)
                if sent != True:
                    await ctx.send(embed=discord.Embed(title=f":white_check_mark: Deoped `{user}` from roles in `{setname}` set.", color = discord.Color.green()))
                    sent = True
            else:
                await ctx.send(embed=discord.Embed(title=f":x: There are no role with the name `{check}`.", color=discord.Color.red()))

@deop.error
async def deop_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title=":x: Missing permissions", color=discord.Color.red())
        await ctx.send(embed=embed)
        

with open('config', "r") as config:
    token = config.read()
    bot.run(token)