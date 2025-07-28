import nextcord
from nextcord.ext import commands
import random

class CommunityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.verified_role = int(os.getenv('VERIFIED_ROLE_ID'))
        self.suggestions_channel = int(os.getenv('SUGGESTIONS_CHANNEL_ID'))

    @nextcord.slash_command(description="Verify to get Verified role")
    async def verify(self, interaction: nextcord.Interaction):
        number = random.randint(1000, 9999)
        await interaction.response.send_message(f"Please reply with this number: {number}", ephemeral=True)
        
        def check(m):
            return m.author == interaction.user and m.content == str(number)
        
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30.0)
            role = interaction.guild.get_role(self.verified_role)
            await interaction.user.add_roles(role)
            await interaction.followup.send("Verification successful! You now have the Verified role.", ephemeral=True)
        except asyncio.TimeoutError:
            await interaction.followup.send("Verification timed out.", ephemeral=True)

    @nextcord.slash_command(description="Submit a suggestion")
    async def suggest(self, interaction: nextcord.Interaction, suggestion: str):
        channel = self.bot.get_channel(self.suggestions_channel)
        embed = nextcord.Embed(title="New Suggestion", description=suggestion, color=0x00ff00)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        msg = await channel.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        await interaction.response.send_message("Suggestion submitted!", ephemeral=True)

    @nextcord.slash_command(description="Create a poll")
    async def poll(self, interaction: nextcord.Interaction, question: str, option1: str, option2: str):
        embed = nextcord.Embed(title=question, color=0x00ff00)
        embed.add_field(name="Option 1", value=option1, inline=False)
        embed.add_field(name="Option 2", value=option2, inline=False)
        msg = await interaction.channel.send(embed=embed)
        await msg.add_reaction("1️⃣")
        await msg.add_reaction("2️⃣")
        await interaction.response.send_message("Poll created!", ephemeral=True)

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        channel = self.bot.get_channel(int(os.getenv('WELCOME_CHANNEL_ID')))
        role = member.guild.get_role(int(os.getenv('DEFAULT_ROLE_ID')))
        await member.add_roles(role)
        await channel.send(f"Welcome {member.mention} to the server! Please use /verify to get started.")

    @commands.Cog.listener()
    async def on_member_remove(self, member: nextcord.Member):
        channel = self.bot.get_channel(int(os.getenv('WELCOME_CHANNEL_ID')))
        await channel.send(f"Goodbye {member.name}.")

def setup(bot):
    bot.add_cog(CommunityCog(bot))