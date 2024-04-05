import dash
from dash import dcc, html, Input, Output
import matplotlib.colors as mcolors
import plotly.express as px
import pandas as pd

shopping_df = pd.read_csv('shopping_trends_updated_copy.csv')
categorical_columns = shopping_df.select_dtypes(exclude=['number']).columns.tolist()
numeric_columns = shopping_df.select_dtypes(include=['number']).columns.tolist()

genders = shopping_df['Gender'].unique()
age_ranges = sorted(shopping_df['Age Range'].unique())

#Making a color map for charts involving the colors of purchased items
colors = shopping_df['Color'].unique().tolist()
colors.remove('Charcoal')
colors.remove('Peach')
color_mapping = {name: mcolors.CSS4_COLORS[name.lower()] for name in colors}
color_mapping.update({
    'Charcoal': 'rgb(54, 69, 79)',
    'Peach': 'rgb(255, 218, 185)'
})

options = ['Male', 'Female', 'Both']

#checklist1 = html.Div(className="child1_1_1", children=[dcc.Checklist(id='genders-checklist', options=genders, value=genders, inline=True)], style=dict(width="100%"))
checklist2 = html.Div(className="child1_1_1", children=[dcc.Checklist(id='ages-checklist', options=age_ranges, value=age_ranges, inline=True)], style=dict(width="100%"))
radio1 = html.Div(className='child1_1_1', children=[dcc.RadioItems(id='radio1', options=options, value=options[2], inline=True)], style=dict(width="100%"))

app = dash.Dash(__name__)

app.layout = html.Div(className="parent", children=[
    html.Div(className='row1', children=[html.P('Clothing Store Customer Info Dashboard')]),
    html.Div(className="row2",children=[
        html.Div([html.P("Select gender options:", style={'font-size': '18px', 'font-weight': 'bold'}), radio1],
                 className="child2_1"),
        html.Div([html.P("Select age options:", style={'font-size': '18px', 'font-weight': 'bold'}), checklist2],
                 className="child2_2"),
    ]),
    html.Div(className="row3",children=[
        html.Div(dcc.Graph(id='graph1'), className="child3_1"),
        html.Div(dcc.Graph(id='graph2'), className="child3_2")
    ]),
    html.Div(className="row4",children=[
        html.Div(dcc.Graph(id='graph3'), className="child4_1"),
        html.Div(dcc.Graph(id='graph4'), className="child4_2")
    ])
])

# Callback for Graph 1 (Pie chart showing subscription status)
@app.callback(
        Output('graph1', 'figure'),
        [Input('radio1', 'value'), Input('ages-checklist', 'value')]
)
def update_graph1(gender, age_range):
    if gender == 'Both':
        filtered_df = shopping_df[shopping_df['Age Range'].isin(age_range)]
    else:
        filtered_df = shopping_df[shopping_df['Gender']==gender][shopping_df['Age Range'].isin(age_range)]
    sub_df = filtered_df['Subscription Status'].value_counts().reset_index()
    sub_df.columns = ['Subscription', 'Count']
    desired_order = ['Yes', 'No']
    fig = px.pie(sub_df, values='Count', names='Subscription', color='Subscription', category_orders={'Subscription': desired_order},
                 color_discrete_map={'Yes': 'rgb(0, 163, 108)', 'No': 'rgb(215, 0, 64)'},
                 title='Subscription Status', hole=0.2)
    return fig

# Callback for Graph 2 (Bar chart showing colors of purchased items)
@app.callback(
        Output('graph2', 'figure'),
        [Input('radio1', 'value'), Input('ages-checklist', 'value')]
)
def update_graph2(gender, age_range):
    if gender == 'Both':
        filtered_df = shopping_df[shopping_df['Age Range'].isin(age_range)]
    else:
        filtered_df = shopping_df[shopping_df['Gender']==gender][shopping_df['Age Range'].isin(age_range)]
    color_df = filtered_df['Color'].value_counts().reset_index()
    color_df.columns = ['Color', 'Count']
    color_df['color_map'] = color_df.index.map(color_mapping)
    fig = px.bar(color_df, y='Count', x='Color', color='Color', color_discrete_map=color_mapping, title='Most Common Colors Purchased')
    fig.update_layout(xaxis_title='Color', yaxis_title='Frequency')
    fig.update_traces(showlegend=False)
    return fig

# Callback for Graph 3 (Pie chart showing seasons)
@app.callback(
        Output('graph3', 'figure'),
        [Input('radio1', 'value'), Input('ages-checklist', 'value')]
)
def update_graph3(gender, age_range):
    if gender == 'Both':
        filtered_df = shopping_df[shopping_df['Age Range'].isin(age_range)]
    else:
        filtered_df = shopping_df[shopping_df['Gender']==gender][shopping_df['Age Range'].isin(age_range)]
    season_df = filtered_df['Season'].value_counts().reset_index()
    season_df.columns = ['Season', 'Count']
    desired_order = ['Spring', 'Summer', 'Fall', 'Winter']
    fig = px.pie(season_df, values='Count', names='Season', color='Season', category_orders={'Season': desired_order},
                 color_discrete_map={'Spring': 'rgb(163,212,104)',
                                     'Summer': 'rgb(249,214,46)',
                                     'Fall': 'rgb(195,103,40)',
                                     'Winter': 'rgb(165,193,253)'},
                 title='Most Visited Seasons', hole=0.2)
    return fig

# Callback for Graph 4 (Bar chart showing item sizes)
@app.callback(
        Output('graph4', 'figure'),
        [Input('radio1', 'value'), Input('ages-checklist', 'value')]
)
def update_graph4(gender, age_range):
    if gender == 'Both':
        filtered_df = shopping_df[shopping_df['Age Range'].isin(age_range)]
    else:
        filtered_df = shopping_df[shopping_df['Gender']==gender][shopping_df['Age Range'].isin(age_range)]
    size_df = filtered_df['Size'].value_counts().reset_index()
    size_df.columns = ['Size', 'Count']
    desired_order = ['S', 'M', 'L', 'XL']
    fig = px.bar(size_df, y='Count', x='Size', category_orders={'Size': desired_order}, title='Most Common Sizes Purchased')
    fig.update_layout(xaxis_title='Size', yaxis_title='Frequency')
    fig.update_traces(showlegend=False)
    return fig

# For local
# if __name__ == '__main__':
#     app.run_server(debug=True)

# For AWS
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=False)
