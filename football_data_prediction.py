# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 19:27:57 2017

"""
import pandas as pd
import sqlite3
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
import time
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler
from xgboost import XGBClassifier
import matplotlib.pyplot as plt


def find_previous_in_df(df):
    #Doesnt help that much
   previous_home_team_results = []
   previous_away_team_results = []
   for index, row in df.iterrows():
       previous = df[(df['season'] == row['season']) & (df['stage']<row['stage']) & (df['stage'] >= (row['stage']-10))]
       previous_home_team_as_home = len(previous[(previous['home_team_api_id'] == row['home_team_api_id']) & (previous['outcome'] == 'home win')])
       previous_home_team_as_away = len(previous[(previous['away_team_api_id'] == row['home_team_api_id']) & (previous['outcome'] == 'away win')])
       previous_away_team_as_home = len(previous[(previous['home_team_api_id'] == row['away_team_api_id']) & (previous['outcome'] == 'home win')])
       previous_away_team_as_away = len(previous[(previous['away_team_api_id'] == row['away_team_api_id']) & (previous['outcome'] == 'away win')])
       previous_home_team_results.append(previous_home_team_as_home + previous_home_team_as_away)
       previous_away_team_results.append(previous_away_team_as_home + previous_away_team_as_away)
   df['home_team_previous'] = pd.Series(previous_home_team_results)
   df['away_team_previous'] = pd.Series(previous_away_team_results)
   return df

def find_previous_between_teams(df):
    #Doesnt change anything
    previous_home_team_results = []
    previous_away_team_results = []
    for index, row in df.iterrows():
            previous = df[(df['season'] < row['season']) | ((df['stage']<row['stage']) & (df['season'] == row['season']))]
            previous_home_team_as_home = len(previous[(previous['home_team_api_id'] == row['home_team_api_id']) & (previous['away_team_api_id'] == row['away_team_api_id']) & (previous['outcome'] == 'home win')])
            previous_home_team_as_away = len(previous[(previous['away_team_api_id'] == row['home_team_api_id']) & (previous['home_team_api_id'] == row['away_team_api_id']) & (previous['outcome'] == 'away win')])
            previous_away_team_as_home = len(previous[(previous['home_team_api_id'] == row['away_team_api_id']) & (previous['away_team_api_id'] == row['home_team_api_id']) & (previous['outcome'] == 'home win')])
            previous_away_team_as_away = len(previous[(previous['away_team_api_id'] == row['away_team_api_id']) & (previous['home_team_api_id'] == row['home_team_api_id']) &  (previous['outcome'] == 'away win')])
            previous_home_team_results.append(previous_home_team_as_home + previous_home_team_as_away)
            previous_away_team_results.append(previous_away_team_as_home + previous_away_team_as_away)
    df['home_team_previous_between'] = pd.Series(previous_home_team_results)
    df['away_team_previous_between'] = pd.Series(previous_away_team_results)
    return df

def classifier(df):
    df = df.dropna()
    le = LabelEncoder()
    y = df['outcome']
    le.fit(y)
    y = le.transform(y)
    X = df.drop(['outcome','home_team_goal','away_team_goal','score', 'stage',
                 'home_team_api_id','away_team_api_id','season', 'team_api_id','team_api_id', 'team_fifa_api_id'], axis=1)
    to_dummy = [x for x in X.columns if 'Class' in x ]
    X_no_dummy = X.drop(to_dummy,axis=1)
    X = X_no_dummy
    #X_dummy = pd.get_dummies(X[to_dummy])
    #X = pd.concat([X_no_dummy, X_dummy], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=0.25,
                                                        random_state=7)
    scaler = StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    xgb = XGBClassifier(max_depth=3, n_estimators=4)

#    forest = RandomForestClassifier()
#    params = {'max_depth' : [3],
#              'n_estimators':[4]}
#    grid = GridSearchCV(estimator=xgb, param_grid=params)
#
    xgb.fit(X_train,y_train)
    #print(grid.feature_importances_)

    inferred = xgb.predict(X_test)

    print(accuracy_score(inferred, y_test))
    print(f1_score(inferred, y_test, average='weighted'))
    confusion_matrix(inferred, y_test)
    #print(xgb.feature_importances_)
    return xgb, X

def preparation():

    conn = sqlite3.connect(r"C:\Users\Maciek\Desktop\database.sqlite")
    df = pd.read_sql_query("""SELECT * FROM Match
                           INNER JOIN 'Team_Attributes' t1 ON Match.home_team_api_id = t1.team_api_id
                           INNER JOIN 'Team_Attributes' t2 ON Match.away_team_api_id = t2.team_api_id""", conn)
    conn.close()

    df.drop(['date','id','country_id','league_id','match_api_id',
             'goal','shoton','shotoff', 'foulcommit','card','cross','corner',
             'possession', 'PSH','PSD','PSA' ], axis=1, inplace=True)

    cols = [c for c in df.columns if not 'player' in c]

    df = df[cols]

    df['score'] = df['home_team_goal'] - df['away_team_goal']

    temp = pd.Series(index=df.index)
    temp[df['score'] == 0] = 'draw'
    temp[df['score'] > 0] = 'home win'
    temp[df['score'] < 0] = 'away win'

    df['outcome'] = temp

    print(df['outcome'].value_counts())
    with open('with_previous.pkl', 'wb') as f:
        pickle.dump(df,f)
    return df
    df_with_previous = find_previous_in_df(df)
    return df_with_previous


with open('with_previous.pkl', 'rb') as f:
   df = pickle.load(f)


#df = find_previous_between_teams(df)
print('ok')

xgb, data = classifier(df)

plt.barh(range(len(xgb.feature_importances_)), xgb.feature_importances_)
plt.show()
