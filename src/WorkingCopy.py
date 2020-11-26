import dash
import os
import pandas as pd
from data_processing import scaler
from helper_functions import update_scatter_map
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
data_path = "/Users/americanthinker/DataScience/Projects/DataEngineering/Cap_Stone_II/data/"
vets = pd.read_csv(os.path.join(data_path, 'merged_df_dash.csv'))

#***Use map_df for mapping only!!!***
#rescale sizing and set df for mapping /
map_df = vets[vets['scaled'].notnull()]
map_df = map_df[map_df['Branch'] != 'Coast Guard']
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

branch_colors = ['blue', 'green', 'red', 'skyblue']

#create figure object for map
fig = go.Figure(go.Scattermapbox(
        mode='markers')
        )

fig.layout.update(
    autosize=False,
    width=1100, height=600, paper_bgcolor='green',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style='dark',
        center=dict(lat=38.7, lon=-98.5795),
        zoom=3.75),
    margin={'l':0, 'r':0, 'b':0, 't':0}
    )
#update future fig.layout.updates
def setScatLayout(fig):
    fig.update_layout(
        autosize=False,
        width=1100, height=600,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            style='light',
            center=dict(lat=38.7, lon=-98.5795),
            zoom=3.75),
    margin={'l':0, 'r':0, 'b':0, 't':0}
    )

#create figure object for bar graph
barchart = go.Figure(go.Bar())

barchart.update_layout(
    autosize=False,
    width=800,
    height=600,
    margin={'l':0, 'r':25, 'b':0, 't':0}
)

#fig.update_yaxes(automargin=True)

