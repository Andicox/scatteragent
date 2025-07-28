import nextcord
from nextcord.ext import commands
import re

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.profanity = ['badword1', 'badword2']  # Add more as needed
        self.log_channel = int(os.getenv('MOD_LOG_CHANNEL_ID'))

    @nextcord.slash_command(description="Kick a member")
    @commands.has_permissions(kick_members=True)
    async def kick(self, interaction: nextcord.Interaction, member: nextcord.Member, *, reason: str = "No reason"):
        await member.kick(reason=reason)
        await interaction.response.send_message(f"Kicked {member.mention}")
        await self.bot.get_channel(self.log_channel).send(f"{member.mention} was kicked: {reason}")

    @nextcord.slash_command(description="Ban a member")
    @commands.has_permissions(ban_members=True)
    async def ban(self, interaction: nextcord.Interaction, member: nextcord.Member, *, reason: str = "No reason"):
        await member.ban(reason=reason)
        await interaction.response.send_message(f"Banned {member.mention}")
        await self.bot.get_channel(self.log_channel).send(f"{member.mention} was banned: {reason}")

    @nextcord.slash_command(description="Timeout a member")
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, interaction: nextcord.Interaction, member: nextcord.Member, minutes: int, *, reason: str = "No reason"):
        await member.timeout(nextcord.utils.utcnow() + nextcord.utils.timedelta(minutes=minutes), reason=reason)
        await interaction.response.send_message(f"Timed out {member.mention} for {minutes} minutes")
        await self.bot.get_channel(self.log_channel).send(f"{member.mention} was timed out for {minutes} minutes: {reason}")

    @nextcord.slash_command(description="Warn a member")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, interaction: nextcord.Interaction, member: nextcord.Member, *, reason: str = "No reason"):
        await interaction.response.send_message(f"Warned {member.mention}")
        await self.bot.get_channel(self.log_channel).send(f"{member.mention} was warned: {reason}")

    @nextcord.slash_command(description="Clear messages")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, interaction: nextcord.Interaction, amount: int):
        await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"Cleared {amount} messages", ephemeral=True)
        await self.bot.get_channel(self.log_channel).send(f"{amount} messages cleared by {interaction.user.mention}")

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if message.author.bot:
            return
        content = message.content.lower()
        if any(word in content for word in self.profanity):
            await message.delete()
            await message.author.timeout(nextcord.utils.utcnow() + nextcord.utils.timedelta(minutes=5), reason="Profanity")
            await self.bot.get_channel(self.log_channel).send(f"{message.author.mention} timed out for profanity")

def setup(bot):
    bot.add_cog(ModerationCog(bot))