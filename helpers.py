import datetime
import sys
from espn_api.basketball import League
import pandas as pd


curr_yr = datetime.date.today().year + 1

#setting up the stats we want to pull for each team
stats = ['PTS','BLK','STL','AST','OREB','DREB','TO','FGM','FTM','3PTM', 'FGA', '3PTA', 'FTA']

def lsetup(s2,sw,lid,lyear):
    return League(league_id=lid, year=lyear, espn_s2 = s2, swid = sw)

def teamsetup(league, id):
    team = league.teams[id]
    roster = dict()
    
    stats = ['PTS','BLK','STL','AST','OREB','DREB','TO','FGM','FTM','3PTM', 'FGA', '3PTA', 'FTA']

    for player in team.roster:
        roster[player.name] = dict()
        roster[player.name]['Position'] = player.position
        for stat in stats:
            roster[player.name][stat] = 0
        try: 
            for stat in player.stats[f"{curr_yr}_total"]['avg']:
                if stat in stats:
                    roster[player.name][stat] = player.stats[f"{curr_yr}_total"]['avg'][stat]
        except:
            continue
                
    df = pd.DataFrame(roster)
    df = df.transpose()

    df['FGA'] = df['FGA'] + .0001
    df['TO'] = df['TO'] + .00001
    df['FTA'] = df['FTA'] + .00001

    df['AFG%'] = (df['3PTM']*0.5+df['FGM']).divide((df['FGA']))
    df['A/TO'] = df['AST'].divide((df['TO']))
    df['FT%'] = df['FTM'].divide((df['FTA']))

    return df[['Position','PTS', 'BLK','STL','AST','OREB','DREB','FTM','3PTM','AFG%','A/TO','FT%']].sort_values(by=['PTS'], ascending=False)

def teamstatsetup(league):
    #creating a dictionary of each team, with each team's cumulated stat in the categories above, and cleaning it
    avgs = dict()

    for team in league.teams:
        avgs[team.team_name] = dict()
        for stat in stats:
            avgs[team.team_name][stat] = 0
        for player in team.roster:
            try: 
                for stat in player.stats[f"{curr_yr}_total"]['avg']:
                    if stat in stats:
                        avgs[team.team_name][stat] += player.stats[f"{curr_yr}_total"]['avg'][stat]
            except:
                continue
                
    df = pd.DataFrame(avgs)
    df = df.transpose()
    df['AFG%'] = (df['3PTM']*0.5+df['FGM']).divide(df['FGA'])
    df['A/TO'] = df['AST'].divide(df['TO'])
    df['FT%'] = df['FTM'].divide(df['FTA'])
    df.loc['League Average'] = df.mean()
    df.loc['League Standard Deviation'] = df.std()
    cleandf = df[['PTS', 'BLK','STL','AST','OREB','DREB','FTM','3PTM','AFG%','A/TO','FT%']]
    return cleandf

def teamcomp(myteam, otherteam, league):
    myteam = league.teams[int(myteam)].team_name
    otherteam = league.teams[int(otherteam)].team_name
    df = teamstatsetup(league)
    teamcomp = df.loc[[myteam, otherteam, 'League Average', 'League Standard Deviation']]
    return teamcomp.round(2)

#new df that just shows the stats of the players you are trading away
def totrade(list, league):
    trading = dict()
    for player in list:
        player = player.strip()
        trading[player] = dict()
        for stat in league.player_info(name = player).stats[f"{curr_yr}_total"]['avg']:
            if stat in stats:
                trading[player][stat] = 0
                trading[player][stat] = league.player_info(name = player).stats[f"{curr_yr}_total"]['avg'][stat]
                
    tradingdf = pd.DataFrame(trading).transpose()
    tradingdf['AFG%'] = (tradingdf['3PTM']*0.5+tradingdf['FGM'])/tradingdf['FGA']
    tradingdf['A/TO'] = tradingdf['AST']/tradingdf['TO']
    tradingdf['FT%'] = tradingdf['FTM']/tradingdf['FTA']
    tradingdf = tradingdf[['PTS', 'BLK','STL','AST','OREB','DREB','FTM','3PTM','AFG%','A/TO','FT%']]
    return tradingdf.round(2)

