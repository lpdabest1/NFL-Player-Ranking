
import streamlit as st
import Passing_Stats_Modern_Era
import Passing_Stats_Past_Era
import Rushing_Stats

# Page Configuration
st.set_page_config(
    page_title="NFL Position Performance Metrics",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.title('Pro Football Performance Metric')
st.sidebar.title('Pro Football Statistics')


Pages = {"Passing Stats (Modern Era)": Passing_Stats_Modern_Era,
         "Passing Stats (Past Era)": Passing_Stats_Past_Era,
         "Rushing Stats": Rushing_Stats
        }
selection = st.sidebar.selectbox("Select One Of The Following Individual Categories",list(Pages.keys()))
page = Pages[selection]

if page:
    page.app()



