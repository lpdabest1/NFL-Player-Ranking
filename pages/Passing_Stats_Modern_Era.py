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


markdown = """This app performs simple webscraping of NFL Football player stats data and creates a radar chart that we will be using as a common metric in order to have a visual representation of the performance done 
by each team (according to the passing category)!
* **Python libraries:** pandas, streamlit, numpy, matplotlib, pillow, beautifulsoup4
* **Data source:** [pro-football-reference.com](https://www.pro-football-reference.com/).
Data is from 2006 to 2022."""

st.markdown(markdown)




# calculating current nfl season as most recent season available to scrape
current_season = 2024
st.sidebar.header('User Customization')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(2006,current_season))))

@st.cache
def scraping_2022_QB_Stats(selected_year):
    players = []


    url = 'https://www.pro-football-reference.com/years/'+ str(selected_year) + '/passing.htm'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
    page = requests.get(url,headers=headers, timeout=2, allow_redirects = True )
    soup = bs(page.content, 'html.parser')
    href_tbody = soup.find_all('tbody')


    for i in href_tbody:
        href_tr_data = i.find_all('tr')
        for i in href_tr_data:
            while True:
                try:
                    #Rank of Player Collected
                    ranking_search = i.find('th', {'data-stat':'ranker'})
                    ranking = ranking_search['csk']

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

                    #QB Record and Percentage Wins for Players Collected
                    qbRec_search = i.find('td',{'data-stat':'qb_rec'})
                    qbRec_percentage = qbRec_search['csk']
                    qbRec = qbRec_search.text       

                    #Passes Completed of Player Collected
                    passes_completed_search = i.find('td',{'data-stat':'pass_cmp'})
                    passes_completed = passes_completed_search.text        

                    #Passes Attempted of Player Collected
                    passes_attempted_search = i.find('td',{'data-stat':'pass_att'})
                    passes_attempted = passes_attempted_search.text       


                    #Completion Percentage of Player Collected
                    completion_percentage_search = i.find('td',{'data-stat':'pass_cmp_perc'})
                    completion_percentage = completion_percentage_search.text         


                    #Passing Yards of Player Collected
                    passing_yards_search = i.find('td',{'data-stat':'pass_yds'})
                    passing_yards = passing_yards_search.text         


                    #Passing Touchdowns of Player Collected
                    passing_touchdowns_search = i.find('td',{'data-stat':'pass_td'})
                    passing_touchdowns = passing_touchdowns_search.text
                

                    #Touchdown Percentage of Player Collected
                    touchdown_percentage_search = i.find('td',{'data-stat':'pass_td_perc'})
                    touchdown_percentage = touchdown_percentage_search.text

                    #Interceptions of Player Collected
                    interceptions_search = i.find('td',{'data-stat':'pass_int'})
                    interceptions = interceptions_search.text


                    #Interception Percentage of Player Collected
                    interception_percentage_search = i.find('td',{'data-stat':'pass_int_perc'})
                    interception_percentage = interception_percentage_search.text


                    #First Downs of Player Collected
                    firstdowns_search = i.find('td',{'data-stat':'pass_first_down'})
                    firstdowns = firstdowns_search.text        

                    #Longest Pass of Player Collected
                    pass_long_search = i.find('td',{'data-stat':'pass_long'})
                    pass_long = pass_long_search.text


                    #Yards per Attempt of Player Collected
                    yards_per_attempt_search = i.find('td',{'data-stat':'pass_yds_per_att'})
                    yards_per_attempt = yards_per_attempt_search.text


                    #Adjusted Yards per Attempt of Players Collected
                    adj_yards_per_attempt_search = i.find('td',{'data-stat':'pass_adj_yds_per_att'})
                    adj_yards_per_attempt = adj_yards_per_attempt_search.text


                    #Yards per Completion of Players Collected
                    yards_per_completion_search = i.find('td',{'data-stat':'pass_yds_per_cmp'})
                    yards_per_completion = yards_per_completion_search.text


                    #Yards per Game
                    yards_per_game_search = i.find('td',{'data-stat':'pass_yds_per_g'})
                    yards_per_game = yards_per_game_search.text


                    #Rating
                    passer_rating_search = i.find('td',{'data-stat':'pass_rating'})
                    passer_rating = passer_rating_search.text


                    #QBR
                    qbr_search = i.find('td',{'data-stat':'qbr'})
                    qbr = qbr_search.text


                    #Sacks
                    sacks_taken_search = i.find('td',{'data-stat':'pass_sacked'})
                    sacks_taken = sacks_taken_search.text


                    #Sack Percentage
                    sacks_taken_percentage_search = i.find('td',{'data-stat':'pass_sacked_perc'})
                    sacks_taken_percentage = sacks_taken_percentage_search.text
    

                    #Sack Yards Loss
                    sack_yards_search = i.find('td',{'data-stat':'pass_sacked_yds'})
                    sack_yards = sack_yards_search.text


                    #Formatting Data Collected
                    player = { "Player": names, "Team": team, "Age": age, "Games Played": games, "Games Started": games_played, "QB-Record": qbRec, "QB Wins Percentage": qbRec_percentage,
                "Passes Completed": passes_completed, "Passes Attempted": passes_attempted, "Completion Percentage": completion_percentage, "Passing Yards": passing_yards, "Passing Touchdowns": passing_touchdowns,
                "Touchdown Percentage": touchdown_percentage, "Interceptions": interceptions, "Interceptions Percentage": interception_percentage, "First Downs": firstdowns, "Longest Pass": pass_long,
                "Yards Per Attempt": yards_per_attempt, "Adjusted Yards Per Attempt": adj_yards_per_attempt, "Yards per Completion": yards_per_completion, "Yards Per Game": yards_per_game,
                "Passer Rating": passer_rating, "QBR": qbr, "Times Sacked": sacks_taken, "Sacked Percentage": sacks_taken_percentage, "Yards Loss (Sack)": sack_yards}
                    #Appending Each player to Players List
                    players.append(player)
        
        
            #print(ranking, names, team, age, games, games_played)
        
                    break
                except:
                    break




    df = pd.DataFrame(players)
    df.to_csv("NFL_Player_QB_Search_without_image.csv")
    #print(df)
    return df
