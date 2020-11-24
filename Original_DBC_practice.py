import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
server = app.server

colors = {
    'background1': '#111111',
    'background2': '#008080',
    'text': '#7FDBFF'
}

app.layout = html.Div([
    html.Div(
    [
        dbc.Row(
            [
            dbc.Col(html.P('Col 1', style={'background':'grey'})),
            dbc.Col(html.P('Col 2', style={'background':'black'})),
            dbc.Col(html.P('Col 3', style={'background':'yellow'}))
            ]
        )
    ]),

    html.Div(
    [
        dbc.Row(
            [dbc.Col(html.Div("A single, half-width column",
                                 style={'background':'yellow'}), width=6),
            dbc.Col(html.Div("A second half-width column", style={'background':'green'}))
            ]
                ),
        dbc.Row(
            [
            dbc.Col(html.Div("An automatically sized column"),
                    style={'background':'green'}, width="auto"),
            dbc.Col(html.Div("And another automatically sized column"),
                    style={'background':'grey'}, width="auto")
             ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div("Branch Dropdown",
                                 style={'background':'yellow', 'fontFamily':'Garamond', 'color':colors['text'], 'height':40}),
                                 width=2),
                dbc.Col(html.Div("Tribe Dropdown",
                                 style={'background':'yellow', 'fontFamily':'Garamond', 'color':colors['text'], 'height':40}),
                                 width=2),
            ],  no_gutters=True, justify='center'
        ),
        dbc.Row(
            dbc.Col(html.Div("First Offset",
                             style={'background':'yellow', 'height':40}),
                             width={"size": 3, "offset": 1}),
                ),
        dbc.Row(
            dbc.Col(html.Div("2nd Offset",
                             style={'background':'yellow', 'height':40}),
                             width={"size": 3, "offset": 2}),
                ),
        dbc.Row(
            dbc.Col(html.Div("3rd Offset",
                             style={'background':'yellow', 'height':40}),
                             width={"size": 3, "offset": 3}),
                ),
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True)