# -------------------------------
# Étape 1 : Image de base
# -------------------------------
FROM python:3.10-slim

# Répertoire de travail
WORKDIR /app

# Copier le fichier de dépendances en premier (meilleur cache Docker)
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
COPY . .

# Exposer le port 8000 pour Prometheus
EXPOSE 8010

# Définir la variable d'environnement (sera injectée par Kubernetes)
ENV GROQ_API_KEY=""

# Commande de lancement
CMD ["python", "main.py"]
