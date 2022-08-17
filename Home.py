
import streamlit as st
#import pages.Passing_Stats_Modern_Era as Passing_Stats_Modern_Era
#mport pages.Passing_Stats_Past_Era as Passing_Stats_Past_Era
#import pages.Rushing_Stats as Rushing_Stats
#import pages.Receiving_Stats as Receiving_Stats


# Page Configuration
st.set_page_config(
    page_title="NFL Position Performance Metrics",
    page_icon="🏈",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title('Pro Football Performance Metrics')

st.markdown(
"""
**This Data Application Focuses on three main aspects:**
- Web scraper collect the data based on the desired year of the user and the position or "phase of the game.
- The data visualization of the data scraped. The visualizations are in the form of a radar chart, which depicts how well a player performed in a given selected season.
  *Note: This only applies if the player qualified for rankings.*
- The ranking of the players of the selected season based on an equation that I came up with to compare a set of players based on the following categories: Passing, Rushing, Receiving.
"""
)

st.markdown('*Note: Data is from the NFL🏈*')

st.markdown(
"""
**Select one of the pages listed on the left sidebar to continue with this application:**
- [Passing Stats (Modern Era)](Passing_Stats_Modern_Era)
- [Passing Stats (Past Era)](Passing_Stats_Past_Era)
- [Receiving Stats](Receiving_Stats)
- [Rushing Stats](Rushing_Stats)
"""
)

st.info(
"""
I hope you enjoy the fascinating player data (based on position) and the visualizations/rankings accompanying them.
"""    
)