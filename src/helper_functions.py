#modular functions used for various reasons for app.py to declutter the code
import plotly.express as px

#initialize mapbox access token
mapbox_access_token = "pk.eyJ1IjoiYW1lcmljYW50aGlua2VyIiwiYSI6ImNraGx5ZXlvYjBrMjEyd285bjJkMDloeDYifQ.kGUzdL3-USJ46CGJUTBQqQ"
px.set_mapbox_access_token(mapbox_access_token)


def update_scatter_map(fig):
    '''
    Updates scatter map (fig) with "update_layout" method
    '''
    fig.update_layout(
        autosize=False,
        width=1100, height=600,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            style='light',
            #set center as center of US
            center=dict(lat=38.7, lon=-98.5795),
            #set zoom to show entire US
            zoom=3.75),
    margin={'l':0, 'r':0, 'b':0, 't':0}
    )