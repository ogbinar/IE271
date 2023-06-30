# Import necessary libraries 
from dash import html, Dash, dash_table,dcc,Input, Output, no_update, State
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine
engine = create_engine('sqlite:///test.db', echo=True)
import pandas as pd


q = """SELECT tasks.id, tasks.name, tasks.service_type from tasks order by tasks.id"""
df = pd.read_sql_query(q,con=engine)


# Define the page layout
layout = html.Center(html.Div([
    html.H1('Tasks Definition Management'),
    html.P('View Tasks List, & Add, Edit Tasks'),
    dbc.Row([
    dbc.Col(),
    dbc.Col([dcc.Input(id="task-name", value="", placeholder="Enter New Task Name")]),
    dbc.Col([dcc.Dropdown(['RD', 'ME', 'TE'], 'RD', id='task-dropdown')]),
    dbc.Col([dbc.Button("Register Task Definition", id="add-task-button", color="primary")]),
    dbc.Col()]),
                         
    dbc.Row([
    dbc.Col([]),
    dbc.Col([dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],filter_action="native", sort_action="native",page_action="native",page_size=5,fill_width=True,id='tasks-list')]),
    dbc.Col([])]), 
    
    dbc.Modal(
            id="tasks_modal",
            size="lg",is_open=False,)
    ]
    ))


