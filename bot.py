import os
import random
import aiohttp
import discord
from discord.ext import commands
import datetime
import asyncio
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
determine_flip = [1, 0]


bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@bot.command()
async def sync(ctx):
    """Syncs the cogs and other components"""
    await ctx.send("Syncing components...")
    bot.unload_extension("cogs.jokes")
    bot.load_extension("cogs.jokes")
    await ctx.send("Components synced successfully.")

@bot.event
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
    elif messageContent == "fak":
        await message.delete()
        angr = await message.channel.send(f"{message.author.mention}, you can't say that")
        await asyncio.sleep(3)
        await angr.delete()
    elif messageContent == "niggah":
        await message.delete()
        angr = await message.channel.send(f"{message.author.mention}, you can't say that")
        await asyncio.sleep(3)
        await angr.delete()
    elif messageContent == "nigger":
        await message.delete()
        angr = await message.channel.send(f"{message.author.mention}, you can't say that")
        await asyncio.sleep(3)
        await angr.delete()
    else:
        return
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx: commands.Context, error: Exception):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("```**You can't do that ;-;**```")
        await ctx.message.delete()
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("```**Please enter all the required arguments**```")
        await ctx.message.delete()
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("```**Member not found, Please mention a valid user!**```")
        await ctx.message.delete()
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("```**I don't have the permissions to do that!**```")
        await ctx.message.delete()
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("```**I don't have the permissions to do that!**```")
        await ctx.message.delete()

    else:
        raise error

@bot.tree.command()
async def dadjoke(interaction: discord.Interaction) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://icanhazdadjoke.com", headers={"Accept": "application/json"}) as resp:
                data = await resp.json()
                await interaction.response.send_message(data["joke"])
@bot.tree.command()
async def joke(interaction: discord.Interaction) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://official-joke-api.appspot.com/random_joke') as resp:
                data = await resp.json()
                await interaction.response.send_message(f"{data['setup']}\n\n{data['punchline']}")
@bot.tree.command()
async def coinflip(interaction: discord.Interaction) -> None:
    try:
        if random.choice(determine_flip) == 1:
            embed = discord.Embed(title="Coinflip | (Welcomer Bot)",
                                  description=f"{interaction.user.mention} Flipped coin, we got **Heads**!")
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="Coinflip | (Welcomer Bot)",
                                  description=f"{interaction.user.mention} Flipped coin, we got **Tails**!")
            await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(e)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, *, amt):
    await ctx.channel.purge(limit=int(amt)+1)
    msg = await ctx.send(f"{amt} messages have been purged")
    await asyncio.sleep(3)
    await msg.delete()

@bot.event
async def on_member_join(member: discord.Member):
    try:
        channel = discord.utils.get(
            member.guild.text_channels, name="welcome")
        embed = discord.Embed(
            description=f"Welcome To The Crew, {member.mention}",
            color=0xFF5555,
            timestamp=datetime.datetime.now()
        )
        role = discord.utils.get(member.guild.roles, name="Member")
        await member.add_roles(role)
        await channel.send(embed=embed)
        print(f"{role}role given to memeber{member.mention}")
    except Exception as e:
        print(f"Exception :{e} and erorr was in member join")


@bot.event
async def on_ready():
    print(f"{bot.user} is now running")

bot.run(f"{TOKEN}")
