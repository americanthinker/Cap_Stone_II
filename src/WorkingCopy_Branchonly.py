import dash
import os
import pandas as pd
import json
from data_processing import scaler
from helper_functions import update_scatter_map, update_bar_chart, plot_points
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_daq as daq
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
vets = pd.read_csv(os.path.join(data_path, 'updated_pilots.csv'))
table_df = vets['Branch'].value_counts()[:4].to_frame().T
table_df['Total'] = table_df.sum(axis=1)

#***Use map_df for mapping only!!!***
#rescale sizing and set df for mapping /
map_df = vets[vets['scaled'].notnull()]
map_df = map_df[map_df['CityState'] != 'NC, NC']
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
update_bar_chart(barchart)

#HTML structure for app
app.layout = html.Div(id='app-container',
    children = [
                dbc.Row(
#Title and header block
                    [dbc.Col(width=4, style=dict(marginLeft='30px'),
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
                    dbc.Col(width=3,
                            children=[
                                html.Img(id='em-logo', #style=dict(height='20%', marginLeft='65%', marginTop=20),
                                         src=app.get_asset_url('em-logo.png'))
                                    ]
                            ),
                     dbc.Col(width=4, id='data-table', align='baseline',
                        children=[
                                html.H2('Service Branch Total Counts',
                                        style=dict(fontFamily='Balto',
                                                   marginTop=40,
                                                   textAlign='center')),
                                dbc.Table.from_dataframe(table_df,
                                             striped=True,
                                             style=dict(fontFamily='Balto',
                                                        textAlign='center',
                                                        fontSize=20
                                                        ),
                                             dark=True,
                                             responsive=True,
                                             bordered=True,
                                             hover=True)
                             ]
                             )
                     ]
                 ),
#Branch dropdown
    dbc.Row(id='dropdowns',
        children=[
            dbc.Col(id='branch-dropdown', style=dict(marginLeft='25px'),
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
                        value=['Navy', 'Army', 'Marine Corps', 'Air Force'],
                        # allows user to select multiple drop down options
                        multi=True,
                        clearable=True
                        # allows the user to remove all options
                        #placeholder='Select a Service Branch...',
                                )
                        ]
                    )
                ]
            ),
#scatter map block
    html.Div(id='graph-container', style=dict(marginLeft='25px'),
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
                             children=html.Div(id='bar-chart-div', style=dict(marginRight='25px'),
                                  children=dcc.Graph(id='bar-chart',
                                                 style=dict(height='60vh'),
                                                 figure=barchart,
                                                 responsive=True)
                                               )
                            )

                            ])

                    ]),

#Tribe dropdown
    dbc.Row(id='dropdown-2',
        children=[
            dbc.Col(id='tribe-dropdown', width=dict(size=3), style=dict(marginTop='25px', marginLeft='25px'),
                children=[
                    html.Label('SOF Tribe',
                               style=dict(
                                   fontSize=24,
                                   fontFamily='Times',
                                   marginLeft='20px')
                               ),
                    dcc.Dropdown(
                        id='Tribes',
                        options=tribe_selection,
                        style=dict(
                            marginLeft='10px'),
                        value=['SEAL', 'Green Beret'],
                        # allows user to select multiple drop down options
                        multi=True,
                        # allows the user to remove all options
                        clearable=True,
                                )
                        ]
                    )
                ]
            ),

#Tribe scatter map block
    html.Div(id='graph-container-2', style=dict(marginLeft='25px'),
             children=[
                 dbc.Row([
                     dbc.Col(width=7,
                            children=html.Div(id='scatter-div-2', style=dict(marginLeft='20px', ),
                                           children=dcc.Graph(id='scatter-map-2',
                                                    figure=map_fig,
                                                    style=dict(height='60vh'),
                                                    responsive=True)
                                           )
                             ),
#Tribe bar chart block
                     dbc.Col(width=5,
                             children=html.Div(id='bar-chart-div-2', style=dict(marginRight='25px'),
                                  children=dcc.Graph(id='bar-chart-2',
                                                 style=dict(height='60vh'),
                                                 figure=barchart,
                                                 responsive=True)
                                               )
                            )

                            ])

                    ])
                ])

