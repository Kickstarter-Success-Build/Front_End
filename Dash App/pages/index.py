# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """

            ## <Your Value Proposition>

            """
        ),
        dcc.Link(dbc.Button('Get Prediction', color='primary'), href='/predictions')
    ],
    md=4,
)

column2 = dbc.Col(
    [
    
    ]
)

layout = dbc.Row([column1, column2])