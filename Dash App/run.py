from app import app, server
from pages import index, predictions, insights, process
from dash.dependencies import Input, Output

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

# Navbar docs:
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/navbar
navbar = dbc.NavbarSimple(
    brand='Kickstarter Success Prediction',
    brand_href='/',
    children=[
        dbc.NavItem(dcc.Link(href='/predictions', className='nav-link'))
    ],
    sticky='fixed',
    color='secondary'
    # className='mx-auto',
    # style={'width': '200px'},
    # fluid='True'
    # light=True,
    # dark=False
)

# Footer docs:
# dbc.Container, dbc.Row, dbc.Col:
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
# html.P: https://dash.plot.ly/dash-html-components
# fa (font awesome) : https://fontawesome.com/icons/github-square?style=brands
# mr (margin right) : https://getbootstrap.com/docs/4.3/utilities/spacing/
# className='lead' : https://getbootstrap.com/docs/4.3/content/typography/#lead
footer = dbc.Container(
    dbc.Row(
        dbc.Col(
            html.P(
                [
                    html.Span('Organization', className='mr-2'),
                    html.A(html.I(className='fab fa-github mr-1'), href='https://github.com/Kickstarter-Success-Build/front-end'),
                    # html.Span('Ahmed Hadri -', className='mr-2'),
                    html.Span('|', className='mr-1'),
                    html.Span('Lester Gomez', className='mr-2'),
                    html.A(html.I(className='fab fa-github mr-1'), href='https://github.com/machine-17'),
                    html.A(html.I(className='fab fa-linkedin-in mr-1'), href='https://www.linkedin.com/in/lg17/'),
                    html.A(html.I(className='fab fa-twitter mr-1'), href='https://twitter.com/_machine17'),
                    html.Span('|', className='mr-1'),
                    html.Span('Steven Lee', className='mr-2'),
                    html.A(html.I(className='fab fa-github mr-1'), href='https://github.com/StevenBryceLee'),
                    html.A(html.I(className='fab fa-linkedin-in mr-1'), href='https://www.linkedin.com/in/stevenbrlee/'),
                    html.A(html.I(className='fab fa-twitter mr-1'), href='https://twitter.com/Steven_B_Lee')
                ],
                className='lead'
            )
        )
    )
)

# Layout docs:
# html.Div: https://dash.plot.ly/getting-started
# dcc.Location: https://dash.plot.ly/dash-core-components/location
# dbc.Container:
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    dbc.Container(id='page-content', className='mt-4'),
    html.Hr(),
    footer
])


# URL Routing for Multi-Page Apps: https://dash.plot.ly/urls
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return index.layout
    elif pathname == '/predictions':
        return predictions.layout
    elif pathname == '/insights':
        return insights.layout
    elif pathname == '/process':
        return process.layout
    else:
        return dcc.Markdown('## Page not found')

# Run app server: https://dash.plot.ly/getting-started
if __name__ == '__main__':
    app.run_server(debug=True)
