from app import app
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
#from pandas_datareader import data as web
from datetime import datetime as dt
import re
import os
import pymongo
import pandas as pd

today_date=dt.now()
connection = pymongo.MongoClient("mongodb://"+os.environ['clarify_user']+":"+os.environ['clarify_pwd']+"@mongodb:27017/libertyglobal-bss-clarify?ssl=false")
db=connection['libertyglobal-bss-clarify']
layout = html.Div([
    #Including local stylesheet
    html.Br(),
    html.Br(),
    dcc.Location(id='url', refresh=False),
    html.Div(id='start_date_temp_store',style={'display':'none'}),
    html.Div(id='end_date_temp_store',style={'display':'none'}),
    html.Div(id='affiliate_temp_store',style={'display':'none'}),
    html.Div(id='load_layout')
           ])
initial_layout=html.Div([
    html.Table(
        # Header
        children=[

        # Body
            html.Tbody(
                [html.Tr([
                    html.Td('Affiliate',style={'padding-bottom':'10px','padding-right': '30px','textAlign': 'left','color':'#597E16','fontSize': 18,'fontWeight':'bold'}),
                    html.Td(children=html.Div(dcc.Dropdown(id='Affiliate',
                                                           options=[{'label': k, 'value': k} for k in ['CH','NL','AT','IE','RO','CZ']],
                                                           style={'color':'#000000','width':'100px',})),style={'padding-bottom':'10px','padding-left': '10px','padding-right': '40px'})
                    ]),
                html.Tr([
                    html.Td('From Date',style={'padding-bottom':'10px','padding-right': '30px','textAlign': 'left','color':'#597E16','fontSize': 18,'fontWeight':'bold'}),
                    html.Td(children=html.Div(dcc.DatePickerSingle(
                                                           id='start_date',
                                                           min_date_allowed=dt(2018, 1, 1),
                                                           max_date_allowed=today_date,
                                                           initial_visible_month=today_date,
														   date=str(today_date),
                                                          
                                                       )),style={'padding-bottom':'10px','padding-left': '10px','padding-right': '40px'})
                    ]),
                html.Tr([
                    html.Td('To Date',style={'padding-bottom':'10px','padding-right': '30px','textAlign': 'left','color':'#597E16','fontSize': 18,'fontWeight':'bold'}),
                    html.Td(children=html.Div(dcc.DatePickerSingle(
                                                           id='end_date',
                                                           min_date_allowed=dt(2018, 1, 1),
                                                           max_date_allowed=today_date,
                                                           initial_visible_month=today_date,
                                                           date=str(today_date),
                                                       )),style={'padding-bottom':'10px','padding-left': '10px','padding-right': '40px'})
                    ])
                ])
    ],style={
            'margin-left': 'auto',
            'margin-right': 'auto',
            'padding-left': '50px',
            'padding-right': '50px',
            'textAlign': 'left',
            'border':'1px'
            }),
        html.Br(),
        html.Div(id='submit_button'),
        html.Br()])

result_layout=html.Div([
    dcc.RadioItems(
    id='env_checklist',
    options=[
        {'label': 'JIT', 'value': 'JIT'},
        {'label': 'UAT', 'value': 'UAT'},
        {'label': 'ORT', 'value': 'ORT'},
        {'label': 'PROD', 'value': 'PROD'}
    ],
    value='',
    labelStyle={'display': 'inline-block'},
    inputStyle={'marginLeft':'50px'},
    style={'padding-right':'50px'}
   ),
   html.Br(),
   html.Br(),
   html.Div([html.Label('RM Number:',style={'color':'#597E16','fontWeight':'bold'}),
   html.Div(dcc.Input(id='rm_number',
             placeholder='Enter RM number',
             type='text',
             style={'width':'120px','height':'30px','borderRadius':'4px','textAlign':'center'}
         ),
    style={'display':'inline-block','padding-left':'10px'}),],style={'textAlign':'center','display':'inline-block'}),
   html.Div(html.Button('Search', id='search_button',n_clicks=0),style={'display':'inline-block','padding-left':'50px','height':'30px','borderRadius':'4px'}),
   html.Br(),
   html.Br(),
   html.Br(),
   html.Div(id='rm_list',style={'display':'inline-block','float':'left','padding-right':'80px','padding-left':'200px'}),
   html.Div([html.Div(id='rm_data'),
   html.Br(),
   html.Br(),
   html.Div(id='rm_search_data'),
   html.Br(),
   html.Br(),
   html.Br(),
   html.Br()],style={'display':'inline-block','float':'right','padding-right':'300px','padding-left':'80px'}),
   html.Div(html.Button(id='back',
                             n_clicks=0, children = dcc.Link('BACK',href='/release-history'),
                             style={'padding-top':'5px','padding-bottom':'5px','color':'#008080','backgroundColor':'#A9A9A9','width':'85px','borderRadius':'4px'}),style={'padding-left':'600px'})
   ],style={'textAlign':'center'})

