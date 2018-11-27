import dash   # libracy for webapp
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask, request, redirect
from datetime import datetime as dt
import re  # reg expression
import os  # os related cat etc...
import pymongo
from app import app

#table data style
td_style={'padding-top':'10px', 'padding-bottom':'10px','padding-left': '10px','padding-right': '10px','color':'#1A5276'}
#table heading style
th_style={'padding-top':'10px', 'padding-bottom':'10px','padding-left': '10px','padding-right': '10px','color':'#BA4A00'}

#Generating table data from json output obtained from mongoDB
def generate_table(deployed_data,collectionName):
    print collectionName
    simplified_list=[]
    connection = pymongo.MongoClient('mongodb://mongodb')
    db=connection['libertyglobal-online-aem']
    collec=db[collectionName]
    try:
        while True:
            data=deployed_data.next()
            for key,value in data.iteritems():
                if key == 'version':
                    version=int(value)
                    print "version:::"+str(version)
                    records=collec.find({'job':'PATCH','version':version},{'Environment':1,'status':1,'date':1,'_id':0})
                    patch_count=collec.find({'job':'PATCH','version':version},{'Environment':1,'status':1,'date':1,'_id':0}).count()
                    print "counttt:"+str(patch_count)
                elif key == 'Release_Notes':
                    releaseNotes=value

            if patch_count > 0:
                try:
                    while True:
                        patch_data=records.next()
                        print patch_data
                        print "env:"+patch_data['Environment']
                        simplified_list.append([version,releaseNotes,patch_data['Environment'],patch_data['status'],patch_data['date']])
                except StopIteration:
                    pass
            else:
                simplified_list.append([version,releaseNotes,"","",""])

    except StopIteration:
        pass


    return html.Div([
        html.Table(className='reaponsive-table',
        # Header
        children=[
            html.Thead(
                html.Tr([
                    html.Th('Version', style=th_style),
                    html.Th('Release-Notes',style=th_style),
                    html.Th('Deployed-Into',style=th_style),
                    html.Th('Job-Status',style=th_style),
                    html.Th('Date',style=th_style)])
                ),

        # Body
            html.Tbody(
                [html.Tr([
                    html.Td(eachList[0],style=td_style),
                    html.Td((html.Div([html.Div(eachartifact) for eachartifact in eachList[1]])),style=td_style),
                    html.Td(eachList[2],style=td_style),
                    html.Td(eachList[3],style=td_style),
                    html.Td(eachList[4],style=td_style)
                    ]) for eachList in simplified_list]
                )
    ],style={
            'margin-left': 'auto',
            'margin-right': 'auto',
            'padding-left': '50px',
            'padding-right': '50px',
            'textAlign': 'left',
            })
])
aem_env_list=["AEM56_CH","AEM56_NL"]

#Desiging layout of page
layout = html.Div([
    #Including local stylesheet
    html.Link(href='/static/table_style.css', rel='stylesheet'),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div([
            html.B(html.Div('Environment', className='app_name',style={'color':'#597E16','fontSize': 16})),
            html.Div(dcc.Dropdown(id='environments-dropdown',
                                  options=[{'label': k, 'value': k} for k in aem_env_list]))
            ],style={'width': '50%','display': 'inline-block','float': 'left'}),
        #html.Br(),
        html.Div([
            html.B(html.Div('SprintRelease', className='app_name',style={'color':'#597E16','fontSize': 16})),
            html.Div(dcc.Dropdown(id='SprintRelease-dropdown'))
            ],style={'width': '50%','display': 'inline-block','float': 'right'})
        ],style={'width': '45%'}),
    html.Br(),
    html.Br(),
    html.Div(id='resultant_display')
])

@app.callback(
    dash.dependencies.Output('SprintRelease-dropdown', 'options'),
    [dash.dependencies.Input('environments-dropdown', 'value')])
def set_SprintRelease_options(selected_collection):
        print "Selected environment is : "+selected_collection
        connection = pymongo.MongoClient('mongodb://mongodb')
        db=connection['libertyglobal-online-aem']
        collectionList=db.collection_names()
        collectionList=filter(None,collectionList)
        print collectionList
        sprintrelease_list=[]
        for item in collectionList:
                if selected_collection in item:
                        sprintrelease_list.append(item.split(selected_collection+'-')[-1])
        print sprintrelease_list
        return [{'label': i, 'value': i} for i in sprintrelease_list]

@app.callback(
    dash.dependencies.Output('resultant_display', 'children'),
    [dash.dependencies.Input('environments-dropdown', 'value'),
         dash.dependencies.Input('SprintRelease-dropdown', 'value')])
def set_SprintRelease_options1(selected_collection,selected_sprintRelease):
    print selected_collection,selected_sprintRelease
    connection = pymongo.MongoClient('mongodb://mongodb')
    db=connection['libertyglobal-online-aem']
    coll=db[selected_collection+'_'+selected_sprintRelease]
    records=coll.find({'job':'DEV'},{'version':1,'Release_Notes':1,'_id':0})
    records_count=coll.find({'job':'DEV'},{'version':1,'Release_Notes':1,'_id':0}).count()
    print "TOTAL DEV RECORDS:"+str(records_count)
    return generate_table(records,selected_collection+'-'+selected_sprintRelease)
