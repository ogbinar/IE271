from dash import  dash,html, dash_table,dcc,Input, Output, no_update, State
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from components import navbar
import pandas as pd
from pages import dashboard,clients,technicians,tasks,orders
import model

engine = create_engine('sqlite:///test.db', echo=True)


app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.CERULEAN], 
                meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                suppress_callback_exceptions=True)

server=app.server

# Define the navbar
nav = navbar.Navbar()

# Define the index page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav, 
    html.Div(id='page-content', children=[dashboard.layout]), 
])
app.config.suppress_callback_exceptions = True


# Create the callback to handle mutlipage inputs
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return dashboard.layout
    if pathname == '/orders':
        return orders.layout
    if pathname == '/clients':
        return clients.layout
    if pathname == '/technicians':
        return technicians.layout
    if pathname == '/tasks':
        return tasks.layout

    else: # if redirected to unknown link
        return "404 Page Error! Please choose a link"


@app.callback(
    Output("client_modal", "is_open"),
    Output("client_modal", "children"),Output("clients-list","data"),
    Input("add-client-button", "n_clicks"),
    State("name", "value"),
)
def register_client(n_clicks, name):
    




    if n_clicks:
        children = dbc.Container(
        [
            dbc.ModalHeader(
                "NOTICE!"
            ),
            dbc.ModalBody(
                [
                    html.H3(f"{name} client has been registered."),
                    html.P("Press ESC or click outside to close.")
                   
                ]
            ), 
        ],
        )
    
        q = """select max(id) from clients"""
        df = pd.read_sql_query(q,con=engine)
        j = df.values[0][0]
        new_client = model.Clients(id=(int(j)+1),name=name)
        Session = sessionmaker(bind=engine)
        with Session() as session:
            session.add(new_client)
            session.commit()
    
    
        q = """SELECT clients.id, clients.name from clients order by clients.id"""
        clients.df = pd.read_sql_query(q,con=engine)
        return True, children, clients.df.to_dict('records')
    return False, no_update, clients.df.to_dict('records')

@app.callback(
    Output("tech_modal", "is_open"),
    Output("tech_modal", "children"),Output("tech-list","data"),
    Input("add-tech-button", "n_clicks"),
    State("tech-name", "value"),
)
def register_tech(n_clicks, name):
    




    if n_clicks:
        children = dbc.Container(
        [
            dbc.ModalHeader(
                "NOTICE!"
            ),
            dbc.ModalBody(
                [
                    html.H3(f"{name} technician has been registered."),
                    html.P("Press ESC or click outside to close.")
                   
                ]
            ), 
        ],
        )
    
        q = """select max(id) from technicians"""
        df = pd.read_sql_query(q,con=engine)
        j = df.values[0][0]
        new_tech= model.Technicians(id=(int(j)+1),name=name)
        Session = sessionmaker(bind=engine)
        with Session() as session:
            session.add(new_tech)
            session.commit()
    
    
        q = """SELECT technicians.id, technicians.name from technicians order by technicians.id"""
        technicians.df = pd.read_sql_query(q,con=engine)
        return True, children, technicians.df.to_dict('records')
    return False, no_update, technicians.df.to_dict('records')


@app.callback(
    Output("tasks_modal", "is_open"),
    Output("tasks_modal", "children"),Output("tasks-list","data"),
    Input("add-task-button", "n_clicks"),
    State("task-name", "value"),State("task-dropdown", "value"),
)
def register_tasks(n_clicks, name,service):
    




    if n_clicks:
        children = dbc.Container(
        [
            dbc.ModalHeader(
                "NOTICE!"
            ),
            dbc.ModalBody(
                [
                    html.H3(f"{name} tasks has been registered."),
                    html.P("Press ESC or click outside to close.")
                   
                ]
            ), 
        ],
        )
    
        q = """select max(id) from tasks"""
        df = pd.read_sql_query(q,con=engine)
        j = df.values[0][0]
        new_task= model.Tasks(id=(int(j)+1),name=name,service_type=service)
        Session = sessionmaker(bind=engine)
        with Session() as session:
            session.add(new_task)
            session.commit()
    
    
        q = """SELECT tasks.id, tasks.name, tasks.service_type from tasks order by tasks.id"""
        tasks.df = pd.read_sql_query(q,con=engine)
        return True, children, tasks.df.to_dict('records')
    return False, no_update, tasks.df.to_dict('records')

# Run the app on localhost:8050
if __name__ == '__main__':
    app.run_server(debug=False)