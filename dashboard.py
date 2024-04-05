from dash import Dash, dcc, html, Input, Output, dash_table
import pandas as pd
from main import API_SPORTS

chave = '5fd35bd58b97229b27118bd641213ece'

series = ['A', 'B', 'C', 'D']

for serie in series:
    API_SPORTS.brasileirao(chave, serie)
    
# Carrega os DataFrames
SerieA = pd.read_csv('brasileirao_serie_71.csv')
SerieB = pd.read_csv('brasileirao_serie_72.csv')
SerieC = pd.read_csv('brasileirao_serie_75.csv')
SerieD = pd.read_csv('brasileirao_serie_76.csv')

# Dicionário para facilitar o acesso aos DataFrames com base na seleção do usuário
dfs = {
    'SerieA': SerieA,
    'SerieB': SerieB,
    'SerieC': SerieC,
    'SerieD': SerieD
}

# Inicializa o app
app = Dash(__name__)

# Layout do app
app.layout = html.Div([
    html.Div(children='Dashboard Para API de Campeonatos de Futebol'),
    dcc.Dropdown(
        id='dropdown-series',
        options=[
            {'label': 'Serie A', 'value': 'SerieA'},
            {'label': 'Serie B', 'value': 'SerieB'},
            {'label': 'Serie C', 'value': 'SerieC'},
            {'label': 'Serie D', 'value': 'SerieD'}
        ],
        value='SerieA'  # Valor padrão
    ),
    dash_table.DataTable(id='table', page_size=10)
])

# Callback para atualizar a tabela com base na seleção do dropdown
@app.callback(
    Output('table', 'data'),
    Input('dropdown-series', 'value')
)
def update_table(selected_year):
    df = dfs[selected_year]
    return df.to_dict('records')

# Roda o app
if __name__ == '__main__':
    app.run_server(debug=True)