app.layout = html.Div(id='app-container',
    children = [
        html.Div(id='title-block',
            children =[
                dbc.Row(
                    [dbc.Col( width=7,
                        children=[
                            html.Label('Elite Meet National Distribution',
                                 style=dict(
                                 fontSize=30,
                                 fontFamily='Times',
                                 marginLeft='15px',
                                 marginTop='20px')
                                   ),
                            html.H5(
                                    id='left-description',
                                    children=[
                                        html.Ul("Filter search results by Service Branch of SOF Tribe.",
                                            style = dict(
                                            fontFamily='Times',
                                            color=colors['text'],
                                            marginLeft='15px')
                                              ),
                                        html.Li("Bubble size indicates size of population."),
                                        html.Li("Color is indicitave of service branch.")
                                            ]
                                    )]),
                    dbc.Col(width=dict(size=3, offset=9),
                            children=[
                                html.Div(html.Img(id='em-logo', style=dict(height='80px'),
                                         src=app.get_asset_url('EM-logo.svg')))
                                    ]
                            )
                     ])
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
                             fontFamily='Times',
                             marginLeft='15px')
                               ),
                    dcc.Dropdown(
                        id='Branches',
                        options=branch_selection,
                        value='Navy',
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
                                   fontFamily='Times',
                                   marginLeft='15px')
                               ),
                    dcc.Dropdown(
                        id='Tribes',
                        options=[],
                        style=dict(
                            marginBottom='15px'
                        ),
                        value=[],
                        # allows user to select multiple drop down options
                        multi=True,
                        # allows the user to remove all options
                        clearable=True,
                                )
                        ]
                    )
                ]
            ),

    html.Div(id='graph-container', style={'height':'60vh', 'background_color':'yellow'},
             children=[
                 dbc.Row([
                     dbc.Col(
                         html.Div(id='scatter-div', style={'height':'50vh'},
                                  children=[html.Div(id='internal-scatter-div',
                                                     style=dict(height='80vh'),
                                    children=[dcc.Graph(id='scatter-map',
                                              figure=fig,
                                              responsive=True,
                                              config=dict(
                                                  responsive=True
                                              )

                                             )]
                                                    )
                                           ]
                                  ), style={'height':'100%'},
                                     width=7, lg=7, xs=12
                            ),
                     dbc.Col(
                         html.Div(id='bar-chart-div',
                                  children=[
                                      dcc.Graph(id='bar-chart',
                                            figure=dict(
                                                data=[dict(x=0, y=0)],
                                                layout=dict(
                                                    paper_bgcolor="grey",
                                                    plot_bgcolor="grey",
                                                    autofill=True,
                                                    margin=dict(t=75, r=50, b=100, l=50)
                                                        ),

                                                    ),
                                            responsive=True,
                                                )
                                            ],
                                  ), style={'height': '100%', 'background-color':'grey'},
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

#Plot points on map based on input values

@app.callback(
    Output('scatter-map', 'figure'),
    Input('Branches', 'value'),
    Input('Tribes', 'value')
)
def update_map(selected_branches, selected_tribes):
    px.set_mapbox_access_token(mapbox_access_token)

    #if no tribes are selected return points grouped by Service Branch
    if len(selected_tribes) == 0:
        print(selected_branches)
        if isinstance(selected_branches, str):
            selected_branches = [selected_branches]
        temp = map_df[map_df['Branch'].isin(selected_branches)]
        points = temp.groupby(['Branch','latitude', 'longitude', 'CityState'])['Id'] \
            .count().to_frame().reset_index()
        #create text column for hover info
        points['text'] = points['CityState'] + ': ' + points['Id'].astype(str)
        points['Id'] = scaler(points['Id'], 4, 26)
        print(len(points))
        new_update = px.scatter_mapbox(points,
                       hover_name='text',
                       hover_data=dict(
                        Id=False,
                        latitude=False,
                        longitude=False
                       ),
                       opacity=0.7,
                       color='Branch',
                       color_discrete_map={
                           'Navy':'blue',
                           'Army':'green',
                           'Air Force':'skyblue',
                           'Marine Corps':'red'},
                       lat='latitude',
                       lon='longitude',
                       size='Id',
                       size_max=points['Id'].max()
                       )


        new_update.layout.update(showlegend=False,
                                 hoverlabel=dict(
                                     font_size=12,
                                     font_family='Times New Roman'
                                 ))
        return new_update
    else:
        if isinstance(selected_branches, str):
            selected_branches = [selected_branches]
        temp = map_df[(map_df['Branch'].isin(selected_branches))&(map_df['Tribe'].isin(selected_tribes))]
        print(temp.head())
        points = temp.groupby(['Branch', 'Tribe', 'latitude', 'longitude', 'CityState'])['Id'] \
            .count().to_frame().reset_index()
        points['text'] = points['CityState'] + ': ' + points['Id'].astype(str)
        print(points['text'].head())
        points['Id'] = scaler(points['Id'], 4, 26)
        print(len(points))

        new_update = px.scatter_mapbox(points,
                                       hover_name='text',
                                       hover_data=dict(
                                           Id=False,
                                           latitude=False,
                                           longitude=False
                                       ),
                                       opacity=0.7,
                                       color='Branch',
                                       color_discrete_map={
                                           'Navy': 'blue',
                                           'Army': 'green',
                                           'Air Force': 'skyblue',
                                           'Marine Corps': 'red'},
                                       lat='latitude',
                                       lon='longitude',
                                       size='Id',
                                       size_max=points['Id'].max()
                                       )


        new_update.layout.update(showlegend=False)
        return new_update


@app.callback(
    Output('bar-chart', 'figure'),
    Input('Branches', 'value'),
    Input('Tribes', 'value')
)
def update_bar(selected_branches, selected_tribes):
    if len(selected_tribes) == 0:
        print(selected_branches)
        if isinstance(selected_branches, str):
            selected_branches = [selected_branches]
        temp = vets[vets['Branch'].isin(selected_branches)]
        #transform dataframe into branch and values format for ease of use with px.bar
        chart_df = temp['Branch'].value_counts().to_frame().reset_index()
        chart_df.rename(columns={'Branch':'Count', 'index':'Branch'}, inplace=True)
        print(chart_df.head)

        bar_update = px.bar(chart_df,
                            x='Branch',
                            y='Count',
                            color='Branch',
                            hover_name='Count',
                            #hover_data={chart_df.index:False},
                            color_discrete_map={
                                'Navy': 'blue',
                                'Army': 'green',
                                'Air Force': 'skyblue',
                                'Marine Corps': 'red'},
                            text='Count',
                            )

        bar_update.update_layout(
            font_family='Balto',
            title=dict(text='Raw Count of Service Members', x=0.5),
            font=dict(size=18),
            titlefont_size=24,
            showlegend=False,
            height=600
        )
        bar_update.update_traces(
            marker_line=dict(
                        width=2.5,
                        color='black'),
            selector=dict(type='bar'))
        return bar_update

if __name__ == "__main__":
    app.run_server(debug=True)