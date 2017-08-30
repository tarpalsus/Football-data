# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 18:52:26 2017


"""
import pandas as pd
import sqlite3
import json

def get_match_squad(team):
"""Big sql queries, combining match data with team and player names
Returns 2 dfs, one for home and one for away matches"""
    conn = sqlite3.connect(r"C:\Users\Maciek\Desktop\database.sqlite")
    df_home = pd.read_sql_query("""SELECT Match.stage, Match.date,
                                t2.team_long_name AS Rival,
                           pl1.player_name AS player1, pl2.player_name AS player2,
                           pl3.player_name AS player3, pl4.player_name AS player4,
                           pl5.player_name AS player5, pl6.player_name AS player6,
                           pl7.player_name AS player7, pl8.player_name AS player8,
                           pl9.player_name AS player9, pl10.player_name AS player10,
                           pl11.player_name AS player11,
                           Match.home_player_X1,
                           Match.home_player_X2,
                           Match.home_player_X3,
                           Match.home_player_X4,
                           Match.home_player_X5,
                           Match.home_player_X6,
                           Match.home_player_X7,
                           Match.home_player_X8,
                           Match.home_player_X9,
                           Match.home_player_X10,
                           Match.home_player_X11,
                           Match.home_player_Y1,
                           Match.home_player_Y2,
                           Match.home_player_Y3,
                           Match.home_player_Y4,
                           Match.home_player_Y5,
                           Match.home_player_Y6,
                           Match.home_player_Y7,
                           Match.home_player_Y8,
                           Match.home_player_Y9,
                           Match.home_player_Y10,
                           Match.home_player_Y11
                           FROM Match
                           INNER JOIN 'Team' t1 ON Match.home_team_api_id = t1.team_api_id
                           INNER JOIN 'Team' t2 ON Match.away_team_api_id = t2.team_api_id
                           INNER JOIN 'Player' pl1 ON Match.home_player_1 = pl1.player_api_id
                           INNER JOIN 'Player' pl2 ON Match.home_player_2 = pl2.player_api_id
                           INNER JOIN 'Player' pl3 ON Match.home_player_3 = pl3.player_api_id
                           INNER JOIN 'Player' pl4 ON Match.home_player_4 = pl4.player_api_id
                           INNER JOIN 'Player' pl5 ON Match.home_player_5 = pl5.player_api_id
                           INNER JOIN 'Player' pl6 ON Match.home_player_6 = pl6.player_api_id
                           INNER JOIN 'Player' pl7 ON Match.home_player_7 = pl7.player_api_id
                           INNER JOIN 'Player' pl8 ON Match.home_player_8 = pl8.player_api_id
                           INNER JOIN 'Player' pl9 ON Match.home_player_9 = pl9.player_api_id
                           INNER JOIN 'Player' pl10 ON Match.home_player_10 = pl10.player_api_id
                           INNER JOIN 'Player' pl11 ON Match.home_player_11 = pl11.player_api_id
                           WHERE t1.team_long_name=?"""
                           ,conn,params=[team])
    df_away = pd.read_sql_query("""SELECT Match.stage, Match.date,
                                t2.team_long_name AS Rival,
                           pl1.player_name AS player1, pl2.player_name AS player2,
                           pl3.player_name AS player3, pl4.player_name AS player4,
                           pl5.player_name AS player5, pl6.player_name AS player6,
                           pl7.player_name AS player7, pl8.player_name AS player8,
                           pl9.player_name AS player9, pl10.player_name AS player10,
                           pl11.player_name AS player11,
                           Match.away_player_X1,
                           Match.away_player_X2,
                           Match.away_player_X3,
                           Match.away_player_X4,
                           Match.away_player_X5,
                           Match.away_player_X6,
                           Match.away_player_X7,
                           Match.away_player_X8,
                           Match.away_player_X9,
                           Match.away_player_X10,
                           Match.away_player_X11,
                           Match.away_player_Y1,
                           Match.away_player_Y2,
                           Match.away_player_Y3,
                           Match.away_player_Y4,
                           Match.away_player_Y5,
                           Match.away_player_Y6,
                           Match.away_player_Y7,
                           Match.away_player_Y8,
                           Match.away_player_Y9,
                           Match.away_player_Y10,
                           Match.away_player_Y11
                           FROM Match
                           INNER JOIN 'Team' t1 ON Match.away_team_api_id = t1.team_api_id
                           INNER JOIN 'Team' t2 ON Match.home_team_api_id = t2.team_api_id
                           INNER JOIN 'Player' pl1 ON Match.away_player_1 = pl1.player_api_id
                           INNER JOIN 'Player' pl2 ON Match.away_player_2 = pl2.player_api_id
                           INNER JOIN 'Player' pl3 ON Match.away_player_3 = pl3.player_api_id
                           INNER JOIN 'Player' pl4 ON Match.away_player_4 = pl4.player_api_id
                           INNER JOIN 'Player' pl5 ON Match.away_player_5 = pl5.player_api_id
                           INNER JOIN 'Player' pl6 ON Match.away_player_6 = pl6.player_api_id
                           INNER JOIN 'Player' pl7 ON Match.away_player_7 = pl7.player_api_id
                           INNER JOIN 'Player' pl8 ON Match.away_player_8 = pl8.player_api_id
                           INNER JOIN 'Player' pl9 ON Match.away_player_9 = pl9.player_api_id
                           INNER JOIN 'Player' pl10 ON Match.away_player_10 = pl10.player_api_id
                           INNER JOIN 'Player' pl11 ON Match.away_player_11 = pl11.player_api_id
                           WHERE t1.team_long_name=?"""
                           ,conn,params=[team])
    conn.close()
    return df_away,df_home



def prepare_json(away,home):
    away = away.sort_values('date')
    home = home.sort_values('date')
    for i in range(1,12):
        if i == 1 :
            away['Player_data'+str(i)] = list(zip(away['player' + str(i)] \
            ,away['away_player_X' + str(i)]  + 4 ,away['away_player_Y' + str(i)]))
            home['Player_data'+str(i)] = list(zip(home['player' + str(i)] \
            ,home['home_player_X' + str(i)] + 4 ,home['home_player_Y' + str(i)]))
        else:
            away['Player_data'+str(i)] = list(zip(away['player' + str(i)] \
            ,away['away_player_X' + str(i)],away['away_player_Y' + str(i)]))
            home['Player_data'+str(i)] = list(zip(home['player' + str(i)] \
            ,home['home_player_X' + str(i)],home['home_player_Y' + str(i)]))


    json_data_away = json.loads(away.to_json(orient='records'))
    json_data_home = json.loads(home.to_json(orient='records'))

    for var in json_data_away:
        var['Players'] = [value for key, value in var.items() if key.startswith('Player_data')]
    for var in json_data_home:
        var['Players'] = [value for key, value in var.items() if key.startswith('Player_data')]
    return json_data_away, json_data_home

away, home = get_match_squad('Manchester United')
json_data_away, json_data_home = prepare_json(away, home)

with open('home_players.json', 'w') as f:
    json.dump(json_data_home, f)

with open('away_players.json', 'w') as f:
    json.dump(json_data_away, f)
