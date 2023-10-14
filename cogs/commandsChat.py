import discord
from discord.ext import commands
import random

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Estou conectado como {bot.user.name} - {bot.user.id}')

# COMANDOS BASES PARA O BOT APENAS RESPONDER
@bot.command()
async def teste(ctx):
    await ctx.send("Bot está no ar!")

@bot.command()
async def hello(ctx):
    await ctx.send("Olá!")

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! {latency}ms")

@bot.command()
async def caracoroa(ctx):
    escolha = random.choice(["cara", "coroa"])

    if escolha == "cara":
        emoji = "🌝"
    else:
        emoji = "👑"

    await ctx.message.add_reaction(emoji)
