from keep_alive import keep_alive
import discord
from discord.ext import commands
import wikipedia
import os

# Initialize bot
bot = commands.Bot(command_prefix='w!')

# Run the bot
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="w!invite | w!invite"))
    print("Bot is ready.")

# Set up environment variable for token
TOKEN = os.getenv("TOKEN")

# Function to split content into chunks of 1024 characters
def split_chunks(content):
    return [content[i:i+1000] for i in range(0, len(content), 1000)]

# Command to search Wikipedia
@bot.command()
async def search(ctx, *, query):
    try:
        # Search Wikipedia
        wikipedia.set_lang("en")  # Set language to English
        page = wikipedia.page(query)

        # Get page summary, image, and URL
        summary = wikipedia.summary(query, sentences=5)  # Increased to 5 sentences
        image_url = page.images[0] if page.images else None
        wikipedia_url = page.url

        # Create and send embed with Wikipedia information
        embed = discord.Embed(title=page.title, url=wikipedia_url, description=summary)
        embed.set_footer(text="✨ Powered By Wikipedia Bot")  # Added footer

        if image_url:
            embed.set_image(url=image_url)

        # Split content into chunks if exceeds 1000 characters
        embed_chunks = split_chunks(embed.description)
        for i, chunk in enumerate(embed_chunks):
            if i == 0:
                msg = await ctx.send(embed=embed)
            else:
                await msg.channel.send(embed=discord.Embed(description=chunk))

    except wikipedia.exceptions.DisambiguationError as e:
        await ctx.send(f"Multiple results found. Please specify your query more precisely.")
    except wikipedia.exceptions.PageError as e:
        await ctx.send(f"No Wikipedia page found for \"{query}\".")
    except Exception as e:
        await ctx.send(f"An error occurred")

# Command to get random Wikipedia article
@bot.command()
async def random(ctx):
    try:
        # Get a random Wikipedia article
        random_page = wikipedia.random()
        page = wikipedia.page(random_page)

        # Get page summary, image, and URL
        summary = wikipedia.summary(random_page, sentences=5)  # Increased to 5 sentences
        image_url = page.images[0] if page.images else None
        wikipedia_url = page.url

        # Create and send embed with Wikipedia information
        embed = discord.Embed(title=page.title, url=wikipedia_url, description=summary)
        embed.set_footer(text="✨ Powered By Wikipedia Bot")  # Added footer

        if image_url:
            embed.set_image(url=image_url)

        # Split content into chunks if exceeds 1000 characters
        embed_chunks = split_chunks(embed.description)
        for i, chunk in enumerate(embed_chunks):
            if i == 0:
                msg = await ctx.send(embed=embed)
            else:
                await msg.channel.send(embed=discord.Embed(description=chunk))

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

# Ping command
@bot.command()
async def ping(ctx):
    latency = bot.latency * 1000  # latency in milliseconds
    await ctx.send(f'Pong! Latency: {latency:.2f}ms')

# Invite command
@bot.command()
async def invite(ctx):
    invite_link = "https://discord.com/oauth2/authorize?client_id=1221381422204584018&permissions=2147797056&scope=bot+applications.commands"
    support_server_link = "https://discord.com/oauth2/authorize?client_id=1221381422204584018&permissions=2147797056&scope=bot+applications.commands"
    embed = discord.Embed(title="Invite Links", description=f"[Click Here To Invite Wikipedia]({invite_link})\n[Click Here To Join Wikipedia Support]({support_server_link})", color=discord.Color.blurple())
    await ctx.send(embed=embed)

# Remove default help command
bot.remove_command('help')

# Custom help command
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Wikipedia Bot Help", description="[Invite](https://discord.com/oauth2/authorize?client_id=1221381422204584018&permissions=2147797056&scope=bot+applications.commands) | [Support Server](https://discord.com/oauth2/authorize?client_id=1221381422204584018&permissions=2147797056&scope=bot+applications.commands) | [Vote](https://discord.com/oauth2/authorize?client_id=1221381422204584018&permissions=2147797056&scope=bot+applications.commands)\n\n- Default Prefix **:** `w!`\n- Usage **:** `w!command-name`\n\n> __**Wiki Commands**__\n`search`, `random`\n\n> __**Misc Commands**__\n`ping`, `invite`, `help`", color=discord.Color.blurple())

    # Add user's thumbnail
    embed.set_thumbnail(url=ctx.author.avatar_url)

    await ctx.send(embed=embed)

#  Custom commands command
@bot.command()
async def commands(ctx):
    embed = discord.Embed(title="Wikipedia Bot Help", description="[Invite](https://discord.com/oauth2/authorize?client_id=1221381422204584018&permissions=2147797056&scope=bot+applications.commands) | [Support Server](https://discord.com/oauth2/authorize?client_id=1221381422204584018&permissions=2147797056&scope=bot+applications.commands) | [Vote](https://discord.com/oauth2/authorize?client_id=1221381422204584018&permissions=2147797056&scope=bot+applications.commands)\n\n- Default Prefix **:** `w!`\n- Usage **:** `w!command-name`\n\n> __**Wiki Commands**__\n`search`, `random`\n\n> __**Misc Commands**__\n`ping`, `invite`, `help`", color=discord.Color.blurple())

    # Add user's thumbnail
    embed.set_thumbnail(url=ctx.author.avatar_url)

    await ctx.send(embed=embed)
keep_alive()

# Run the bot
bot.run(TOKEN)
