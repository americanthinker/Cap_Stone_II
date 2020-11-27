import dash
import os
import pandas as pd
import json
from data_processing import scaler
from helper_functions import update_scatter_map, update_bar_chart, plot_points
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px

#launch app, using  __name__ for deployment and SLATE style theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE], meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=3'}])
server = app.server

#initialize mapbox access through API
mapbox_access_token = os.environ.get('MAPBOX_API_KEY')
px.set_mapbox_access_token(mapbox_access_token)

#Load data
data_path = "/Users/americanthinker/DataScience/Projects/DataEngineering/Cap_Stone_II/data/"
vets = pd.read_csv(os.path.join(data_path, 'merged_df_dash.csv'))

#***Use map_df for mapping only!!!***
#rescale sizing and set df for mapping /
map_df = vets[vets['scaled'].notnull()]
map_df = map_df[map_df['Branch'] != 'Coast Guard']

#bubble_sizes = scaler(map_df['scaled'], 4, 26)

#reate branch and tribe options
branches = map_df['Branch'].unique()
tribes = map_df['Tribe'].unique()
branch_selection = [{'label':val, 'value':val} for val in branches]
tribe_selection = [{'label':val, 'value':val} for val in tribes]

#set color scheme
colors = {
    'background1': '#111111',
    'background2': '#008080',
    'text': '#7FDBFF'}
branch_colors = ['blue', 'green', 'red', 'skyblue']

#create figure object for map
map_fig = go.Figure(go.Scattermapbox(mode='markers'))
update_scatter_map(map_fig)
#fig.update_yaxes(automargin=True)

#create figure object for bar graph
barchart = go.Figure(go.Bar())
update_bar_chart(barchart, None)

