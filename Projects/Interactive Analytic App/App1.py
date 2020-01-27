#-*- coding:utf-8 -*-
## IMPORT PACKAGES

# dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_table.FormatTemplate as FormatTemplate
from dash.dependencies import Input, Output
from dash_table.Format import Format, Scheme, Sign, Symbol

# plotly
import plotly.graph_objs as go
import plotly.express as px

# data wrangling
import pandas as pd

###################################################################################################################
## DATA READ

df = pd.read_csv('D:/Users/BKU/SteffenKnoedler/Desktop/dash/data.csv')

df_mengen_kosten = pd.read_csv('D:/Users/BKU/SteffenKnoedler/Desktop/dash/data_kosten.csv')

###################################################################################################################
################# DATA WRANGLING (TAB 1)

df['Monat_Abrechnung']= pd.to_datetime(df['Monat_Abrechnung']) # transform to datetime type
df_00 = df['Monat_Abrechnung'].dt.year # get only year
df_01 = pd.DataFrame(df_00) # put it into DataFrame
df_01.columns = ['Jahr'] # Rename column
df = pd.concat([df, df_01], axis=1, sort=False) # merge both columns


# AGGREGATED DataFrame: df1
data = df.drop(columns="Bauart")
df1 = data.groupby(['Monat_Abrechnung', 'IH_Kategorie', 'Jahr'], as_index=False).sum()

# COSTS Per IH_Kategorie for each month & year
pt = df1.pivot_table(values='summe_nettowert', index='Monat_Abrechnung', columns='IH_Kategorie', aggfunc='sum', fill_value=0)
df2 = pd.DataFrame(pt)
df2.reset_index(level=0, inplace=True)
df2.index.names = ['Index']
df_02 = df2['Monat_Abrechnung'].dt.year #extract year
df_03 = pd.DataFrame(df_02)
df_03.columns = ['Jahr']
df2 = pd.concat([df2, df_03], axis=1, sort=False) #add column year


################# DATA WRANGLING (TAB 2)
df_mengen_kosten['Datum_Abrechnung']= pd.to_datetime(df_mengen_kosten['Datum_Abrechnung'])
df_mengen_kosten_year = df_mengen_kosten['Datum_Abrechnung'].dt.year #extract year
df_mengen_kosten_year_df = pd.DataFrame(df_mengen_kosten_year)
df_mengen_kosten_year_df.columns = ['Jahr']
df_mengen_kosten_1 = pd.concat([df_mengen_kosten, df_mengen_kosten_year_df], axis=1, sort=False)





###################################################################################################################

# css file for design
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


###################################################################################################################
## GET UNIQUE NAMES FOR DROPDOWN

Bauart_name = df['Bauart'].unique()
Bauart_name_li = ['Alle Bauarten']
for i in Bauart_name:
    Bauart_name_li.append(i)



IH_Kategorie_name = sorted(df['IH_Kategorie'].unique())

Table_columns = ['Gesamtkosten']
for i in IH_Kategorie_name:
    Table_columns.append(i)

year_selected = [df2['Monat_Abrechnung'].dt.year.min(), df2['Monat_Abrechnung'].dt.year.max()]

Table2_columns = ['Produkt_SAP', 'Datum_Abrechnung', 'Bauart', 'Menge', 'Jahr', 'Nettowert']

###################################################################################################################

## FUNCTIONS


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

###################################################################################################################

## APP DESIGN