@app.callback(
    Output('submit_button','children'),
    [Input('Affiliate', 'value'),
     Input('start_date', 'date'),
     Input('end_date', 'date')])
def display_submit_button(Affiliate,start_date,end_date):
    if Affiliate:
        if start_date<=end_date:
            return html.Div(html.Button(id='Submit',
                             n_clicks=0, children = dcc.Link('Submit',href='/release-history/release-history-result'),
                             style={'padding-top':'5px','padding-bottom':'5px','color':'#008080','backgroundColor':'#A9A9A9','width':'85px','borderRadius':'4px'}),style={'padding-left':'510px'})
        else:
            return html.Div('End date should be greater than start date!!!',style={'padding-left': '425px','textAlign': 'left','color': '#DF0101','fontSize':25})

@app.callback(Output('start_date_temp_store','children'),
              [Input('start_date','date')])
def store_start_date(start_date):
    return start_date

@app.callback(Output('end_date_temp_store','children'),
              [Input('end_date','date')])
def store_end_date(end_date):
    return end_date

@app.callback(Output('affiliate_temp_store','children'),
              [Input('Affiliate','value')])
def store_start_date(Affiliate):
    return Affiliate

@app.callback(Output('load_layout', 'children'),
              [Input('url', 'pathname')],
              [State('affiliate_temp_store','children')])
def display_page(pathname,affiliate):
    if pathname == '/release-history' or pathname == '/release-history/':
        return initial_layout
    elif pathname=='/release-history/release-history-result':
        return html.Div([
                    html.Div('Affiliate : '+affiliate,style={'textAlign':'center','fontSize':16,'fontWeight':'bold'}),
                    html.Br(),
                    html.Br(),
                    result_layout
                    ])

@app.callback(
    Output('rm_list','children'),
    [Input('env_checklist','value')],
    [State('start_date_temp_store','children'),State('end_date_temp_store','children'),State('affiliate_temp_store','children')])
def display_uat_rm_list(env,start_date,end_date,affiliate):
    #return 'You selected "{}" and start date "{}" and end date "{}"'.format(env_list,start_date,end_date)
    env_rm_final_dict={}
    if env != '':
        date_RM_dict={}
        RM_list_sorted_date=[]
        coll=db[affiliate.lower()+'-'+env]
        print affiliate+'-'+env
        deploy_data=coll.find()
        for each_doc in deploy_data:
          for each_rm_keys in each_doc['RM_ID'].keys():
            release_date = dt.strptime(str(each_doc['RM_ID'][each_rm_keys]['deployed_time']), '%Y_%m_%d_%H_%M_%S')
            start_date=dt.strptime(str(start_date).split()[0], '%Y-%m-%d')
            end_date=dt.strptime(str(end_date).split()[0], '%Y-%m-%d')
            if release_date >= start_date and release_date<=end_date:
              date_RM_dict[release_date]= each_rm_keys
        RM_list_sorted_date = list(set([rm_dict for date,rm_dict in sorted(date_RM_dict.items(), key=lambda p: p[0], reverse=True)]))
        env_rm_final_dict[env] = RM_list_sorted_date
        env_dataframe=pd.DataFrame.from_dict(env_rm_final_dict)
        return html.Div([
                    html.Br(),
                    html.Br(),
                    dash_table.DataTable(
                        id='rm_list_table',
                        columns=[{"name": i, "id": i} for i in env_dataframe.columns],
                        data=env_dataframe.to_dict("rows"),
                        is_focused=True,
                        style_cell={'textAlign': 'center','backgroundColor':'#F0FFF0','minWidth': '80px', 'maxWidth': '1000px'},
                        row_selectable="single",
                        selected_rows=[],
                        style_table={
                        'maxHeight': '300px',
                        'overflowY': 'scroll'
                    },
                       n_fixed_columns=1,
                       n_fixed_rows=1,
                       style_data={'whiteSpace': 'normal'},
                        #content_style='fit',
                        style_header={
                        'backgroundColor': '#3CB371',
                        'fontWeight': 'bold',
                        'color': 'white',
                        'fontSize':20
                        })
                ])
    else:
        return

