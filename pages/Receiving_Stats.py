from ast import Index
import streamlit as st
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


st.markdown("""
This app performs simple webscraping of NFL Football player stats data and creates a radar chart that we will be using as a common metric in order to have a visual representation of the performance done 
by each team (according to the receiving category)!
* **Python libraries:** pandas, streamlit, numpy, matplotlib, pillow, beautifulsoup4
* **Data source:** [pro-football-reference.com](https://www.pro-football-reference.com/).
Data is from 1950 to 2022.
""")


# The original selected_year variable for user selection of the year of the choosing as being of the range of 1932, current_season var
# I am going to be test trialing to change the range of the selected_year var to 1970, current_season var
# calculating current nfl season as most recent season available to scrape
current_season = 2023
st.sidebar.header('User Customization')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1932,current_season))))

@st.cache
def scraping_receiving_Stats(selected_year):
    players = []


    url = 'https://www.pro-football-reference.com/years/'+ str(selected_year) + '/receiving.htm'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
    page = requests.get(url,headers=headers, timeout=2, allow_redirects = True )
    soup = bs(page.content, 'html.parser')
    href_tbody = soup.find_all('tbody')


    for i in href_tbody:
        href_tr_data = i.find_all('tr')
        for i in href_tr_data:
            while True:
                try:
                    #Name of Player Collected
                    names_search = i.find('td', {'data-stat':'player'})
                    #names = names_search['csk']
                    names_text = names_search.find('a')
                    names = names_text.text


                    #Team of PLayer Collected
                    team_search = i.find('td', {'data-stat':'team'})
                    team_name = team_search.find('a')
                    team = team_name['title']

                    #Age of Player Collected
                    age_search = i.find('td',{'data-stat':'age'})
                    age = age_search.text

                    #Games and Games played by Player Collected
                    games_search = i.find('td',{'data-stat':'g'})
                    games = games_search.text

                    games_played_search = i.find('td',{'data-stat':'gs'})
                    games_played = games_played_search.text     

                    #Receptions of Player Collected
                    rec_search = i.find('td',{'data-stat':'rec'})
                    rec_data = rec_search.text        

                    #Receiving Yards of Player Collected
                    rec_yards_search = i.find('td',{'data-stat':'rec_yds'})
                    rec_yards_data = rec_yards_search.text       


                    #Receiving Yards Per Reception Player Collected
                    rec_yards_per_rec_search = i.find('td',{'data-stat':'rec_yds_per_rec'})
                    rec_yards_per_rec_data = rec_yards_per_rec_search.text         


                    #Receiving TDs of Player Collected
                    rec_td_search = i.find('td',{'data-stat':'rec_td'})
                    rec_td_data = rec_td_search.text         


                    #Rec Long of Player Collected
                    rec_long_search = i.find('td',{'data-stat':'rec_long'})
                    rec_long_data = rec_long_search.text
                

                    #Rec Per Game of Player Collected
                    rec_per_game_search = i.find('td',{'data-stat':'rec_per_g'})
                    rec_per_game_data = rec_per_game_search.text

                    #Rec Yards Per Game of Player Collected
                    rec_yds_per_game_search = i.find('td',{'data-stat':'rec_yds_per_g'})
                    rec_yds_per_game_data = rec_yds_per_game_search.text

                    #Formatting Data Collected
                    player = { "Player": names, "Team": team, "Age": age, "Games Played": games, "Games Started": games_played, 
                                "Receptions": rec_data, "Receiving Yards": rec_yards_data, "Receiving Yards Per Catch": rec_yards_per_rec_data,
                                "Receiving TD": rec_td_data, "Reception Long": rec_long_data, "Receptions Per Game": rec_per_game_data, 
                                "Receiving Yards Per Game": rec_yds_per_game_data
                            }
                    #Appending Each player to Players List
                    players.append(player)
        
        
            #print(ranking, names, team, age, games, games_played)
        
                    break
                except:
                    break




    df = pd.DataFrame(players)
    #print(df)
    return df
