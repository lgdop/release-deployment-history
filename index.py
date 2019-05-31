import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from app import app, server
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path='/config/asap.env')
load_dotenv(dotenv_path='/config/aem.env')
load_dotenv(dotenv_path='/config/clarify.env')
from apps import asap_layout,clarify_layout,aem_layout
app.layout = html.Div([
    #Including local stylesheet
    html.Link(href='/static/cdc_layout_style.css', rel='stylesheet'),
    html.Link(href='/static/table_style.css', rel='stylesheet'),
    html.Div([
        html.Img(
        src='/img/Accenture-logo-red.png',
        style={
            'height' : '100%',
            'width' : '12%',
            'display':'inline-block',
            'float':'left',
            'padding-right':'20px'
        }
       ),
        html.Div([
             html.H1(children='RELEASE DEPLOYMENT HISTORY',style={'textAlign': 'center','color': '#000000'})
           ],style={'padding-left':'200px','display':'inline-block','float':'left'}),
        html.Img(
        src='/img/logo-client-liberty-color.jpg',
        style={
            'height' : '80%',
            'width' : '11%',
            'display':'inline-block',
            'float':'right',
            'padding-right':'20px'
        }
       )],className='head-conatiner'),
    html.Div([
    dcc.Location(id='main_url', refresh=False),
    html.Div([
        dcc.Tabs(
            id="tabs",
            #parent_className='custom-tabs',
            #className='custom-tabs-container',
            #20B2AA
            style={"height":"20",'textAlign': 'center','fontWeight':'bold','color': '#000000','cursor': 'pointer','align-items': 'center','justify-content': 'center','fontSize': 20},
            #style=tabs_styles,
            children=[
                dcc.Tab(label="ASAP", value="asap_tab",selected_style={'color': '#FFFFFF','fontWeight':'bold','backgroundColor': '#7F8C8D',"border": "#A52A2A"}),
                dcc.Tab(label="CLARIFY", value="clarify_tab",selected_style={'color': '#FFFFFF','fontWeight':'bold','backgroundColor': '#7F8C8D',"border": "#A52A2A"}),
                dcc.Tab(label="AEM", value="aem_tab",selected_style={'color': '#FFFFFF','fontWeight':'bold','backgroundColor': '#7F8C8D',"border": "#A52A2A"}),
                ],
            value="asap_tab",
            colors={
                "border": "#FFFFFF",
                "primary": "#F5F5DC",
                "background": "#A6ACAF"
                }
            #vertical="vertical",
            )]
            ),
    html.Div(id="tab_content")
    ],className='main-container')])

@app.callback(Output("tab_content", "children"), [Input("tabs", "value")])
def render_content(tab):
    if tab == "asap_tab":
        return asap_layout.layout
    elif tab == "clarify_tab":
        return clarify_layout.layout
    elif tab == "aem_tab":
        return aem_layout.layout
    else:
        return

@app.callback(Output('main_url', 'pathname'),
              [Input("tabs", "value")])
def display_url(tab):
    if tab != "clarify_tab":
        return "/release-history/"

if __name__ == '__main__':
    server.run(debug=True)

