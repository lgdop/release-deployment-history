from app import app
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask, request, redirect
#from pandas_datareader import data as web
from datetime import datetime as dt
import re
import os
import pymongo

#table data style
td_style={'padding-top':'10px', 'padding-bottom':'10px','padding-left': '10px','padding-right': '10px','color':'#1A5276'}
#table heading style
th_style={'padding-top':'10px', 'padding-bottom':'10px','padding-left': '10px','padding-right': '10px','color':'#BA4A00'}

#Generating table data from json output obtained from mongoDB
def generate_table(deployed_data):
    print deployed_data
    simplified_dict={}
    for key,value in deployed_data.iteritems():
        if key != 'Cartridges':
            for key1 in value.keys():
                if type(value[key1])!= list and value[key1].isdigit():
                    simplified_dict[key]=value[key1]
        else:
            for key1,value1 in value.iteritems():
                for key2 in value1.keys():
                    if value1[key2].isdigit():
                        if key2 == 'service_model_build':
                            simplified_dict[key1]=value1[key2]
                        else:
                            simplified_dict[key2]=value1[key2]
    return html.Div([
        html.Table(className='reaponsive-table',
        # Header
        children=[
            html.Thead(
                html.Tr([
                    html.Th('Module', style=th_style),
                    html.Th('Buildnumber',style=th_style)])
                ),

        # Body
            html.Tbody(
                [html.Tr([
                    html.Td(key,style=td_style),
                    html.Td(value,style=td_style)
                    ]) for key,value in simplified_dict.iteritems()]
                )
    ],style={
            'margin-left': 'auto',
            'margin-right': 'auto',
            'padding-left': '50px',
            'padding-right': '50px',
            'textAlign': 'left',
            })
])

with open('asap_hosts') as fp:
    asap_host=fp.readlines()
asap_env_list=[]
for line in asap_host:
    try:
        env=re.search(r'^\[[A-Z]{2}[A-z][a-z0-9]',line).group(0)
        asap_env_list.append(re.search(r'[A-Z]{2}[A-z][a-z0-9]',env).group(0))
    except AttributeError:
        pass
#Desiging layout of page
layout = html.Div([
    #Including local stylesheet
    html.Link(href='/static/table_style.css', rel='stylesheet'),
    html.Br(),
    html.Br(),
    html.Div([
    #html.Br(style={'display': 'inline-block'}),
    html.Div([
        html.B(html.Div('Environment', className='app_name',style={'color':'#597E16','fontSize': 16})),
        html.Div(dcc.Dropdown(id='environments-dropdown',
                              options=[{'label': k, 'value': k} for k in asap_env_list]))
        ],style={'width': '60%'}
    )
    ],style={'width': '45%'}),
    html.Br(),
    html.Br(),
    html.Div(id='display-selected-values')
])

#Below callback takes the 2 dropdown inputs and generates a table by taking details from mongoDB and displays the result on the page
@app.callback(
    dash.dependencies.Output('display-selected-values', 'children'),
    [dash.dependencies.Input('environments-dropdown', 'value')])
def set_display_children(selected_environment):
#Connecting to LGDOP mongoDB
    connection = pymongo.MongoClient('mongodb://mongodb')
    db=connection['libertyglobal-oss-asap']
    coll=db['Environment']
    document_data=coll.find_one({'_id' : selected_environment }, { 'Old_version' : 1, '_id' : 0 })
    print document_data
    return generate_table(document_data['Old_version'])