df = scraping_receiving_Stats(selected_year)


st.header('Receiving Statistics')
st.subheader('NFL Season ' + str(selected_year) + ' Receiving Statistics')

st.dataframe(df)


df.rename(columns={'Receptions': 'Rec',
'Receiving Yards': 'Rec Yds', 'Receiving Yards Per Catch': 'Yds/Rec', 'Receiving TD': 'Rec TD', 'Receptions Per Game': 'Rec/G', 'Receiving Yards Per Game': 'Yds/G'}, inplace= True)
#print(df)

#   Naveen Venkatesan --> Data Scientist url:https://towardsdatascience.com/scraping-nfl-stats-to-compare-quarterback-efficiencies-4989642e02fe
#   This is where I found a template for how to generate radar charts for comparing nfl quarterbacks


stat_categories = ['Rec','Rec Yds','Rec TD','Yds/Rec','Rec/G','Yds/G']

stats_data_categories = df[['Player','Team'] + stat_categories] 

# Convert data to numerical values
for i in stat_categories:
    stats_data_categories[i] = pd.to_numeric(df[i])

#Displaying new DataFrame that will be used for analyzing stats for radar charts
#st.dataframe(stats_data_categories)

# Create rankings for stat categories
for i in stat_categories:
    stats_data_categories[i + ' Rank'] = stats_data_categories[i].rank(pct=True)

# Viewing our updated stats DataFrame
#print(stats_data_categories.head)

# General plot parameters for radar chart
#mpl.rcParams['font.family'] = 'Avenir'
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

# Function to get Receiving data
def get_rec_data(data, team):
    return np.asarray(data[data['Team'] == team])[0]

def get_rec_player_data(data, player):
    return np.asarray(data[data['Player'] == player])[0]


# ******************User Input for customized Radar Chart ****************************
# Sidebar User Options based on selected team and player
sorted_unique_team_ = sorted(stats_data_categories.Team.unique())
sorted_unique_players_ = sorted(stats_data_categories.Player.unique())


st.title('Performance Charts')
st.info('Both the Team and Player Checkboxes under Chart Preferences on the left sidebar provide customization for which way you would like to view the receiving performance charts. The two options are either by Team or by Player. The choice is yours.')


st.sidebar.subheader('Chart Perference(s):')
if st.sidebar.checkbox('Team(s)'):
    st.subheader('Team Receiving Performance:')
    user_input_demo_ = st.sidebar.selectbox('Team(s):', sorted_unique_team_)
    st.sidebar.info('Select a team from the left sidebar that you want to view the receiving performance from their best receiver to see how they stacked up for the season!')

    # Create figure based on Team #################################################################################################
    fig = plt.figure(figsize=(8, 8), facecolor='white')# Add subplots
    ax1 = fig.add_subplot(221, projection='polar', facecolor='#ededed')
    plt.subplots_adjust(hspace=0.8, wspace=0.5)# Get RB data
    data_demo = get_rec_data(stats_data_categories, user_input_demo_)# Plot RB data
    if user_input_demo_ not in team_colors:
        ax1 = create_radar_chart(ax1, angles, data_demo, color='grey')
    else:
        ax1 = create_radar_chart(ax1, angles, data_demo, team_colors[user_input_demo_])
    st.pyplot(fig)
    st.write('As displayed above, the main points of emphasis that I have selected to compare for the receivers in regards to the receiving game are: Rec, Rec Yds, Rec TD, Yds/Rec, Rec/G, Yds/G. The greater the height and shape of one category, the better the player was in that category.')
    
    # DataFrame for Team Rushing Rankings
    Team_Ranks_df = stats_data_categories.loc[stats_data_categories['Team']==user_input_demo_]
    st.subheader(user_input_demo_)
    st.dataframe(Team_Ranks_df)
    #if st.checkbox('Team_Table'):
    #    st.table(Team_Ranks_df)



