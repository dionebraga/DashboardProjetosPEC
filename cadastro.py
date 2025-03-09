import dash
from dash import dcc, html, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
from datetime import datetime
import dash_bootstrap_components as dbc

# Inicializar o aplicativo Dash com tema Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Função para extrair dados do site (simulação)
def extrair_dados_do_site():
    """
    Esta é uma simulação de extração de dados.
    Em um caso real, você usaria requests e BeautifulSoup para extrair os dados do site.
    """
    try:
        # Em um cenário real:
        # response = requests.get("https://cadastrocultural.com.br/")
        # soup = BeautifulSoup(response.content, "html.parser")
        # Aqui viria a lógica de extração
        
        # Dados simulados para o dashboard
        return {
            "artistas": pd.DataFrame({
                "nome": ["Maria Silva", "João Pereira", "Ana Santos", "Carlos Oliveira", "Julia Lima", 
                         "Rafael Costa", "Fernanda Souza", "Bruno Alves", "Patrícia Rocha", "Lucas Vieira"],
                "categoria": ["Música", "Artes Visuais", "Teatro", "Dança", "Literatura", 
                             "Música", "Teatro", "Artes Visuais", "Dança", "Literatura"],
                "cidade": ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Salvador", "Recife", 
                          "Porto Alegre", "Curitiba", "Fortaleza", "Brasília", "Manaus"],
                "cadastro": [datetime(2023, 5, 12), datetime(2023, 8, 20), datetime(2024, 1, 15), 
                            datetime(2023, 11, 5), datetime(2024, 2, 8), datetime(2023, 7, 19), 
                            datetime(2024, 1, 30), datetime(2023, 9, 22), datetime(2023, 12, 10), 
                            datetime(2024, 2, 15)],
                "projetos": [3, 1, 5, 2, 4, 2, 3, 1, 6, 2]
            }),
            "projetos": pd.DataFrame({
                "titulo": ["Festival de Música", "Exposição Arte Moderna", "Peça Teatral", "Espetáculo de Dança",
                          "Lançamento de Livro", "Concerto Clássico", "Performance Teatral", "Galeria Virtual", 
                          "Dança Contemporânea", "Sarau Literário"],
                "categoria": ["Música", "Artes Visuais", "Teatro", "Dança", "Literatura", 
                             "Música", "Teatro", "Artes Visuais", "Dança", "Literatura"],
                "data_inicio": [datetime(2023, 6, 15), datetime(2023, 9, 10), datetime(2024, 2, 20), 
                               datetime(2023, 12, 5), datetime(2024, 3, 15), datetime(2023, 8, 25), 
                               datetime(2024, 2, 10), datetime(2023, 10, 18), datetime(2024, 1, 22), 
                               datetime(2024, 3, 5)],
                "data_fim": [datetime(2023, 6, 18), datetime(2023, 10, 10), datetime(2024, 3, 5), 
                            datetime(2023, 12, 7), datetime(2024, 3, 15), datetime(2023, 8, 27), 
                            datetime(2024, 2, 15), datetime(2023, 11, 20), datetime(2024, 1, 25), 
                            datetime(2024, 3, 5)],
                "status": ["Concluído", "Concluído", "Em andamento", "Concluído", "Agendado", 
                          "Concluído", "Em andamento", "Concluído", "Concluído", "Agendado"],
                "participantes": [15, 8, 12, 10, 5, 20, 7, 6, 14, 9],
                "visualizacoes": [1200, 850, 400, 600, 120, 750, 380, 920, 540, 150]
            }),
            "estatisticas": {
                "total_artistas": 258,
                "total_projetos": 142,
                "categorias": {
                    "Música": 74,
                    "Artes Visuais": 52,
                    "Teatro": 38,
                    "Dança": 31,
                    "Literatura": 29,
                    "Cinema": 24
                },
                "estados": {
                    "SP": 68,
                    "RJ": 42,
                    "MG": 35,
                    "BA": 20,
                    "RS": 18,
                    "PR": 15,
                    "CE": 12,
                    "DF": 10,
                    "Outros": 38
                },
                "cadastros_mensais": {
                    "Jan/2024": 18,
                    "Dez/2023": 22,
                    "Nov/2023": 15,
                    "Out/2023": 20,
                    "Set/2023": 12,
                    "Ago/2023": 25
                }
            }
        }
    except Exception as e:
        print(f"Erro ao extrair dados: {e}")
        return None

