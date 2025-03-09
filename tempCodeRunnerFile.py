import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table, Input, Output
import plotly.express as px

# Carregar o arquivo corrigido
file_path = 'projetos_culturais_ilhabela_corrigido.csv'
df = pd.read_csv(file_path)

# Garantir que até Francisco Firmino (faixa 3) seja classificado
indice_francisco = df[(df['proponente'] == 'FRANCISCO FIRMINIO DOS SANTOS FILHO')].index[0]
df.loc[(df.index <= indice_francisco) & (df['faixa'] == 3), 'status'] = 'Classificado'

# Filtrar apenas os projetos classificados
df_classificados = df[df['status'] == 'Classificado']

# Calcular o valor total dos projetos classificados, garantindo o limite de R$ 1.000.000,00
valor_total_classificados = df_classificados['valor_projeto'].sum()
valor_total_classificados = min(valor_total_classificados, 1000000)

# Criar aplicação Dash com Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Layout da aplicação
app.layout = dbc.Container([
    html.H1('Dashboard de Projetos Culturais - Ilhabela 2024', className='text-center mt-4 mb-4'),
    
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total de Projetos", className="card-title"),
                html.H3(f"{len(df)}", className="card-text")
            ])
        ], color="primary", inverse=True), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Projetos Classificados", className="card-title"),
                html.H3(f"{len(df_classificados)}", className="card-text")
            ])
        ], color="success", inverse=True), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Projetos Suplentes", className="card-title"),
                html.H3(f"{len(df[df['status'] == 'Suplente'])}", className="card-text")
            ])
        ], color="warning", inverse=True), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Valor Total Investido", className="card-title"),
                html.H3(f"R$ {valor_total_classificados:,.2f}", className="card-text")
            ])
        ], color="info", inverse=True), width=3)
    ], className='mb-4'),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='status-chart',
                figure=px.pie(
                    names=df['status'].unique(),
                    values=df['status'].value_counts(),
                    title='Distribuição dos Projetos por Status',
                    color_discrete_sequence=px.colors.sequential.RdBu
                )
            )
        ], width=6),
        
        dbc.Col([
            dcc.Graph(
                id='faixa-chart',
                figure=px.histogram(
                    df, x='faixa', title='Projetos por Faixa',
                    color='status', barmode='group',
                    color_discrete_sequence=px.colors.qualitative.Plotly
                )
            )
        ], width=6)
    ]),
    
    html.H3("Filtrar Projetos", className='mt-4'),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='status-filter',
                options=[{'label': status, 'value': status} for status in df['status'].unique()],
                placeholder="Selecione um Status",
                multi=True,
                className='mb-4'
            )
        ], width=4),
        
        dbc.Col([
            dcc.Dropdown(
                id='faixa-filter',
                options=[{'label': f'Faixa {i}', 'value': i} for i in sorted(df['faixa'].unique())],
                placeholder="Selecione uma Faixa",
                multi=True,
                className='mb-4'
            )
        ], width=4)
    ]),
    
    dash_table.DataTable(
        id='tabela-projetos',
        columns=[
            {'name': 'Proponente', 'id': 'proponente'},
            {'name': 'Faixa', 'id': 'faixa'},
            {'name': 'Pontuação', 'id': 'pontuacao'},
            {'name': 'Valor do Projeto', 'id': 'valor_projeto', 'type': 'numeric', 'format': {'specifier': ',.2f'}},
            {'name': 'Status', 'id': 'status'}
        ],
        data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '10px', 'fontFamily': 'Arial'},
        style_header={'backgroundColor': 'rgb(240, 240, 240)', 'fontWeight': 'bold'}
    )
])

# Callbacks para atualizar a tabela com base nos filtros
@app.callback(
    Output('tabela-projetos', 'data'),
    [Input('status-filter', 'value'), Input('faixa-filter', 'value')]
)
def atualizar_tabela(status_selecionado, faixa_selecionada):
    df_filtrado = df.copy()
    
    if status_selecionado:
        df_filtrado = df_filtrado[df_filtrado['status'].isin(status_selecionado)]
    
    if faixa_selecionada:
        df_filtrado = df_filtrado[df_filtrado['faixa'].isin(faixa_selecionada)]
    
    return df_filtrado.to_dict('records')

# Executar a aplicação
if __name__ == '__main__':
    app.run_server(debug=True)
