# === main.py ===

from flask import Flask, jsonify, request
from groq import Groq
import os
import requests

app = Flask(__name__)

# Récupérer la clé API Groq depuis la variable d'environnement
groq_api_key = os.environ.get("GROQ_API_KEY")

if not groq_api_key:
    raise Exception("Groq API key is missing!")

# Initialiser le client Groq
groq_client = Groq(api_key=groq_api_key)

def generate_module_description(ilos, groq_api_key):
    """Génère une description professionnelle du module à partir des ILOs."""

    ilos_formatted = "\n".join(f"- {ilo}" for ilo in ilos)
    prompt = f"""
Rédigez une description professionnelle et fluide du module qui résume les résultats d'apprentissage sans les répéter mot à mot.
La description doit se concentrer sur les compétences et les connaissances que les étudiants acquerront à la fin du module, étant donné les résultats d'apprentissage suivants :
{ilos_formatted}
"""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "Vous êtes un assistant utile spécialisé dans la rédaction de descriptions professionnelles de modules académiques."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 300
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        description = result['choices'][0]['message']['content']
        return description.strip()
    else:
        raise Exception(f"Échec de la requête API Groq : {response.status_code} - {response.text}")

# === API Routes ===

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "✅ API Groq App is running!"})

@app.route('/generate', methods=['POST'])
def generate():
    """
    Exemple de requête :
    POST /generate
    {
        "ilos": [
            "Expliquer les différences entre apprentissage supervisé et non supervisé",
            "Décrire les concepts fondamentaux de l'apprentissage par renforcement"
        ]
    }
    """
    data = request.get_json()
    if not data or 'ilos' not in data:
        return jsonify({"error": "Paramètre 'ilos' manquant"}), 400

    try:
        description = generate_module_description(data['ilos'], groq_api_key)
        return jsonify({"description": description})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === Point d’entrée ===
if __name__ == "__main__":
    # Écoute sur toutes les interfaces pour Kubernetes
    app.run(host="0.0.0.0", port=5000)
