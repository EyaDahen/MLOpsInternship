# === main.py ===
from groq import Groq
import os
import requests
import time
from prometheus_client import start_http_server, Counter, Histogram

# ====== [1] DÉFINIR LES MÉTRIQUES ======
REQUEST_COUNT = Counter('groq_requests_total', 'Total number of calls to Groq API')
REQUEST_LATENCY = Histogram('groq_request_latency_seconds', 'Latency of Groq API requests in seconds')

# ====== [2] DÉMARRER LE SERVEUR PROMETHEUS ======
port = int(os.getenv("METRICS_PORT", 8010))  # par défaut 8010 si non défini
start_http_server(port)
print(f"🚀 Prometheus metrics available at http://localhost:{port}/metrics")

# ====== [3] TON CODE EXISTANT ======
groq_api_key = os.environ.get("GROQ_API_KEY")

if not groq_api_key:
    raise Exception("Groq API key is missing!")

groq_client = Groq(api_key=groq_api_key)

def generate_module_description(ilos, groq_api_key):
    """Génère une description professionnelle du module à partir des ILOs (Intended Learning Outcomes)."""

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

    # ====== [4] MESURER LE TEMPS ET COMPTER LES REQUÊTES ======
    start_time = time.time()
    try:
        response = requests.post(url, headers=headers, json=payload)
        latency = time.time() - start_time
        REQUEST_LATENCY.observe(latency)
        REQUEST_COUNT.inc()

        if response.status_code == 200:
            result = response.json()
            description = result['choices'][0]['message']['content']
            return description.strip()
        else:
            raise Exception(f"Échec de la requête API Groq : {response.status_code} - {response.text}")

    except Exception as e:
        REQUEST_COUNT.inc()
        raise e


# === Exemple d'utilisation ===
ilos = [
    "Expliquer comment l'apprentissage par renforcement diffère des autres paradigmes d'apprentissage automatique.",
    "Décrire les concepts fondamentaux de l'apprentissage par renforcement.",
    "Formuler des problèmes de prise de décision comme des processus de décision markoviens.",
    "Implémenter des algorithmes d'apprentissage par renforcement, y compris la programmation dynamique, les méthodes de Monte Carlo, l'apprentissage par différence temporelle, Q-learning et les réseaux de neurones Q profonds (DQN)."
]

description = generate_module_description(ilos, groq_api_key)

print("\n📚 Description du module générée :\n")
print(description)

# Si on n'est pas dans Jenkins, garder le monitoring actif
if os.environ.get("RUN_MODE", "prod") == "prod":
    print("\n🕒 Monitoring actif. Appuyez sur Ctrl+C pour arrêter.")
    while True:
        time.sleep(10)
