from pandas._config.config import reset_option
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

import csv
with open('NFL_Player_QB_Search.csv', 'r') as file_csv:
    read = csv.reader(file_csv)
    for i in read:
        print(i)

nfl_qb_data_season_2021 = pd.read_csv('NFL_Player_QB_Search.csv')  
#print(nfl_qb_data_season_2021)
#nfl_qb_data_season_2021.head()  
#print(nfl_qb_data_season_2021.head())
#print(nfl_qb_data_season_2021.Player_Image)
df = pd.DataFrame(nfl_qb_data_season_2021)
#print(df)

''' Sorting dataframe for customization/user input'''
players_sorted = sorted(df.Player.unique())

user_input = input('Enter a player: ')

selected_player = df[(df.Player.isin(players_sorted))]

if user_input in players_sorted:
    print(user_input, df.loc[df['Player']==user_input])




y = nfl_qb_data_season_2021

x = nfl_qb_data_season_2021.Player_Image


for i in x:
    r = requests.get(i)
    img = Image.open(BytesIO(r.content))
    #img.show()
    
    #img = plt.savefig(i)
    #plt.show()
    #a = plt.imread(i)
    #plt.imshow(img)
    #plt.show(a)
    #plt.savefig(i)
    #Image.open(i)
