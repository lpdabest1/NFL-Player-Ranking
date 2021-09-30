
import streamlit as st
import NFL_QB_Season_2021_Stats
import Passing_Stats_Passer_Rating_Era
import Passing_Stats_Passer_Rating_Era_Players

# Page Configuration
st.set_page_config(
    page_title="NFL Position Performance Metrics",
    layout="centered",
    initial_sidebar_state="expanded",
)


st.title('Pro Football Performance Metric')
st.sidebar.title('Pro Football Statistics')


Pages = {"Passing Stats (Modern Era)": NFL_QB_Season_2021_Stats,
         "Passing Stats (Passer Rating Era)": Passing_Stats_Passer_Rating_Era,
         "Player Search (Past Era)": Passing_Stats_Passer_Rating_Era_Players
        }
selection = st.sidebar.selectbox("Select One Of The Following Individual Categories",list(Pages.keys()))
page = Pages[selection]

if page:
    page.app()