df = scraping_2022_QB_Stats(selected_year)


st.header('Quarterback Passing Statistics')
st.subheader('NFL Season ' + str(selected_year) + ' Passing Statistics')

st.dataframe(df)


df.rename(columns={'Completion Percentage': 'Cmp%',
'Passing Yards': 'Pass Yds', 'Passing Touchdowns':'Pass TD','Touchdown Percentage':'TD%','Interceptions Percentage':'INT%'}, inplace= True)
#print(df)

#   Naveen Venkatesan --> Data Scientist url:https://towardsdatascience.com/scraping-nfl-stats-to-compare-quarterback-efficiencies-4989642e02fe
#   This is where I found a template for how to generate radar charts for comparing nfl quarterbacks
# Stat Categories
# Cmp%, Pass Yds, Passing TDs, TD%, INT, INT%, QBR

#stat_categories = ['Completion Percentage','Passing Yards','Passing Touchdowns','Touchdown Percentage','Interceptions','QBR']
stat_categories = ['Cmp%','Pass Yds','Pass TD','TD%','INT%','QBR']
#stats_data_categories_rankings = df['Cmp%','Pass Yds','Pass TD','TD%','INT','QBR']

stats_data_categories = df[['Player','Team'] + stat_categories] 

# Convert data to numerical values
for i in stat_categories:
    stats_data_categories[i] = pd.to_numeric(df[i])

#Displaying new DataFrame that will be used for analyzing stats for radar charts
#st.dataframe(stats_data_categories)

# Create rankings for stat categories
for i in stat_categories:
    stats_data_categories[i + ' Rank'] = stats_data_categories[i].rank(pct=True)

# reverse the stats of ascension sort for interceptions stat category
stats_data_categories['INT% Rank'] = (1 - stats_data_categories['INT% Rank'])

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

# Function to get QB data
def get_qb_data(data, team):
    return np.asarray(data[data['Team'] == team])[0]

def get_qb_player_data(data, player):
    return np.asarray(data[data['Player'] == player])[0]


# ******************User Input for customized Radar Chart ****************************
# Sidebar User Options based on selected team and player
sorted_unique_team_ = sorted(stats_data_categories.Team.unique())
sorted_unique_players_ = sorted(stats_data_categories.Player.unique())


st.title('Performance Charts')
st.info('Both the Team and Player Checkboxes under Chart Preferences on the left sidebar provide customization for which way you would like to view the passing performance charts. The two options are either by Team or by Player. The choice is yours.')


st.sidebar.subheader('Chart Perference(s):')
if st.sidebar.checkbox('Team(s)'):
    st.subheader('Team Passing Performance: Quarterback')
    user_input_demo_ = st.sidebar.selectbox('Team(s):', sorted_unique_team_)
    st.sidebar.info('Select a team from the left sidebar that you want to view the passing performance from their Quarterback to see how they stacked up for the season!')

    # Create figure based on Team #################################################################################################
    fig = plt.figure(figsize=(8, 8), facecolor='white')# Add subplots
    ax1 = fig.add_subplot(221, projection='polar', facecolor='#ededed')
    plt.subplots_adjust(hspace=0.8, wspace=0.5)# Get QB data
    data_demo = get_qb_data(stats_data_categories, user_input_demo_)# Plot QB data
    if user_input_demo_ not in team_colors:
        ax1 = create_radar_chart(ax1, angles, data_demo, color='grey')
    else:
        ax1 = create_radar_chart(ax1, angles, data_demo, team_colors[user_input_demo_])
    st.pyplot(fig)
    st.write('As displayed above, the main points of emphasis that I have selected to compare for the quarterbacks in regards to the passing game are: Cmp%, Pass Yds, Passing TDs, TD%, INT, INT%, QBR. The greater the height and shape of one category, the better the player was in that category.')
    
    # DataFrame for Team Passing Rankings
    Team_Ranks_df = stats_data_categories.loc[stats_data_categories['Team']==user_input_demo_]
    st.subheader(user_input_demo_)
    st.dataframe(Team_Ranks_df)
    #if st.checkbox('Team_Table'):
    #    st.table(Team_Ranks_df)



