# Import necessary libraries 
from dash import html, Dash, dash_table,dcc,Input, Output, no_update, State
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine
engine = create_engine('sqlite:///test.db', echo=True)
import pandas as pd


q = """SELECT clients.id, clients.name from clients order by clients.id"""
df = pd.read_sql_query(q,con=engine)


# Define the page layout
layout = html.Center(html.Div([
    html.H1('Client Management'),
    html.P('View Client List, & Add, Edit Clients'),
    html.Div([dcc.Input(
                            id="name",
                            value="",
                            placeholder="Enter New Client Name",
                        ),
              dbc.Button("Register Client", id="add-client-button", color="primary")
                        ]),
    dbc.Col([]),
    dbc.Col([dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],filter_action="native", sort_action="native",page_action="native",page_size=5,fill_width=True,id='clients-list')])
    ,
    dbc.Col([]), 
    
    dbc.Modal(
            id="client_modal",
            size="lg",is_open=False,)
    ]
    ))


