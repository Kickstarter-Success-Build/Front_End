# Imports from other .py files
from app import app
from joblib import load
# from .keras_model import create_end_to_end_model

from dash.dependencies import Input, Output, State
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
# import numpy as np
import pandas as pd

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout

# Styling the submit button
button_style = {
  'background-color': '#226be8',
  'border': 'none',
  'color': 'white',
  'width': '100%',
  'padding': '12px 28px',
  'text-align': 'center',
  'text-decoration': 'none',
  'display': 'inline-block',
  'font-size': '14px',
  'margin': '4px 2px',
  'cursor': 'pointer',
  'border-radius': '12px',
  'box-shadow': '0 4px 8px 0 rgba(0,0,0,0.2), 0 3px 10px 0 rgba(0,0,0,0.19)'
}

column1 = dbc.Col(
    [
        dcc.Markdown('##### **Enter a short description below**'),
        dcc.Textarea(
            id='blurb_input',
            value='Example Kickstarter Blurb: Sneak in, find treasures, avoid cats and collect the loot before time runs out!',
            style={'width': '100%', 'height': 100},
            maxLength=180
        ),
        html.Button('Submit', id='blurb_button', n_clicks=0, className='ml-0',
                    style=button_style),
        html.Div(id='advise-user'),
        html.H5('Predicted Kickstarter Success', className='mt-1'),
        html.Div(id='prediction-content', className='lead')
    ],
    md=5
)

# Main - user input dash component
column2 = dbc.Col(
    [
        dcc.Markdown(
            """
            ## **Judgment**
            <text>
            """
        ),

        dcc.Markdown(
            """
            <placeholder>
            """
        )
    ],
    md=4
)

# Website layout
layout = dbc.Row([column1, column2])

# Loading the model from keras_model.py
# model = create_end_to_end_model()
# Saving min and max prediction output to a variable
# MIN = 0.24284366
# MAX = 0.46393377

# Loading regression model from a joblib file
model = load('assets/regression.joblib')


# This callback is only used for button execution
# and it advises the user
@app.callback(
    Output('advise-user', 'children'),
    [Input('blurb_button', 'n_clicks')],
    [State('blurb_input', 'value')]
)
# To let user know the button is working and
# the entry is submitted
def update_output(n_clicks, _):
    if n_clicks > 0:
        return f'Entry loaded! Button clicked {n_clicks} times.'


# Calling textarea and button for user inputs
@app.callback(
    Output('prediction-content', 'children'),
    [Input('blurb_button', 'n_clicks')],
    [State('blurb_input', 'value')]
)
# Function to predict kickstarter blurbs
def predict(clicked, value):
    if clicked:
        text = [value]
        y_pred = model.predict(text)
        # return f'{y_pred}' # For testing pred
        # Replacing output with success or fail
        if y_pred > .50:
            y_pred = 'Successful'
            return f'{y_pred}'
        elif y_pred < .50:
            y_pred = 'Failed'
            return f'{y_pred}'
        else:
            return f'Try new blurb'
