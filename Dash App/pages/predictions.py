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
            style={'width': '100%', 'height': 150},
            maxLength=280
        ),
        html.Button('Submit', id='blurb_button', n_clicks=0, className='ml-0',
                    style=button_style),
        html.Div(id='advise-user'),
        html.H5('Predicted Kickstarter Success:', className='mt-1'),
        html.Div(id='prediction-content', className='display-4')
    ],
    md=4
)

# Main - user input dash component
column2 = dbc.Col(
    [
        dcc.Markdown(
            """
            ## **Prediction**
            We trained a model using logistic regression from scikit-learn. It
            gave us the best accuracy score from other models we used. Such as,
            neural networks and a lighter version. Logistic regression gives us
            a 67% accuracy whereas neural networks is 51% and that's a big jump
            from a simple and easy to use machine learning model. We needed a
            bigger dataset for our neural network model to work as intended.
            Additionally, we started off with a baseline accuracy of 55% before
            training the models.
            """
        ),
    ],
    md=4
)

column3 = dbc.Col(
    [
        dcc.Markdown(
            """
            ## **Summary**
            The dataset we worked on for this application comes from Kaggle and
            it is from 2017, and it contains about 200k projects. Also, it
            contains the 4000 most successful kickstarters. Anyway, the
            majority of the projects failed which is unfortunate. Kickstarter
            receives billions every year in pledges from thousands of backers
            to fund projects. This app predicts who were successful and those
            that failed by just entering their statement. To be successful,
            however, it means they got funded. Even more so past the asking
            funding amount.
            """
        )
    ],
    md=4
)


# Website layout
layout = dbc.Row([column2, column1, column3])

# Loading the model from keras_model.py
# model = create_end_to_end_model()
# Saving min and max prediction output to a variable
# MIN = 0.24284366
# MAX = 0.46393377

# Loading regression model from a joblib file
model = load('assets/regression_lite.joblib')


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
