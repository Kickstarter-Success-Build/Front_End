# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
from joblib import load

# Imports from this application
from app import app

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
        # html.H2('Predicted Kickstarter Success:', className='mb-5'),
        # html.Div(id='prediction-content', className='lead')
    ],
    md=4
)

column2 = dbc.Col(
    [
        dcc.Markdown('#### **Enter blurb below**'),
            dcc.Textarea(
            id='blurb-input',
            placeholder='Enter a description...',
            value='Example Blurb: Sneak in, find treasures, avoid cats and collect the loot before time runs out!',
            style={'width': '75%', 'height': 125},
            maxLength=100
        ),
        html.Button('Submit', id='blurb-button', n_clicks=1),
        html.H2('Predicted Kickstarter Success:', className='mb-5'),
        html.Div(id='prediction-content', className='lead')
    ],
    md=5
)

layout = dbc.Row([column1, column2])

model = load('assets/regression.joblib')

@app.callback(
    Output('prediction-content', 'children'),
            [
                # Input('blurb', 'value'),
                Input('blurb-button', 'n_clicks')
            ],
            [State('blurb-input', 'value')]
)

# def predict(blurb):
#     df = pd.DataFrame(
#         columns=['blurb'],
#         data=[[blurb]]
#     )

#     y_pred = model.predict(df)[0]
#     return f'Prediction ---> {y_pred}'

def predict(clicked, text):
    if clicked:
        text = [text]
        y_pred = model.predict(text)
        # return f'{y_pred}'
        if y_pred > .50:
            y_pred = 'Successful'
            return f'{y_pred}'
        elif y_pred < .50:
            y_pred = 'Failed'
            return f'{y_pred}'
        else:
            return f'Try new blurb'