@app.callback(
    Output('rm_data','children'),
    [Input('rm_list_table','data'),Input('rm_list_table','selected_rows')],
    [State('env_checklist','value'),State('affiliate_temp_store','children')])
def display_selected_rm_details(rm_list,selected_row,env,affiliate):
    if len(selected_row)!=0:
        print rm_list[selected_row[0]][env]
        rm_data_list=[]
        for each_env in ['JIT','UAT']:
            rm_data_dict={}
            coll=db[affiliate.lower()+'-'+each_env]
            try:
                required_details=coll.find({'RM_ID.'+rm_list[selected_row[0]][env]: { '$exists': True }}, {'RM_ID.'+rm_list[selected_row[0]][env]+'.release_version': 1,'RM_ID.'+rm_list[selected_row[0]][env]+'.deployed_time': 1, '_id': 0})
                data=required_details.next()
                print data
                rm_data_dict['App Environment']=each_env
                rm_data_dict['Release-Version']=data['RM_ID'][rm_list[selected_row[0]][env]]['release_version']
                rm_data_dict['Deployed-Date']=dt.strptime(str(data['RM_ID'][rm_list[selected_row[0]][env]]['deployed_time']), '%Y_%m_%d_%H_%M_%S').ctime()
                print rm_data_dict
            except Exception as e:
                print e
                rm_data_dict['App Environment']=each_env
                rm_data_dict['Release-Version']='Not Deployed'
                rm_data_dict['Deployed-Date']='Not Deployed'
                print rm_data_dict
            rm_data_list.append(rm_data_dict)
        rm_df=pd.DataFrame.from_dict(rm_data_list)
        return html.Div([
            html.Div(rm_list[selected_row[0]][env],style={'fontSize':15}),
            html.Br(),
            dash_table.DataTable(
                        id='rm_data_table',
                        columns=[{"name": i, "id": i} for i in rm_df.columns],
                        data=rm_df.to_dict("rows"),
                        is_focused=True,
                        style_cell={'textAlign': 'center','backgroundColor':'#FFFFFF','minWidth': '110px', 'maxWidth': '1000px'},
                       style_data={'whiteSpace': 'normal'},
                        #content_style='fit',
                        style_header={
                        'backgroundColor': '#98AFC7',
                        'fontWeight': 'bold',
                        'color': 'white',
                        'fontSize':20
                        })
            ])
    else:
        return

@app.callback(
    Output('rm_search_data','children'),
    [Input('rm_number','value'),Input('search_button', 'n_clicks')],
    [State('affiliate_temp_store','children')])
def searched_rm_details(rm_number,n_clicks,affiliate):
    if n_clicks>0 and re.search(r'(RM-[0-9]{5,6})',rm_number):
        print rm_number
        rm_data_list=[]
        for each_env in ['JIT','UAT']:
            rm_data_dict={}
            coll=db[affiliate.lower()+'-'+each_env]
            try:
                required_details=coll.find({'RM_ID.'+rm_number: { '$exists': True }}, {'RM_ID.'+rm_number+'.release_version': 1,'RM_ID.'+rm_number+'.deployed_time': 1, '_id': 0})
                data=required_details.next()
                print data
                rm_data_dict['App Environment']=each_env
                rm_data_dict['Release-Version']=data['RM_ID'][rm_number]['release_version']
                rm_data_dict['Deployed-Date']=dt.strptime(str(data['RM_ID'][rm_number]['deployed_time']), '%Y_%m_%d_%H_%M_%S').ctime()
                print rm_data_dict
            except Exception as e:
                print e
                rm_data_dict['App Environment']=each_env
                rm_data_dict['Release-Version']='Not Deployed'
                rm_data_dict['Deployed-Date']='Not Deployed'
                print rm_data_dict
            rm_data_list.append(rm_data_dict)
        rm_df=pd.DataFrame.from_dict(rm_data_list)
        return html.Div([
            html.Div(rm_number,style={'fontSize':15}),
            html.Br(),
            dash_table.DataTable(
                        id='rm_data_table',
                        columns=[{"name": i, "id": i} for i in rm_df.columns],
                        data=rm_df.to_dict("rows"),
                        is_focused=True,
                        style_cell={'textAlign': 'center','backgroundColor':'#F0FFF0','minWidth': '110px', 'maxWidth': '1000px'},
                       style_data={'whiteSpace': 'normal'},
                        #content_style='fit',
                        style_header={
                        'backgroundColor': '#00CED1',
                        'fontWeight': 'bold',
                        'color': 'white',
                        'fontSize':20
                        })
            ])