# Created Figure for Player ###########################################################################################################
if st.sidebar.checkbox('Player(s)'):
    st.subheader('Player Search:')
    user_input_demo_player_ = st.sidebar.selectbox('Player(s):', sorted_unique_players_)
    st.sidebar.info('Have a certain receiver in mind? Select a player that you want to view the receiving performance for to see how they stacked up for the season!')

    # Unique Player Create Figure
    fig_player = plt.figure(figsize=(8, 8), facecolor='white')# Add subplots
    ax2 = fig_player.add_subplot(222, projection='polar', facecolor='#ededed')
    data_demo_player = get_rec_player_data(stats_data_categories, user_input_demo_player_)# Plot RB data
    
    if user_input_demo_player_:
        if st.sidebar.checkbox('Custom Color'):
            st.info('You can type in a color to customize the radar chart to your liking. Blue, Teal, Red perhaps? Just enter it to give it a try. Note: The default color is blue if text is left empty.')
            custom_color = st.sidebar.text_input("Enter a custom color for chart")
            if not custom_color:
                default = 'blue'
                custom_color=default
            ax2 = create_radar_chart(ax2, angles, data_demo_player, color=custom_color)
        else:
            ax2 = create_radar_chart(ax2, angles, data_demo_player)
        st.pyplot(fig_player)
        st.write('As displayed above, the main points of emphasis that I have selected to compare for the receivers in regards to the receiving game are: Rec, Rec Yds, Rec TD, Yds/Rec, Rec/G, Yds/G. The greater the height and shape of one category, the better the player was in that category.')
        
        # DataFrame for Team Passing Rankings
        Player_Ranks_df = stats_data_categories.loc[stats_data_categories['Player']==user_input_demo_player_]
        st.subheader(user_input_demo_player_ + ' Receiving Stats W/ Ranking Percent Per Category')
        st.dataframe(Player_Ranks_df)

# Player Comparisons ###################################################################################
if st.sidebar.checkbox('Player(s) Comparison ** Bonus **'):
    user_input_demo_player_1 = st.sidebar.selectbox('Receiver 1:', sorted_unique_players_)
    user_input_demo_player_2 = st.sidebar.selectbox('Receiver 2:', sorted_unique_players_)
    st.sidebar.info('Have a certain few Receivers in mind? Select two Rushers that you want to view the receiving performance for to see how they stacked up for the season in comparison to each other!')

    # Unique Two Players Create Figure
    fig_players = plt.figure(figsize=(15, 15), facecolor='white')
    ax_player_1 = fig_players.add_subplot(221, projection='polar', facecolor='#ededed')
    ax_player_2 = fig_players.add_subplot(222, projection='polar', facecolor='#ededed')
    data_demo_player1 = get_rec_player_data(stats_data_categories, user_input_demo_player_1)
    data_demo_player2 = get_rec_player_data(stats_data_categories, user_input_demo_player_2)
    
    
    if user_input_demo_player_1:
        if st.sidebar.checkbox('Custom Color'):
            custom_color = st.sidebar.text_input("Enter a custom color for chart")
            st.sidebar.info('You can type in a color to customize the radar chart to your liking. Blue, Teal, Red perhaps? Just enter it to give it a try. Note: The default color is blue if text is left empty.')
            if not custom_color:
                default = 'blue'
                custom_color=default
            ax_player_1 = create_radar_chart(ax_player_1, angles, data_demo_player1, color=custom_color)
            ax_player_2 = create_radar_chart(ax_player_2, angles, data_demo_player2, color=custom_color)
        else:
            ax_player_1 = create_radar_chart(ax_player_1, angles, data_demo_player1)
            ax_player_2 = create_radar_chart(ax_player_2, angles, data_demo_player2)
        st.pyplot(fig_players)
        
        # DataFrame for Team Passing Rankings
        Player_Ranks_1 = stats_data_categories.loc[stats_data_categories['Player']==user_input_demo_player_1]
        Player_Ranks_2 = stats_data_categories.loc[stats_data_categories['Player']==user_input_demo_player_2]

        st.subheader(user_input_demo_player_1 + ' Receiving Stats W/ Ranking Percent Per Category')
        st.dataframe(Player_Ranks_1)

        st.subheader(user_input_demo_player_2 + ' Receiving Stats W/ Ranking Percent Per Category')
        st.dataframe(Player_Ranks_2)


