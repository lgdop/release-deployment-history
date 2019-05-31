from app import app
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
#from pandas_datareader import data as web
from datetime import datetime as dt
import re
import os
import pymongo

#server = Flask(__name__)

#table data style
td_style={'padding-top':'10px', 'padding-bottom':'10px','padding-left': '10px','padding-right': '10px','color':'#306EFF'}
#1A5276'}
#table heading style
th_style={'padding-top':'10px', 'padding-bottom':'10px','padding-left': '10px','padding-right': '10px','color':'#2B3856'}
#'#BA4A00'}

connection = pymongo.MongoClient("mongodb://"+os.environ['asap_user']+":"+os.environ['asap_pwd']+"@mongodb:27017/libertyglobal-oss-asap?ssl=false")
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
    return simplified_dict

asap_env_list=['DEV1', 'DEd1', 'DEj1', 'DEu1', 'DEp3', 'DEj4', 'DEu4', 'DEp4', 'NLj4', 'NLu4', 'NLo4', 'NLp4', 'PLj3', 'PLu3', 'PLo3', 'PLp3', 'HUj2', 'HUu2', 'HUo2', 'HUp2', 'CZj4', 'CZu4', 'CZo4', 'CZp4', 'SKj2', 'SKu2', 'SKo2', 'SKp2', 'ROj2', 'ROu2', 'ROp2', 'CHj3', 'CHu3', 'CHo3', 'CHp3', 'ATj1', 'ATu1', 'ATo1', 'ATp1', 'CZj3', 'CZu2', 'CZp2', 'CHj4', 'CHu4', 'CHo4', 'CHp4','ATj4', 'ATu4', 'ATo4', 'ATp4','ROj1', 'ROu1', 'ROp1','IEj3','IEu3','IEo3','IEp3']

#Desiging layout of page
layout = html.Div([
    #Including local stylesheet
    html.Link(href='/static/cdc_layout_style.css', rel='stylesheet'),
    html.Link(href='/static/table_style.css', rel='stylesheet'),
    html.Div([
        dcc.Tabs(
            id="asap_tabs",
            style={"height":"5",'textAlign': 'center','color': '#008080','cursor': 'pointer','align-items': 'center','justify-content': 'center','fontSize': 20},
            #style=tabs_styles,
            children=[
                dcc.Tab(label="Environment status", value="env_tab",selected_style={'color': '#CD5C5C','backgroundColor': '#66CDAA',"border": "#A52A2A"}),
                dcc.Tab(label="Latest build", value="build_tab",selected_style={'color': '#CD5C5C','backgroundColor': '#66CDAA',"border": "#A52A2A"}),
                dcc.Tab(label="Compare ENV-to-ENV", value="env_cmp_tab",selected_style={'color': '#CD5C5C','backgroundColor': '#66CDAA',"border": "#A52A2A"}),
                dcc.Tab(label="Comapre ENV-to-Latest-Build", value="env_crq_tab",selected_style={'color': '#CD5C5C','backgroundColor': '#66CDAA',"border": "#A52A2A"}),
                ],
            value="env_tab",
            colors={
                "border": "#FFFFFF",
                "primary": "#F5F5DC",
                "background": "#F5F5DC"
                }
            #vertical="vertical",
            )]
            ),
    html.Br(),
    html.Div(id='display_next_layout')

])

env_status_layout=html.Div([
                        html.Br(),
                        html.Table(
                        # Header
                        children=[
                            html.Thead(
                                html.Tr([
                                    html.Th(html.Div([
                                                     html.B(html.Div('Environment : ', className='env_name',style={'color':'#597E16','fontSize': 18,'display':'inline-block','float':'left','padding-right':'10px'})),
                         ]), style={'padding-top':'10px', 'padding-bottom':'10px','color':'#1A5276'}),
                                    html.Th(html.Div([
                                                     html.Div(dcc.Dropdown(id='environment1-dropdown',
                                                                           options=[{'label': k, 'value': k} for k in asap_env_list],
                                                                           placeholder='Select the environment'),
                                                               style={'display':'inline-block','float':'right','width':'200px'})
                         ]), style={'padding-top':'10px', 'padding-bottom':'10px','padding-right': '100px','color':'#1A5276'})
                                    ])
                                ), 
                        ],style={
                                'margin-left': 'auto',
                                'margin-right': 'auto',
                                'padding-left': '50px',
                                'padding-right': '50px',
                                'textAlign': 'left',
                                }),
                        html.Br(),
                        html.Br(),
                        html.Div(id='display_table_1'),
                       ])
@app.callback(
    dash.dependencies.Output('display_table_1', 'children'),
    [dash.dependencies.Input('environment1-dropdown', 'value')])
def set_env_status_table(selected_environment):
#Connecting to LGDOP mongoDB
    print selected_environment
    db=connection['libertyglobal-oss-asap']
    coll=db['Environment']
    document_data=coll.find_one({'_id' : selected_environment }, { 'Old_version' : 1, '_id' : 0 })
    print document_data
    simplified_dict=generate_table(document_data['Old_version'])
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

