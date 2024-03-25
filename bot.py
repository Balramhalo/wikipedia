import discord
from discord.ext import commands
import os

# Initialize bot with intents
intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
bot = commands.Bot(command_prefix='w!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def setup(ctx):
    # Send a DM to the user
    await ctx.author.send("Please provide your name, age, gender, and hobby in the following format:\nName: Your Name\nAge: Your Age\nGender: Your Gender\nHobby: Your Hobby")

    # Wait for user's responses
    def check(m):
        return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)

    try:
        response = await bot.wait_for("message", check=check, timeout=60.0)
    except asyncio.TimeoutError:
        await ctx.author.send("You took too long to respond.")
        return

    # Parse user's responses
    user_info = {}
    lines = response.content.split('\n')
    for line in lines:
        key, value = line.split(': ', 1)  # Split each line into key-value pair
        user_info[key.lower()] = value

    # Send confirmation message
    confirmation_message = await ctx.author.send("Are you sure you want to submit this information? Reply with 'yes' to confirm or 'no' to cancel.")

    # Wait for user's confirmation
    def confirm_check(m):
        return m.author == ctx.author and isinstance(m.channel, discord.DMChannel) and m.content.lower() in ['yes', 'no']

    try:
        confirm_response = await bot.wait_for("message", check=confirm_check, timeout=60.0)
    except asyncio.TimeoutError:
        await ctx.author.send("You took too long to respond.")
        return

    if confirm_response.content.lower() == 'yes':
        # Process the submitted information
        await ctx.author.send("Information submitted successfully.")
        # Perform further actions (e.g., assigning roles)
    else:
        await ctx.author.send("Operation canceled.")

# Set up environment variable for token
TOKEN = os.getenv("TOKEN")

bot.run(TOKEN)