#Plot points on map based on input values
@app.callback(
    Output('scatter-map', 'figure'),
    Input('Branches', 'value')
)
def update_map(selected_branches):
    if selected_branches is None:
        raise PreventUpdate
    elif len(selected_branches) == 0:
        return map_fig
    else:
        px.set_mapbox_access_token(mapbox_access_token)
        if isinstance(selected_branches, str):
            selected_branches = [selected_branches]
            temp = map_df[map_df['Branch'].isin(selected_branches)]
            points = temp.groupby(['Branch', 'latitude', 'longitude', 'CityState'])['Id'] \
                .count().to_frame().reset_index()
            # create text column for hover info
            points['text'] = points['CityState'] + ': ' + points['Id'].astype(str)
            points['Id'] = scaler(points['Id'], 4, 26)

            # call helper functions to update points on map
            new_map_update = plot_points(points)
            update_scatter_map(new_map_update)
            return new_map_update

        else:
            print(selected_branches)
            temp = map_df[map_df['Branch'].isin(selected_branches)]
            points = temp.groupby(['Branch', 'latitude', 'longitude', 'CityState'])['Id'] \
                .count().to_frame().reset_index()
            # create text column for hover info
            points['text'] = points['CityState'] + ': ' + points['Id'].astype(str)
            points['Id'] = scaler(points['Id'], 4, 26)

            # call helper functions to update points on map
            new_map_update = plot_points(points)
            update_scatter_map(new_map_update)

            return new_map_update

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
        total_sum = chart_df['Count'].sum()

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
        update_bar_chart(new_bar_update, location, total_sum)
        new_bar_update.update_traces(
            marker_line=dict(
                width=2.5,
                color='black'),
            selector=dict(type='bar'))
        return new_bar_update

    else:
        location = hoverData['points'][0]['hovertext'].split(':')[0]
        temp_df = map_df[map_df['CityState'] == location]
        # transform dataframe into branch and values format for ease of use with px.bar
        chart_df = temp_df['Branch'].value_counts().to_frame().reset_index()
        chart_df.rename(columns={'Branch': 'Count', 'index': 'Branch'}, inplace=True)
        total_sum = chart_df['Count'].sum()

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
        update_bar_chart(new_bar_update, location, total_sum)
        new_bar_update.update_traces(
            marker_line=dict(
                width=2.5,
                color='black'),
            selector=dict(type='bar'))
        return new_bar_update

@app.callback(
    Output('scatter-map-2', 'figure'),
    Input('Tribes', 'value')
)
def update_map(selected_tribes):
    if selected_tribes is None:
        raise PreventUpdate
    elif len(selected_tribes) == 0:
        return map_fig
    else:
        px.set_mapbox_access_token(mapbox_access_token)
        if isinstance(selected_tribes, str):
            selected_branches = [selected_tribes]
            temp = map_df[map_df['Tribe'].isin(selected_tribes)]
            points = temp.groupby(['Branch', 'Tribe', 'latitude', 'longitude', 'CityState'])['Id'] \
                .count().to_frame().reset_index()
            # create text column for hover info
            points['text'] = points['CityState'] + ': ' + points['Id'].astype(str)
            points['Id'] = scaler(points['Id'], 4, 26)

            # call helper functions to update points on map
            new_map_update = plot_points(points)
            update_scatter_map(new_map_update)
            return new_map_update

        else:
            print(selected_tribes)
            temp = map_df[map_df['Tribe'].isin(selected_tribes)]
            points = temp.groupby(['Branch', 'Tribe', 'latitude', 'longitude', 'CityState'])['Id'] \
                .count().to_frame().reset_index()
            # create text column for hover info
            points['text'] = points['CityState'] + ': ' + points['Id'].astype(str)
            points['Id'] = scaler(points['Id'], 4, 26)

            # call helper functions to update points on map
            new_map_update = plot_points(points)
            update_scatter_map(new_map_update)

            return new_map_update

@app.callback(
    Output('bar-chart-2', 'figure'),
    Input('scatter-map-2', 'hoverData')
)
def update_bar(hoverData):
    if hoverData is None:
        location = "San Diego, California"
        temp_df = map_df[map_df['CityState'] == location]
        chart_df = temp_df.groupby(['Branch', 'Tribe'])['Id'].count().reset_index()
        chart_df.rename(columns={'Id': 'Count'}, inplace=True)
        chart_df = chart_df.sort_values('Count', ascending=False)
        total_sum = chart_df['Count'].sum()

        new_bar_update = px.bar(chart_df,
                                x='Tribe',
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
        update_bar_chart(new_bar_update, location, total_sum)
        new_bar_update.update_traces(
            marker_line=dict(
                width=2.5,
                color='black'),
            selector=dict(type='bar'))
        return new_bar_update

    else:
        location = hoverData['points'][0]['hovertext'].split(':')[0]
        temp_df = map_df[map_df['CityState'] == location]
        chart_df = temp_df.groupby(['Branch', 'Tribe'])['Id'].count().reset_index()
        chart_df.rename(columns={'Id': 'Count'}, inplace=True)
        chart_df = chart_df.sort_values('Count', ascending=False)
        total_sum = chart_df['Count'].sum()

        new_bar_update = px.bar(chart_df,
                                x='Tribe',
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
        update_bar_chart(new_bar_update, location, total_sum)
        new_bar_update.update_traces(
            marker_line=dict(
                width=2.5,
                color='black'),
            selector=dict(type='bar'))
        return new_bar_update





if __name__ == "__main__":
    app.run_server(debug=True)

'''



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
'''