crq_status_layout=html.Div([
                        html.Br(),
                        html.Table(
                        # Header
                        children=[
                            html.Thead(
                                html.Tr([
                                    html.Th(html.Div([
                                                     html.B(html.Div('CRQ :', className='crq_name',style={'color':'#597E16','fontSize': 18,'display':'inline-block','float':'left','padding-right':'10px'})),
                         ]), style={'padding-top':'10px', 'padding-bottom':'10px','color':'#1A5276'}),
                                    html.Th(html.Div([
                                                     html.Div(dcc.Input(id='crq',
                                                                        placeholder='Enter the CRQ number',
                                                                        type='text',
                                                                        style={'width':'200px','height':'30px','borderRadius':'4px'}
                                                                    ),
                                                               style={'display':'inline-block','float':'right'})
                         ]), style={'padding-top':'10px', 'padding-bottom':'10px','padding-right': '100px','color':'#1A5276'})
                                    ])
                                ), 
                        ],style={
                                'margin-left': 'auto',
                                'margin-right': 'auto',
                                'padding-left': '50px',
                                'padding-right': '50px',
                                'textAlign': 'left',
                                }),
                        html.Br(),
                        html.Br(),
                        html.Div(id='display_table_2'),
                       ])
@app.callback(
    dash.dependencies.Output('display_table_2', 'children'),
    [dash.dependencies.Input('crq', 'value')])
def set_crq_status_table(crq):
#Connecting to LGDOP mongoDB
    #print selected_environment
    db=connection['libertyglobal-oss-asap']
    coll=db['ChangeRequests']
    document_data=coll.find_one({'_id' : crq }, { 'Property_file' : 1, '_id' : 0 })
    print document_data
    simplified_dict=generate_table(document_data['Property_file'])
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

compare_env_layout=html.Div([
                        html.Br(),
                        html.Table(
                        # Header
                        children=[
                            html.Thead(
                                html.Tr([
                                    html.Th(html.Div([
                                                     html.B(html.Div('Environment :', className='env_name',style={'color':'#597E16','fontSize': 18,'display':'inline-block','float':'left','padding-right':'10px'})),
                         ]), style={'padding-top':'10px', 'padding-bottom':'10px','color':'#1A5276'}),
                                    html.Th(html.Div([
                                                     html.Div(dcc.Dropdown(id='env1-dropdown',
                                                                           options=[{'label': k, 'value': k} for k in asap_env_list],
                                                                           placeholder='Select the environment'),
                                                               style={'display':'inline-block','float':'right','width':'200px'})
                         ]), style={'padding-top':'10px', 'padding-bottom':'10px','color':'#1A5276'}),
                                    html.Th(html.Div([
                                                     html.B(html.Div('Environment :', className='env_name',style={'color':'#597E16','fontSize': 18,'display':'inline-block','float':'left','padding-right':'10px','padding-left':'250px'})),
                         ]), style={'padding-top':'10px', 'padding-bottom':'10px','padding-left':'100px','color':'#1A5276'}),
                                    html.Th(html.Div([
                                                     html.Div(dcc.Dropdown(id='env2-dropdown',
                                                                           options=[{'label': k, 'value': k} for k in asap_env_list],
                                                                           placeholder='Select the environment'),
                                                               style={'display':'inline-block','float':'right','width':'200px'})
                         ]), style={'padding-top':'10px', 'padding-bottom':'10px','padding-right': '100px','color':'#1A5276'})])
                                ), 
                        ],style={
                                'margin-left': 'auto',
                                'margin-right': 'auto',
                                #'padding-left': '50px',
                                #'padding-right': '50px',
                                'textAlign': 'left',
                                }),
                        html.Br(),
                        html.Br(),
                        html.Div(id='display_table_3')
                       ])

@app.callback(
    dash.dependencies.Output('display_table_3', 'children'),
    [dash.dependencies.Input('env1-dropdown', 'value'),
     dash.dependencies.Input('env2-dropdown', 'value')])
def set_env_compare_table(selected_environment1,selected_environment2):
#Connecting to LGDOP mongoDB
    #print selected_environment
    db=connection['libertyglobal-oss-asap']
    coll=db['Environment']
    document_data1=coll.find_one({'_id' : selected_environment1 }, { 'Old_version' : 1, '_id' : 0 })
    document_data2=coll.find_one({'_id' : selected_environment2 }, { 'Old_version' : 1, '_id' : 0 })
    print document_data1
    print document_data2
    simplified_dict1=generate_table(document_data1['Old_version'])
    simplified_dict2=generate_table(document_data2['Old_version'])
    
    return html.Table(
                # Header
                children=[
                    html.Thead(
                        html.Tr([
                            html.Th(html.Div([
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
                                                    ]) for key,value in simplified_dict1.iteritems()]
                                                )
                                    ],style={
                                            'margin-left': 'auto',
                                            'margin-right': 'auto',
                                            #'padding-left': '50px',
                                            #'padding-right': '50px',
                                            'textAlign': 'left',
                                            })
                                    ]),style={'padding-left': '100px','padding-right':'75px','verticalAlign':'top'}),
                            html.Th(html.Div([
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
                                                    ]) for key,value in simplified_dict2.iteritems()]
                                                )
                                    ],style={
                                            'margin-left': 'auto',
                                            'margin-right': 'auto',
                                            #'padding-left': '50px',
                                            #'padding-right': '50px',
                                            'textAlign': 'left',
                                            })
                                    ]),style={'padding-right': '100px','padding-left':'240px','verticalAlign':'top'})
                            ])
                        ), 
                ])

