import warnings

import folium
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from PIL import Image
from streamlit import caching
from streamlit_folium import folium_static

import app_body as body

warnings.filterwarnings('ignore')

st.title('Education Analytics')

## Side Bar Information
image = Image.open('eskwelabs.png')
st.sidebar.image(image, caption='', use_column_width=True)
st.sidebar.markdown("<h1 style='text-align: center;margin-bottom:50px'>DS Cohort VI</h1>", unsafe_allow_html=True)

## Create Select Box and options
add_selectbox = st.sidebar.radio(
    "",
    ("Introduction and Problem Statement", "Data Information", "List of Tools", "Data Cleaning", 
    "Exploratory Data Analysis", "Removing Outliers", "Determining Optimal K", "K-Means Clustering", "Insights Derived from Clustering", 
    "Conclusions and Recommendations", "Contributors")
)


if add_selectbox == 'Introduction and Problem Statement':
    body.introduction()

elif add_selectbox == 'Data Information':
    body.dataset()

elif add_selectbox == 'List of Tools':
    body.tools()

elif add_selectbox == 'Data Cleaning':
    body.cleaning()

elif add_selectbox == 'Exploratory Data Analysis':
    body.eda()

elif add_selectbox == 'Removing Outliers':
    body.outliers()

elif add_selectbox == 'Determining Optimal K':
    body.optimal()

elif add_selectbox == 'K-Means Clustering':
    body.kmeans()

elif add_selectbox == 'Insights Derived from Clustering':
    body.insights()

elif add_selectbox == 'Conclusions and Recommendations':
    body.candr()

elif add_selectbox == 'Contributors':
    body.contributors()