# Layout do Dashboard
def criar_layout(dados):
    if not dados:
        return html.Div([
            html.H3("Erro ao carregar dados", className="text-danger"),
            html.P("Verifique sua conexão e tente novamente.")
        ])
    
    artistas_df = dados["artistas"]
    projetos_df = dados["projetos"]
    stats = dados["estatisticas"]
    
    # Gráficos e visualizações
    fig_categorias = px.pie(
        names=list(stats["categorias"].keys()),
        values=list(stats["categorias"].values()),
        title="Distribuição por Categoria",
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    
    fig_estados = px.bar(
        x=list(stats["estados"].keys()),
        y=list(stats["estados"].values()),
        title="Artistas por Estado",
        labels={"x": "Estado", "y": "Quantidade"},
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    
    fig_projetos_tempo = px.line(
        x=list(stats["cadastros_mensais"].keys()),
        y=list(stats["cadastros_mensais"].values()),
        title="Novos Cadastros por Mês",
        labels={"x": "Mês", "y": "Quantidade"},
        markers=True
    )
    
    fig_projetos_status = px.pie(
        projetos_df,
        names="status",
        title="Status dos Projetos",
        color_discrete_sequence=px.colors.sequential.Turbo
    )
    
    # Cards para métricas chave
    cards = dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total de Artistas", className="card-title text-center"),
                    html.H2(f"{stats['total_artistas']}", className="text-center text-primary")
                ])
            ], className="mb-4 shadow")
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total de Projetos", className="card-title text-center"),
                    html.H2(f"{stats['total_projetos']}", className="text-center text-success")
                ])
            ], className="mb-4 shadow")
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H4("Categoria Principal", className="card-title text-center"),
                    html.H2("Música", className="text-center text-info")
                ])
            ], className="mb-4 shadow")
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H4("Projetos Ativos", className="card-title text-center"),
                    html.H2(f"{len(projetos_df[projetos_df['status'] == 'Em andamento'])}", className="text-center text-warning")
                ])
            ], className="mb-4 shadow")
        )
    ])
    
    # Layout do aplicativo
    return dbc.Container([
        html.H1("Dashboard Cadastro Cultural", className="text-center my-4"),
        html.Hr(),
        
        # Seção de métricas-chave
        html.H3("Visão Geral", className="mt-4"),
        cards,
        
        # Gráficos principais
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_categorias), md=6),
            dbc.Col(dcc.Graph(figure=fig_estados), md=6)
        ]),
        
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_projetos_tempo), md=6),
            dbc.Col(dcc.Graph(figure=fig_projetos_status), md=6)
        ]),
        
        # Seção de Artistas
        html.H3("Artistas Cadastrados", className="mt-4"),
        dbc.Card(
            dbc.CardBody(
                dash_table.DataTable(
                    id='artistas-table',
                    columns=[{"name": col.capitalize(), "id": col} for col in artistas_df.columns],
                    data=artistas_df.to_dict('records'),
                    style_header={
                        'backgroundColor': '#f8f9fa',
                        'fontWeight': 'bold'
                    },
                    style_cell={
                        'textAlign': 'left',
                        'padding': '10px'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#f8f9fa'
                        }
                    ],
                    page_size=5
                )
            ),
            className="shadow-sm"
        ),
        
        # Seção de Projetos
        html.H3("Projetos Culturais", className="mt-4"),
        dbc.Card(
            dbc.CardBody(
                dash_table.DataTable(
                    id='projetos-table',
                    columns=[{"name": col.replace("_", " ").capitalize(), "id": col} for col in projetos_df.columns],
                    data=projetos_df.to_dict('records'),
                    style_header={
                        'backgroundColor': '#f8f9fa',
                        'fontWeight': 'bold'
                    },
                    style_cell={
                        'textAlign': 'left',
                        'padding': '10px'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#f8f9fa'
                        },
                        {
                            'if': {
                                'filter_query': '{status} = "Em andamento"'
                            },
                            'backgroundColor': '#d7f3e3',
                        },
                        {
                            'if': {
                                'filter_query': '{status} = "Agendado"'
                            },
                            'backgroundColor': '#fff3cd',
                        }
                    ],
                    page_size=5
                )
            ),
            className="shadow-sm"
        ),
        
        html.Footer([
            html.Hr(),
            html.P("Dashboard Cadastro Cultural © 2025", className="text-center text-muted")
        ], className="mt-4")
    ], fluid=True)

# Carregar dados
dados = extrair_dados_do_site()

# Definir layout do app
app.layout = criar_layout(dados)

# Servidor principal
if __name__ == '__main__':
    app.run_server(debug=True)