app.layout = html.Div([

## TAB 2

    dcc.Tabs([
        dcc.Tab(label='Übersicht Instandhaltungskosten', children=[
            #Add markdown text as header
            dcc.Markdown('''
            ## Dashboard by Steffen Knödler
            '''),

            #Add add dropdown
            html.Div([
                dcc.Dropdown(
                    id='Button-Bauart',
                    options=[{'label': i, 'value': i} for i in Bauart_name_li],
                    searchable=True,
                    value=['Alle Bauarten'],
                    multi=True
                            ),
            ],
            # style of Dropdown:
            style={'width': '25%', 'display': 'inline-block'}),

            # Create another division for the graph
            html.Div([

                # Graph
                dcc.Graph(
                    id='Instandhaltungskosten',
                    figure={
                        'data': [
                            dict(
                                x=df2['Monat_Abrechnung'],
                                y=df2[str(i)],
                                mode='none',
                                stackgroup='one',
                                name=i
                                ) for i in df.IH_Kategorie.unique()
                                ],
                        'layout': dict(
                            legend={'x': 0, 'y': 1},
                            xaxis={'title': 'Jahr'},
                            yaxis={'title': 'Nettowert'},
                            title="Übersicht Instandhaltungskosten"
                            )}
                        ),
                        ], style={'width': '92%', 'margin-left': 'auto', 'margin-right': 'auto'}),

            # Create another division for the slider
            html.Div([

                dcc.RangeSlider(
                    id='slider',
                    min=df2['Monat_Abrechnung'].dt.year.min(),
                    max=df2['Monat_Abrechnung'].dt.year.max(),
                    value=[df2['Monat_Abrechnung'].dt.year.min(), df2['Monat_Abrechnung'].dt.year.max()],
                    marks={str(date): str(date) for date in df2['Monat_Abrechnung'].dt.year.unique()},
                    step=None
                )],
                style={'width': '85%', 'margin-left': 'auto', 'margin-right': 'auto'}),

            html.Div([
            dash_table.DataTable(
                id='table1',
                columns=[
                    {"name": i, "id": i, 'type': 'numeric',
                'format': Format(
                    group=',',
                    precision=0,
                    scheme=Scheme.fixed,
                    symbol=Symbol.yes,
                    symbol_suffix=u'€'
                )} for i in Table_columns
                ]
            )],
            style={'width': '80%', 'padding-top': '4%', 'margin-left': 'auto', 'margin-right': 'auto'})
    ]),

###################################################################################################################

## TAB 2


    dcc.Tab(label='Kosten- und Mengentreiber', children=[
        #Add markdown text as header
        dcc.Markdown('''
        ## Dashboard by Steffen Knödler
        '''),

        #Add add dropdown
        html.Div([
            dcc.Dropdown(
                id='Button-Bauart-Tab2',
                options=[{'label': i, 'value': i} for i in Bauart_name_li],
                searchable=True,
                value=['Alle Bauarten'],
                multi=True
                        ),
        ],
        # style of Dropdown:
        style={'width': '25%', 'display': 'inline-block'}),



        html.Div([
        dash_table.DataTable(
            id='table2',
            columns=[
                {"name": i, "id": i, 'type': 'numeric',
            'format': Format(
                group=',',
                precision=0,
                scheme=Scheme.fixed
            )} for i in Table2_columns
            ]
        )],
        style={'width': '80%', 'padding-top': '4%', 'margin-left': 'auto', 'margin-right': 'auto'}),


        html.Div([

            dcc.RangeSlider(
                id='slider-Tab2',
                min=df2['Monat_Abrechnung'].dt.year.min(),
                max=df2['Monat_Abrechnung'].dt.year.max(),
                value=[df2['Monat_Abrechnung'].dt.year.min(), df2['Monat_Abrechnung'].dt.year.max()],
                marks={str(date): str(date) for date in df2['Monat_Abrechnung'].dt.year.unique()},
                step=None
            )],
            style={'width': '85%', 'padding-top': '3%', 'margin-left': 'auto', 'margin-right': 'auto'})
        ]



    ),
    ])



]) #close entire app layout


###################################################################################################################

## INTERACTION FOR TABLE (TAB1)

@app.callback( #each callback is assigned to a function
    Output('table1', 'data'),
    [Input('Button-Bauart', 'value'),
    Input('slider', 'value')])

def update_table(selected_Bauart, year_value):

    if len(selected_Bauart) == 0 or 'Alle Bauarten' in selected_Bauart:
        data_0 = df.drop(columns="Bauart")
    else:
        filtered_df0 = df[df.Bauart.isin(selected_Bauart)]
        data_0 = filtered_df0.drop(columns="Bauart")


    df_0 = data_0.groupby(['Monat_Abrechnung', 'IH_Kategorie'], as_index=False).sum()
    pt_0 = df_0.pivot_table(values='summe_nettowert', index='Monat_Abrechnung', columns='IH_Kategorie', aggfunc='sum', fill_value=0)
    df_01 = pd.DataFrame(pt_0)
    df_01.reset_index(level=0, inplace=True)
    df_01.index.names = ['Index']
    df_01['Monat_Abrechnung']= pd.to_datetime(df_01['Monat_Abrechnung'])

    df_04 = df_01['Monat_Abrechnung'].dt.year #extract year
    df_04 = pd.DataFrame(df_04)
    df_04.columns = ['Jahr']
    df_001 = pd.concat([df_01, df_04], axis=1, sort=False)

    # AGGREGATED TABLE: Monat_Abrechnung - BNI - BNI mobil - Frist - Revision - SoArb - Jahr
    dff2_year = df_001[(df_001['Jahr'] >= year_value[0]) & (df_001['Jahr'] <= year_value[1])]

    df_table = pd.DataFrame(dff2_year.iloc[:,1:6].sum()).T.round()
    df_table.loc[:,'Gesamtkosten'] = df_table.sum(axis=1)
    cols = df_table.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df_table = df_table[cols]

    return df_table.to_dict('records')


## INTERACTION FOR GRAPH

@app.callback(
    Output('Instandhaltungskosten', 'figure'),
    [Input('Button-Bauart', 'value'),
    Input('slider', 'value')])

