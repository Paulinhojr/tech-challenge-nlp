# 1. Imagem base oficial do Python
FROM python:3.10-slim

# 2. Diretório de trabalho dentro do container
WORKDIR /app

# 3. Variáveis de ambiente para o Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 4. Copia o arquivo de dependências
COPY requirements.txt .

# 5. Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia todo o projeto para o container
COPY . .

# 7. Expõe a porta 8000
EXPOSE 8000

# 8. Comando para iniciar o servidor Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]