# Team Comparisons ###############################################################################################
if st.sidebar.checkbox('Team(s) Comparison ** Bonus **'):
    user_input_demo_team_1 = st.sidebar.selectbox('Team 1:', sorted_unique_team_)
    user_input_demo_team_2 = st.sidebar.selectbox('Team 2:', sorted_unique_team_)
    st.sidebar.info('Have a certain few Teams in mind? Select two teams that you want to view the receiving performance for to see how they stacked up for the season in comparison to each other!')

    # Unique Teams Create Figure
    fig_teams = plt.figure(figsize=(15, 15), facecolor='white')
    ax_team_1 = fig_teams.add_subplot(221, projection='polar', facecolor='#ededed')
    ax_team_2 = fig_teams.add_subplot(222, projection='polar', facecolor='#ededed')
    data_demo_team1 = get_rec_data(stats_data_categories, user_input_demo_team_1)# Plot QB data
    data_demo_team2 = get_rec_data(stats_data_categories, user_input_demo_team_2)
    
    
    if user_input_demo_team_1:
        if user_input_demo_team_1 not in team_colors:
            default = 'grey'
            custom_color=default
            ax_team_1 = create_radar_chart(ax_team_1, angles, data_demo_team1, color=custom_color)
        else:
            ax_team_1 = create_radar_chart(ax_team_1, angles, data_demo_team1, team_colors[user_input_demo_team_1])

    if user_input_demo_team_2:
        if user_input_demo_team_2 not in team_colors:
            default = 'grey'
            custom_color=default
            ax_team_2 = create_radar_chart(ax_team_2, angles, data_demo_team2, color=custom_color)
        else:
            ax_team_2 = create_radar_chart(ax_team_2, angles, data_demo_team2, team_colors[user_input_demo_team_2])

    st.pyplot(fig_teams)
    st.write('As displayed above, the main points of emphasis that I have selected to compare for the receivers in regards to the receiving game are: Rec, Rec Yds, Rec TD, Yds/Rec, Rec/G, Yds/G. The greater the height and shape of one category, the better the player was in that category.')

    # DataFrame for Team Rushing Rankings
    Team_Ranks_1 = stats_data_categories.loc[stats_data_categories['Team']==user_input_demo_team_1]
    Team_Ranks_2 = stats_data_categories.loc[stats_data_categories['Team']==user_input_demo_team_2]

    st.subheader(user_input_demo_team_1)
    st.dataframe(Team_Ranks_1)

    st.subheader(user_input_demo_team_2)
    st.dataframe(Team_Ranks_2)


# **************** Ranking(s) **************************************
# ['Rec','Rec Yds','Rec TD','Yds/Rec','Rec/G','Yds/G']


st.title('Receiving Rankings')
st.markdown("""
Ranking the Receivers of this season based on the criteria of Receptions, Receiving Yards, Receiving TD, Receiving Yards Per Reception, Receptions Per Game, Yards Per Game!
I will use a formula that fits the criteria mentioned to rank the receivers.
""")

# Equation for rankings:
# Receiving Ranking = (50)Rec Yards + (10)Rec + (10)Rec TD + (10)Yds/Rec + (10)Rec/G + (10)Yds/G

st.latex('Receiving Ranking = (40)Rec Yds + (15)Rec + (20)Rec TD + (10)Yds/Rec + (5)Rec/G + (10)Yds/G')

if selected_year >= 1932 and selected_year < 1940:
    rankings_df = stats_data_categories.head(15)
if selected_year >= 1940 and selected_year < 1950:
    rankings_df = stats_data_categories.head(32)
else:
    rankings_df = stats_data_categories.head(50)
