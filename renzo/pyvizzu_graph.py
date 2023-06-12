from streamlit.components.v1 import html
import ssl
import streamlit as st
import pandas as pd
from ipyvizzu import Chart, Data, Config, Style, DisplayTarget


data = Data()

df = pd.read_csv('/home/ricorenzo/code/renzorico/speeches-at-UN/raw_data/data_st.csv')
chart = Chart()
chart.animate(data,
   Config({
            'x': 'year',
            'y': 'topic',
            'title': 'UN speeches Topics 1946 - 2022'
        })
)
