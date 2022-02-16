from dash import Dash, html, dcc, Input, Output
import altair as alt
from gapminder import gapminder
import pandas as pd


cols = ['Life Expectancy', 'Population', 'GDP per Capita']
gapminder = gapminder.query('year == 2007')

app = Dash(__name__,  external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

app.layout = html.Div([
    html.Div('A little widget', style={'fontSize': 44}),
    html.P('This tool is to show the box plots of the Gapminder dataset in 2007 in the view of continents with different indicators including life expectancy, population, and GDP per capita.', style={'marginTop': 50}),
    dcc.Dropdown(
        id='xcol-widget',
        value='3',
        options=[{'label': col, 'value': count+3} for count, col in enumerate(cols)]),
    html.Iframe(
        id='box_plot',
        style={'border-width': '0', 'width': 1000, 'height': 500, 'marginTop': 50})
])


@app.callback(
    Output('box_plot', 'srcDoc'),
    Input('xcol-widget', 'value'))
def plot_altair(xcol):
    xcol = int(xcol)
    df = gapminder.groupby('continent').mean()
    df.sort_values(gapminder.columns[xcol], ascending=True, inplace=True)
    cont_order = df.index.tolist()
    chart = alt.Chart(gapminder).mark_boxplot(outliers=False).encode(
        x=alt.X(gapminder.columns[xcol], title=cols[xcol-3]),
        y=alt.Y('continent', title='Continent', sort=cont_order),
        color=alt.Color('continent', legend=None)
    ).interactive()
    return chart.to_html()


if __name__ == '__main__':
    app.run_server(debug=True)
