import os
import discord
from discord.ext import commands

# Create bot instance
bot = commands.Bot(command_prefix='.')
register_channel_id = 1216396741134389299  # Change this to your desired channel ID

# Command: setup
@bot.command()
async def setup(ctx):
    embed = discord.Embed(
        title="Registration",
        description="React with ✅ to register.",
        color=discord.Color.blue()
    )
    message = await ctx.send(embed=embed)
    await message.add_reaction("✅")

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Event: Reaction added
@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == register_channel_id and payload.emoji.name == "✅":
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if message.author == bot.user:
            # Check if the reaction is added by the bot itself
            return
        
        # Prompt user for information
        await message.channel.send("Please provide your information:")
        try:
            response_message = await bot.wait_for("message", check=lambda m: m.author == payload.member, timeout=300)
            response_embed = discord.Embed(
                title="Registration Details",
                description=f"Name: {response_message.content}\nAge: {response_message.content}\nGender: {response_message.content}\nHobby: {response_message.content}",
                color=discord.Color.blue()
            )
            register_channel = bot.get_channel(register_channel_id)
            registration_message = await register_channel.send(embed=response_embed)
            await registration_message.add_reaction("✅")  # Accept
            await registration_message.add_reaction("❌")  # Decline
            await message.channel.send("Registration details have been submitted successfully.")
        except asyncio.TimeoutError:
            await message.channel.send("Registration timed out. Please try again.")

# Run the bot
bot.run(os.getenv('TOKEN'))
