import discord
from discord.ext import commands
from decouple import config
import youtube_dl
from discord import FFmpegPCMAudio
from youtubesearchpython import VideosSearch
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"Aplicação Python está rodando na porta {port}")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

players = {}
queue = []  # Lista para armazenar as músicas na fila
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
async def play(ctx, *, query):
    try:
        if ctx.voice_client:
            videosSearch = VideosSearch(query, limit=1)
            results = videosSearch.result()
            video_url = results['result'][0]['link']

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
                info = ydl.extract_info(video_url, download=False)
                url2 = info['formats'][0]['url']

            # Adicione a música à fila
            queue.append({'url': url2, 'query': query})

            if not ctx.voice_client.is_playing() and not ctx.voice_client.is_paused():
                await play_next(ctx)
            else:
                await ctx.send(f"Música adicionada à fila: {query}")
        else:
            channel = ctx.author.voice.channel
            voice_channel = await channel.connect()
            videosSearch = VideosSearch(query, limit=1)
            results = videosSearch.result()
            video_url = results['result'][0]['link']

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
                info = ydl.extract_info(video_url, download=False)
                url2 = info['formats'][0]['url']
                voice_channel.play(FFmpegPCMAudio(url2, **ffmpeg_options))

            await ctx.send(f"Tocando agora: {query}")
    except Exception as e:
        await ctx.send(f"Error: `{e}`")



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

@bot.command()
async def skip(ctx):
    try:
        if ctx.voice_client:
            ctx.voice_client.stop()
            await play_next(ctx)  # Toca a próxima música na fila
    except Exception as error:
        await ctx.send(f"Error6: `{error}`")

async def play_next(ctx):
    if len(queue) > 0:
        video = queue.pop(0)
        source = FFmpegPCMAudio(video['url'], **ffmpeg_options)
        await ctx.send(f"Preparando para tocar: {video['query']}")
        ctx.voice_client.play(source, after=lambda e: play_next(ctx))
        await ctx.send(f"Tocando agora: {video['query']}")
    else:
        await ctx.send("A fila de reprodução está vazia.")
        
token = config('TOKEN_SERVER')

if token is not None:
    bot.run(token)
else:
    print("A variável de ambiente 'TOKEN_SERVER' não está definida.")
