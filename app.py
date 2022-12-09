from dash import dash, dcc, html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
                
server = app.server

app.layout = html.Div([ 
    html.H1("App homepage")
])

if __name__ == "__main__":
    app.run_server(debug=False)