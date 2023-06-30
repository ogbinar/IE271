# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc

# Define the navbar structure
def Navbar():

    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Dashboard", href="/")),
                dbc.NavItem(dbc.NavLink("Orders", href="/orders")),
                dbc.NavItem(dbc.NavLink("Clients", href="/clients")),
                dbc.NavItem(dbc.NavLink("Technicians", href="/technicians")),
                dbc.NavItem(dbc.NavLink("Tasks", href="/tasks")),

            ] ,
            brand="DOST: Electronics Product Development Center Services System",
            brand_href="/"

           ,
        ), 
    ])

    return layout