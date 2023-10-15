# Use a imagem Alpine Linux como base
FROM python:3.9-alpine

# Instale as dependências do FFmpeg
RUN apk --no-cache add ffmpeg

# Configure o ambiente para evitar problemas de codificação
ENV PYTHONUNBUFFERED 1

# Crie e defina o diretório de trabalho
WORKDIR /app

# Copie o código da sua aplicação para o contêiner
COPY . .

# Instale as dependências Python listadas no arquivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Especifique o comando padrão que será executado quando o contêiner for iniciado
CMD ["python", "main.py"]
