from keep_alive import keep_alive
import discord
from discord.ext import commands
import openai
import os

# Initialize your Discord bot with a prefix
bot = commands.Bot(command_prefix='r!')

# Set up your OpenAI API key
openai.api_key = os.getenv('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')

# Command to list dishes based on ingredients
@bot.command()
async def dish(ctx, *, ingredients):
    # Use ChatGPT to understand user input and generate a response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"I want to make a dish with ingredients: {ingredients}.",
        max_tokens=50
    )
    
    # Extract dish names from the response
    dishes = response.choices[0].text.strip().split("\n")
    
    # Create an embed for displaying the list of dishes
    embed = discord.Embed(title="Dishes made with {}".format(ingredients), color=discord.Color.green())
    for dish in dishes:
        embed.add_field(name="Dish", value=dish, inline=False)
    
    # Send the embed as a message
    await ctx.send(embed=embed)

# Command to list ingredients for a specific dish
@bot.command()
async def recipe(ctx, *, dish_name):
    # Use ChatGPT to understand user input and generate a response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Ingredients for {dish_name}.",
        max_tokens=50
    )
    
    # Extract ingredients from the response
    ingredients = response.choices[0].text.strip()
    
    # Create an embed for displaying the ingredients
    embed = discord.Embed(title="Ingredients for {}".format(dish_name), description=ingredients, color=discord.Color.blue())
    
    # Send the embed as a message
    await ctx.send(embed=embed)

keep_alive()

# Run the bot
bot.run(os.getenv('TOKEN'))
