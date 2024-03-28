import os
import discord
from discord.ext import commands
import openai

# Set up Discord bot
bot = commands.Bot(command_prefix='!')

# Set up OpenAI model without requiring an API key
openai.api_key = None  # Disable the need for an API key
openai.api_base = "https://api.openai.com/v1"  # Set API base URL

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def ask(ctx, *, question):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question + "\n",
        max_tokens=50
    )
    await ctx.send(response.choices[0].text.strip())

# Run the bot with the Discord token
bot.run(os.environ['TOKEN'])
