This app is written with Python and Flask, and helps you decide how a trade will affect your team in ESPN NBA Fantasy.

This app is live at https://espn-trade-helper.fly.dev/league.

Simply clone the repo and install virtualenv via pip in the directory of this repo. Then, initiate a virtual environment, and install the following dependencies (I recommend installing with with pip):
Flask, flask_sqlalchemy, espn-api, requests, and pandas.

Once dependencies are installed, navigate to the folder in your terminal and run the file with the command "flask run". Open the local server address shown in your terminal, and you can get to trading from there!

You will need your league ID and, for private leagues, your SW and S2 IDs as well. This discussion talks about finding your SW and S2 ids. https://github.com/cwendt94/espn-api/discussions/150

Big shoutout to @cwendt94 for the espn-api, which the data for this whole project pulls from. You can find that repo here: https://github.com/cwendt94/espn-api

First, you'll enter your league's various IDs:
<img width="1433" alt="CleanShot 2023-06-15 at 10 47 38@2x" src="https://github.com/usborn116/espn-nba-trade-helper/assets/64931297/1413fc2a-fdda-48a6-8fbf-b9689b9f2ead">

Next, you will see a list of each team in your league and their index. You can click on a team to see their roster, and see the stats for each player. You will fill out the form asking for the necessary information needed to process the trade:
<img width="1431" alt="CleanShot 2023-06-15 at 10 47 58@2x" src="https://github.com/usborn116/espn-nba-trade-helper/assets/64931297/cb5b88d9-677c-477e-b432-4aa513bad16f">

The screen will show a loading animation as it parses the data to see how the trade affects you:
<img width="1416" alt="CleanShot 2023-06-15 at 10 48 19@2x" src="https://github.com/usborn116/espn-nba-trade-helper/assets/64931297/f06848f8-7b80-44b5-a8ff-6afd896bf223">

Finally, you'll see data tables to show you the stat comparison between you and your trade partner, the stats of the players you are giving and getting, and how your team's stats are increased or decreased after the trade:
![CleanShot 2023-06-15 at 10 49 01](https://github.com/usborn116/espn-nba-trade-helper/assets/64931297/61ed8896-8ac5-43bf-ae44-8627cfd1ce8b)

Articles that helped me with the Fly deployment of this project:
- https://fly.io/docs/languages-and-frameworks/python/
- https://fly.io/docs/postgres/connecting/connecting-internal/
- https://fly.io/docs/postgres/connecting/connecting-external/
- https://community.fly.io/t/deploying-python-flask-db/8456/7
- https://docs.sqlalchemy.org/en/20/core/engines.html
- https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/config/#connection-url-format

