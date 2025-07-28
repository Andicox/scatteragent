import nextcord
from nextcord.ext import commands
import sqlite3
import os

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect('scatteragent.db')
        self.db.execute('''CREATE TABLE IF NOT EXISTS custom_commands 
                         (name TEXT, response TEXT)''')
        self.db.execute('''CREATE TABLE IF NOT EXISTS ping_opt 
                         (user_id TEXT, opted_in INTEGER)''')

    @nextcord.slash_command(description="Create an announcement")
    @commands.has_permissions(administrator=True)
    async def announce(self, interaction: nextcord.Interaction, message: str):
        channel = self.bot.get_channel(int(os.getenv('ANNOUNCEMENT_CHANNEL_ID')))
        embed = nextcord.Embed(title="Announcement", description=message, color=0xff0000)
        await channel.send(embed=embed)
        await interaction.response.send_message("Announcement posted!", ephemeral=True)

    @nextcord.slash_command(description="Opt in/out of announcement pings")
    async def pingopt(self, interaction: nextcord.Interaction, option: str):
        opted_in = 1 if option.lower() == "in" else 0
        self.db.execute('INSERT OR REPLACE INTO ping_opt (user_id, opted_in) VALUES (?, ?)', 
                       (str(interaction.user.id), opted_in))
        self.db.commit()
        await interaction.response.send_message(f"You have opted {'in' if opted_in else 'out'} of announcement pings.", ephemeral=True)

    @nextcord.slash_command(description="Create a custom command")
    @commands.has_permissions(administrator=True)
    async def createcommand(self, interaction: nextcord.Interaction, name: str, response: str):
        self.db.execute('INSERT INTO custom_commands (name, response) VALUES (?, ?)', (name, response))
        self.db.commit()
        await interaction.response.send_message(f"Custom command /{name} created!", ephemeral=True)

    @nextcord.slash_command(description="Assign role via reaction")
    @commands.has_permissions(manage_roles=True)
    async def reactrole(self, interaction: nextcord.Interaction, emoji: str, role: nextcord.Role, message: str):
        embed = nextcord.Embed(title="Role Assignment", description=message, color=0x00ff00)
        msg = await interaction.channel.send(embed=embed)
        await msg.add_reaction(emoji)
        self.db.execute('INSERT INTO react_roles (message_id, emoji, role_id) VALUES (?, ?, ?)', 
                       (str(msg.id), emoji, str(role.id)))
        self.db.commit()
        await interaction.response.send_message("Reaction role created!", ephemeral=True)

def setup(bot):
    bot.add_cog(AdminCog(bot))