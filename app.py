from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging

# Configurar log
logging.basicConfig(level=logging.INFO)

# Carregar variáveis de ambiente
load_dotenv()

# Obter a chave da API do ambiente
API_KEY = os.getenv('API_KEY')
NOTICIAS_API_URL = 'https://api.bigdatacloud.net/news'

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Projeto de Notícias com Flask!"

@app.route('/noticias', methods=['GET'])
def get_noticias():
    # Obter o código do país do parâmetro da URL, padrão para notícias globais
    country_code = request.args.get('countryCode', '')

    # Configurar parâmetros para a solicitação de notícias
    params = {'apiKey': API_KEY}
    if country_code == 'BR':
        params['countryCode'] = 'BR'  # Adicionar filtro para notícias do Brasil

    # Fazer a solicitação para a API de notícias
    response = requests.get(NOTICIAS_API_URL, params=params)

    logging.info(f"Status da resposta: {response.status_code}")
    logging.info(f"Conteúdo da resposta: {response.text}")

    if response.status_code == 200:
        try:
            data = response.json()  # Tentar converter para JSON
            return jsonify(data)
        except requests.exceptions.JSONDecodeError:
            return jsonify({'error': 'Resposta da API não era JSON'}), 500
    else:
        return jsonify({'error': 'Erro ao buscar notícias'}), response.status_code


if __name__ == '__main__':
    app.run(debug=True)
