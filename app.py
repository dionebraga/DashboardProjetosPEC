from dash import Dash, html
app = Dash(__name__)
app.layout = html.H1("Dashboard AWS Free Tier")
server = app.server

if __name__ == "__main__":
    app.run_server(host='127.0.0.1', port=8080)
