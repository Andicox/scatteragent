import nextcord
from nextcord.ext import commands
import os
from dotenv import load_dotenv
import json
import asyncio

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID', 0))

# Bot setup with intents
intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Load cogs
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await load_cogs()

# Run bot
bot.run(TOKEN)