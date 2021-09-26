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


def scraping_2021_QB_Stats():
    players = []


    url = 'https://www.pro-football-reference.com/years/2021/passing.htm'
    #url = 'https://www.nfl.com/stats/player-stats/'
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
                    qbRec_search = i.find('td',{'data-stat':'qb_rec'})
                    qbRec_percentage = qbRec_search['csk']
                    qbRec = qbRec_search.text       

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
                    firstdowns_search = i.find('td',{'data-stat':'pass_first_down'})
                    firstdowns = firstdowns_search.text        

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
                    qbr_search = i.find('td',{'data-stat':'qbr'})
                    qbr = qbr_search.text


                    '''Sacks'''
                    sacks_taken_search = i.find('td',{'data-stat':'pass_sacked'})
                    sacks_taken = sacks_taken_search.text


                    '''Sack Percentage'''
                    sacks_taken_percentage_search = i.find('td',{'data-stat':'pass_sacked_perc'})
                    sacks_taken_percentage = sacks_taken_percentage_search.text
    

                    '''Sack Yards Loss'''
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