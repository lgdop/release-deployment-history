import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
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

app = dash.Dash('dashboard_code')
#app.config.supress_callback_exceptions=True  #It is set to suppress the exception that is generated while assigning callbacks to components that are not in the initial layout but are generated by other callbacks
server = app.server
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

with open('asap_hosts') as fp:
    asap_host=fp.readlines()
asap_env_list=[]
for line in asap_host:
    try:
        env=re.search(r'^\[[A-Z]{2}[A-z][a-z0-9]',line).group(0)
        asap_env_list.append(re.search(r'[A-Z]{2}[A-z][a-z0-9]',env).group(0))
    except AttributeError:
	pass
#This key value pair is for loading the 2 dropdowns AAplication Name and Environment
#Key is for Application name and Value is for Environment
all_options = {
    'ASAP': asap_env_list,
    'Clarify': ['DEV-NL','DEV-CH','JIT-NL']
}

#Desiging layout of page
app.layout = html.Div([
    #Including local stylesheet
    html.Link(href='/static/table_style.css', rel='stylesheet'),
    html.H1(children='Release Deployment History', style={'textAlign': 'center','color': '#F39C12'}),
    html.Div([
        html.B(html.Div('Application Name', className='app_name',style={'color':'#597E16'})),
        html.Div(dcc.Dropdown(
            id='application-dropdown',
            options=[{'label': k, 'value': k} for k in all_options.keys()],
            )
                 )
        ]),
    html.Br(),
    html.Div([
        html.B(html.Div('Environment', className='app_name',style={'color':'#597E16'})),
        html.Div(dcc.Dropdown(id='environments-dropdown'))
        ]),
    html.Br(),
    html.Br(),
    html.Div(id='display-selected-values')
 
])

#app.callback are decorators. The functions that follow the decorator are executed immediately when the app is launched or there is change in inputs
#Output indicate the result to be displayed on the screen
#Input indicates the user input from the layout provided to the function
#Below callback loads the dropdown options for environments based on application selected
@app.callback(
    dash.dependencies.Output('environments-dropdown', 'options'),
    [dash.dependencies.Input('application-dropdown', 'value')])
def set_environments_options(selected_application):
    return [{'label': i, 'value': i} for i in all_options[selected_application]]

#This callback displays the value selected from environment dropdown as selected option
@app.callback(
    dash.dependencies.Output('environments-dropdown', 'value'),
    [dash.dependencies.Input('environments-dropdown', 'options')])
def set_environments_value(available_options):
    return available_options[0]['value']

#Below callback takes the 2 dropdown inputs and generates a table by taking details from mongoDB and displays the result on the page
@app.callback(
    dash.dependencies.Output('display-selected-values', 'children'),
    [dash.dependencies.Input('application-dropdown', 'value'),
     dash.dependencies.Input('environments-dropdown', 'value')])
def set_display_children(selected_application, selected_environment):
#Connecting to LGDOP mongoDB
    connection = pymongo.MongoClient('mongodb://mongodb')
    if selected_application == 'ASAP':
        db=connection['libertyglobal-bss-clarify']
        coll=db['Environment']
        document_data=coll.find_one({'_id' : selected_environment }, { 'Old_version' : 1, '_id' : 0 })
        print document_data
        return generate_table(document_data['Old_version'])
        #return dcc.Link(html.Button(id='submit-button',children='Submit'), href='/asap_deployments')
    else:
        return dcc.Link(html.Button(id='submit-button',children='Submit'), href='/clarify_deployments')

if __name__ == '__main__':
    app.run_server(port=3005,debug=True)
