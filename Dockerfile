# Use a imagem Python como base
FROM python:3.8

# Atualize os pacotes do sistema e instale as dependências do sistema
RUN apt-get update && apt-get install -y \
    libgirepository1.0-dev \
    pkg-config \
    libcairo2-dev \
    libsystemd-dev \
    libdbus-1-dev\
    ffmpeg

# Crie um diretório de trabalho e copie seu código e requirements.txt
WORKDIR /app
COPY . /app

# Instale as dependências Python listadas no arquivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Especifique o comando padrão que será executado quando o contêiner for iniciado
CMD ["python", "main.py"]
