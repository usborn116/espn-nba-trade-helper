from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from helpers import lsetup, teamcomp, totrade, getting, posttrade, teamsetup
import pandas as pd

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///league.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2ckgBcCu4iVf3ZI@espn-fantasy-trade-helper.flycast:5432'

db.init_app(app)

class ThisLeague(db.Model):
    __tablename__='this_league'
    sw = db.Column(db.String)
    s2 = db.Column(db.String)
    lid = db.Column(db.Integer, primary_key=True)
    lyear = db.Column(db.Integer)

    def __init__(self, s2, sw, lid, lyear):
        self.s2 = s2
        self.sw = sw
        self.lid = lid
        self.lyear = lyear

    def __repr__(self):
        return '<Name %r>' % self.s2  

with app.app_context():
    db.create_all()

@app.route('/', methods=['POST','GET'])
def index():
    db.drop_all()
    db.create_all()
    return render_template('index.html')

@app.route('/league', methods=['POST','GET'])
def league():
    league = ThisLeague.query.first()
    if not league:
        record = ThisLeague(str(request.form['s2']),str(request.form['sw']),int(request.form['lid']),int(request.form['lyear']))
        db.session.add(record)
        db.session.commit()
        league = lsetup(record.s2,record.sw,record.lid, record.lyear)
    else:
        l = ThisLeague.query.first()
        league = lsetup(l.s2, l.sw, l.lid,l.lyear)
    #creating a dict to show each team's index number and showing that dictionary for reference
    kys = dict()
    for i, team in enumerate(league.teams):
        kys[team.team_name] = {}
        kys[team.team_name]['id'] = i

    return render_template('index.html', leagueid=ThisLeague.query.first(), ids=kys)

@app.route('/teams/<int:id>', methods=['POST','GET'])
def ros(id):
    record = ThisLeague.query.first()
    league = lsetup(record.s2,record.sw,record.lid, record.lyear)
    name = league.teams[id].team_name
    cleandf = teamsetup(league, id)

    return render_template('roster.html', leagueid=ThisLeague.query.first(), roster=cleandf.to_html(), team=name)

@app.route('/league/comp', methods=['POST','GET'])
def comp():
    record = ThisLeague.query.first()
    league = lsetup(record.s2, record.sw, record.lid, record.lyear)
    #gather league id of two trading teams and show df with the stats from both teams
    ids = [request.form['myteamid'],request.form['otherteamid']]
    teamcompdf = teamcomp(ids[0], ids[1], league)
    players_giving = str(request.form['giving'])
    to_trade = players_giving.split(',')
    to_tradedf = totrade(to_trade, league)
    players_getting = str(request.form['getting'])
    to_attain = players_getting.split(',')
    gettingdf = getting(to_attain, league)
    tmpteam1df = posttrade(ids[0], to_trade, to_attain, league)

    #finding trade stats before and after trade
    comp = [teamcompdf.head(1),tmpteam1df]
    comp = pd.concat(comp)
    diffs = comp.diff()
    comp = comp.append(diffs)
    i = diffs.index.tolist()[1]
    return render_template('comp.html', data=0, leagueid=ThisLeague.query.first(), tcomptable=teamcompdf.to_html(), playersreleasing=to_tradedf.to_html(), playersgetting=gettingdf.to_html(), statchange=diffs.loc[[i]].to_html())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')