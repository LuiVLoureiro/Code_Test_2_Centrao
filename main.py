import pandas as pd
import numpy as np
import requests
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class API_SPORTS:
    def __init__(self) -> None:
        pass

    def brasileirao(chave, serie):
        global Database
        series = ['A', 'B', 'C', 'D']

        for i in series:
            if serie == series[0]:
                serie = 71
                break
            elif serie == series[1]:
                serie = 72
                break
            elif serie == series[2]:
                serie = 75
                break
            elif serie == series[3]:
                serie = 76
                break
            elif serie != i:
                print('Essa serie não existe no Brasileirão, tente novamente...')
                exit()
        
        # Url do Site que vai ser consumida a api
        url_brasileirao_A = f"https://v3.football.api-sports.io/fixtures/?season=2024&league={serie}"
        payload={}

        # Adicionar Headers para suprir os parâmetros estabelecidos pelo site
        headers = {
        'x-rapidapi-key': f'{chave}', # Adicionar sua chave de acesso para a API aqui...
        'x-rapidapi-host': 'v3.football.api-sports.io'
        }

        # Utilizar método request, passando como protocolo o GET para o url especifico, com os headers necessários
        response = requests.request("GET", url_brasileirao_A, headers=headers, data=payload)

        # Transformar resposta em JSON para manipulação dos arquivos
        data = response.json()
        data = data['response']

        # Separando informações no JSON para cada estrutura
        partidas = np.array([partida['fixture'] for partida in data])
        data_partidas = np.array([data['date'] for data in partidas])
        estadios = np.array([estadio['venue']['name'] for estadio in partidas])
        cidades = np.array([cidade['venue']['city'] for cidade in partidas])
        times_casa = np.array([time['teams']['home']['name'] for time in data])
        times_fora = np.array([time['teams']['away']['name'] for time in data])

        # Manipular Datas para formato visualmente agradável
        data_partidas = pd.to_datetime(data_partidas)
        data_partidas = data_partidas.strftime('%d/%m/%Y')

        # Organizando informações no Pandas, para a criação de uma Database
        Database = pd.DataFrame({
            'Time Casa': times_casa,
            'Time Fora': times_fora,
            'Data': data_partidas,
            'Estadio': estadios,
            'Cidade': cidades
        })

        # Exportando para CSV
        Database.to_csv('brasileirao_serie_{}.csv'.format(serie), index=False)

API_SPORTS.brasileirao('9c1beec7649cd19e43589903cb082bc0', 'A')
API_SPORTS.brasileirao('9c1beec7649cd19e43589903cb082bc0', 'B')
API_SPORTS.brasileirao('9c1beec7649cd19e43589903cb082bc0', 'C')
API_SPORTS.brasileirao('9c1beec7649cd19e43589903cb082bc0', 'D')