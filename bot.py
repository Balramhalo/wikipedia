import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
import aiohttp
import os

# Initialize the bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
client = commands.Bot(command_prefix="!", intents=intents)
slash = SlashCommand(client, sync_commands=True)

# API details
API_URL = "https://blox-fruit-stock-fruit.p.rapidapi.com/check_stock"
API_HEADERS = {
    "x-rapidapi-key": "e56398d3aamsh2d2882a00a60e2cp15925bjsn4aae874b0887",
    "x-rapidapi-host": "blox-fruit-stock-fruit.p.rapidapi.com",
}

@client.event
async def on_ready():
    print(f"{client.user} is now online!")
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name="/bloxstock | Check stock!"))

@slash.slash(
    name="bloxstock",
    description="Get the current stock of Blox Fruits."
)
async def bloxstock(ctx: SlashContext):
    await ctx.defer()  # Acknowledge the command

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL, headers=API_HEADERS) as response:
                if response.status == 200:
                    data = await response.json()
                    stock_list = data.get("stock", [])

                    if stock_list:
                        embed = discord.Embed(
                            title="Current Blox Fruits Stock",
                            description="Here's the list of fruits currently in stock:",
                            color=discord.Color.blue()
                        )
                        for fruit in stock_list:
                            embed.add_field(name=fruit["name"], value=f"Price: {fruit['price']} B$", inline=False)

                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("No fruits are currently in stock!")
                else:
                    error_body = await response.text()
                    await ctx.send(
                        f"Failed to fetch stock data. HTTP Status: {response.status}\nDetails: {error_body}"
                    )
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

# Run the bot
client.run(os.getenv("TOKEN"))