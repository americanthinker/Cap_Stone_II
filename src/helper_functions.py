#modular functions used for various reasons for app.py to declutter the code
import plotly.express as px
from textwrap import wrap
import os

#initialize mapbox access token
mapbox_access_token = os.environ.get('MAPBOX_API_KEY')
px.set_mapbox_access_token(mapbox_access_token)

def update_scatter_map(fig):
    '''
    Updates scatter map (fig) with "update_layout" method
    '''
    fig.update_layout(
        showlegend=False,
        hoverlabel=dict(
            font_size=12,
            font_family='Times New Roman'),
        autosize=False,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            style='dark',
            #style='carto-positron',
            #set center as center of US
            center=dict(lat=38.7, lon=-98.5795),
            #set zoom to show entire US
            zoom=3.75),
    margin={'l':0, 'r':0, 'b':0, 't':0}
    )

def plot_points(data):
    '''
    Plots all points from input dataframe
    '''
    fig = px.scatter_mapbox(data,
                       hover_name='text',
                       hover_data=dict(
                        Id=False,
                        latitude=False,
                        longitude=False
                       ),
                       opacity=0.7,
                       color=data.columns[0],
                       color_discrete_map={
                           'Navy':'blue',
                           'Army':'green',
                           'Air Force':'skyblue',
                           'Marine Corps':'red'},
                       lat='latitude',
                       lon='longitude',
                       size='Id',
                       size_max=data['Id'].max(),
                       height=500
                       )
    return fig

def update_bar_chart(chart, chart_title=None, total_sum=None):
    '''
    Updates bar chart with "update layout" method
    '''
    update = chart.update_layout(
        font_family='Balto',
        title=dict(text=f'{chart_title}       Total = {total_sum}', x=0.5),
        font=dict(size=18, color='#7FDBFF'),
        titlefont_size=34,
        showlegend=False,
        paper_bgcolor="slategrey",
        plot_bgcolor="slategrey",
        #margin={'l': 0, 'r': 0, 'b': 0, 't': 0}
        margin=dict(t=75, r=50, b=100, l=50)
    )
    return update