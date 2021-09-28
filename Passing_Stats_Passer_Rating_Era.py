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
from prettytable import PrettyTable

def app():

    st.markdown("""
    This app performs simple webscraping of NFL Football player stats data and creates a radar chart that we will be using as a common metric in order to have a visual representation of the performance done 
    by each team (according to the passing category)!
    * **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn
    * **Data source:** [pro-football-reference.com](https://www.pro-football-reference.com/).
    Data is from 1932 to 2005.
    """)



    # calculating current nfl season as most recent season available to scrape
    last_passer_rating_season = 2006
    st.sidebar.header('User Customization')
    selected_year = st.sidebar.selectbox('Year', list(reversed(range(1932,last_passer_rating_season))))

    @st.cache
    def scraping_QB_Stats(selected_year):
        players = []


        url = 'https://www.pro-football-reference.com/years/'+ str(selected_year) + '/passing.htm'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
        page = requests.get(url,headers=headers, timeout=2, allow_redirects = True )
        soup = bs(page.content, 'html.parser')
        href = soup.find('table', {'id': 'passing'})
        href_th = soup.find_all('th',{'class':'right'})
        href_tbody = soup.find_all('tbody')
        href_tr = soup.find_all('tr')


        for i in href_tbody:
            href_tr_data = i.find_all('tr')
            for i in href_tr_data:
                while True:
                    try:
                        '''Rank of Player Collected'''
                        ranking_search = i.find('th', {'data-stat':'ranker'})
                        ranking = ranking_search['csk']

                        '''Name of Player Collected'''
                        names_search = i.find('td', {'data-stat':'player'})
                        #names = names_search['csk']
                        names_text = names_search.find('a')
                        names = names_text.text


                        '''Team of PLayer Collected'''
                        team_search = i.find('td', {'data-stat':'team'})
                        team_name = team_search.find('a')
                        team = team_name['title']

                        '''Age of Player Collected '''
                        age_search = i.find('td',{'data-stat':'age'})
                        age = age_search.text

                        '''Games and Games played by Player Collected'''
                        games_search = i.find('td',{'data-stat':'g'})
                        games = games_search.text

                        games_played_search = i.find('td',{'data-stat':'gs'})
                        games_played = games_played_search.text
    
                        '''QB Record and Percentage Wins for Players Collected'''
                        #qbRec_search = i.find('td',{'data-stat':'qb_rec'})
                        #bRec_percentage = qbRec_search['csk']
                        #qbRec = qbRec_search.text       

                        '''Passes Completed of Player Collected'''
                        passes_completed_search = i.find('td',{'data-stat':'pass_cmp'})
                        passes_completed = passes_completed_search.text        
    
                        '''Passes Attempted of Player Collected'''
                        passes_attempted_search = i.find('td',{'data-stat':'pass_att'})
                        passes_attempted = passes_attempted_search.text       


                        '''Completion Percentage of Player Collected'''
                        completion_percentage_search = i.find('td',{'data-stat':'pass_cmp_perc'})
                        completion_percentage = completion_percentage_search.text         


                        '''Passing Yards of Player Collected'''
                        passing_yards_search = i.find('td',{'data-stat':'pass_yds'})
                        passing_yards = passing_yards_search.text         


                        '''Passing Touchdowns of Player Collected'''
                        passing_touchdowns_search = i.find('td',{'data-stat':'pass_td'})
                        passing_touchdowns = passing_touchdowns_search.text
                    

                        '''Touchdown Percentage of Player Collected'''
                        touchdown_percentage_search = i.find('td',{'data-stat':'pass_td_perc'})
                        touchdown_percentage = touchdown_percentage_search.text

                        '''Interceptions of Player Collected'''
                        interceptions_search = i.find('td',{'data-stat':'pass_int'})
                        interceptions = interceptions_search.text


                        '''Interception Percentage of Player Collected'''
                        interception_percentage_search = i.find('td',{'data-stat':'pass_int_perc'})
                        interception_percentage = interception_percentage_search.text


                        '''First Downs of Player Collected'''
                        #firstdowns_search = i.find('td',{'data-stat':'pass_first_down'})
                        #firstdowns = firstdowns_search.text        

                        '''Longest Pass of Player Collected'''
                        pass_long_search = i.find('td',{'data-stat':'pass_long'})
                        pass_long = pass_long_search.text


                        '''Yards per Attempt of Player Collected'''
                        yards_per_attempt_search = i.find('td',{'data-stat':'pass_yds_per_att'})
                        yards_per_attempt = yards_per_attempt_search.text


                        '''Adjusted Yards per Attempt of Players Collected'''
                        adj_yards_per_attempt_search = i.find('td',{'data-stat':'pass_adj_yds_per_att'})
                        adj_yards_per_attempt = adj_yards_per_attempt_search.text


                        '''Yards per Completion of Players Collected'''
                        yards_per_completion_search = i.find('td',{'data-stat':'pass_yds_per_cmp'})
                        yards_per_completion = yards_per_completion_search.text


                        '''Yards per Game'''
                        yards_per_game_search = i.find('td',{'data-stat':'pass_yds_per_g'})
                        yards_per_game = yards_per_game_search.text


                        '''Rating'''
                        passer_rating_search = i.find('td',{'data-stat':'pass_rating'})
                        passer_rating = passer_rating_search.text


                        '''QBR'''
                        #qbr_search = i.find('td',{'data-stat':'qbr'})
                        #qbr = qbr_search.text


                        '''Sacks'''
                        #sacks_taken_search = i.find('td',{'data-stat':'pass_sacked'})
                        #acks_taken = sacks_taken_search.text


                        '''Sack Percentage'''
                        #sacks_taken_percentage_search = i.find('td',{'data-stat':'pass_sacked_perc'})
                        #sacks_taken_percentage = sacks_taken_percentage_search.text
        

                        '''Sack Yards Loss'''
                        #sack_yards_search = i.find('td',{'data-stat':'pass_sacked_yds'})
                        #sack_yards = sack_yards_search.text







                        #Formatting Data Collected
                        player = { "Player": names, "Team": team, "Age": age, "Games Played": games, "Games Started": games_played,
                    "Passes Completed": passes_completed, "Passes Attempted": passes_attempted, "Completion Percentage": completion_percentage, "Passing Yards": passing_yards, "Passing Touchdowns": passing_touchdowns,
                    "Touchdown Percentage": touchdown_percentage, "Interceptions": interceptions, "Interceptions Percentage": interception_percentage, "Longest Pass": pass_long,
                    "Yards Per Attempt": yards_per_attempt, "Adjusted Yards Per Attempt": adj_yards_per_attempt, "Yards per Completion": yards_per_completion, "Yards Per Game": yards_per_game,
                    "Passer Rating": passer_rating}
                        #Appending Each player to Players List
                        players.append(player)
            
            
                #print(ranking, names, team, age, games, games_played)
            
                        break
                    except:
                        break




        df = pd.DataFrame(players)
        df.to_csv("NFL_Player_QB_Search_Passer_Rating_Era.csv")
        #print(df)
        return df
    df = scraping_QB_Stats(selected_year)


    st.header('Quarterback Passing Statistics')
    st.subheader('NFL Season ' + str(selected_year) + ' Passing Statistics')

    st.dataframe(df)



    # Code taken from app.py
    #NFL_QB_Season_2021_Stats.scraping_2021_QB_Stats

    # Read csv with data into a new variable
    #nfl_qb_data_season_2021 = pd.read_csv('NFL_Player_QB_Search_without_image.csv') 
    #print(nfl_qb_data_season_2021)
    #nfl_qb_data_season_2021.head()  
    #print(nfl_qb_data_season_2021.head())
    #print(nfl_qb_data_season_2021.Player_Image)


    # New Method ---> set continue reading df

    #df = pd.DataFrame(nfl_qb_data_season_2021)


    df.rename(columns={'Completion Percentage': 'Cmp%',
    'Passing Yards': 'Pass Yds', 'Passing Touchdowns':'Pass TD','Touchdown Percentage':'TD%','Interceptions':'INT'}, inplace= True)
    #print(df)


    #Pretty Table Import CSV Example
    #from prettytable import from_csv
        
    #with open('NFL_Player_QB_Search.csv', 'r') as fp: 
    #    x = from_csv(fp)
        
    #print(x)

    #tab_df_table = tabulate(df, headers='keys',tablefmt='psql')

    #print(tabulate(df, headers='keys',tablefmt='psql'))


    # Stat Categories
    # Cmp%, Pass Yds, Passing TDs, TD%, INT, INT%, QBR
    #stat_categories = ['Completion Percentage','Passing Yards','Passing Touchdowns','Touchdown Percentage','Interceptions','QBR']
    stat_categories = ['Cmp%','Pass Yds','Pass TD','TD%','INT','Passer Rating']

    stats_data_categories = df[['Player','Team'] + stat_categories] 

    #Displaying new DataFrame that will be used for analyzing stats for radar charts
    #st.dataframe(stats_data_categories)


    #stats_data_categories.head()
    #print(stats_data_categories.dtypes)

    #   Naveen Venkatesan --> Data Scientist url:https://towardsdatascience.com/scraping-nfl-stats-to-compare-quarterback-efficiencies-4989642e02fe
    #   This is where I found a template for how to generate radar charts for comparing nfl quarterbacks

    # Create rankings for stat categories
    for i in stat_categories:
        stats_data_categories[i + ' Rank'] = stats_data_categories[i].rank(pct=True)

    # reverse the stats of ascension sort for interceptions stat category
    stats_data_categories['INT Rank'] = (1 - stats_data_categories['INT Rank'])

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
    # Sidebar User Options based on selected team
    sorted_unique_team_ = sorted(stats_data_categories.Team.unique())
    sorted_unique_players_ = sorted(stats_data_categories.Player.unique())
    user_input_demo_ = st.sidebar.selectbox('Team(s):', sorted_unique_team_)
    user_input_demo_player_ = st.sidebar.selectbox('Player(s):', sorted_unique_players_)

    # Demo: Trial and Error
    # Sidebar - Team selection
    #sorted_unique_team = sorted(stats_data_categories.Team.unique())
    #selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)


    # Sidebar - Player selection
    #sorted_unique_player = sorted(stats_data_categories.Player.unique())
    #selected_player = st.sidebar.multiselect('Player', sorted_unique_player, sorted_unique_player) 

    #df_selection = stats_data_categories[(stats_data_categories.Team.isin(selected_team)) ]
    #st.dataframe(df_selection)
    # Create figure based on Team
    #if len(df_selection) > 0:
    #    for i in df_selection:
    #        fig_demo = plt.figure(figsize=(8, 8), facecolor='white')# Add subplots
    #        ax11 = fig_demo.add_subplot(221, projection='polar', facecolor='#ededed')
    #        plt.subplots_adjust(hspace=0.8, wspace=0.5)# Get QB data
    #        lar_data_demo11 = get_qb_data(stats_data_categories, i)# Plot QB data
    #        ax11 = create_radar_chart(ax11, angles, lar_data_demo11)
            #plt.show()
    #        st.pyplot(fig_demo)    







    # Create figure based on Team
    fig = plt.figure(figsize=(8, 8), facecolor='white')# Add subplots
    ax1 = fig.add_subplot(221, projection='polar', facecolor='#ededed')
    plt.subplots_adjust(hspace=0.8, wspace=0.5)# Get QB data
    lar_data_demo = get_qb_data(stats_data_categories, user_input_demo_)# Plot QB data


    # Testing if team selected does not exist in current team set (team_colors)
    #fig = plt.figure(figsize=(8, 8), facecolor='white')# Add subplots
    #ax1 = fig.add_subplot(221, projection='polar', facecolor='#ededed')
    #plt.subplots_adjust(hspace=0.8, wspace=0.5)# Get QB data
    #lar_data_demo = get_qb_data(stats_data_categories, user_input_demo_)# Plot QB data
    ax1 = create_radar_chart(ax1, angles, lar_data_demo, team_colors[user_input_demo_])
    #plt.show()
    st.pyplot(fig)


    # Unique Player Create Figure
    fig_player = plt.figure(figsize=(8, 8), facecolor='white')# Add subplots
    ax2 = fig_player.add_subplot(222, projection='polar', facecolor='#ededed')
    #plt.subplots_adjust(hspace=0.8, wspace=0.5)# Get QB data
    lar_data_demo1 = get_qb_player_data(stats_data_categories, user_input_demo_player_)# Plot QB data
    
    if user_input_demo_player_:
        if st.sidebar.checkbox('Custom Color'):
            custom_color = st.sidebar.text_input("Enter a custom color for chart")
            if not custom_color:
                default = 'blue'
                custom_color=default
            ax2 = create_radar_chart(ax2, angles, lar_data_demo1, color=custom_color)
        else:
            ax2 = create_radar_chart(ax2, angles, lar_data_demo1)
        #plt.show()
        st.pyplot(fig_player)