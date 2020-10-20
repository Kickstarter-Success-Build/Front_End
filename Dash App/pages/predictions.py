# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from joblib import load
import pandas as pd

# Imports from this application
from app import app

model = load('assets/regression.joblib')

@app.callback(
    Output('prediction-content', 'children'),
            [
                Input('blurb', 'value'),
                Input('state', 'value'),
                Input('binary_state', 'value'),
            ]
)

def predict(blurb, state, binary_state):
    df = pd.DataFrame(
        columns=['blurb', 'state', 'binary_state'],
        data=[[blurb, state, binary_state]]
    )

    y_pred = model.predict(df)[0]
    return f'Prediction ---> {y_pred}'

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        # """image"""
        # html.Img(src='assets/car crash.jpg', className='img-fluid'),

        dcc.Markdown(
            """

            ## **Make Predictions**

            """
        ),

        dcc.Markdown(
            """

            Below is the prediction:

            """
        )
        # ,
        # html.H2('Predicted Kickstarter Success', className='mb-5'),
        # html.Div(id='prediction-content', className='lead')
    ],
    md=4,
)

column2 = dbc.Col(
    [
        dcc.Markdown('#### **Enter blurb below**'),
        html.Div([
            dcc.Textarea(
            id='blurb',
            placeholder='Enter a description...',
            value='Ex: Sneak in, find treasures, avoid cats and collect the loot before time runs out!',
            style={'width': '75%', 'height': 125},
            className='mb-5',
        )
        html.Button('Submit', id='blurb-button', n_clicks=0),
        html.Div(id='prediction-content', className='lead')
        ])
    ]
)

@app.callback(
    Output('prediction-content', 'children'),
    [Input('blurb-button', 'n_clicks')],
    [State('blurb', 'value')]
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        return 'You have entered: \n{}'.format(value)

layout = dbc.Row([column1, column2])