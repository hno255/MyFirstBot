import discord
from discord.ext import commands
import asyncio
import random
import os

# إعداد البوت
bot = commands.Bot(command_prefix='-', intents=discord.Intents.all())
IMAGE_LINK = "https://i.postimg.cc/rs2NWCzW/6500f0dc5986495c6d6d04fc09b56b77-edit-227797447341226.jpg"

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

# --- كلاس XO ---
class TicTacToeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.board = [" " for _ in range(9)]
        self.turn = "X"

    async def play_move(self, i, b, idx):
        if self.board[idx] == " ":
            self.board[idx] = self.turn
            b.label = self.turn
            b.disabled = True
            self.turn = "O" if self.turn == "X" else "X"
            await i.response.edit_message(view=self)
        else:
            await i.response.send_message("محجوزة!", ephemeral=True)

    @discord.ui.button(label=" ", row=0)
    async def b1(self, i, b): await self.play_move(i, b, 0)
    @discord.ui.button(label=" ", row=0)
    async def b2(self, i, b): await self.play_move(i, b, 1)
    @discord.ui.button(label=" ", row=0)
    async def b3(self, i, b): await self.play_move(i, b, 2)
    @discord.ui.button(label=" ", row=1)
    async def b4(self, i, b): await self.play_move(i, b, 3)
    @discord.ui.button(label=" ", row=1)
    async def b5(self, i, b): await self.play_move(i, b, 4)
    @discord.ui.button(label=" ", row=1)
    async def b6(self, i, b): await self.play_move(i, b, 5)
    @discord.ui.button(label=" ", row=2)
    async def b7(self, i, b): await self.play_move(i, b, 6)
    @discord.ui.button(label=" ", row=2)
    async def b8(self, i, b): await self.play_move(i, b, 7)
    @discord.ui.button(label=" ", row=2)
    async def b9(self, i, b): await self.play_move(i, b, 8)

# --- أوامر البوت ---
@bot.command()
async def روليت(ctx):
    view = RouletteView()
    embed = discord.Embed(title="🎰 روليت Echo", description="اضغط على 'دخول' لتشارك!")
    embed.set_image(url=IMAGE_LINK)
    await ctx.send(embed=embed, view=view)

@bot.command()
async def xo(ctx):
    await ctx.send("لعبة XO بدأت!:", view=TicTacToeView())

# --- تشغيل البوت و Flask ---
from flask import Flask
from threading import Thread
app = Flask('')
@app.route('/')
def home(): return "البوت يعمل!"
Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

bot.run(os.environ.get('TOKEN'))

