#from pandas._config.config import reset_option
import requests
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import random
import re
import urllib.request
from PIL import Image
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpim
import numpy as np
from mpl_toolkits import mplot3d
#%matplotlib inline
from io import BytesIO
#from prettytable import PrettyTable
#from texttable import Texttable
#from tabulate import tabulate
#import plotly

#import csv
#with open('NFL_Player_QB_Search.csv', 'r') as file_csv:
#    read = csv.reader(file_csv)
#    for i in read:
#        print(i)


nfl_qb_data_season_2021 = pd.read_csv('NFL_Player_QB_Search_without_image.csv')  
#print(nfl_qb_data_season_2021)
#nfl_qb_data_season_2021.head()  
#print(nfl_qb_data_season_2021.head())
#print(nfl_qb_data_season_2021.Player_Image)
df = pd.DataFrame(nfl_qb_data_season_2021)
#print(df)

#Pretty Table Example
'''df1 = df
df1 = PrettyTable(df1)
print(df1)
'''

#Pretty Table Import CSV Example
#from prettytable import from_csv
    
#with open('NFL_Player_QB_Search.csv', 'r') as fp: 
#    x = from_csv(fp)
    
#print(x)

#tab_df_table = tabulate(df, headers='keys',tablefmt='psql')

#print(tabulate(df, headers='keys',tablefmt='psql'))


#Texttable Example
#table = Texttable()
#table.add_rows(x1)
#print(table.draw())

# Stat Categories
# Cmp%, Pass Yds, Passing TDs, TD%, INT, INT%, QBR
stat_categories = ['Completion Percentage','Passing Yards','Passing Touchdowns','Touchdown Percentage','Interceptions','QBR']
stats_data_categories = df[['Player','Team'] + stat_categories] 
stats_data_categories.head()
print(stats_data_categories.dtypes)

#   Naveen Venkatesan --> Data Scientist url:https://towardsdatascience.com/scraping-nfl-stats-to-compare-quarterback-efficiencies-4989642e02fe
#   This is where I found a template for how to generate radar charts for comparing nfl quarterbacks

# Create rankings for stat categories
for i in stat_categories:
    stats_data_categories[i + ' Rank'] = stats_data_categories[i].rank(pct=True)

# reverse the stats of ascension sort for interceptions stat category
stats_data_categories['Interceptions Rank'] = (1 - stats_data_categories['Interceptions Rank'])

# Viewing our updated stats DataFrame
print(stats_data_categories.head)

# General plot parameters for radar chart
mpl.rcParams['font.family'] = 'Avenir'
mpl.rcParams['font.size'] = 16
mpl.rcParams['axes.linewidth'] = 0
mpl.rcParams['xtick.major.pad'] = 15

# Hex Codes for the NFL Teams, which will be stored
team_colors = {'Arizona Cardinals':'#97233f', 'Atlanta Falcons':'#a71930', 'Baltimore Ravens':'#241773', 'Buffalo Bills':'#00338d', 'Carolina Panthers':'#0085ca',
               'Chicago Bears':'#0b162a', 'Cincinnati Bengals':'#fb4f14', 'Cleveland Browns':'#311d00', 'Dallas Cowboys':'#041e42', 'Denver Broncos':'#002244', 
               'Detroit Lions':'#0076b6', 'Green Bay Packers':'#203731', 'Houston Texans':'#03202f', 'Indianapolis Colts':'#002c5f', 'Jacksonville Jaguars':'#006778', 
               'Kansas City Chiefs':'#e31837', 'Los Angeles Chargers':'#002a5e', 'Los Angeles Rams':'#003594', 'Miami Dolphins':'#008e97', 
               'Minnesota Vikings':'#4f2683', 'New England Patriots':'#002244', 'New Orleans Saints':'#d3bc8d', 'New York Giants':'#0b2265', 
               'New York Jets':'#125740', 'Las Vegas Raiders':'#000000', 'Philadelphia Eagles':'#004c54', 'Pittsburgh Steelers':'#ffb612', 
               'San Francisco 49ers':'#aa0000', 'Seattle Seahawks':'#002244', 'Tampa Bay Buccaneers':'#d50a0a', 'Tennessee Titans':'#0c2340', 'Washington Football Team':'#773141'}

# Calculate angles for radar chart
offset = np.pi/6
angles = np.linspace(0, 2*np.pi, len(stat_categories) + 1) + offset

def create_radar_chart(ax, angles, player_data, color='blue'):
    # Plot data and fill with team color
    ax.plot(angles, np.append(player_data[-(len(angles)-1):], player_data[-(len(angles)-1)]), color=color, linewidth=2)
    ax.fill(angles, np.append(player_data[-(len(angles)-1):], player_data[-(len(angles)-1)]), color=color, alpha=0.2)

    # Set category labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(stat_categories)

    # Remove radial labels
    ax.set_yticklabels([])

    # Add player name
    ax.text(np.pi/2, 1.7, player_data[0], ha='center', va='center', size=18, color=color)


    # Use white grid
    ax.grid(color='white', linewidth=1.5)

    # Set axis limits
    ax.set(xlim=(0, 2*np.pi), ylim=(0, 1))

    return ax

# Function to get QB data
def get_qb_data(data, team):
    return np.asarray(data[data['Team'] == team])[0]


# NFC West
# Create figure
fig = plt.figure(figsize=(8, 8), facecolor='white')# Add subplots
ax1 = fig.add_subplot(221, projection='polar', facecolor='#ededed')
#ax2 = fig.add_subplot(222, projection='polar', facecolor='#ededed')
#ax3 = fig.add_subplot(223, projection='polar', facecolor='#ededed')
#ax4 = fig.add_subplot(224, projection='polar', facecolor='#ededed')# Adjust space between subplots
plt.subplots_adjust(hspace=0.8, wspace=0.5)# Get QB data
sf_data = get_qb_data(stats_data_categories, 'San Francisco 49ers')
sea_data = get_qb_data(stats_data_categories, 'Seattle Seahawks')
ari_data = get_qb_data(stats_data_categories, 'Arizona Cardinals')
lar_data = get_qb_data(stats_data_categories, 'Los Angeles Rams')# Plot QB data
ax1 = create_radar_chart(ax1, angles, lar_data, team_colors['Los Angeles Rams'])
#ax2 = create_radar_chart(ax2, angles, ari_data, team_colors['Arizona Cardinals'])
#ax3 = create_radar_chart(ax3, angles, sea_data, team_colors['Seattle Seahawks'])
#ax4 = create_radar_chart(ax4, angles, sf_data, team_colors['San Francisco 49ers'])
plt.show()

''' Sorting dataframe for customization/user input'''
players_sorted = sorted(df.Player.unique())

user_input = input('Enter a player: ')

selected_player = df[(df.Player.isin(players_sorted))]

if user_input in players_sorted:
    print(user_input, df.loc[df['Player']==user_input])





y = nfl_qb_data_season_2021

x = nfl_qb_data_season_2021.Player_Image

#Viewing Image
#for i in x:
#    r = requests.get(i)
#    img = Image.open(BytesIO(r.content))
    #img.show()
    
    #img = plt.savefig(i)
    #plt.show()
    #a = plt.imread(i)
    #plt.imshow(img)
    #plt.show(a)
    #plt.savefig(i)
    #Image.open(i)

# DataFrame Columns
#df.head()


