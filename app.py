from pandas._config.config import reset_option
import streamlit as st
import NFL_QB_Season_2021_Stats
import Passing_Stats_Passer_Rating_Era
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

# Page Configuration
st.set_page_config(
    page_title="NFL Position Performance Metrics",
    layout="centered",
    initial_sidebar_state="expanded",
)


st.title('Pro Football Performance Metric')
st.sidebar.title('Pro Football Statistics')


Pages = {"Passing Stats (Modern Era)": NFL_QB_Season_2021_Stats,
         "Passing Stats (Passer Rating Era)": Passing_Stats_Passer_Rating_Era
        }
selection = st.sidebar.selectbox("Select One Of The Following Individual Categories",list(Pages.keys()))
page = Pages[selection]

if page:
    page.app()