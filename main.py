import discord
from discord.ext import commands
import asyncio
import random

bot = commands.Bot(command_prefix='-', intents=discord.Intents.all())

# ضعي رابط صورتك هنا
IMAGE_LINK =  "https://postimg.cc/5693BGNf"

class RouletteView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.participants = []

    @discord.ui.button(label="دخول", style=discord.ButtonStyle.green)
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.name not in self.participants:
            self.participants.append(interaction.user.name)
            await interaction.response.send_message(f"✅ تم تسجيلك يا {interaction.user.name}!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ أنت مسجل بالفعل!", ephemeral=True)

    @discord.ui.button(label="بدء الروليت", style=discord.ButtonStyle.blurple)
    async def start(self, interaction: discord.Interaction, button: discord.ui.Button):
        if len(self.participants) < 1:
            return await interaction.response.send_message("يجب أن يدخل شخص واحد على الأقل!", ephemeral=True)
        
        await interaction.response.edit_message(content="🌀 **العجلة تدور الآن...**", view=None)
        
        # تأثير الدوران
        for _ in range(3):
            await asyncio.sleep(0.8)
            
        winner = random.choice(self.participants)
        embed = discord.Embed(title="🎰 نتيجة روليت Echo", description=f"🎉 **الفائز هو:** {winner}")
        embed.set_image(url=IMAGE_LINK)
        await interaction.message.edit(content=None, embed=embed)

@bot.command()
async def روليت(ctx):
    view = RouletteView()
    embed = discord.Embed(title="🎰 روليت Echo", description="اضغط على 'دخول' لتشارك!")
    embed.set_image(url=IMAGE_LINK)
    await ctx.send(embed=embed, view=view)

bot.run(os.environ.get('TOKEN'))

