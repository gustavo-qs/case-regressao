FROM python:3.11-slim

WORKDIR /app

# 1) Atualiza índices via IPv4 e instala todas as deps nativas
RUN apt-get update -o Acquire::ForceIPv4=true \
 && apt-get install -y --no-install-recommends \
      gcc \
      libpq-dev \
      python3-dev \
 && rm -rf /var/lib/apt/lists/*

# 2) Copia requirements e instala Python deps
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt gunicorn

# 3) Copia o restante do código
COPY . .
RUN mkdir -p staticfiles

# 4) Porta exposta e comando de inicialização
EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn pred_app.wsgi:application --bind 0.0.0.0:8000"]
