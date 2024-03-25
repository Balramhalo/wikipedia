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
        description="Click the button below to register.",
        color=discord.Color.blue()
    )
    register_button = discord.ui.Button(label="Register", style=discord.ButtonStyle.primary, custom_id="register")
    view = discord.ui.View()
    view.add_item(register_button)
    await ctx.send(embed=embed, view=view)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Event: Interaction
@bot.event
async def on_button_click(interaction):
    if interaction.custom_id == "register":
        await interaction.respond(
            type=discord.InteractionType.ChannelMessageWithSource,
            content="Please provide your information:"
        )
        registration_embed = discord.Embed(
            title="Registration Form",
            description="Please provide the following details:",
            color=discord.Color.green()
        )
        registration_message = await interaction.channel.send(embed=registration_embed)
        
        def check(message):
            return message.author == interaction.user

        try:
            response_message = await bot.wait_for("message", check=check, timeout=300)  # Timeout after 5 minutes
            response_embed = discord.Embed(
                title="Registration Details",
                description=f"Name: {response_message.content}\nAge: {response_message.content}\nGender: {response_message.content}\nHobby: {response_message.content}",
                color=discord.Color.blue()
            )
            register_channel = bot.get_channel(register_channel_id)
            registration_message = await register_channel.send(embed=response_embed)
            await registration_message.add_reaction("✅")  # Accept
            await registration_message.add_reaction("❌")  # Decline
            await interaction.followup.send("Registration details have been submitted successfully.")
        except asyncio.TimeoutError:
            await interaction.followup.send("Registration timed out. Please try again.")

# Run the bot
bot.run(os.getenv('TOKEN'))
