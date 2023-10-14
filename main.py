import discord
from discord.ext import commands
from decouple import config
import youtube_dl
from discord import FFmpegPCMAudio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

players = {}
COR = 0xF7FE2E

@bot.event
async def on_ready():
    print(bot.user.name)
    print("===================")

@bot.command()
async def entrar(ctx):
    try:
        channel = ctx.author.voice.channel
        await channel.connect()
    except discord.errors.InvalidArgument:
        await ctx.send("O bot já está em um canal de voz")
    except Exception as error:
        await ctx.send(f"Ein Error1: `{error}`")

@bot.command()
async def sair(ctx):
    try:
        mscleave = discord.Embed(
            title="\n",
            color=COR,
            description="Sai do canal de voz e a música parou!"
        )
        voice_client = ctx.guild.voice_client
        await ctx.send(embed=mscleave)
        await voice_client.disconnect()
    except AttributeError:
        await ctx.send("O bot não está em nenhum canal de voz.")
    except Exception as Hugo:
        await ctx.send(f"Ein Error2: `{Hugo}`")

ffmpeg_options = {
    'options': '-vn'
}

@bot.command()
async def play(ctx, *, yt_url):
    try:
        if ctx.voice_client:
            voice = ctx.voice_client
            if ctx.guild.id in players:
                players[ctx.guild.id].stop()
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'default_search': 'ytsearch',  # Define a pesquisa padrão para YouTube
                'outtmpl': 'downloads/%(title)s.%(ext)s',
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(yt_url, download=False)
                url2 = info['formats'][0]['url']
                source = FFmpegPCMAudio(url2, **ffmpeg_options)
            voice.play(source)
            # Resto do código permanece o mesmo
        else:
            channel = ctx.author.voice.channel
            voice_channel = await channel.connect()
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'default_search': 'ytsearch',  # Define a pesquisa padrão para YouTube
                'outtmpl': 'downloads/%(title)s.%(ext)s',
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(yt_url, download=False)
                url2 = info['formats'][0]['url']
                source = FFmpegPCMAudio(url2, **ffmpeg_options)
            players[ctx.guild.id] = voice_channel
            voice_channel.play(source)
    except Exception as e:
        await ctx.send(f"Error3: `{e}`")

@bot.command()
async def pause(ctx):
    try:
        mscpause = discord.Embed(
            title="\n",
            color=COR,
            description="Música pausada com sucesso!"
        )
        await ctx.send(embed=mscpause)
        players[ctx.guild.id].pause()
    except Exception as error:
        await ctx.send(f"Error4: `{error}`")

@bot.command()
async def resume(ctx):
    try:
        mscresume = discord.Embed(
            title="\n",
            color=COR,
            description="Música pausada com sucesso!"
        )
        await ctx.send(embed=mscresume)
        players[ctx.guild.id].resume()
    except Exception as error:
        await ctx.send(f"Error5: `{error}`")

token = config('TOKEN_SERVER')

if token is not None:
    bot.run(token)
else:
    print("A variável de ambiente 'TOKEN_SERVER' não está definida.")