#new df that just shows the stats of the players you are getting
def getting(list, league):
    fromtrade = dict()
    print(list, file=sys.stderr)
    for player in list:
        player = player.strip()
        print(player, file=sys.stderr)
        fromtrade[player] = dict()
        print(league.player_info(name = player), file=sys.stderr)
        for stat in league.player_info(name = player).stats[f"{curr_yr}_total"]['avg']:
            if stat in stats:
                fromtrade[player][stat] = 0
                fromtrade[player][stat] += league.player_info(name = player).stats[f"{curr_yr}_total"]['avg'][stat]
                
    gettingdf = pd.DataFrame(fromtrade).transpose()
    gettingdf['AFG%'] = (gettingdf['3PTM']*0.5+gettingdf['FGM'])/gettingdf['FGA']
    gettingdf['A/TO'] = gettingdf['AST']/gettingdf['TO']
    gettingdf['FT%'] = gettingdf['FTM']/gettingdf['FTA']
    gettingdf = gettingdf[['PTS', 'BLK','STL','AST','OREB','DREB','FTM','3PTM','AFG%','A/TO','FT%']]
    return gettingdf.round(2)

def posttrade(myteam, add, subtract, league):
    myteam = league.teams[int(myteam)]

    tmpteam1 = dict()

    for stat in stats:
        tmpteam1[stat] = 0

    for player in myteam.roster:
        if player.name not in add:
            try: 
                for stat in player.stats[f"{curr_yr}_total"]['avg']:
                    if stat in stats:
                        tmpteam1[stat] += player.stats[f"{curr_yr}_total"]['avg'][stat]
            except:
                continue
    
    for player in subtract:
        player = player.strip()
        for stat in league.player_info(name = player).stats[f"{curr_yr}_total"]['avg']:
            if stat in stats:
                tmpteam1[stat] += league.player_info(name = player).stats[f"{curr_yr}_total"]['avg'][stat]

    tmpteam1df = pd.DataFrame(tmpteam1, index=[myteam.team_name])
    tmpteam1df['AFG%'] = (tmpteam1df['3PTM']*0.5+tmpteam1df['FGM'])/tmpteam1df['FGA']
    tmpteam1df['A/TO'] = tmpteam1df['AST']/tmpteam1df['TO']
    tmpteam1df['FT%'] = tmpteam1df['FTM']/tmpteam1df['FTA']
    tmpteam1df = tmpteam1df[['PTS', 'BLK','STL','AST','OREB','DREB','FTM','3PTM','AFG%','A/TO','FT%']]
    return tmpteam1df.round(2)

def roster_maker(league, teamid):
    team = league.teams([teamid])
    roster = dict()
    for player in team.roster:
        roster[player.name] = dict()
        for stat in stats:
            roster[player.name][stat] = 0
            try: 
                for stat in player.stats[f"{curr_yr}_total"]['avg']:
                    if stat in stats:
                        roster[player.name][stat] += player.stats[f"{curr_yr}_total"]['avg'][stat]
            except:
                continue
                
    df = pd.DataFrame(roster)
    df = df.transpose()
    df['AFG%'] = (df['3PTM']*0.5+df['FGM'])/df['FGA']
    df['A/TO'] = df['AST']/df['TO']
    df['FT%'] = df['FTM']/df['FTA']
    df.loc['mean'] = df.mean()
    df.loc['stddev'] = df.std()
    cleandf = df[['PTS', 'BLK','STL','AST','OREB','DREB','FTM','3PTM','AFG%','A/TO','FT%']]
    return cleandf