import pandas as pd
import dash
from dash import dcc, html, dash_table
import plotly.express as px

# Carregar o arquivo corrigido
file_path = 'projetos_culturais_ilhabela_corrigido.csv'
df = pd.read_csv(file_path)

# Garantir que até Francisco Firmino (faixa 3) seja classificado
indice_francisco = df[(df['proponente'] == 'FRANCISCO FIRMINIO DOS SANTOS FILHO')].index[0]

# Ajustar o status para 'Classificado' até esse índice na faixa 3
df.loc[(df.index <= indice_francisco) & (df['faixa'] == 3), 'status'] = 'Classificado'

# Filtrar apenas os projetos classificados
df_classificados = df[df['status'] == 'Classificado']

# Calcular o novo valor total dos projetos classificados, garantindo o limite de R$ 1.000.000,00
valor_total_classificados = df_classificados['valor_projeto'].sum()
valor_total_classificados = min(valor_total_classificados, 1000000)

# Criar aplicação Dash
app = dash.Dash(__name__)

# Layout da aplicação
app.layout = html.Div([
    html.H1('Dashboard de Projetos Culturais - Ilhabela 2024', style={'textAlign': 'center'}),
    
    html.Div([
        html.H3('Visão Geral'),
        html.P(f'Total de Projetos: {len(df)}'),
        html.P(f'Total de Projetos Classificados: {len(df_classificados)}'),
        html.P(f'Total de Projetos Suplentes: {len(df[df["status"] == "Suplente"])}'),
        html.P(f'Total de Projetos Eliminados: {len(df[df["status"] == "Eliminado"])}'),
        html.P(f'Valor Total de Projetos Classificados: R$ {valor_total_classificados:,.2f}')
    ], style={'width': '50%', 'margin': 'auto'}),
    
    dcc.Graph(
        figure=px.pie(
            df['status'].value_counts(),
            names=df['status'].value_counts().index,
            values=df['status'].value_counts().values,
            title='Status dos Projetos'
        )
    ),
    
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
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
    )
])

# Executar a aplicação
if __name__ == '__main__':
    app.run_server(debug=True)

# Salvar dados ajustados em CSV
df.to_csv('projetos_culturais_ilhabela_ajustado.csv', index=False)
print("Dados ajustados salvos em 'projetos_culturais_ilhabela_ajustado.csv'")