st.caption('A DataFrame of the Receivers in regards to Receptions (Depicted Below)')
st.dataframe(rankings_df)


# ['Rec','Rec Yds','Rec TD','Yds/Rec','Rec/G','Yds/G']
for i in rankings_df:
    if i == 'Rec Rank':
        rec_perc_type = rankings_df[i].astype(float)
        rec_rank_value = rec_perc_type * 15
        #st.write(att_rank_value)
    if i == 'Rec Yds Rank':
        rec_yds_type = rankings_df[i].astype(float)
        rec_yds_rank_value = rec_yds_type * 40
        #st.write(rush_yds_rank_value)
    if i == 'Rec TD Rank':
        rec_td_type = rankings_df[i].astype(float)
        rec_td_value = rec_td_type * 20
        #st.write(rush_td_value)
    if i == 'Yds/Rec Rank':
        yds_per_rec_perc_type = rankings_df[i].astype(float)
        yds_per_rec_rank_value = yds_per_rec_perc_type * 10
        #st.write(yds_att_rank_value)
    if i == 'Rec/G Rank':
        rec_per_g_type = rankings_df[i].astype(float)
        rec_per_g_rank_value = rec_per_g_type * 5
        #st.write(yds_att_rank_value)        
    if i == 'Yds/G Rank':
        yds_g_type = rankings_df[i].astype(float)
        yds_g_rank_value = yds_g_type * 10
        #st.write(yds_g_rank_value)
    
rankings_df['Player Rating'] = rec_rank_value + rec_yds_rank_value + rec_td_value + yds_per_rec_rank_value + rec_per_g_rank_value + yds_g_rank_value
player_ratings = rankings_df[[ 'Player','Player Rating']]
player_ratings = player_ratings.sort_values(by=['Player Rating'], ascending=False)

# Display ratings in descending order for players under the receiving stats category
#st.caption('A DataFrame of the Top 32 Receivers sorted by Player Rating, which was calculated based on the Receiving Ranking Formula.')
#st.dataframe(player_ratings)

if selected_year >= 1932 and selected_year < 1940:
    col1, col2 = st.columns(2)
    # Top 10 Rushers 
    col1.subheader('Top 5 Rated Receivers')
    top = player_ratings.head(5)
    col1.dataframe(top)

    # Bottom 10 Rushers 
    col2.subheader('Bottom 10 Rated Receivers')
    bottom = player_ratings.tail(10)
    col2.dataframe(bottom)

if selected_year >= 1940 and selected_year < 1950:
    col1, col2, col3 = st.columns(3)
    # Top 10 Rushers 
    col1.subheader('Top 10 Rated Receivers')
    top = player_ratings.head(10)
    col1.dataframe(top)

    # Average (Middle of The Pack) Rushers
    col2.subheader('"Middle Of The Pack" Rated Receivers')
    middle = player_ratings[10:22]
    col2.dataframe(middle)
    #st.dataframe(player_ratings[10:22])

    # Bottom 10 Rushers 
    col2.subheader('Bottom 10 Rated Receivers')
    bottom = player_ratings.tail(10)
    col2.dataframe(bottom)


if selected_year >= 1950:

    # Making the dataframe(s) based on top, middle, bottom classifications prettier
    col1, col2, col3 = st.columns(3)
    
    # Top 10 Rushers 
    col1.subheader('Top 10 Rated Receivers')
    top = player_ratings.head(10)
    col1.dataframe(top)
    #st.dataframe(player_ratings.head(10))

    # Average (Middle of The Pack) Rushers
    col2.subheader('"Middle Of The Pack" Rated Receivers')
    middle = player_ratings[10:40]
    col2.dataframe(middle)
    #st.dataframe(player_ratings[10:22])   

    # Bottom 10 Rushers 
    col3.subheader('Bottom 10 Rated Receivers')
    bottom = player_ratings.tail(10)
    col3.dataframe(bottom)
    #st.dataframe(player_ratings.tail(10))

