from dash import Dash, dash_table,dcc
import pandas as pd
from dash import html
import dash_bootstrap_components as dbc
from datetime import datetime
from sqlalchemy import create_engine
engine = create_engine('sqlite:///test.db', echo=True)

q = """SELECT orders.id AS orders_id, orders.added_datetime AS orders_added_datetime, orders.etc_datetime AS orders_etc_datetime, orders.started_datetime AS orders_started_datetime, orders.closed_datetime AS orders_closed_datetime, orders.client_id AS orders_client_id, orders.task_id AS orders_task_id, orders.status_id AS orders_status_id, orders.tech_id AS orders_tech_id, status.id AS status_id, status.name AS status_name, tasks.id AS tasks_id, tasks.name AS tasks_name, tasks.service_type AS tasks_service_type, clients.id AS clients_id, clients.name AS clients_name, technicians.id AS technicians_id, technicians.name AS technicians_name 
FROM orders, status, tasks, clients, technicians 
WHERE orders.status_id = status.id AND orders.task_id = tasks.id AND orders.client_id = clients.id AND orders.tech_id = technicians.id"""
df = pd.read_sql_query(q,con=engine)
df1 = df[['tasks_service_type','orders_id']]
df1 = df1.apply(lambda x:x['tasks_service_type']+str(x['orders_id']).zfill(3),axis=1)
df2 = df[['tasks_name', 'orders_added_datetime', 'orders_etc_datetime',
       'orders_started_datetime', 'orders_closed_datetime',
        'clients_name',  'technicians_name', 
       'status_name' ]]
final_df=pd.concat([df1,df2],axis=1)
final_df.columns=['id','task', 'added', 'etc',
       'started', 'closed',
        'client',  'technician', 
       'status']
final_df = final_df.sort_values('status',ascending=False)

final_df['added'] = final_df['added'].apply(lambda x: pd.to_datetime(x))
final_df['etc'] = final_df['etc'].apply(lambda x: pd.to_datetime(x))
final_df['started'] = final_df['started'].apply(lambda x: pd.to_datetime(x) if(x is not None) else " ")
final_df['closed'] = final_df['closed'].apply(lambda x: pd.to_datetime(x) if(x is not None) else " ")



q = """SELECT tasks.id, tasks.name, tasks.service_type from tasks order by tasks.id"""
df = pd.read_sql_query(q,con=engine)
#tasks = df['name'].values
tasks = {j:i for i,j in df[['name','id']].values}
print(tasks)

q = """SELECT clients.id, clients.name from clients order by clients.id"""
df = pd.read_sql_query(q,con=engine)
#clients = df['name'].values
clients = {j:i for i,j in df[['name','id']].values}

q = """SELECT technicians.id, technicians.name from technicians order by technicians.id"""
df = pd.read_sql_query(q,con=engine)
#technicians = df['name'].values
technicians = {j:i for i,j in df[['name','id']].values}

layout = html.Center(html.Div([
    html.H1('EPDC Services Management'),
    html.P('View Service Orders, & Add, Edit Orders'),
    
    
    html.Div([
    dbc.Row([
    dbc.Col(dcc.Dropdown(tasks, '',  id='select-task-dropdown',placeholder="Select Task")),
    dbc.Col(dcc.Dropdown(clients, '', id='select-client-dropdown',placeholder="Select Client")),
    dbc.Col(dcc.Dropdown(technicians, '', id='select-tech-dropdown',placeholder="Select Technician")),
    dbc.Col(dbc.Button("Schedule Order Request", id="add-order-button", color="primary"))])
    
      ]),
    
    dbc.Col([]),
    dbc.Col([dash_table.DataTable(final_df.to_dict('records'), [{"name": i, "id": i} for i in final_df.columns],filter_action="native", sort_action="native",page_size=5,fill_width=False,id='orders-list')])
    ,
    dbc.Col([])
    ,
        dbc.Modal(
            id="orders_modal",
            size="lg",is_open=False,)
    
    ]
    ))

