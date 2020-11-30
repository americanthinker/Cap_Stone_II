import dash
import pandas as pd
from data_processing import scaler
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE], meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=3'}])
server = app.server

mapbox_access_token = "pk.eyJ1IjoiYW1lcmljYW50aGlua2VyIiwiYSI6ImNraGx5ZXlvYjBrMjEyd285bjJkMDloeDYifQ.kGUzdL3-USJ46CGJUTBQqQ"
px.set_mapbox_access_token(mapbox_access_token)

#Load data
vets = pd.read_csv('data/merged_df_dash.csv')

#***Use map_df for mapping only!!!***
#rescale sizing and set df for mapping /
map_df = vets[vets['scaled'].notnull()]
bubble_sizes = scaler(map_df['scaled'], 4, 26)

#remove Coast Guard from dataset and create branch and tribe options
branches = vets['Branch'].unique()[:4]
tribes = vets['Tribe'].unique()
branch_selection = [{'label':val, 'value':val} for val in branches]
tribe_selection = [{'label':val, 'value':val} for val in tribes]

colors = {
    'background1': '#111111',
    'background2': '#008080',
    'text': '#7FDBFF'
}
#create figure object for map
fig = go.Figure(go.Scattermapbox(
        lat=['35.5017'],
        lon=['-78.0973'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=28
        ),
        text=['San Diego'],
        )
    )

fig.layout.update(
    autosize=False,
    width=1100,
    height=600,
    paper_bgcolor='green',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style='dark',
        center=dict(lat=38.7, lon=-98.5795),
        zoom=3.75),
    margin={'l':0, 'r':0, 'b':0, 't':0}
    )

#create figure object for bar graph
barchart = go.Figure(go.Bar(
    x=["Apples", "Oranges", "Watermelon", "Pears"],
    y=[3, 2, 1, 4]))

barchart.update_layout(
    autosize=False,
    width=800,
    height=600,
    yaxis=dict(
        title_text="Y-axis Title",
        ticktext=["Very long label", "long label", "3", "label"],
        tickvals=[1, 2, 3, 4],
        tickmode="array",
        titlefont=dict(size=30),
    )
)

#fig.update_yaxes(automargin=True)


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
                                        marginLeft = '20px',
                                        marginTop='20px'
                                              )
                                    ),
                            html.H5(
                                id='left-description',
                                children="Filter search results by Service Branch of SOF Tribe. Bubble size\
                                indicates size of population.  Color is indicitave of service branch.",
                                style = dict(
                                fontFamily='Times',
                                color=colors['text'],
                                marginLeft='15px')
                                  )],
                            width=7)
                    ]
                        )
                    ]
                 ),

    dbc.Row(id='dropdowns',
        children=[
            dbc.Col(id='branch-dropdown',
                    width=3,
                children=[
                    html.Label('Service Branch',
                               style=dict(
                                   fontSize=24,
                                   fontFamily='Times')
                               ),
                    dcc.Dropdown(
                        id='Branches',
                        options=branch_selection,
                        value=['Navy'],
                        # allows user to select multiple drop down options
                        multi=True,
                        # allows the user to remove all options
                        clearable=True,
                                )
                        ]
                    ),
            dbc.Col(id='tribe-dropdown',
                    width=3,
                children=[
                    html.Label('SOF Tribe',
                               style=dict(
                                   fontSize=24,
                                   fontFamily='Times',)
                               ),
                    dcc.Dropdown(
                        id='Tribes',
                        options=[],
                        value='SEAL',
                        # allows user to select multiple drop down options
                        multi=True,
                        # allows the user to remove all options
                        clearable=True,
                                )
                        ]
                    ),
            dbc.Col(html.Div(dbc.Alert("This is a column", color='primary')),
                    width=dict(size=4, offset=1))
                ]
            ),

    html.Div(id='graph-container', style={'height':'60vh', 'background':'yellow'},
             children=[
                 dbc.Row([
                     dbc.Col(
                         html.Div(id='scatter-div', style={'height':'50vh'},
                                  children=[html.Div(id='internal-scatter-div',
                                                     style=dict(height='80vh'),
                                    children=[dcc.Graph(id='scatter-map',
                                              figure=fig
                                             )]
                                                    )
                                           ]
                                  ), style={'height': '100%'},
                                     width=7, lg=7, xs=12
                            ),
                     dbc.Col(
                         html.Div(id='bar-chart-div',
                                  children=[
                                      dcc.Graph(id='bar-chart',
                                            figure=barchart
                                                )]
                                  ), style={'height': '100%'},
                                     width=5, lg=5, xs=12
                            )

                            ])

                    ])
                ])

#Populate the SOF Tribes options based on Service Branch dropdown
@app.callback(
    Output('Tribes', 'options'),
    Input('Branches', 'value')
)
def set_tribe_options(branch):
    tribes = vets[vets['Branch'].isin(branch)]['Tribe'].unique()
    return [{'label': tribe, 'value':tribe} for tribe in tribes]

#Populate intitial SOF Tribes options based on initial Service Branch DD option
@app.callback(
    Output('Tribes', 'value'),
    Input('Tribes', 'options')
)
def set_tribes_value(available_options):
    return [x['value'] for x in available_options]



if __name__ == "__main__":
    app.run_server(debug=True)