def update_figure(selected_Bauart, year_value):

    # TABLE: Monat_Abrechnung - Bauart - IH_Kategorie - summe_nettowert - Jahr
    dff_year = df[(df['Jahr'] >= year_value[0]) & (df['Jahr'] <= year_value[1])]

    # AGGREGATED TABLE: Monat_Abrechnung - BNI - BNI mobil - Frist - Revision - SoArb - Jahr
    dff2_year = df2[(df2['Jahr'] >= year_value[0]) & (df2['Jahr'] <= year_value[1])]

    if len(selected_Bauart) == 0 or 'Alle Bauarten' in selected_Bauart:
        return {
            'data': [
                dict(
                    x=dff2_year['Monat_Abrechnung'],
                    y=dff2_year[str(i)],
                    mode='none',
                    stackgroup='one',
                    name=i
                ) for i in df.IH_Kategorie.unique()
                ],
                'layout': dict(
                    legend={'x': 0, 'y': 1},
                    xaxis={'title': 'Jahr'},
                    yaxis={'title': 'Nettowert'},
                    title="Übersicht Instandhaltungskosten"
                )}

    else:
        filtered_df0 = df[df.Bauart.isin(selected_Bauart)]
        data_0 = filtered_df0.drop(columns="Bauart")
        df_0 = data_0.groupby(['Monat_Abrechnung', 'IH_Kategorie'], as_index=False).sum()
        pt_0 = df_0.pivot_table(values='summe_nettowert', index='Monat_Abrechnung', columns='IH_Kategorie', aggfunc='sum', fill_value=0)
        df_01 = pd.DataFrame(pt_0)
        df_01.reset_index(level=0, inplace=True)
        df_01.index.names = ['Index']
        df_01['Monat_Abrechnung']= pd.to_datetime(df_01['Monat_Abrechnung'])

        return {
            'data': [
                dict(
                    x=dff2_year['Monat_Abrechnung'],
                    y=df_01[str(i)],
                    mode='none',
                    stackgroup='one',
                    name=i
                ) for i in IH_Kategorie_name
            ],
            'layout': dict(
                legend={'x': 0, 'y': 1},
                xaxis={'title': 'Jahr'},
                yaxis={'title': 'Nettowert'},
                title="Übersicht Instandhaltungskosten"
            )}




## INTERACTION FOR table2

@app.callback( #each callback is assigned to a function
    Output('table2', 'data'),
    [Input('Button-Bauart', 'value'),
    Input('slider', 'value')])

def update_table(selected_Bauart, year_value):
    df_mengen_kosten_2= df_mengen_kosten_1[(df_mengen_kosten_1['Jahr'] >= year_value[0]) & (df_mengen_kosten_1['Jahr'] <= year_value[1])]
    df_mengen_kosten_3 = df_mengen_kosten_2.groupby(['Produkt_SAP', 'Datum_Abrechnung', 'Bauart', 'Menge','Jahr'], as_index=False).sum()
    df_mengen_kosten_4= df_mengen_kosten_3.sort_values(by='Nettowert', ascending=False)
    df_mengen_kosten_4 = df_mengen_kosten_4.iloc[0:10,:]

    #df_mengen_kosten_4 = df_mengen_kosten_3.iloc[0:10, 3:8]

#    if len(selected_Bauart) == 0 or 'Alle Bauarten' in selected_Bauart:
#        data_0 = df.drop(columns="Bauart")
#    else:
#        filtered_df0 = df[df.Bauart.isin(selected_Bauart)]
#        data_0 = filtered_df0.drop(columns="Bauart")
#
#
#    df_0 = data_0.groupby(['Monat_Abrechnung', 'IH_Kategorie'], as_index=False).sum()
#    pt_0 = df_0.pivot_table(values='summe_nettowert', index='Monat_Abrechnung', columns='IH_Kategorie', aggfunc='sum', fill_value=0)
#    df_01 = pd.DataFrame(pt_0)
#    df_01.reset_index(level=0, inplace=True)
#    df_01.index.names = ['Index']
##    df_01['Monat_Abrechnung']= pd.to_datetime(df_01['Monat_Abrechnung'])

##    df_04 = df_01['Monat_Abrechnung'].dt.year #extract year
#    df_04 = pd.DataFrame(df_04)
#    df_04.columns = ['Jahr']
#    df_001 = pd.concat([df_01, df_04], axis=1, sort=False)
#
#    # AGGREGATED TABLE: Monat_Abrechnung - BNI - BNI mobil - Frist - Revision - SoArb - Jahr
#    dff2_year = df_001[(df_001['Jahr'] >= year_value[0]) & (df_001['Jahr'] <= year_value[1])]
#
    return df_mengen_kosten_4.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
