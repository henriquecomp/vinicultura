# Usa uma imagem oficial do Python como base
FROM python:latest

# Define o diretório de trabalho dentro do container
WORKDIR /

# Copia os arquivos do projeto para o container
COPY . .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta do FastAPI
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]