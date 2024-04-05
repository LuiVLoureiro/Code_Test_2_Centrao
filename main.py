import pandas as pd
import numpy as np
import requests
import json

class API_SPORTS:
    def __init__(self) -> None:
        pass

    def brasileirao_serie_a(chave):

        # Url do Site que vai ser consumida a api
        url_brasileirao_A = "https://v3.football.api-sports.io/fixtures/?season=2024&league=71"
        payload={}

        # Adicionar Headers para suprir os parâmetros estabelecidos pelo site
        headers = {
        'x-rapidapi-key': f'{chave}', # Adicionar sua chave de acesso para a API aqui...
        'x-rapidapi-host': 'v3.football.api-sports.io'
        }

        # Utilizar método request, passando como protocolo o GET para o url especifico, com os headers necessários
        response = requests.request("GET", url_brasileirao_A, headers=headers, data=payload)

        #Transformar resposta em JSON para manipulação dos arquivos
        data = response.json()
        data = data['response']
