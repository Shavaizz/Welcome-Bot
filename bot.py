import os
import random
import traceback
from discord.ext.commands import Context
import aiohttp
import discord
from discord.ext import commands
import datetime
import asyncio
from typing import Optional, Literal
from discord.ext.commands import Greedy
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.environ['TOKEN']
determine_flip = [1, 0]
now = datetime.datetime.now()
formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author},You don't have perms!")
    else :
        print(traceback.format_exc())

@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
  ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()
        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1
    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")
@bot.listen()
async def on_message(message):
    username = str(message.author)
    channel = str(message.channel)
    user_message = str(message.content)
    if message.author == bot.user:
        return
    else:
        print(f"{username} said: {user_message} in {channel}")
    if message.author == bot.user:
        return
    messageContent = message.content.lower()
    if messageContent == "hello":
        await message.channel.send("Hi,How are you?")
    elif messageContent == "oye":
        await message.channel.send("Han Oye")
    elif messageContent == "bruh":
        await message.channel.send("What?")
    elif messageContent == "this bot sucks":
        await message.channel.send("No, you do")
@bot.command()
@commands.has_permissions(manage_roles=True)
async def verify(ctx, *,member:discord.Member):
    role1 = discord.utils.get(member.guild.roles, name="Member")
    role2 = discord.utils.get(member.guild.roles, name="Unverified Member")
    channel = discord.utils.get(ctx.guild.channels, name="lounge")
    await channel.send(f"Welcome {member.mention} to {ctx.guild.name}")
    await ctx.send(f"{member.mention} has been verified")
    await member.remove_roles(role2)
    await member.add_roles(role1)
@bot.command()
@commands.has_permissions(manage_roles=True)
async def unverify(ctx,*, member:discord.Member):
    await member.ban(reason=f"{member.mention} has been banned by Welcome Bot, He has been unverified")
    await ctx.send(f"{member.mention} has been banned, he was unverified.")
@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, *, amt):
    await ctx.channel.purge(limit=int(amt)+1)
    msg = await ctx.send(f"Purged, {amt} messages successfully")
    await asyncio.sleep(3)
    await msg.delete()
@bot.tree.command(name="dadjoke",description='Makes a random dadjoke')
async def dadjoke(interaction: discord.Interaction) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://icanhazdadjoke.com", headers={"Accept": "application/json"}) as resp:
            data = await resp.json()
            await interaction.response.send_message(data["joke"])
@bot.tree.command(name="joke",description='Makes a random joke')
async def joke(interaction: discord.Interaction) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get('https://official-joke-api.appspot.com/random_joke') as resp:
            data = await resp.json()
            await interaction.response.send_message(f"{data['setup']}\n\n{data['punchline']}")
@bot.tree.command(name="coinflip",description='Flips a coin to get either heads or tails')
async def coinflip(interaction: discord.Interaction) -> None:
    if random.choice(determine_flip) == 1:
        embed = discord.Embed(title="Coinflip | (Welcomer Bot)",
                                description=f"{interaction.user.mention} Flipped coin, we got **Heads**!")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title="Coinflip | (Welcomer Bot)",
                                  description=f"{interaction.user.mention} Flipped coin, we got **Tails**!")
        await interaction.response.send_message(embed=embed)
@bot.tree.command(name="pie",description='Throw a pie at someone')
async def pie(interaction:discord.Interaction, member:discord.Member, message:str) -> None:
  embed= discord.Embed(title=f"User:{member.name} Has a pie for you 🥧",
                    description=f'{member.mention} says {message}',
                    color=0xFF5555
                        )
  await interaction.response.send_message(embed=embed)
@bot.event
async def on_member_join(member: discord.Member):
    channel = discord.utils.get(
        member.guild.text_channels, name="welcome")
    embed = discord.Embed(
        description=f"Welcome To The Crew, {member.mention}",
        color=0xFF5555,
        timestamp=datetime.datetime.now(),
        )
    role = discord.utils.get(member.guild.roles, name="Unverified Member")
    await member.add_roles(role)
    await channel.send(embed=embed)
    print(f"{role}role given to memeber{member.mention}")
@bot.event
async def on_ready():
    print(f"{bot.user} is now running")
bot.run(f"{TOKEN}")