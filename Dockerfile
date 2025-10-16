# -------------------------------
# Étape 1 : Image de base
# -------------------------------
FROM python:3.10-slim

# Répertoire de travail dans le conteneur
WORKDIR /app

# Copier le code source
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir requests groq

# Définir la variable d'environnement pour Groq
ENV GROQ_API_KEY=""

# Commande de lancement
CMD ["python", "main.py"]
