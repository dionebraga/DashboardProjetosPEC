import pandas as pd
import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px

# Dados corrigidos dos projetos
df_projetos = pd.read_excel("lista_de_projetos_inscritos.xlsx")  # Substitua pelo caminho correto do arquivo

# Criar aplicação Dash
app = dash.Dash(__name__)

# Layout da aplicação
app.layout = html.Div([
    html.H1("📊 Dashboard Projetos Culturais - Ilhabela", style={'textAlign': 'center'}),

    html.Div([
        html.Div([html.H3("Total de Projetos"), html.P(f"{len(df_projetos)}")], style={'width': '24%', 'display': 'inline-block'}),
        html.Div([html.H3("Classificados"), html.P(f"{len(df_projetos[df_projetos['situacao'] == 'Classificado'])}")], style={'width': '24%', 'display': 'inline-block'}),
        html.Div([html.H3("Suplentes"), html.P(f"{len(df_projetos[df_projetos['situacao'] == 'Suplente'])}")], style={'width': '24%', 'display': 'inline-block'}),
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),

    dcc.Graph(id='grafico-situacao', figure=px.pie(df_projetos, names='situacao', title='Distribuição de Situações')),
    dcc.Graph(id='grafico-faixas', figure=px.bar(df_projetos.groupby('faixa')['proponente'].count().reset_index(),
                                                  x='faixa', y='proponente', title='Projetos por Faixa')),
    dcc.Graph(id='grafico-pontuacao', figure=px.histogram(df_projetos, x='pontuacao', title='Distribuição de Pontuações')),

    html.Div([
        html.H3("📋 Tabela de Projetos"),
        dash_table.DataTable(
            id='tabela-projetos',
            columns=[{"name": col, "id": col} for col in df_projetos.columns],
            data=df_projetos.to_dict('records'),
            page_size=10,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_selectable="multi",
            selected_rows=[],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '10px'}
        )
    ], style={'marginTop': '20px'}),
])

# Executar a aplicação Dash
if __name__ == '__main__':
    app.run_server(debug=True)
