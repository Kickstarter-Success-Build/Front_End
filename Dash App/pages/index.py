from app import app
from dash.dependencies import Input, Output
from .predictions import button_style  # To use the same button style

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
            ## Can we predict if a Kickstarter will succeed or fail?

            This app could help a user predict if a Kickstarter might succeed
            or fail by entering the short description they state on their page.
            You can input any blurbs you want but it is best to use theirs
            to gauge a decision.

            **For example:**
            - 1. One Kickstarter's main statement was "A team-based
            first-person shooter!". Before using the app to predict
            this sentence. You can assume it will fail since there's a
            bunch of team-based first person shooter games out there!
            - 2. Another Kickstarter main statement said, "Easily remove
            twist-off bottle caps!". This one was successful because it is
            simple yet creative. Some people struggle to open bottles but
            it is not their fault, it is the stubborn bottle. And, this product
            helps to alleviate the effort to open one.

            """
        )
    ],
    md=4
)

column2 = dbc.Col(
    [
        html.Img(src='assets/Inkedfailure-to-success_LI.jpg',
                 className='img-fluid'),
        dcc.Markdown(
            """
            **Application usage**
            - 1. You want to predict if a Kickstarter you're planning to invest
            in might fail or succeed.
            - 2. You want to test your Kickstarter statement and find out
            if you get a successful output.

            Click the button below to find out results!
            """,
            className='mt-3'
        ),
        dcc.Link(dbc.Button('Get Prediction', color='primary',
                            style=button_style), href='/predictions')
    ],
    md=8
)

layout = dbc.Row([column1, column2])
