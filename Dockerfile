# -------------------------------
# Étape 1 : Image de base
# -------------------------------
FROM python:3.10-slim

# Répertoire de travail
WORKDIR /app

# Copier le code source dans le conteneur
COPY . .

# Installer les dépendances nécessaires
RUN pip install --no-cache-dir flask requests groq

# Exposer le port Flask
EXPOSE 5000

# Variable d’environnement pour Groq (sera surchargée par Kubernetes)
ENV GROQ_API_KEY=""

# Commande de lancement Flask
CMD ["python", "main.py"]
