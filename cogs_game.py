import nextcord
from nextcord.ext import commands
import json
import sqlite3

class GameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect('scatteragent.db')
        self.db.execute('''CREATE TABLE IF NOT EXISTS users 
                         (discord_id TEXT, game_username TEXT)''')
        self.db.execute('''CREATE TABLE IF NOT EXISTS tickets 
                         (ticket_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, issue TEXT)''')

    @nextcord.slash_command(description="Register in-game username")
    async def register(self, interaction: nextcord.Interaction, username: str):
        self.db.execute('INSERT OR REPLACE INTO users (discord_id, game_username) VALUES (?, ?)', 
                       (str(interaction.user.id), username))
        self.db.commit()
        await interaction.response.send_message(f"Registered {username} to your account!", ephemeral=True)

    @nextcord.slash_command(description="Open a support ticket")
    async def ticket(self, interaction: nextcord.Interaction, issue: str):
        ticket_id = self.db.execute('INSERT INTO tickets (user_id, issue) VALUES (?, ?)', 
                                  (str(interaction.user.id), issue)).lastrowid
        self.db.commit()
        support_channel = self.bot.get_channel(int(os.getenv('SUPPORT_CHANNEL_ID')))
        await support_channel.send(f"Ticket #{ticket_id} from {interaction.user.mention}: {issue}")
        await interaction.response.send_message(f"Ticket #{ticket_id} created!", ephemeral=True)

    @nextcord.slash_command(description="View game leaderboard")
    async def leaderboard(self, interaction: nextcord.Interaction):
        # Mock leaderboard data
        leaderboard = [
            {"name": "Player1", "score": 1000},
            {"name": "Player2", "score": 800},
            {"name": "Player3", "score": 600}
        ]
        embed = nextcord.Embed(title="War Scatter Leaderboard", color=0x00ff00)
        for idx, player in enumerate(leaderboard, 1):
            embed.add_field(name=f"{idx}. {player['name']}", value=f"Score: {player['score']}", inline=False)
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(GameCog(bot))