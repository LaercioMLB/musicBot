import discord
from discord.ext import commands

# Defina as intenções
intents = discord.Intents.all()  # Ou personalize as intenções conforme necessário

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Estou conectado como {bot.user.name} - {bot.user.id}')


# BOT ENTRA E SAI DO CHAT
@bot.command()
async def entrar(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def sair(ctx):
    await ctx.voice_client.disconnect()

#---------------------------------------------------------#

@bot.command()
async def oifilho(ctx):
    await ctx.send("Oi pai!")

@bot.command()
async def hello(ctx):
    await ctx.send("Olá!")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")