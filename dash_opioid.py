import os
import re
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from data_processing import scaler
#import cufflinks as cf

external_stylesheets = [dbc.themes.DARKLY]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}],)
server = app.server

#Load data
vets = pd.read_csv('data/merged_df_dash.csv')
#rescale sizing and set df for mapping
map_df = vets[vets['scaled'].notnull()]
bubble_sizes = scaler(map_df['scaled'], 4, 30)
#remove Coast Guard from dataset and create branch and tribe options
branches = vets['Branch'].unique()[:4]
tribes = vets['Tribe'].unique()



#drop down options
branch_options = [{'label': branch, 'value': branch} for branch in branches]
branch_options.append({'label': 'All', 'value': ''})
tribe_options = [{'label': tribe, 'value': tribe} for tribe in tribes]
tribe_options.append({'label': 'All', 'value': ''})

#Step 4. Create figure
fig = go.Figure(data=go.Scattergeo(
        locationmode = 'USA-states',
        lon = map_df['longitude'],
        lat = map_df['latitude'],
        text = map_df['text'],
        mode = 'markers',
        hoverinfo='text',
        marker = dict(
            size = bubble_sizes,
            opacity = 0.8,
            reversescale = False,
            autocolorscale = False,
            symbol = 'circle',
            line = dict(
                width=0.5,
                color='rgb(40,40,40)'
            ),
            colorscale = 'portland',
            cmin = 0,
            color = map_df['Combined'],
            cmax = map_df['Combined'].max(),
            colorbar_title="# of Members"
        )))

fig.update_layout(
        title = 'Elite Meet National Distribution',
        title_font_family='Garamond',
        title_font_size=40,
        title_x=0.5,
        title_y=0.9,
        geo = dict(
            scope='usa',
            projection_type='albers usa',
            showland = True,
            landcolor = "rgb(217, 217, 217)",
            #subunitcolor = "rgb(217, 217, 217)",
            #countrycolor = "rgb(217, 217, 217)",
            #countrywidth = 1.5,
            #subunitwidth = 1.5
        )
    )
app.layout = html.Div(id="root",
    children=[
        html.Div(id="header",
            children=[
                html.H1(children="Elite Meet National Distribution", style={'fontfamily':'Garamond'}),
                html.H2(
                    id="description",
                    children="Distribution of Elite Meet members based on Branch or Tribe affiliation",
                        ),
                    ],
                ),

        html.Div(id="app-container",
                 children=[
                html.Div(id="left-column",
                    children=[

                        html.Div(id="branch-drop-down",
                            children=[
                                html.P(
                                    id="bdd-text",
                                    children="Service Branch",
                                    ),
                                dcc.Dropdown(
                                    id='Branches',
                                    options=branch_options,
                                    value='None',
                                    # allows user to select multiple drop down options
                                    multi=True,
                                    # allows the user to remove all options
                                    clearable=True,
                                    style={'width': '40%', 'float': 'left',
                                           'background':'green'})
                                           #'display': 'inline-block'}),
                                     ],
                                ),

                        html.Div(id="tribe-drop-down",
                            children=[
                                html.P(
                                    id="tribe-text",
                                    children="Tribe",
                                    style={'margin-left:': '25%'}
                                      ),
                                dcc.Dropdown(
                                    id='Tribes',
                                    options=tribe_options,
                                    value='None',
                                    # allows user to select multiple drop down options
                                    multi=True,
                                    # allows the user to remove all options
                                    clearable=True,
                                    style={'width': '40%', 'margin-left':'25%',
                                           'background': 'blue'
                                           }),
                                      ]
                                 )]]]]]]]
                            ]),
                        html.Div(
                            id="map-container",
                            children=[
                                html.P(
                                    "Elite Meet National Distribution: Total {}".format(len(map_df)),
                                    id="map-title",
                                ),
                                dcc.Graph(
                                    id="em_dist",
                                    figure=fig,
                                    style={"height": 650, "width": 1000}),
                                # dict(
                                #  layout=dict(
                                #      autosize=True,),
                            ],
                        ),
                    ],
                ),
                dcc.Graph(id="selected-data",
                            figure=dict(
                                data=[dict(x=0, y=0)],
                                layout=dict(
                                    paper_bgcolor="#F4F4F8",
                                    plot_bgcolor="#F4F4F8",
                                    autofill=True,
                                    margin=dict(t=75, r=50, b=100, l=50),
                                ),
                            ),
                        ),
                    ],
                )

if __name__ == "__main__":
    app.run_server(debug=True)