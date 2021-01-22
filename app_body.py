import warnings

import folium
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
from streamlit import caching

def introduction():
    st.write('')
    st.subheader('Introduction')
    st.write('-----------------------------------------------------------------------') 
    st.write('Determine the resources allocated (MOOE, Number of Rooms) to different Student-Teacher Ratio clusters.')
    # st.write('For this purpose, we will define the behavior of customers and we will put the customers into same '             'groups who exhibit common behaviors and then we will try to develop sales and marketing techniques '             'specific to these groups:')
    # st.markdown('<b style="margin-left:7%">PROFIT </b> (to increase) = <b>REVENUE</b> (to increase) - <b>COST</b> (to decrease)'
    #             , unsafe_allow_html=True)
    # st.write('However, there are a lot of things that the company does not know with regard to its own business. '             'First, the company does not know who its customers are. Some of the questions, but not limited to, '             'are: what countries are they from, what do they tend to buy given the choices, and, what day of the '             'week they usually transact? Next problem is the company has little idea what product sells versus what '             'does not sell on a given quarter or season.')


def dataset():
    st.write('')
    st.subheader('Data Information')
    st.write('-----------------------------------------------------------------------') 
    st.write('This is a collection of data sets from DepEd which contains Philippine public school information.')
    
    st.write('')
    st.markdown('<b>Data Sets:</b>', unsafe_allow_html=True)
    dataset_sample = {
                      'Data Set Name': ['Masterlist of Schools', 'Schools Location', 'Number of Rooms', 'Number of Teachers', 'Enrollment Master', 'MOOE'], 
                      'Rows': ['46,603', '46,624', '46,412', '45,040', '46,626', '46,028'],
                      'Columns': ['22', '12', '5', '5', '17', '5'],
                      'Description': ['Masterlist of Public Elementary and Secondary Schools', 'Location of Public Schools', 'Instructional Rooms in Public Elementary and Secondary Schools', 'Masterlist of Public School Teachers', 'Total Enrollment in Public Elementary and Secondary Schools', 'Maintenance and Other Operational Expenses (MOOE) allocation for Public Elementary and Secondary Schools']
                     }
    
    st.table(dataset_sample)

def tools():
    st.write('')
    st.subheader('List of Tools')
    st.write('-----------------------------------------------------------------------') 
    image = Image.open('logo/jupyter.png').convert('RGB')
    st.image(image, caption='', width=300, height=150)
    image = Image.open('logo/pandas.png').convert('RGB')
    st.image(image, caption='', width=300, height=150)
    image = Image.open('logo/heroku.jpg').convert('RGB')
    st.image(image, caption='', width=150, height=50)
    image = Image.open('logo/streamlit.png').convert('RGB')
    st.image(image, caption='', width=300, height=150)
    image = Image.open('logo/github.png').convert('RGB')
    st.image(image, caption='', width=300, height=150)
    image = Image.open('logo/scipy.png').convert('RGB')
    st.image(image, caption='', width=300, height=150)
    image = Image.open('logo/seaborn.png').convert('RGB')
    st.image(image, caption='', width=300, height=150)
    image = Image.open('logo/matplotlib.png').convert('RGB')
    st.image(image, caption='', width=300, height=150)
    image = Image.open('logo/numpy.png').convert('RGB')
    st.image(image, caption='', width=300, height=150)


def cleaning():
    caching.clear_cache()
    st.write('')
    st.subheader('Data Cleaning')
    st.write('-----------------------------------------------------------------------') 
    st.write('1. Check Null Values Per Column:')
    
    
    source1 = ColumnDataSource(data=dict(column_values=['InvoiceNo', 'StockCode', 'Description', 'Quantity', 
                                                        'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country'], 
                                         column_null_count=[0, 0, 0, 100, 0, 0, 10000, 0], 
                                         color=['#35193e', '#35193e', '#701f57','#701f57', '#ad1759', '#e13342', 
                                                '#f37651', '#f6b48f']))
    
    null_plot= figure(x_range=['InvoiceNo', 'StockCode', 'Description', 'Quantity', 
                                                        'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country'], plot_height=600, title='Column Null Counts')
    
    null_plot.vbar(x='column_values', top='column_null_count', width=0.5, color='color', 
                   legend_field='column_values', source=source1)
    
    null_plot.xaxis.axis_label = 'Columns'
    null_plot.yaxis.axis_label = 'Null Counts'
    null_plot.xaxis.major_label_orientation = 1.2
    st.bokeh_chart(null_plot)
    
    st.write('Conclusion: We Need To Remove Null Values from CustomerID Column')    

    
    source1 = ColumnDataSource(data=dict(column_values=['InvoiceNo', 'StockCode', 'Description', 'Quantity', 
                                                        'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country'], 
                                         column_null_count=[406829, 406829, 406829, 406829, 406829, 406829, 406829, 406829], 
                                         color=['#35193e', '#35193e', '#701f57','#701f57', '#ad1759', '#e13342', 
                                                '#f37651', '#f6b48f']))
    clean_p= figure(x_range=['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 
                             'CustomerID', 'Country'], plot_height=600, title='Clean Data Count')
    clean_p.vbar(x='column_values', top='column_null_count', width=0.5, color='color', legend_field='column_values', 
           source=source1)
    clean_p.xaxis.axis_label = 'Columns'
    clean_p.yaxis.axis_label = 'Null Counts'
    clean_p.xaxis.major_label_orientation = 1.2
    clean_p.legend.visible = False
    st.bokeh_chart(clean_p)
    
    
    st.write('2. Checking Float Field Minimum And Maximum Values')
    number_data = {
        'Column':  ['Quantity', 'UnitPrice'],
        'Minimum': [-80995, -11062.06],
        'Maximum': [80995, 38970.0]
    }
    
    st.write('Conclusion: We Need To Remove Negative Values from Quantity Column')
    
    st.write('3. Creating Total Amount Column: Quantity * UnitPrice')
    st.write('4. We Need to Convert Invoice Date to Datetime Field')
    st.write('New Data Dimensions: Rows:397924, Columns: 9')
    
    
    dataset_sample = {
                      'InvoiceNo': ['536365', '536365', '536365', '536365', '536365'], 
                      'StockCode': ['85123A', '71053', '84406B', '84029G', '84029E'],
                      'Description': ['WHITE HANGING HEART T-LIGHT HOLDER', 'WHITE METAL LANTERN', 
                                      'CREAM CUPID HEARTS COAT HANGER', 'KNITTED UNION FLAG HOT WATER BOTTLE',
                                     'RED WOOLLY HOTTIE WHITE HEART'],
                      'Quantity': [6, 6, 8, 6, 6],
                      'InvoiceDate': ['2010-12-01 08:26:00', '2010-12-01 08:26:00', '2010-12-01 08:26:00',
                                     '2010-12-01 08:26:00', '2010-12-01 08:26:00'],
                      'UnitPrice': ['2.55', '3,39', '2,75', '3.39', '3,39'],
                      'CustomerID': ['536365', '536365', '536365', '536365', '536365'],
                      'Country': ['United Kingdom', 'United Kingdom','United Kingdom','United Kingdom','United Kingdom'],
                      'Total Amount': ['15.3', '20.34', '22', '20.34', '20.34']
                    }
    
    st.table(dataset_sample)