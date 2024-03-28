import os
import discord
from discord.ext import commands
import openai

# Set up Discord bot
bot = commands.Bot(command_prefix='!')

# Load OpenAI API key from environment variable
openai.api_key = os.environ['OPENAI_API_KEY']

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def ask(ctx, *, question):
    response = openai.Completion.create(
        engine="davinci",
        prompt=question + "\n",
        max_tokens=50
    )
    await ctx.send(response.choices[0].text.strip())

# Run the bot with the Discord token from environment variable
bot.run(os.environ['TOKEN'])
