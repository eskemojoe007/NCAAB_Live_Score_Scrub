# %% Import packages
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

# %% Get the the content
# Define where we want to go
url = 'https://www.ncaa.com/scoreboard/basketball-men/d1'

# Get or download the page content...with out all the sexyness
page = requests.get(url)

# Parse the html so we can search through it
soup = BeautifulSoup(page.text, 'html.parser')

# Now we start down the HTML DOM tree...we want to identify elements we care about
# so we look for IDs or classes that have descriptive names of content we want

# First we grab the container for all the games we care about
scoreboard = soup.find(attrs={'id': 'scoreboardGames'})

# Now we find the list of all the gamePods...we assume this is all of the games
games = scoreboard.find_all(attrs={'class': 'gamePod-type-game'})

# I set up an empty list, just to make a table at the end and store everything
all_info = []

# Loop through all the found games (gamePods) we found and extract what we want
for game in games:
    # For each game, we want the current time, teams, score, etc

    # Its not guaranteed that a game will be going...so we put this shity try/except
    try:
        # Try to get the current clock...
        time = game.find(attrs={'class': 'game-clock'}).text
    except:
        # If no clock...we assume we can get a game-time
        time = game.find(attrs={'class': 'game-time'}).text

    # Now we just extract teams and scores and names and store them all
    teams = game.find('ul', attrs={'class': 'gamePod-game-teams'}).find_all('li')
    name0 = teams[0].find(attrs={'class': 'gamePod-game-team-name'}).text
    score0 = teams[0].find(attrs={'class': 'gamePod-game-team-score'}).text
    name1 = teams[1].find(attrs={'class': 'gamePod-game-team-name'}).text
    score1 = teams[1].find(attrs={'class': 'gamePod-game-team-score'}).text

    # Add all that info to our list so we can make a table
    all_info.append({'time': time, 'name0':name0, 'score0': score0, 'name1': name1, 'score1': score1})

# Use pandas to make the table awesome...probably overkill for this application, but Pandas is the best
df = pd.DataFrame(all_info)

#Use Pandas to make a CSV really quickly.
df.to_csv('output.csv')
