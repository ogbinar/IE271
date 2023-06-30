# Import necessary libraries 
from dash import  dash,html, dash_table,dcc,Input, Output, no_update, State
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
import plotly.express as px

engine = create_engine('sqlite:///test.db', echo=True)

q = """SELECT orders.id AS orders_id, orders.added_datetime AS orders_added_datetime, orders.etc_datetime AS orders_etc_datetime, orders.started_datetime AS orders_started_datetime, orders.closed_datetime AS orders_closed_datetime, orders.client_id AS orders_client_id, orders.task_id AS orders_task_id, orders.status_id AS orders_status_id, orders.tech_id AS orders_tech_id, status.id AS status_id, status.name AS status_name, tasks.id AS tasks_id, tasks.name AS tasks_name, tasks.service_type AS tasks_service_type, clients.id AS clients_id, clients.name AS clients_name, technicians.id AS technicians_id, technicians.name AS technicians_name 
FROM orders, status, tasks, clients, technicians 
WHERE orders.status_id = status.id AND orders.task_id = tasks.id AND orders.client_id = clients.id AND orders.tech_id = technicians.id"""
df = pd.read_sql_query(q,con=engine)
df1 = df[['tasks_service_type','orders_id']]
df1 = df1.apply(lambda x:x['tasks_service_type']+str(x['orders_id']).zfill(3),axis=1)
df2 = df[['tasks_service_type','tasks_name', 'orders_added_datetime', 'orders_etc_datetime',
       'orders_started_datetime', 'orders_closed_datetime',
        'clients_name',  'technicians_name', 
       'status_name' ]]
final_df=pd.concat([df1,df2],axis=1)
final_df.columns=['id','tasks_service_type','task', 'added', 'etc',
       'started', 'closed',
        'client',  'technician', 
       'status']
final_df = final_df.sort_values('status',ascending=False)

final_df['added'] = final_df['added'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f'))
final_df['etc'] = final_df['etc'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f'))
final_df['started'] = final_df['started'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f') if(x is not None) else " ")
final_df['closed'] = final_df['closed'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f') if(x is not None) else " ")

i=final_df.shape[0]

data = final_df[['id','status']].groupby('status').count().reset_index()
fig = px.pie(data, 
            values="id", names="status", title='Orders Status',
                 width=500, height=300)
fig.update_layout(showlegend=True) 


data = final_df[['id','tasks_service_type']].groupby('tasks_service_type').count().reset_index()
service_type_fig = px.pie(data, 
            values="id", names="tasks_service_type", title='Service Counts',
                 width=500, height=300)
service_type_fig.update_layout(showlegend=True) 

data = final_df[['id','client']].groupby('client').count().reset_index().sort_values("id",ascending=True)
client_fig = px.bar(data, 
            x="id", y='client', title='Client Work Counts', orientation='h',
                 width=500, height=300)
client_fig.update_layout(showlegend=False)

data = final_df[['id','technician']].groupby('technician').count().reset_index().sort_values("id",ascending=True)
tech_fig = px.bar(data, 
            x="id", y='technician', title='Technician Work Counts', orientation='h',
                 width=500, height=300)
tech_fig.update_layout(showlegend=False) 




# Define the page layout
layout = dbc.Container([
    dbc.Row([html.H1('EPDC Service Orders Dashboard')]),
    dbc.Row([
        dbc.Col([]),
        html.H2(f'Total Orders: {i}')]),
        dbc.Row([
        dbc.Col([html.Div(
         dcc.Graph(id='stat-graph',figure=fig)   
        )])
        ,
        dbc.Col([
        html.Div(
         dcc.Graph(id='service-graph',figure=service_type_fig)   
        )])]),
        dbc.Row([
        dbc.Col([html.Div(
         dcc.Graph(id='client-graph',figure=client_fig)   
        )])
        ,
        dbc.Col([
        html.Div(
         dcc.Graph(id='tech-graph',figure=tech_fig)   
        )])]),
        html.Br(),
        html.Hr()
      
    ,
    dbc.Row([])
    
])