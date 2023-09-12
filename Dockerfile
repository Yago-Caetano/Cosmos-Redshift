# Use a imagem base do Python
FROM python:latest

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie os arquivos do seu projeto para o contêiner
COPY . /app

# Instale as dependências (se você tiver um arquivo requirements.txt)
RUN pip install -r requirements.txt

# Comando para executar a sua aplicação
CMD ["python", "main.py"]