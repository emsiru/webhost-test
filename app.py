from dash import dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from opcua import Client
import dash_daq as daq


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])

server = app.server

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row([
                dbc.Col([
                    html.Img(src=app.get_asset_url('logo2.png'), height="60px"),
                    dbc.NavbarBrand('Robotic-Assembly Line Dashboard', style={'color': 'black', 'fontSize': 20}, className = 'ms-4')
                ], width = {'size':'auto'})
            ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Nav([
                            dbc.NavItem(dbc.NavLink('Home', href = '/')),
                            # dbc.NavItem(dbc.NavLink('Drill Torque Gauge', href = '/apps/gauge')),
                            dbc.NavItem(dbc.NavLink('Live-Graph', href = '/graph')),
                            # dbc.NavItem(dbc.DropdownMenu(
                            #     children = [
                            #         dbc.DropdownMenuItem('More pages etc.', header = True),
                            #         dbc.DropdownMenuItem('Extra component', href = '/extras')
                            #     ],
                            #         nav = True,
                            #         in_navbar = True,
                            #         label = 'More'
                            #                             ))
                                ],
                                    navbar=True
                                )
                            ], width={'size':'auto'})
                        ], align='center')
            ],
        fluid = True
        )
)

graph = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id = 'torque-graph', figure = {}),
                            dcc.Interval(id = 'graph-update', n_intervals = 0, interval = 1000*1)
                        ])
                    ]),

                    dbc.Row([
                        dbc.Col([
                            html.Div('% Change: ', style = {'size':20})
                        ], width = 1, className = 'ms-5'),

                        dbc.Col([
                            html.P([
                                dcc.Graph(id = 'delta-indicator', figure = {}),
                                dcc.Interval(id = 'delta-update', n_intervals = 0, interval = 1000*1)
                            ], style = {'width':'12rem'})
                        ])
                    ]),
                ])
            ], style = {'width' : '145rem'}, className = 'm-5', color = 'secondary')
        ])
    ], justify='center')
], fluid = True)


card = dbc.Card(
    [dbc.CardHeader("Header"), dbc.CardBody("Body")], className="h-100"
)


layout = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Row([dbc.Col(card), dbc.Col(card)], style={"height": "280px"}),
                    dbc.Row([dbc.Col(card), dbc.Col(card)], style={"height": "280px"}, className = 'mt-5'),
                ],
                width=8,
            ),
            dbc.Col(card, width=2),
        ],
        justify="center",
    ),
    fluid=True,
    className="mt-3",
)



app.layout = html.Div([ 
    navbar,
    dcc.Location(id = 'url', refresh=False),
    html.Div(id = 'content', children = [])
])


@app.callback(
    Output('content', 'children'),
    Input('url', 'pathname')
)
def update_page(pathname):
    if pathname == '/graph':
        return graph
    else:
        return layout



if __name__ == '__main__':
    app.run_server(debug=False)


