!pip install groq

#Groq




from groq import Groq
import os

# Correctly set the API key
groq_api_key = os.environ.get("GROQ_API_KEY")

# Initialize Groq with the API key directly
groq_client = Groq(api_key=groq_api_key)

# Check if the Groq client is initialized correctly
if not groq_client:
    raise Exception("Groq API key is missing!")

# Now you can use `groq_client` to interact with the Groq API


import requests

def generate_module_description(ilos, groq_api_key):
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

    # Définir la charge utile pour la requête API Groq
    payload = {
        "model": "llama-3.1-8b-instant",  # Modèle pris en charge
        "messages": [
            {"role": "system", "content": "Vous êtes un assistant utile spécialisé dans la rédaction de descriptions professionnelles de modules académiques."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 300
    }

    # Effectuer la requête
    response = requests.post(url, headers=headers, json=payload)

    # Gérer la réponse
    if response.status_code == 200:
        result = response.json()
        description = result['choices'][0]['message']['content']
        return description.strip()
    else:
        raise Exception(f"Échec de la requête API Groq : {response.status_code} - {response.text}")

# Exemple d'utilisation
ilos = [
    "Expliquer comment l'apprentissage par renforcement diffère des autres paradigmes d'apprentissage automatique.",
    "Décrire les concepts fondamentaux de l'apprentissage par renforcement",
    "Formuler des problèmes de prise de décision comme des processus de décision markoviens",
    "Implémenter des algorithmes d'apprentissage par renforcement, y compris la programmation dynamique, les méthodes de Monte Carlo, l'apprentissage par différence temporelle, Q-learning et les réseaux de neurones Q profonds (DQN)"
]

# Générer la description du module en utilisant la fonction
description = generate_module_description(ilos, groq_api_key)

# Afficher la description générée
print("\n📚 Description du module générée :\n")
print(description)

