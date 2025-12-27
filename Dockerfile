# abdoul-didacticiel/Dockerfile
# Image de base légère
FROM python:3.12-slim as builder

# Empêcher l'écriture de .pyc et forcer l'affichage des logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    libpq-dev gcc curl --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# --- Étape finale ---
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copie des packages installés depuis le builder
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Installation de libpq (nécessaire pour Postgres)
RUN apt-get update && apt-get install -y libpq-dev curl --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copie du code
COPY . .

# Sécurité : Création d'un utilisateur non-root
RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

CMD ["gunicorn", "src.wsgi:application", "--bind", "0.0.0.0:8000"]