#HTML structure for app
app.layout = html.Div(id='app-container',
    children = [
                dbc.Row(
#Title and header block
                    [dbc.Col(width=7,
                        children=[
                            html.H2(id='title',
                                 children='Elite Meet National Distribution',
                                 style=dict(
                                 fontSize=34,
                                 fontFamily='Times',
                                 marginLeft='15px',
                                 marginTop='20px')
                                   ),
                            html.H5(id='left-description',
                                    children=[
                                        html.Ul("Filter search results by Service Branch or SOF Tribe.",
                                            style = dict(
                                            fontFamily='Times',
                                            color=colors['text'],
                                            marginLeft='15px')
                                              ),
                                        html.Li("Bubble size indicates size of population.",
                                                style=dict(marginLeft='15px',
                                                           fontFamily='Times')
                                                ),
                                        html.Li("Color is indicitave of service branch.",
                                                style=dict(marginLeft='15px',
                                                           fontFamily='Times')
                                                ),
                                            ]
                                    )]),
#Elite Meet logo block
                    dbc.Col(width=5,
                            children=[
                                html.Div(html.Img(id='em-logo', style=dict(height='20%', marginLeft='65%', marginTop=20),
                                         src=app.get_asset_url('EM-logo.svg')))
                                    ]
                            )
                     ]
                 ),
#Drop down menu row
    dbc.Row(id='dropdowns',
        children=[
            dbc.Col(id='branch-dropdown',
                    width=3,
                children=[
                    html.Label('Service Branch',
                             style=dict(
                             fontSize=24,
                             fontFamily='Times',
                             marginLeft='20px')
                               ),
                    dcc.Dropdown(
                        id='Branches',
                        style=dict(marginLeft='10px'),
                        options=branch_selection,
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
#scatter map block
    html.Div(id='graph-container',
             children=[
                 dbc.Row([
                     dbc.Col(width=7,
                            children=html.Div(id='scatter-div', style=dict(marginLeft='20px', ),
                                           children=dcc.Graph(id='scatter-map',
                                                    figure=map_fig,
                                                    style=dict(height='60vh'),
                                                    responsive=True)
                                           )
                             ),
#bar chart block
                     dbc.Col(width=5,
                             children=html.Div(id='bar-chart-div',
                                  children=dcc.Graph(id='bar-chart',
                                                 style=dict(height='60vh'),
                                                 figure=barchart,
                                                 responsive=True)
                                               )
                            )

                            ])

                    ])
                ])
"""
#Populate the SOF Tribes options based on Service Branch dropdown
@app.callback(
    Output('Tribes', 'options'),
    Input('Branches', 'value')
)
def set_tribe_options(branch):
    if isinstance(branch, str):
        branch = [branch]
    tribes = vets[vets['Branch'].isin(branch)]['Tribe'].unique()
    return [{'label': tribe, 'value':tribe} for tribe in tribes]

#Populate intitial SOF Tribes options based on initial Service Branch DD option
@app.callback(
    Output('Tribes', 'value'),
    Input('Tribes', 'options')
)
def set_tribes_value(available_options):
    return [x['value'] for x in available_options]
"""
#Plot points on map based on input values
@app.callback(
    Output('scatter-map', 'figure'),
    Input('Branches', 'value'),
    #Input('Tribes', 'value')
)
def update_map(selected_branches):
    px.set_mapbox_access_token(mapbox_access_token)

    #return plotted points grouped by Service Branch
    # *** Make sure to include "selected_tribes" asn an option when going back ***
    if isinstance(selected_branches, str):
        selected_branches = [selected_branches]
    temp = map_df[map_df['Branch'].isin(selected_branches)]
    points = temp.groupby(['Branch','latitude', 'longitude', 'CityState'])['Id'] \
        .count().to_frame().reset_index()
    #create text column for hover info
    points['text'] = points['CityState'] + ': ' + points['Id'].astype(str)
    points['Id'] = scaler(points['Id'], 4, 26)

    #call helper functions to update points on map
    new_map_update = plot_points(points)
    update_scatter_map(new_map_update)

    return new_map_update

"""
    else:
        if isinstance(selected_branches, str):
            selected_branches = [selected_branches]
        temp = map_df[(map_df['Branch'].isin(selected_branches))&(map_df['Tribe'].isin(selected_tribes))]
        points = temp.groupby(['Branch', 'Tribe', 'latitude', 'longitude', 'CityState'])['Id'] \
            .count().to_frame().reset_index()
        points['text'] = points['CityState'] + ': ' + points['Id'].astype(str)
        points['Id'] = scaler(points['Id'], 4, 26)

        # call helper functions to update points on map
        new_map_update = plot_points(points)
        update_scatter_map(new_map_update)

        return new_map_update
"""
@app.callback(
    Output('title', 'children'),
    Input('scatter-map', 'hoverData'))
def display_click_data(hoverData):
    if hoverData is None:
        return 'San Diego, California'
    else:
        print(json.dumps(hoverData))
        location = hoverData['points'][0]['hovertext'].split(':')[0]
        return html.P(location)


# plot bars based on plotted points on map
@app.callback(
    Output('bar-chart', 'figure'),
    Input('scatter-map', 'hoverData')
)
def update_bar(hoverData):
    if hoverData is None:
        location = "San Diego, California"
        temp_df = map_df[map_df['CityState'] == location]
        chart_df = temp_df['Branch'].value_counts().to_frame().reset_index()
        chart_df.rename(columns={'Branch': 'Count', 'index': 'Branch'}, inplace=True)

        new_bar_update = px.bar(chart_df,
                                x='Branch',
                                y='Count',
                                hover_name='Count',
                                # hover_data={chart_df.index:False},
                                color='Branch',
                                color_discrete_map={
                                    'Navy': 'blue',
                                    'Army': 'green',
                                    'Air Force': 'skyblue',
                                    'Marine Corps': 'red'},
                                text='Count',
                                )
        update_bar_chart(new_bar_update, location)
        return new_bar_update

    else:
        location = hoverData['points'][0]['hovertext'].split(':')[0]
        temp_df = map_df[map_df['CityState'] == location]
        # transform dataframe into branch and values format for ease of use with px.bar
        chart_df = temp_df['Branch'].value_counts().to_frame().reset_index()
        chart_df.rename(columns={'Branch': 'Count', 'index': 'Branch'}, inplace=True)

        new_bar_update = px.bar(chart_df,
                                x='Branch',
                                y='Count',
                                hover_name='Count',
                                # hover_data={chart_df.index:False},
                                color='Branch',
                                color_discrete_map={
                                    'Navy': 'blue',
                                    'Army': 'green',
                                    'Air Force': 'skyblue',
                                    'Marine Corps': 'red'},
                                text='Count',
                                )
        update_bar_chart(new_bar_update, location)
        return new_bar_update




if __name__ == "__main__":
    app.run_server(debug=True)