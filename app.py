from dash import dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from opcua import Client
import dash_daq as daq


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
                
server = app.server


url = "opc.tcp://192.168.0.30:4840"
client = Client(url)
client.connect()

# LAYOUT COMPONENTS ---------------------------------------------------------------------------------------------------------------

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI])


card = dbc.Card(
    [dbc.CardHeader("Header"), dbc.CardBody("Body")], className="h-100"
)


#  RESULT STORAGE CARD---------------------------------------------------------------------------------------------------------------


gauge_card = dbc.Card([
    dbc.CardHeader("Result Storage"), 
    dbc.CardBody([
        dbc.Row([ 
            dbc.Col([ 
                    daq.Gauge(id = 'result-storage', label = 'Result Storage', size = 180, max = 5000, min = 0),
            ])
        ]),

        dbc.Row([ 
            dbc.Col([ 
                html.Div(id = 'result-storage-text', className = 'text-center')
            ])
        ]),
        dcc.Interval(id = 'gauge-interval', interval = 1*1000, n_intervals = 0)
    ])
], className="h-100")


#  BATTERY CARD ---------------------------------------------------------------------------------------------------------------


battery_card = dbc.Card([
    dbc.CardHeader("Battery Level"), 
    dbc.CardBody([ 
        daq.LEDDisplay(id = 'our-LED-display', label = 'Battery %'),
        daq.GraduatedBar(id= 'our-graduated-bar', label = 'Battery Lvl', min = 0, max = 100),
        dcc.Interval(id = 'battery-interval', interval = 1*1000, n_intervals = 0)
    ])
], className="h-100")


#  TEMP CARD ---------------------------------------------------------------------------------------------------------------


temp_card = dbc.Card([
    dbc.CardHeader("Temperature Value"), 
    dbc.CardBody([
        dbc.Row([ 
            dbc.Col([ 
                    daq.Thermometer(id = 'our-thermometer', label = 'Station 3 Temperature', labelPosition = 'top', height = 150, min = 0, max = 60),
            ])
        ]),

        dbc.Row([ 
            dbc.Col([ 
                html.Div(id = 'temperature-text', className = 'text-left')
            ])
        ]),
        dcc.Interval(id = 'temperature-interval', interval = 1*1000, n_intervals = 0)
    ])
], className="h-100")


#  START/STOP BUTTON LAYOUT ---------------------------------------------------------------------------------------------------------------


# global temp
# key=client.get_node('ns=2;s=Application.GVL_HMI.bInvStop_HMI_i  ')
# key.get_access_level()
# state=key.get_value()
# temp=state

# button_card = dbc.Card([
#     dbc.CardHeader("Start/Stop Entry Station"), 
#     dbc.CardBody([ 
#         daq.PowerButton(id='our-power-button', on=temp),
#         html.Div(id='power-button-result')
#     ])
# ], className="h-100")


#  ALERT NOTIFICATION ---------------------------------------------------------------------------------------------------------------


RS_alert = dbc.Alert("Battery running low, please charge!", color = 'danger', dismissable=True)


#  APP LAYOUT---------------------------------------------------------------------------------------------------------------


app.layout = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Row([dbc.Col(battery_card), dbc.Col(gauge_card)], style={"height": "280px"}),
                    dbc.Row([dbc.Col(temp_card), dbc.Col(card)], style={"height": "280px"}, className = 'mt-5'),
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


# CALLBACKS ---------------------------------------------------------------------------------------------------------------


# BATTERY LEVEL CALLBACKS ---------------------------------------------------------------------------------------------------------------


@app.callback(
        Output('our-LED-display', 'value'),
        Input('battery-interval', 'n_intervals')
)
def update_displays(n):
    batterylvl = client.get_node('ns=2;s=Application.GVL_NexoInterface.nxAutoAkku ')   
    blvl=batterylvl.get_value() 
    value=blvl
    return str(value)


@app.callback(
    Output('our-graduated-bar', 'value'),
    Input('battery-interval', 'n_intervals')
    )

def update_displays(n):
    batterylvl = client.get_node('ns=2;s=Application.GVL_NexoInterface.nxAutoAkku ')   
    blvl=batterylvl.get_value() 
    value=blvl
    return value


#  RESULT STORAGE CALLBACKS ---------------------------------------------------------------------------------------------------

@app.callback(
    Output('result-storage', 'value'), 
    Input('gauge-interval', 'n_intervals')
    )
def update_output(n):
    rltstorage = client.get_node('ns=2;s=Application.GVL_NexoInterface.nxAutoRsltCnt ')   
    rstrg=rltstorage.get_value() 
    global value
    value=rstrg
    print(value)
    return value
    # if value > 1800:
    #     return RS_alert, value
    # else: 
    #     print(value)
    #     return value


@app.callback(
    Output('result-storage-text', 'children'),
    Input('gauge-interval', 'n_intervals')
)
def update_RS(timer):
    rltstorage = client.get_node('ns=2;s=Application.GVL_NexoInterface.nxAutoRsltCnt ')   
    rstrg=rltstorage.get_value() 
    global value
    value=rstrg
    print(value)
    return [html.Span('Value: {0}'.format(value))]


#  TEMPERATURE CALLBACKS ---------------------------------------------------------------------------------------------


@app.callback(
        Output('our-thermometer', 'value'),
        Input('temperature-interval', 'n_intervals')
)
def update_displays(n):
    batterylvl = client.get_node('ns=18;s=System.Temperature ')   
    blvl=batterylvl.get_value() 
    value=blvl
    print(value)
    return (value)


@app.callback(
    Output('temperature-text', 'children'),
    Input('temperature-interval', 'n_intervals')
)
def update_temp(timer):
    batterylvl = client.get_node('ns=18;s=System.Temperature ')   
    blvl=batterylvl.get_value() 
    value=blvl
    print(value)
    return [html.Span('Temp (℃): {0}'.format(value))]


#  BUTTON CALLBACKS ---------------------------------------------------------------------------------------------


# @app.callback(
#     Output('power-button-result', 'children'),
#     Input('our-power-button', 'on')
# )
# def update_output(on):
#     if temp==on:
#         key.set_value(True,varianttype=None)
#         state=key.get_value()
#         print(state)
#     else:
#         key.set_value(False,varianttype=None)
#         state=key.get_value()
#         print(state)
#     return f'The button is {on}.'


if __name__ == '__main__':
    app.run_server(debug=False)


