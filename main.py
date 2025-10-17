# === main.py ===

from groq import Groq
import os
import requests

# Récupérer la clé API Groq depuis la variable d'environnement
groq_api_key = os.environ.get("GROQ_API_KEY")

# Vérifier que la clé est disponible
if not groq_api_key:
    raise Exception("Groq API key is missing!")

# Initialiser le client Groq
groq_client = Groq(api_key=groq_api_key)

def generate_module_description(ilos, groq_api_key):
    """Génère une description professionnelle du module à partir des ILOs (Intended Learning Outcomes)."""

    # Préparer le prompt
    ilos_formatted = "\n".join(f"- {ilo}" for ilo in ilos)
    prompt = f"""
Rédigez une description professionnelle et fluide du module qui résume les résultats d'apprentissage sans les répéter mot à mot.
La description doit se concentrer sur les compétences et les connaissances que les étudiants acquerront à la fin du module, étant donné les résultats d'apprentissage suivants :
{ilos_formatted}
"""

    # Définir l'URL de l'API Groq et les en-têtes
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }

    # Définir la charge utile
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "Vous êtes un assistant utile spécialisé dans la rédaction de descriptions professionnelles de modules académiques."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 300
    }

    # Envoyer la requête
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        description = result['choices'][0]['message']['content']
        return description.strip()
    else:
        raise Exception(f"Échec de la requête API Groq : {response.status_code} - {response.text}")


# === Exemple d'utilisation ===
ilos = [
    "Expliquer comment l'apprentissage par renforcement diffère des autres paradigmes d'apprentissage automatique.",
    "Décrire les concepts fondamentaux de l'apprentissage par renforcement.",
    "Formuler des problèmes de prise de décision comme des processus de décision markoviens.",
    "Implémenter des algorithmes d'apprentissage par renforcement, y compris la programmation dynamique, les méthodes de Monte Carlo, l'apprentissage par différence temporelle, Q-learning et les réseaux de neurones Q profonds (DQN)."
]

# Appeler la fonction et afficher le résultat
description = generate_module_description(ilos, groq_api_key)
print("\n📚 Description du module générée :\n")
print(description)
# === Garder le conteneur en vie ===
while True:
    time.sleep(3600)  # dort 1h et recommence, juste pour que le pod reste vivant

