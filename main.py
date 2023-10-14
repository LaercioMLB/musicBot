from discord.ext import commands
from decouple import config  # Importe a função 'config' do 'decouple'
from commandsChat import bot  # Importe o bot do arquivo commandsChat.py

# Acesse a variável de ambiente 'TOKEN_SERVER' usando 'decouple'
token = config('TOKEN_SERVER')

# Verifique se a variável de ambiente 'TOKEN_SERVER' está definida
if token is not None:
    bot.run(token)
else:
    print("A variável de ambiente 'TOKEN_SERVER' não está definida.")
