import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from app import app, server
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path='/config/asap.env')
load_dotenv(dotenv_path='/config/aem.env')
from apps import asap_layout,aem_layout
app.layout = html.Div([
    #Including local stylesheet
    html.Link(href='/static/table_style.css', rel='stylesheet'),
    html.H1(children='Release Deployment History',id ='release-deployment-history', style={'textAlign': 'center','color': '#008080','display': 'inline-block',}),
    html.Img(
        src='/img/liberty-global-logo.jpg',
        style={
            'height' : '10%',
            'width' : '10%',
            'float' : 'right',
            'display': 'inline-block',
            'float': 'right'
           },
       ),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div([
        dcc.Tabs(
            id="tabs",
            #parent_className='custom-tabs',
            #className='custom-tabs-container',
            #20B2AA
            style={"height":"20",'textAlign': 'center','color': '#008080','cursor': 'pointer','align-items': 'center','justify-content': 'center','fontSize': 20},
            #style=tabs_styles,
            children=[
                dcc.Tab(label="ASAP", value="asap_tab",selected_style={'color': '#CD5C5C','backgroundColor': '#66CDAA',"border": "#A52A2A"}),
                dcc.Tab(label="Clarify", value="clarify_tab",selected_style={'color': '#CD5C5C','backgroundColor': '#66CDAA',"border": "#A52A2A"}),
                dcc.Tab(label="AEM", value="aem_tab",selected_style={'color': '#CD5C5C','backgroundColor': '#66CDAA',"border": "#A52A2A"}),
                ],
            value="asap_tab",
            colors={
                "border": "#FFFFFF",
                "primary": "#F5F5DC",
                "background": "#F5F5DC"
                }
            #vertical="vertical",
            )]
            ),
    html.Br(),
    html.Div(id="tab_content")
    ])

@app.callback(Output("tab_content", "children"), [Input("tabs", "value")])
def render_content(tab):
    if tab == "asap_tab":
        return asap_layout.layout
    elif tab == "aem_tab":
        return aem_layout.layout
    else:
        return


if __name__ == '__main__':
    server.run(debug=True)