compare_env_crq_layout=html.Div([
                        html.Br(),
                        html.Table(
                        # Header
                        children=[
                            html.Thead(
                                html.Tr([
                                    html.Th(html.Div([
                                                     html.B(html.Div('Environment :', className='env_name',style={'color':'#597E16','fontSize': 16,'display':'inline-block','float':'left','padding-right':'10px'})),
                         ]), style={'padding-top':'10px', 'padding-bottom':'10px','color':'#1A5276'}),
                                    html.Th(html.Div([
                                                     html.Div(dcc.Dropdown(id='environment1-dropdown',
                                                                           options=[{'label': k, 'value': k} for k in asap_env_list],
                                                                           placeholder='Select the environment'),
                                                               style={'display':'inline-block','float':'right','width':'200px'})
                         ]), style={'padding-top':'10px', 'padding-bottom':'10px','color':'#1A5276'}),
                                    html.Th(html.Div([
                                                     html.B(html.Div('CRQ :', className='env_name',style={'color':'#597E16','fontSize': 16,'display':'inline-block','float':'left','padding-right':'10px','padding-left':'250px'})),
                         ]), style={'padding-top':'10px', 'padding-bottom':'10px','padding-left':'100px','color':'#1A5276'}),
                                    html.Th(html.Div([
                                                     html.Div(dcc.Input(id='crq_text',
                                                                        placeholder='Enter the CRQ number',
                                                                        type='text',
                                                                        style={'width':'200px','height':'30px','borderRadius':'4px'}
                                                                    ),
                                                               style={'display':'inline-block','float':'right'})
                         ]), style={'padding-top':'10px', 'padding-bottom':'10px','padding-right': '100px','color':'#1A5276'})])
                                ), 
                        ],style={
                                'margin-left': 'auto',
                                'margin-right': 'auto',
                                'padding-left': '50px',
                                'padding-right': '50px',
                                'textAlign': 'left',
                                }),
                        html.Br(),
                        html.Br(),
                        html.Div(id='display_table_4')
                       ])

@app.callback(
    dash.dependencies.Output('display_table_4', 'children'),
    [dash.dependencies.Input('environment1-dropdown', 'value'),
     dash.dependencies.Input('crq_text', 'value')])
def set_env_crq_compare_table(selected_environment1,crq):
#Connecting to LGDOP mongoDB
    #print selected_environment
    db=connection['libertyglobal-oss-asap']
    coll=db['Environment']
    document_data1=coll.find_one({'_id' : selected_environment1 }, { 'Old_version' : 1, '_id' : 0 })
    coll2=db['ChangeRequests']
    document_data2=coll2.find_one({'_id' : crq }, { 'Property_file' : 1, '_id' : 0 })
    print document_data1
    print document_data2
    simplified_dict1=generate_table(document_data1['Old_version'])
    simplified_dict2=generate_table(document_data2['Property_file'])
    
    return html.Table(
                # Header
                children=[
                    html.Thead(
                        html.Tr([
                            html.Th(html.Div([
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
                                                    ]) for key,value in simplified_dict1.iteritems()]
                                                )
                                    ],style={
                                            'margin-left': 'auto',
                                            'margin-right': 'auto',
                                            #'padding-left': '50px',
                                            #'padding-right': '50px',
                                            'textAlign': 'left',
                                            })
                                    ]),style={'padding-left': '150px','padding-right':'75px','verticalAlign':'top'}),
                            html.Th(html.Div([
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
                                                    ]) for key,value in simplified_dict2.iteritems()]
                                                )
                                    ],style={
                                            'margin-left': 'auto',
                                            'margin-right': 'auto',
                                            #'padding-left': '50px',
                                            #'padding-right': '50px',
                                            'textAlign': 'left',
                                            })
                                    ]),style={'padding-right': '100px','padding-left':'220px','verticalAlign':'top'})
                            ])
                        ), 
                ])

@app.callback(Output("display_next_layout", "children"), [Input("asap_tabs", "value")])
def display_tab_content(tab):
    if tab == "env_tab":
        return env_status_layout
    elif tab == "build_tab":
        return crq_status_layout
    elif tab == "env_cmp_tab":
        return compare_env_layout
    else:
        return compare_env_crq_layout

