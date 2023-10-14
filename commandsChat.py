import discord
from discord.ext import commands

# Defina as intenções
intents = discord.Intents.all()  # Ou personalize as intenções conforme necessário

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Estou conectado como {bot.user.name} - {bot.user.id}')

@bot.command()
async def oifilho(ctx):
    await ctx.send("Oi pai!")

@bot.command()
async def hello(ctx):
    await ctx.send("Olá!")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")
