import dash
import dash_table
#from dash import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd

version = 5.131
user_id = 221798572
access_token = 'vk1.a.xDs_ufGKW1NmEa3U64YhcFjCIWryZ8p3_rmdlnNDGnNp-B8_lWAB8JafdkjqxFcxx7ePbdkuX1LtFQFwT4WGRC9ifMlXCPbUa1wJSEpYWDDXvRAkX1FtAL_b1HjDOw9Jz2-OCo4gaZL2SIrCgAwM8fxKuXIRwmxxAq2bx6TOWkGq4zLtxmpmWEejpdyEPcXVEP-lGPx7j8DGz4vFyg4ytQ'

dataset = pd.read_csv('vk_dataset.csv')

def get_dataset():
    dataset['interest'] = dataset['interest'].astype(int)
    return dataset


def save_dataset(path, df):
    dataset.to_csv(path, index=False)


app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children='Dataset App', style={'textAlign': 'center'}),
        html.Div(
            children=[
                dcc.Input(id='input_url', placeholder='Enter URL here...',
                          value=None, type='text',
                          style={'width': '70%', 'textAlign': 'center', 'fontSize': '15px'}),
                dcc.Dropdown(options=[{'label': interest, 'value': interest} for interest in dataset['Interest'].unique()],
                             id='dropdown_selection',
                             placeholder="Select a category",
                             style={'width': '30vH', 'height': '40px', 'fontSize': '15px'}),
                html.Button('Save', id='button', n_clicks=0,
                            style={'width': '30vH', 'height': '40px', 'fontSize': '15px'})
            ],
            style=dict(display='flex', justifyContent='center')),
        html.Div(
            children=[
                dash_table.DataTable(
                    id='table',
                    columns=[{
                        'name': dataset.columns[i],
                        'id': dataset.columns[i]
                    } for i in range(len(dataset.columns))],
                    data=[
                        {dataset.columns[i]: dataset.values[j][i] for i in range(len(dataset.columns))}
                        for j in range(-10, 0)
                    ],
                    style_table={'overflowX': 'scroll'},
                )
            ],
            style={'width': '100%'}
        )
    ],
)

@app.callback(
    Output('table', 'data'),
    [Input('button', 'n_clicks')],
    [State('input_url', 'value'),
     State('dropdown_selection', 'value')]
)
def search_urls(n_clicks, input_url, selected_category):
    filtered_data = dataset.copy()
    if input_url:
        filtered_data = filtered_data[filtered_data['ID'].str.contains(input_url)]
        filtered_data_index = filtered_data.index.tolist()
        if len(filtered_data_index) > 0:
            first_index = filtered_data_index[0]
            filtered_data = filtered_data.iloc[first_index - 9: first_index + 1]
    if selected_category:
        filtered_data = filtered_data[filtered_data['Interest'] == selected_category]
    return [
        {filtered_data.columns[i]: filtered_data.values[j][i] for i in range(len(filtered_data.columns))}
        for j in range(-10, 0)
    ]

if __name__ == '__main__':
    app.run_server(debug=True)
