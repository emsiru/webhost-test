from dash import dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from opcua import Client
import dash_daq as daq


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.layout = html.Div([ 
    dcc.Link(id = 'page-1', href = '/page-1'),
    dcc.Location(id = 'url', refresh=False),
    html.Div(id = 'content', children = [])
])

header = html.Div([ 
    html.H1('Hey')
])


@app.callback(
    Output('content', 'children'),
    Input('url', 'pathname')
)
def update_page(pathname):
    if pathname == '/page-1':
        return header
    else:
        return 'Error'

if __name__ == '__main__':
    app.run_server(debug=False)


