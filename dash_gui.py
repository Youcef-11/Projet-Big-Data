# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 21:43:45 2022

@author: GILLES / CHORFI
"""

import sys

import json
from tkinter import VERTICAL
import numpy as np
import pandas as pd
import plotly.express as px
# import pymysql
from sqlalchemy import create_engine

from dash import Dash, dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

# create sqlalchemy engine
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="user_project",
                               pw="2022_user_project",
                               db="commerce_extérieur_2019"))
# labels for range slide
date_labels = {
    1: {'label': 'Jan'}, 
    2: {'label': 'Fév'}, 
    3: {'label': 'Mar'},
    4: {'label': 'Avr'},
    5: {'label': 'Mai'},
    6: {'label': 'Jui'},
    7: {'label': 'Juil'},
    8: {'label': 'Aoû'},
    9: {'label': 'Sep'},
    10: {'label': 'Oct'},
    11: {'label': 'Nov'},
    12: {'label': 'Déc'},
    }

#  Log scale
viridis = px.colors.sequential.Viridis
colorscale = [
        [0, viridis[0]],
        [1./3e9, viridis[2]],
        [1./3e6, viridis[4]],
        [1./3e3, viridis[7]],
        [1., viridis[9]],
]

app = Dash(external_stylesheets=[dbc.themes.MINTY])

DOUBLE_RANGE_STYLE = {
    'top': 100,
    'left': 0,
    'bottom': 0,
    'width': '20em',
    'padding': '8em 1em',
    'background-color': '#f8f9fa'
}

double_range = html.Div(
    [
        html.H2("Filtres"),
        html.Hr(),
        html.P(
            "Période des transactions", className='lead'
        ),
        
        dcc.RangeSlider(
            min=1,
            max=12,
            value=[1, 12],
            marks=date_labels,
            step=1,
            id='my-drange-slider'
            ),        
    ],
    style=DOUBLE_RANGE_STYLE
)

app.layout = html.Div([
    dbc.Row(
        dbc.Col(html.H1(
            "Commerce extérieur - Année 2019",
            style={
                'text-align': 'center',
                'marginTop': 30,
                'marginBottom': 50
                }
                ))
        ),

    dbc.Row([
        dbc.Col(double_range, width=3, align='top'),
        dbc.Col([
            html.H2("Valeurs d'échanges", style={'textAlign':'center', 'marginBottom': 10}),
            dcc.Graph(id='world_map')
            ]
            )
            ]),

    # html.Br(),


    dbc.Row(
        [
        html.H2("Répartition des transactions par secteur", 
        style={'textAlign':'left', 'marginBottom': 10}),
        dbc.Col(dcc.Graph(id='bar_graph'))
        ]
            ),

    dbc.Row(
    [
    html.H2("Répartition des transactions par sous-secteur", 
    style={'textAlign':'left', 'marginBottom': 10}),
    dbc.Col(dcc.Graph(id='bar_sub_graph'))
    ]
        )
    ])


@app.callback(
    Output(component_id='world_map', component_property='figure'),
    Input(component_id='my-drange-slider', component_property='value')
)
def update_output(value):
    periode = (f"{date_labels[value[0]]['label']}-{date_labels[value[1]]['label']}"
    if value[0] != value[1] else f"{date_labels[value[0]]['label']}")

    Q2 = ("select code_iso3, nom_pays, continent, sum(valeur) as valeur_echanges, flux"
    " from transaction join pays using(code_pays) " 
    f"where mois between {value[0]} and {value[1]} group by flux, code_pays;")
    # f"where mois >= {value[0]} and mois <= {value[1]} group by flux, code_pays;")
    df = pd.read_sql(Q2, engine)

    df2 = df.loc[df["flux"] == 'I'].copy()
    df2.drop("flux", axis=1, inplace=True)
    df2.rename(columns={"valeur_echanges": "importation"},
                        inplace=True)
    df2.reset_index(inplace=True, drop=True)
    
    export = df.loc[df["flux"] == 'E', ["nom_pays", "valeur_echanges"]]

    idx_E = df2.index[df2["nom_pays"].isin(export["nom_pays"])]
    df2["exportation"] = np.nan
    for i, row in df2.iloc[idx_E].iterrows():
        df2.iloc[i, 4] = export.loc[export["nom_pays"] == row["nom_pays"], "valeur_echanges"].values[0]

    df2["valeur_echanges"] = df2["importation"] + df2["exportation"]

    fig2 = px.choropleth(df2, locations="code_iso3",
                    color="valeur_echanges",
                    color_continuous_scale=px.colors.sequential.Darkmint,
                    # hover_name="nom_pays", # column to add to hover information
                    hover_data=[
                        "continent", "nom_pays", "valeur_echanges",
                        "importation", "exportation"
                        ],
                    # custom_data="code_iso3",
                    #projection="orthographic",
                    projection="natural earth",
                    # scope="europe",
                    title=(f"Période : {periode}")
                    )

    fig2.update_layout(margin=dict(l=60, r=60, t=50, b=50))

    return fig2
    # return f"value[0]", fig2

@app.callback(
    Output(component_id='bar_graph', component_property='figure'),
    Input(component_id='world_map', component_property='clickData')
)
def display_click_data(clickData):
    # data = json.dumps(clickData, indent=2)
    if clickData == None:
        raise PreventUpdate
    else:
        iso3 = clickData["points"][0]["location"]

        Q = ("select sum(valeur) as valeur_echanges, flux, code_section, libelle_section, libelle_short, code_iso3"
        " from transaction join pays using(code_pays) join produit using(code_NC8)"
        f" join sections using(code_section) where code_iso3 = '{iso3}'"
        " group by code_section, flux;")
        df = pd.read_sql(Q, engine)

        Q5 = f"select nom_pays from pays where code_iso3 = '{iso3}';"
        df5 = pd.read_sql(Q5, engine)
        global nom_pays 
        nom_pays = df5["nom_pays"][0]
        
        fig = px.bar(df, x='libelle_short', y='valeur_echanges',
             #hover_data=['lifeExp', 'gdpPercap'],
             color='flux',
             text_auto='.2s',
             #labels={'pop':'population of Canada'},
             title=f"Pays : {nom_pays}",
             height=650,
             width=1150
            )
        fig.update_traces(textfont_size=12, textangle=0, 
        textposition="outside", cliponaxis=False)

    return fig

@app.callback(
    Output(component_id='bar_sub_graph', component_property='figure'),
    Input(component_id='bar_graph', component_property='clickData')
)
def display_click_data(clickData):
    if clickData == None:
        raise PreventUpdate
    else:
        secteur = clickData["points"][0]['x']
        Q = ("select sum(valeur) as valeur_echanges, flux, libelle_ss_section"
        " from transaction join pays using(code_pays) join produit using(code_NC8) join sous_sections using(code_ss_section)" 
        f" join sections using(code_section) where nom_pays = '{nom_pays}' and libelle_short = '{secteur}'"
        " group by code_ss_section, flux;")
        df = pd.read_sql(Q, engine)
        df['libelle_ss_section'] = df['libelle_ss_section'].apply(lambda x: x[:40]+'...')

        threshold = .005
        df_filt = df[df['valeur_echanges']/df['valeur_echanges'].sum() > threshold].copy()
        df_filt.reset_index(drop=True, inplace=True)
        df_filt_neg = df[df['valeur_echanges']/df['valeur_echanges'].sum() <= threshold]
        i_autres = df_filt_neg.loc[df_filt_neg['flux']  == 'I', 'valeur_echanges'].sum()
        e_autres = df_filt_neg.loc[df_filt_neg['flux']  == 'E', 'valeur_echanges'].sum()
        df_filt.loc[len(df_filt)] = [i_autres, 'I', 'Autres']
        df_filt.loc[len(df_filt)] = [e_autres, 'E', 'Autres']

        fig = px.bar(df_filt, x='libelle_ss_section', y='valeur_echanges',
        color='flux',
        text_auto='.2s'
        )
        # fig_all = make_subplots(rows=1, cols=1) 
        
        # for trace in range(len(fig["data"])):
        #     fig_all.append_trace(fig["data"][trace], row=1, col=1)
        
        fig.update_layout(height=650, width=1150, title={
            'text' : f"Pays {nom_pays} - Secteur = {secteur}",
            'x':0.1,
            'xanchor': 'left',
            'font_size':16
        })
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

    return fig

if __name__ == '__main__':
    app.run_server(host="localhost", debug=True)
