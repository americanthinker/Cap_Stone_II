import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

app = dash.Dash()

gapminder = px.data.gapminder().query("year == 2007")
mapfig = px.scatter_geo(gapminder,
                        locations="iso_alpha",
                        hover_name="country",
                        size="pop")
app.layout = html.Div([
    dcc.Graph(
        id='country-selector',
        figure=mapfig,
    ),
], className="container")

@app.callback(
    dash.dependencies.Output('country-selector', 'figure'),
    [dash.dependencies.Input('country-selector', 'hoverData')],
    [dash.dependencies.State('country-selector', 'figure')]
)
def drawStockPrice(hover_data, figure):
    data = figure['data']
    layout = figure['layout']

    if hover_data is not None:
        print('Country:', hover_data['points'][0]['hovertext'])

    return {'data': data, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)