import dash
import pandas as pd
from data_processing import scaler
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
server = app.server

mapbox_access_token = "pk.eyJ1IjoiYW1lcmljYW50aGlua2VyIiwiYSI6ImNraGx5ZXlvYjBrMjEyd285bjJkMDloeDYifQ.kGUzdL3-USJ46CGJUTBQqQ"
px.set_mapbox_access_token(mapbox_access_token)

#Load data
vets = pd.read_csv('data/merged_df_dash.csv')
#rescale sizing and set df for mapping
map_df = vets[vets['scaled'].notnull()]
bubble_sizes = scaler(map_df['scaled'], 4, 30)
#remove Coast Guard from dataset and create branch and tribe options
branches = vets['Branch'].unique()[:4]
tribes = vets['Tribe'].unique()


colors = {
    'background1': '#111111',
    'background2': '#008080',
    'text': '#7FDBFF'
}

fig = go.Figure(go.Scattermapbox(
        lat=['32.5017'],
        lon=['-117.0973'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=28
        ),
        text=['San Diego'],
        )
    )

fig.update_layout(
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            style='dark',
            center=go.layout.mapbox.Center(
                lat=32,
                lon=-117),
            pitch=0,
            zoom=5)
        )
fig.layout.update(
    autosize=True,
    paper_bgcolor='#696969',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        center=dict(lat=38.7, lon=-98.5795),
        zoom=3.25
    ),
    margin={'l':0, 'r':0, 'b':0, 't':0})

app.layout = html.Div(id='app-container',
    children = [
        html.Div(id='title-block',
            children =[
                dbc.Row(
                    [dbc.Col(children=[
                        html.H1('Elite Meet National Distribution',
                                    style=dict(
                                        fontFamily='Times',
                                        color=colors['text'],
                                        margin = '20px'
                                              )
                                    ),
                            html.H5(
                                id='left-description',
                                children="Filter search results by Service Branch of SOF Tribe. Bubble size\
                                indicates size of population.  Color is indicitave of service branch.",
                                style = dict(
                                fontFamily='Times',
                                color=colors['text'],
                                margin='25px')
                                  )],
                            width=7)
                    ]
                        )
                    ]
                 ),

    dbc.Row(
        children=[
            dbc.Col(id='branch-dropdown',
                    width=3,
                children=[
                    dcc.Dropdown(
                        id='Branches',
                        options=branches,
                        value='Navy',
                        # allows user to select multiple drop down options
                        multi=True,
                        # allows the user to remove all options
                        clearable=True,
                                )
                        ]
                    )
                ]
            ),

    html.Div(id='map-container',
             children=[
                 dbc.Row(
                     dbc.Col(
                         html.Div(id='scatter-div',
                                  children=[
                                    dcc.Graph(id='scatter-map',
                                        figure=fig)
                                        ]
                                  ), style={'height': '100%'}, width=6)
                        )
                     ]
                 )
             ])


if __name__ == "__main__":
    app.run_server(debug=True)