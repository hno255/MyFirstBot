from game import TicTacToeView, TicTacToe
import discord
from discord.ext import commands
import asyncio
import random
import os

# إعداد البوت
bot = commands.Bot(command_prefix='-', intents=discord.Intents.all())

# الإعدادات
TARGET_CHANNEL_ID = 1526317080943657040
IMAGE_LINK = "https://i.postimg.cc/kXL0BLyq/1783971316738.png"

# --- كلاس الروليت ---
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
        await asyncio.sleep(2)
        winner = random.choice(self.participants)
        embed = discord.Embed(title="🎰 نتيجة روليت Echo", description=f"🎉 **الفائز هو:** {winner}")
        embed.set_image(url=IMAGE_LINK)
        await interaction.message.edit(content=None, embed=embed)

# --- الأوامر ---
@bot.command()
async def روليت(ctx):
    view = RouletteView()
    embed = discord.Embed(title="🎰 روليت Echo", description="اضغط على 'دخول' لتشارك!")
    embed.set_image(url=IMAGE_LINK)
    await ctx.send(embed=embed, view=view)

@bot.command()
async def xo(ctx):
    game = TicTacToe()
    view = TicTacToeView(game, ctx.author, ctx.author)
    await ctx.send("لعبة XO بدأت!:", view=view)

# --- كود الرد بالصورة ---
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.channel.id == TARGET_CHANNEL_ID and message.attachments:
        await message.channel.send(IMAGE_LINK)
    
    await bot.process_commands(message)

# --- تشغيل البوت و Flask ---
from flask import Flask
from threading import Thread
app = Flask('')

@app.route('/')
def home():
    return "البوت يعمل!"

def run():
    app.run(host='0.0.0.0', port=8080)

t = Thread(target=run)
t.start()

bot.run(os.environ.get('TOKEN'))
