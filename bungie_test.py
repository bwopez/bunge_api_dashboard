import dash
import dash_core_components as dcc 
import dash_html_components as html 
import dash_bootstrap_components as dbc
import plotly.express as px 
import pandas as pd 

import datetime


def row_time(row):
    new_row = row
    placeholder = row['activitySecondsPlayed']
    minutes_and_seconds = datetime.timedelta(seconds=placeholder)
    hours, minutes, seconds = str(minutes_and_seconds).split(":")
    new_row['activityTimePlayed'] = "{} hours, {} minutes, and {} seconds".format(hours, minutes, seconds)

    return new_row


def row_kdr(row):
    new_row = row
    if row["activityKillsDeathsRatio"] < 1:
        new_row["activityKillsDeathsRatioIsPositive"] = "False"
    else:
        new_row["activityKillsDeathsRatioIsPositive"] = "True"

        
    return new_row


def get_pvp(df):
    new_list = []
    for index, row in df.iterrows():
        if type(row['activityModeTypes']) is list:
            if 5 in row['activityModeTypes']:
                # new_row = row
                # placeholder = row['activitySecondsPlayed']
                # minutes_and_seconds = datetime.timedelta(seconds=placeholder)
                # hours, minutes, seconds = str(minutes_and_seconds).split(":")
                # new_row['activityTimePlayed'] = "{} hours, {} minutes, and {} seconds".format(hours, minutes, seconds)
                new_row = row_time(row)
                new_row = row_kdr(new_row)
                new_list.append(new_row)
                # new_list.append(row)

    new_df = pd.DataFrame(new_list)

    return new_df.sort_values("name", ascending=False)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_json("titan2_but_json_cleanedish.json")
new_df = get_pvp(df)

fig = px.bar(new_df, x="activitySecondsPlayed", y="name", barmode="group",
            # hover_name="name", hover_data=["activitySecondsPlayed", "activityTimePlayed"],
            hover_name="name",
            hover_data={
                "name": False,
                "activitySecondsPlayed": True,
                "activityTimePlayed": True
            },
            labels={
                "name": "",
                "activitySecondsPlayed": "Time in Seconds",
                "activityTimePlayed": "Time"
            })
fig.update_layout(
    title_text="Time Played For Each PVP map in Destiny 2",
    title_x=0.5,
    height=600
)

fig2 = px.bar(new_df, x="activityKills", y="name", color="activityKillsDeathsRatioIsPositive",
            # hover_name="name", hover_data=["activityKills", "activityDeaths", "activityAssists", "activityKillsDeathsRatio"],
            hover_name="name",
            hover_data={
                "name": False,
                "activityKills": True,
                "activityDeaths": True,
                "activityAssists": True,
                "activityKillsDeathsRatio": True,
                "activityKillsDeathsRatioIsPositive": True
            },
            labels={
                "name": "",
                "activityKills": "Total Kills",
                "activityDeaths": "Total Deaths",
                "activityAssists": "Total Assists",
                "activityKillsDeathsRatio": "Efficiency",
                "activityKillsDeathsRatioIsPositive": "Positive KDR"
            },
            category_orders={
                "name": [
                    "Altar of Flame", "Bannerfall", "Cauldron",
                    "Convergence", "Distant Shore", "Emperor's Respite",
                    "Endless Vale", "Equinox", "Exodus Blue", "Fragment", 
                    "Javelin-4", "Legion's Gulch", "Meltdown", "Midtown",
                    "Pacifica", "Radiant Cliffs", "Retribution", 
                    "Rusted Lands", "Solitude", "The Burnout", 
                    "The Citadel", "The Dead Cliffs", "The Fortress", 
                    "Twilight Gap", "Vostok", "Widow's Court", "Wormhaven"
                ],
                "activityKillsDeathsRatioIsPositive": [
                    "True", "False"
                ]
            },
            color_discrete_map={
                "True": "Blue",
                "False": "Red"
            })
fig2.update_layout(
    title_text="Efficiency For Each PVP map in Destiny 2",
    title_x=0.5,
    height=600
)
# fig2.update_xaxes(showticklabels=False)

app.layout=html.Div(children=[
    html.H1(children="Hello Dash"),

    html.Div(children='''
    Dash: A web application framework for python.
    '''),

    html.Div(children=[
        dcc.Graph(id='example-graph', figure=fig, className="col-md-6"),
        dcc.Graph(id='example-graph2', figure=fig2, className="col-md-6")  
        ],
        className="row"
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)
