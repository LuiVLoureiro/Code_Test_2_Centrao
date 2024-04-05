## Dashboard Interativo para Visualização de Partidas de Futebol em Python

### Exemplo do Dashboard Criado
<img  align='center' src='https://github.com/LuiVLoureiro/Code_Test_2_Centrao/blob/main/fotos/dashboard.png'>

## Como Testar:

Necessário Python estar instalado...
Necessário Chave de Acesso do site https://api-sports.io/

1. faça um ```git clone https://github.com/LuiVLoureiro/Code_Test_2_Centrao``` // **ou** // faça o download do repositório
2. faça no seu terminal um ```pip install -r requirements.txt```
3. Abra o arquivo ```python dashboard.py``` e insira sua chave de acesso
4. por fim, no seu terminal, faça ```python dashboard.py```
5. OBS: Note que criará 4 arquivos .csv, eles serão utilizados como arquivos para gerar o Dashboard

## Importação de Dados em formato JSON
Site de origem para a disponibilização dos dados: https://api-sports.io/
```python

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

```
## Filtro de Apenas Dados Relevantes do JSON
Note que foi utilizado o numpy para a criação de arrays por motivos de melhora na performace do código
```python
# Separando informações no JSON para cada estrutura
partidas = np.array([partida['fixture'] for partida in data])
data_partidas = np.array([data['date'] for data in partidas])
estadios = np.array([estadio['venue']['name'] for estadio in partidas])
cidades = np.array([cidade['venue']['city'] for cidade in partidas])
times_casa = np.array([time['teams']['home']['name'] for time in data])
times_fora = np.array([time['teams']['away']['name'] for time in data])
```
## Criação do Dataframe com o Pandas
Utilizando o Pandas para estruturar os dados e informações coletadas
```python
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
```

## Exportar para CSV
Utilização da função do pandas para transformar o Dataframe em .csv
```python
Database.to_csv('brasileirao_serie_{}.csv'.format(serie), index=False)
```
Lembrando que esse código está dentro do main.py, no qual apenas servirá para consumir a API e criar os arquivos *csv*

## Adicionar Chave de Acesso e Carregar Dataframes
 ```python
chave = 'SUA_CHAVE_AQUI'

series = ['A', 'B', 'C', 'D']

for serie in series:
    API_SPORTS.brasileirao(chave, serie)
 ```

 ```python
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
 ```

## Inicializar Dashboard, Criar as Tabelas, Dropdown e Toda a Interface
 ```python
# Inicializa o app
app = Dash(__name__)

# Layout do app
app.layout = html.Div([
    html.Div(children='Dashboard Para API de Campeonatos de Futebol',
            style={'textAlign': 'center', 'padding': '20px','fontSize': '22px', 'fontFamily': 'Arial, sans-serif', 'margin': '20px','color': '#000000'}),
    dcc.Dropdown(
        id='dropdown-series',
        options=[
            {'label': 'Brasileirão Serie A', 'value': 'SerieA'},
            {'label': 'Brasileirão Serie B', 'value': 'SerieB'},
            {'label': 'Brasileirão Serie C', 'value': 'SerieC'},
            {'label': 'Brasileirão Serie D', 'value': 'SerieD'}
        ],
        value='SerieA'  # Valor padrão
    ),
    dash_table.DataTable(
        id='table',
        page_size=10,
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold',
            'color': 'black',
            'textAlign': 'center',
        },
        style_cell={
            'textAlign': 'left',
            'padding': '10px',
            'fontSize': 16,
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_as_list_view=True,  # Estilo mais limpo, sem bordas externas
    )
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
 ```