# Created Figure for Player ###########################################################################################################
if st.sidebar.checkbox('Player(s)'):
    st.subheader('Player Search:')
    user_input_demo_player_ = st.sidebar.selectbox('Player(s):', sorted_unique_players_)
    st.sidebar.info('Have a certain Quarterback in mind? Select a Quarterback that you want to view the passing performance for to see how they stacked up for the season!')

    # Unique Player Create Figure
    fig_player = plt.figure(figsize=(8, 8), facecolor='white')# Add subplots
    ax2 = fig_player.add_subplot(222, projection='polar', facecolor='#ededed')
    data_demo_player = get_qb_player_data(stats_data_categories, user_input_demo_player_)# Plot QB data
    
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
        st.write('As displayed above, the main points of emphasis that I have selected to compare for the quarterbacks in regards to the passing game are: Cmp%, Pass Yds, Passing TDs, TD%, INT, INT%, QBR. The greater the height and shape of one category, the better the player was in that category.')
        
        # DataFrame for Team Passing Rankings
        Player_Ranks_df = stats_data_categories.loc[stats_data_categories['Player']==user_input_demo_player_]
        st.subheader(user_input_demo_player_ + ' Passing Stats W/ Ranking Percent Per Category')
        st.dataframe(Player_Ranks_df)

# Player Comparisons ###################################################################################
if st.sidebar.checkbox('Player(s) Comparison ** Bonus **'):
    user_input_demo_player_1 = st.sidebar.selectbox('Quarterback 1:', sorted_unique_players_)
    user_input_demo_player_2 = st.sidebar.selectbox('Quarterback 2:', sorted_unique_players_)
    st.sidebar.info('Have a certain few Quarterbacks in mind? Select two Quarterback that you want to view the passing performance for to see how they stacked up for the season in comparison to each other!')

    # Unique Two Players Create Figure
    fig_players = plt.figure(figsize=(15, 15), facecolor='white')
    ax_player_1 = fig_players.add_subplot(221, projection='polar', facecolor='#ededed')
    ax_player_2 = fig_players.add_subplot(222, projection='polar', facecolor='#ededed')
    data_demo_player1 = get_qb_player_data(stats_data_categories, user_input_demo_player_1)# Plot QB data
    data_demo_player2 = get_qb_player_data(stats_data_categories, user_input_demo_player_2)
    
    
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
        #st.write('As displayed above, the main points of emphasis that I have selected to compare for the quarterbacks in regards to the passing game are: Cmp%, Pass Yds, Passing TDs, TD%, INT, INT%, QBR. The greater the height and shape of one category, the better the player was in that category.')
        
        # DataFrame for Team Passing Rankings
        Player_Ranks_1 = stats_data_categories.loc[stats_data_categories['Player']==user_input_demo_player_1]
        Player_Ranks_2 = stats_data_categories.loc[stats_data_categories['Player']==user_input_demo_player_2]

        st.subheader(user_input_demo_player_1 + ' Passing Stats W/ Ranking Percent Per Category')
        st.dataframe(Player_Ranks_1)

        st.subheader(user_input_demo_player_2 + ' Passing Stats W/ Ranking Percent Per Category')
        st.dataframe(Player_Ranks_2)


