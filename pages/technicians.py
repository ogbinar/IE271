# Import necessary libraries 
from dash import html, Dash, dash_table,dcc,Input, Output, no_update, State
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine
engine = create_engine('sqlite:///test.db', echo=True)
import pandas as pd


q = """SELECT technicians.id, technicians.name from technicians order by technicians.id"""
df = pd.read_sql_query(q,con=engine)

p = """SELECT specialties.task_id,tasks.id,tasks.service_type as service_type,tasks.name as specialty,technicians.id,technicians.name as technicians, specialties.technician_id from specialties 
, tasks,  technicians where specialties.task_id=tasks.id and specialties.technician_id=technicians.id

  order by specialties.technician_id"""
df2 = pd.read_sql_query(p,con=engine)
df2 = df2[['service_type','specialty','technicians']]

# Define the page layout
layout = html.Center(html.Div([
    html.H1('Technicians Management'),
    html.P('View Technicians List, & Add, Edit Clients'),
    html.Div([dcc.Input(
                            id="tech-name",
                            value="",
                            placeholder="Enter New Technicians Name",
                        ),
              dbc.Button("Register Technicians", id="add-tech-button", color="primary")
                        ]),
    dbc.Col([]),
    dbc.Col([dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],filter_action="native", sort_action="native",page_action="native",page_size=5,fill_width=True,id='tech-list')])
    ,
    dbc.Col([]), 
    
    dbc.Modal(
            id="tech_modal",
            size="lg",is_open=False,),
    html.Br(),        
    html.H1('Specialization Assignment'),
    html.P('View Specializations, & Assign, Edit'),
       
    dbc.Col([]),
    dbc.Col([dash_table.DataTable(df2.to_dict('records'), [{"name": i, "id": i} for i in df2.columns],filter_action="native", sort_action="native",page_action="native",page_size=5,fill_width=True,id='spec-list')])
    ,
    dbc.Col([]),         
    ]
    ))


# write code to assign expertise of technician 