# Team Comparisons ###############################################################################################
if st.sidebar.checkbox('Team(s) Comparison ** Bonus **'):
    user_input_demo_team_1 = st.sidebar.selectbox('Team 1:', sorted_unique_team_)
    user_input_demo_team_2 = st.sidebar.selectbox('Team 2:', sorted_unique_team_)
    st.sidebar.info('Have a certain few Teams in mind? Select two teams that you want to view the passing performance for to see how they stacked up for the season in comparison to each other!')

    # Unique Teams Create Figure
    fig_teams = plt.figure(figsize=(15, 15), facecolor='white')
    ax_team_1 = fig_teams.add_subplot(221, projection='polar', facecolor='#ededed')
    ax_team_2 = fig_teams.add_subplot(222, projection='polar', facecolor='#ededed')
    data_demo_team1 = get_qb_data(stats_data_categories, user_input_demo_team_1)# Plot QB data
    data_demo_team2 = get_qb_data(stats_data_categories, user_input_demo_team_2)
    
    
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
    st.write('As displayed above, the main points of emphasis that I have selected to compare for the quarterbacks in regards to the passing game are: Cmp%, Pass Yds, Passing TDs, TD%, INT%, QBR. The greater the height and shape of one category, the better the player was in that category.')

    # DataFrame for Team Passing Rankings
    Team_Ranks_1 = stats_data_categories.loc[stats_data_categories['Team']==user_input_demo_team_1]
    Team_Ranks_2 = stats_data_categories.loc[stats_data_categories['Team']==user_input_demo_team_2]

    st.subheader(user_input_demo_team_1)
    st.dataframe(Team_Ranks_1)

    st.subheader(user_input_demo_team_2)
    st.dataframe(Team_Ranks_2)


# **************** Ranking(s) **************************************
# ['Cmp%','Pass Yds','Pass TD','TD%','INT','QBR']
means_rankings = []
mean_cmp = stats_data_categories['Cmp%'].mean()
mean_pass_yds = stats_data_categories['Pass Yds'].mean()
mean_pass_td = stats_data_categories['Pass TD'].mean()
mean_pass_td_percent = stats_data_categories['TD%'].mean()
mean_int_percent = stats_data_categories['INT%'].mean()
mean_qbr = stats_data_categories['QBR'].mean()


st.title('Quarterback Rankings')
st.markdown("""
Ranking the Quarterbacks of this season based on the criteria of Completion Percentage, Passing Yards, Passing Touchdowns, Touchdown Percentage, Interception Percentage, and QBR!
I will use a formula that fits the criteria mentioned to rank the quarterbacks.
""")

# Equation for rankings:
# QB Ranking = (50)QBR + (50)Cmp% + (50)Pass Yds + (50)Pass TD + (50)TD% + (50)INT%

st.latex('QB Ranking = (50)QBR + (10)Cmp Percentage + (10)Pass Yds + (10)Pass TD + (10)Pass TD Percentage + (10)INT Percentage')

rankings_df = stats_data_categories.head(32)
st.caption('A DataFrame of the Top 32 Quarterbacks in regards to Passing Yards (Depicted Below)')
st.dataframe(rankings_df)

for i in rankings_df:
    if i == 'Cmp% Rank':
        cmp_perc_type = rankings_df[i].astype(float)
        cmp_rank_value = cmp_perc_type * 10
        #st.write(cmp_rank_value)
    if i == 'Pass Yds Rank':
        pass_yds_type = rankings_df[i].astype(float)
        pass_yds_rank_value = pass_yds_type * 10
        #st.write(pass_yds_rank_value)
    if i == 'Pass TD Rank':
        pass_td_type = rankings_df[i].astype(float)
        pass_td_value = pass_td_type * 10
        #st.write(pass_td_value)
    if i == 'TD% Rank':
        td_perc_type = rankings_df[i].astype(float)
        td_perc_rank_value = td_perc_type * 10
        #st.write(td_perc_rank_value)
    if i == 'INT% Rank':
        int_perc_type = rankings_df[i].astype(float)
        int_perc_rank_value = int_perc_type * 10
        #st.write(int_perc_rank_value)
    if i == 'QBR Rank':
        QBR_type = rankings_df[i].astype(float)
        QBR_rank_value = QBR_type * 50
        #st.write(QBR_rank_value)
    
rankings_df['Player Rating'] = cmp_rank_value + pass_yds_rank_value + pass_td_value + td_perc_rank_value + int_perc_rank_value + QBR_rank_value
player_ratings = rankings_df[[ 'Player','Player Rating']]
player_ratings = player_ratings.sort_values(by=['Player Rating'], ascending=False)

# Display ratings in descending order for players under the passing stats category
#st.caption('A DataFrame of the Top 32 Quarterbacks sorted by Player Rating, which was calculated based on the QBRanking Formula.')
#st.dataframe(player_ratings)


# Making the dataframe(s) based on top, middle, bottom classifications prettier
col1, col2, col3 = st.columns(3)

# Top 10 Quarterbacks 
col1.subheader('Top 10 Rated Quarterbacks')
top = player_ratings.head(10)
col1.dataframe(top)
#st.dataframe(player_ratings.head(10))

# Average (Middle of The Pack) Quarterbacks
col2.subheader('"Middle Of The Pack" Rated Quarterbacks')
middle = player_ratings[10:22]
col2.dataframe(middle)
#st.dataframe(player_ratings[10:22])   

# Bottom 10 Quarterbacks 
col3.subheader('Bottom 10 Rated Quarterbacks')
bottom = player_ratings.tail(10)
col3.dataframe(bottom)
#st.dataframe(player_ratings.tail(10))

