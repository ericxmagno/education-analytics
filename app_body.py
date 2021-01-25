import warnings

import folium
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
import seaborn as sns
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
from streamlit import caching

def introduction():
    st.write('')
    st.header('Problem Statement')
    st.write('-----------------------------------------------------------------------') 
    st.write('Which regions have the best and worst average access to quality education (elementary) based on the ratio of Rooms, Teachers, and MOOE per student?')

def dataset():
    st.write('')
    st.header('Data Information')
    st.write('-----------------------------------------------------------------------') 
    st.write('This project is based on a collection of data sets from DepEd which contains public school information from the Philippines. Additional datasets used are shown in the image below.')
    st.text("")

    st.markdown('<b>Data Sets:</b>', unsafe_allow_html=True)
    image = Image.open('data.png').convert('RGB')
    st.image(image, caption='', width=708, height=600)
    st.write('')

    # st.markdown('<b>Feature Set:</b>', unsafe_allow_html=True)
    # featureset = {
    #                   'Column Name': ['school.classification', 'Schools Location', 'Number of Rooms', 'Number of Teachers', 'Enrollment Master', 'MOOE'], 
    #                   'Rows': ['46,603', '46,624', '46,412', '45,040', '46,626', '46,028'],
    #                   'Columns': ['22', '12', '5', '5', '17', '5'],
    #                   'Description': ['Masterlist of Public Elementary and Secondary Schools', 'Location of Public Schools', 'Instructional Rooms in Public Elementary and Secondary Schools', 'Masterlist of Public School Teachers', 'Total Enrollment in Public Elementary and Secondary Schools', 'Maintenance and Other Operational Expenses (MOOE) allocation for Public Elementary and Secondary Schools']
    #                  }
    # st.table(featureset)

def tools():
    st.write('')
    st.header('List of Tools')
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
    st.header('Data Cleaning')
    st.write('-----------------------------------------------------------------------') 
    st.subheader('1. Merge all dataframes:')

    if st.checkbox('Show code', value=False, key="1"):
        st.code("""
        df_all = pd.concat([df_schools, df_location, df_rooms, df_teachers, df_elementary, df_secondary, df_mooe], axis=1)
        """, language="python")
    df_all = pd.read_pickle("dataframes/df_all.pkl")
    st.write(df_all)
    st.write('')
    
    st.subheader('2. Remove Duplicates:')
    if st.checkbox('Show code', value=False, key="2"):
        st.code("""
        df_all[df_all.index.duplicated(keep=False)]
        """, language="python")
    st.write("No Duplicates in dataframe.")
    st.write('')

    st.subheader('3. Rename Columns:')
    if st.checkbox('Show code', value=False, key="3"):
        st.code("""
        df_all.rename(columns={"Enrolment":"Enrollment"}, inplace=True)
        """, language="python")
    st.write('')

    st.subheader('4. Create Feature Columns:')
    if st.checkbox('Show code', value=False, key="4"):
        st.code("""
        df_all['Total Elementary SPED Students'] = df_all['SPED NG Male'] + df_all['SPED NG Female']
        df_all['Total Secondary SPED Students'] = df_all['SPED NG Male SS'] + df_all['SPED NG Female SS']
        df_all['Total Rooms'] = (df_all['rooms.standard.academic'] + 
                                    df_all['rooms.standard.unused'] + 
                                    df_all['rooms.nonstandard.academic'] + 
                                    df_all['rooms.nonstandard.unused'])
        df_all['Other Teachers'] = (df_all['teachers.instructor'] + 
                                    df_all['teachers.mobile'] + 
                                    df_all['teachers.regular'])
                                   
        df_all['SPED Teachers'] = df_all['teachers.sped']

        df_all['Total Teachers'] = df_all['Other Teachers'] + df_all['SPED Teachers']

        df_all['ST Ratio'] = df_all['Enrollment'] / df_all['Total Teachers']

        df_all['Students per Room Ratio'] = df_all['Enrollment']/df_all['Total Rooms']

        df_all['MOOE per Student Ratio'] = df_all[' school.mooe ']/df_all['Enrollment']

        df_eda = df_all[['school.region','school.classification','ST Ratio','Students per Room Ratio','MOOE per Student Ratio']]
        """, language="python")
    df_all = pd.read_pickle("dataframes/df_eda.pkl")
    st.write(df_all)
    st.write('')

    st.subheader('5. Replace np.inf and -np.inf values with np.nan:')
    if st.checkbox('Show code', value=False, key="5"):
        st.code("""
        df_eda.replace([np.inf, -np.inf], np.nan, inplace=True)
        """, language="python")
    st.write('')

    st.subheader('6. Drop null values:')
    if st.checkbox('Show code', value=False, key="6"):
        st.code("""
        df_clean = df_eda_copy.dropna()
        """, language="python")
    st.write('')

    st.subheader('7. Create an Elementary only dataset:')
    if st.checkbox('Show code', value=False, key="7"):
        st.code("""
        df_elementary = df_clean[df_clean['school.classification']=='Elementary']
        """, language="python")
    st.write('')


def eda():
    caching.clear_cache()
    st.write('')
    st.header('Exploratory Data Analysis')
    st.write('-----------------------------------------------------------------------') 
    st.write('')

    st.subheader("Average Students per Room per Region (Elementary)")
    image = Image.open('figures/elem_ave_stud_per_room.png').convert('RGB')
    st.image(image, caption='', width=900, height=600)
    if st.checkbox('Show code', value=False, key="1"):
        st.code("""
        # indicates if plotting on the figues or on subplots
        plt.figure(figsize=(18,8)) ## size of the figure

        # the main code to create the graph
        sns.barplot(x=df_elementary_grouped2['Students per Room Ratio'], y=df_elementary_grouped2['school.region'],
                    data=df_elementary_grouped2, palette = 'Blues_d')

        # additional elements that can be customzed
        plt.title("Average Students per Room per Region (Elementary)", fontsize=20)
        plt.ylabel("Regions", fontsize=15)
        plt.xlabel("Average Students per Room", fontsize=15)

        plt.axvline(df_elementary_grouped2['Students per Room Ratio'].mean(), linewidth=4, color='y')

        # display graph
        plt.savefig("figures/elem_ave_stud_per_room.png")
        plt.show()
        """, language="python")
    st.markdown('Conclusion: **NCR** is the top region in terms of **average students per room**.')
    st.write('')

    st.subheader("Average Student-Teacher Ratio per Region (Elementary)")
    image = Image.open('figures/elem_ave_stud_per_teacher.png').convert('RGB')
    st.image(image, caption='', width=900, height=600)
    if st.checkbox('Show code', value=False, key="2"):
        st.code("""
        # indicates if plotting on the figues or on subplots
        plt.figure(figsize=(18,8)) ## size of the figure

        # the main code to create the graph
        sns.barplot(x=df_elementary_grouped2['ST Ratio'], y=df_elementary_grouped2['school.region'],
                    data=df_elementary_grouped2, palette = 'Purples_d')

        # additional elements that can be customzed
        plt.title("Average Student-Teacher Ratio per Region (Elementary)", fontsize=20)
        plt.ylabel("Regions", fontsize=15)
        plt.xlabel("Average Student-Teacher Ratio", fontsize=15)

        plt.axvline(df_elementary_grouped2['ST Ratio'].mean(), linewidth=4, color='y')

        # display graph
        plt.savefig("figures/elem_ave_stud_per_teacher.png")
        plt.show()
        """, language="python")
    st.markdown('Conclusion: **Region XII** is the top region in terms of **average student-teacher ratio**.')
    st.write('')

    st.subheader("Average Student-Teacher Ratio per Region (Elementary)")
    image = Image.open('figures/elem_ave_mooe_per_stud.png').convert('RGB')
    st.image(image, caption='', width=900, height=600)
    if st.checkbox('Show code', value=False, key="3"):
        st.code("""
        # indicates if plotting on the figues or on subplots
        plt.figure(figsize=(18,8)) ## size of the figure

        sns.barplot(x=df_elementary_grouped2['MOOE per Student Ratio'], y=df_elementary_grouped2['school.region'],
                    data=df_elementary_grouped2, palette = 'Greens_d')

        # additional elements that can be customzed
        plt.title("Average MOOE per Student per Region (Elementary)", fontsize=20)
        plt.ylabel("Regions", fontsize=15)
        plt.xlabel("Average MOOE per Student", fontsize=15)

        plt.axvline(df_elementary_grouped2['MOOE per Student Ratio'].mean(), linewidth=4, color='y')

        # display graph
        plt.savefig("figures/elem_ave_mooe_per_stud.png")
        plt.show()
        """, language="python")
    st.markdown('Conclusion: **CAR** is the top region in terms of **average MOOE per student**.')
    st.write('')

def outliers():
    caching.clear_cache()
    st.write('')
    st.header('Removing Outliers')
    st.write('-----------------------------------------------------------------------') 
    st.write('')

    st.subheader("Boxplot of df_elementary.melt()")
    image = Image.open('figures/melt.png').convert('RGB')
    st.image(image, caption='', width=700, height=500)
    if st.checkbox('Show code', value=False, key="1"):
        st.code("""
        melted = df_elementary_kmeans.melt()

        sns.boxplot(melted.variable, melted.value)
        plt.savefig("figures/melt.png")
        """, language="python")
    st.write('')

    st.subheader("Remove MOOE outliers")
    if st.checkbox('Show code', value=False, key="2"):
        st.code("""
        #Remove MOOE outliers

        Q1 = df_elementary_kmeans['MOOE per Student Ratio'].quantile(0.25)
        Q3 = df_elementary_kmeans['MOOE per Student Ratio'].quantile(0.75)
        IQR = Q3 - Q1
        df_elementary_kmeans = (df_elementary_kmeans[(df_elementary_kmeans['MOOE per Student Ratio'] >= Q1 - 1.5*IQR) & 
                                (df_elementary_kmeans['MOOE per Student Ratio'] <= Q3 + 1.5*IQR)])
        """, language="python")
    st.write('')

    st.subheader("Remove Student-Teacher Ratio outliers")
    if st.checkbox('Show code', value=False, key="3"):
        st.code("""
        #Remove ST Ratio outliers
        Q1 = df_elementary_kmeans['ST Ratio'].quantile(0.25)
        Q3 = df_elementary_kmeans['ST Ratio'].quantile(0.75)
        IQR = Q3 - Q1
        df_elementary_kmeans = (df_elementary_kmeans[(df_elementary_kmeans['ST Ratio'] >= Q1 - 1.5*IQR) & 
                                (df_elementary_kmeans['ST Ratio'] <= Q3 + 1.5*IQR)])
        """, language="python")
    st.write('')

    st.subheader("Remove Students per Room outliers")
    if st.checkbox('Show code', value=False, key="4"):
        st.code("""
        #Remove MOOE outliers

        #Remove Students per Room Ratio outliers
        Q1 = df_elementary_kmeans['Students per Room Ratio'].quantile(0.25)
        Q3 = df_elementary_kmeans['Students per Room Ratio'].quantile(0.75)
        IQR = Q3 - Q1
        df_elementary_kmeans = (df_elementary_kmeans[(df_elementary_kmeans['Students per Room Ratio'] >= Q1 - 1.5*IQR) & 
                                (df_elementary_kmeans['Students per Room Ratio'] <= Q3 + 1.5*IQR)])
        """, language="python")
    st.write('')

    st.code("""
    print(f"Dropped rows due to outliers: {df_elementary.shape[0] - df_elementary_kmeans.shape[0]}")
    """, language="python")
    st.write('Dropped rows due to outliers: 5411')
    st.code("""
    (df_elementary.shape[0] - df_elementary_kmeans.shape[0]) / df_elementary.shape[0]
    """,language="python")
    st.write('0.15094286989511269')
    st.subheader("~15% of elementary dataset dropped")

def optimal():
    caching.clear_cache()
    st.write('')
    st.header('Determining Optimal K')
    st.write('-----------------------------------------------------------------------') 
    st.write('')

    st.subheader("K-Means Inertia")
    image = Image.open('figures/kmeans_ssd.png').convert('RGB')
    st.image(image, caption='', width=700, height=500)
    if st.checkbox('Show code', value=False, key="1"):
        st.code("""
        from sklearn.cluster import KMeans
        from sklearn.metrics import davies_bouldin_score,silhouette_score,silhouette_samples

        ssd = []
        db={}

        df_elementary_kmeans

        range_n_clusters = list(np.arange(2,16))

        for num_clusters in range_n_clusters:
            kmeans = KMeans(n_clusters=num_clusters)
            kmeans.fit(df_elementary_kmeans_scaled)
            
            ssd.append(kmeans.inertia_)
            db[num_clusters] = davies_bouldin_score(df_elementary_kmeans_scaled,kmeans.labels_)
        
            
        # plot the SSDs for each n_clusters
        plt.plot(ssd,'bx-',c='purple')
        plt.savefig("figures/kmeans_ssd.png")
        """, language="python")
    st.write('')

    st.subheader("Silhouette Score")
    image = Image.open('figures/sscore.png').convert('RGB')
    st.image(image, caption='', width=700, height=500)
    if st.checkbox('Show code', value=False, key="2"):
        st.code("""
        from sklearn.metrics import silhouette_score
        from sklearn.metrics import silhouette_samples
        range_n_clusters = list(np.arange(2,9))

        for num_clusters in range_n_clusters:
            
            # intialise kmeans
            kmeans = KMeans(n_clusters=num_clusters)
            kmeans.fit(df_elementary_kmeans_scaled)
            
            cluster_labels = kmeans.predict(df_elementary_kmeans_scaled)
            
            # silhouette score
            silhouette_avg = silhouette_score(df_elementary_kmeans_scaled, cluster_labels)
            print("For n_clusters={0}, the silhouette score is {1}".format(num_clusters, silhouette_avg))
        """, language="python")
    st.write('')

def kmeans():
    caching.clear_cache()
    st.write('')
    st.header('K-Means Clustering')
    st.write('-----------------------------------------------------------------------') 
    st.write('')

    st.subheader("Feature Set")
    features = pd.read_pickle('dataframes/features.pkl')
    if st.checkbox('Show dataset', value=False, key="1"):
        st.write(features)
    st.write('')

    st.subheader("Use StandardScaler to scale features")
    if st.checkbox('Show code', value=False, key="2"):
        st.code("""
        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler()
        df_elementary_kmeans_scaled = scaler.fit_transform(df_elementary_kmeans)
        """, language="python")
    st.write('')

    st.subheader("Use Kmeans to cluster dataset")
    if st.checkbox('Show code', value=False, key="3"):
        st.code("""
        kmeans = KMeans(n_clusters=5, random_state=42)
        kmeans.fit(df_elementary_kmeans_scaled)
        cluster_labels_1 = kmeans.predict(df_elementary_kmeans_scaled)   

        df_elementary_kmeans['Cluster_Labels'] = cluster_labels_1
        df_elementary_kmeans['Cluster_Labels'].value_counts()
        """, language="python")
    cluster = {
                'Cluster Label': ['1', '0', '4', '3', '2'], 
                'Row Count': ['9842', '8340', '5303', '4630', '2322'],
                }
    st.table(cluster)
    st.write('')

    st.subheader("Scatterplot per Cluster")
    image = Image.open('figures/scatterplot_kmeans.png').convert('RGB')
    st.image(image, caption='', width=900, height=600)
    if st.checkbox('Show code', value=False, key="4"):
        st.code("""
        sns.set_style("whitegrid", {'axes.grid' : False})

        fig = plt.figure(figsize=(15, 10))
        ax = fig.add_subplot(111, projection='3d')

        ST_Ratio = df_elementary_kmeans['ST Ratio']
        Rooms = df_elementary_kmeans['Students per Room Ratio']
        Budget = df_elementary_kmeans['MOOE per Student Ratio']
        Cluster = df_elementary_kmeans['Cluster_Labels']
        ax.scatter(ST_Ratio, Rooms, Budget, s=5, c = Cluster)


        ax.set_xlabel('Student-Teacher Ratio')
        ax.set_ylabel('Students per Room')
        ax.set_zlabel('Budget per Student')

        plt.savefig("figures/scatterplot_kmeans.png")
        plt.show()
        """, language="python")
    st.write('')

    st.subheader("Boxplot per Feature")
    image = Image.open('figures/boxplot_kmeans.png').convert('RGB')
    st.image(image, caption='', width=900, height=600)
    if st.checkbox('Show code', value=False, key="5"):
        st.code("""
        import seaborn as sns
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10,8))

        sns.boxplot(x="Cluster_Labels", y=df_elementary_kmeans["MOOE per Student Ratio"], data=df_elementary_kmeans, ax=axes[0,0])
        axes[0,0].set_title("Budget per Student", fontsize=16)

        sns.boxplot(x=df_elementary_kmeans.Cluster_Labels, y=df_elementary_kmeans["ST Ratio"], ax=axes[0,1])
        axes[0,1].set_title("Student-Teacher Ratio", fontsize=16)

        sns.boxplot(x=df_elementary_kmeans.Cluster_Labels, y=df_elementary_kmeans["Students per Room Ratio"], ax=axes[1,0])
        axes[1,0].set_title("Students per Room", fontsize=16)

        plt.tight_layout()
        plt.savefig("figures/boxplot_kmeans.png")
        plt.show();
        """, language="python")
    st.write('')

    st.subheader("Radarplot per Feature")
    image = Image.open('figures/radar_plot.png').convert('RGB')
    st.image(image, caption='', width=900, height=600)
    if st.checkbox('Show code', value=False, key="6"):
        st.code("""
        my_dpi=100
        plt.figure(figsize=(1000/my_dpi, 1000/my_dpi), dpi=my_dpi)
        plt.subplots_adjust(hspace=0.5)

        # Create a color palette:
        my_palette = plt.cm.get_cmap("Set2", len(df_clusters.index))

        for row in range(0, len(df_clusters.index)):
            make_spider(row=row, 
                        title='Segment '+(df_clusters['Cluster_Labels'][row]).astype(str), 
                        color=my_palette(row))
        plt.savefig("figures/radar_plot.png")
        """, language="python")
    st.write('')

    st.subheader('Conclusion: ')
    st.markdown('- Schools with the **best** metrics are in **Cluster 3** (low ST ratio, low students per room, high mooe per student)')
    st.markdown('- Schools with **worst** metrics are in **Cluster 4** (high ST ratio, high students per room, low mooe per student)')

def insights():
    caching.clear_cache()
    st.write('')
    st.header('Insights Derived from Clustering')
    st.write('-----------------------------------------------------------------------') 
    st.write('')

    st.subheader("Group Best and Worst Clusters Regionally and Provincially")
    if st.checkbox('Show code', value=False, key="1"):
        st.code("""
        df_best = df_elementary_kmeans[df_elementary_kmeans['Cluster_Labels'] == 3]
        df_worst = df_elementary_kmeans[df_elementary_kmeans['Cluster_Labels'] == 4]

        df_best_regions = df_included_schools.loc[list(df_best.index.unique())]
        df_worst_regions = df_included_schools.loc[list(df_worst.index.unique())]

        df_best_regions = df_best_regions.merge(df_schools[['school.province']], how = 'left',
                left_index=True, right_index=True)
        df_worst_regions = df_worst_regions.merge(df_schools[['school.province']], how = 'left',
                left_index=True, right_index=True)
        """, language="python")
    st.write('')

    st.subheader("Insights found from Clustering")
    st.write('')

    image = Image.open('figures/province_best.png').convert('RGB')
    st.image(image, caption='', width=600, height=900)
    if st.checkbox('Show code', value=False, key="3"):
        st.code("""
        temp = df_best_regions['school.province'].value_counts().head()
        temp = [temp.index.tolist()] + [temp.values.tolist()]
        temp = pd.DataFrame({'index':temp[0],'value':temp[1]}).set_index('index', drop=True)

        # indicates if plotting on the figues or on subplots
        plt.figure(figsize=(6,8)) ## size of the figure

        # the main code to create the graph
        sns.barplot(x=temp.index, y=temp.value,
                    data=temp, palette = 'Blues_d')

        # additional elements that can be customzed
        plt.title("Public Schools with the Best Metrics by Province (Elementary)", fontsize=18)
        plt.ylabel("Schools", fontsize=15)
        plt.xlabel("Province", fontsize=15)

        # display graph
        plt.savefig("figures/province_best.png")
        plt.show()
        """, language="python")
    st.write('')

    image = Image.open('figures/province_worst.png').convert('RGB')
    st.image(image, caption='', width=900, height=600)
    if st.checkbox('Show code', value=False, key="2"):
        st.code("""
        temp = df_worst_regions['school.province'].value_counts().head()
        temp = [temp.index.tolist()] + [temp.values.tolist()]
        temp = pd.DataFrame({'index':temp[0],'value':temp[1]}).set_index('index', drop=True)

        # indicates if plotting on the figues or on subplots
        plt.figure(figsize=(10,8)) ## size of the figure

        # the main code to create the graph
        sns.barplot(x=temp.index, y=temp.value,
                    data=temp, palette = 'Blues_d')

        # additional elements that can be customzed
        plt.title("Public Schools with the Worst Metrics by Province (Elementary)", fontsize=18)
        plt.ylabel("Schools", fontsize=15)
        plt.xlabel("Province", fontsize=15)

        # display graph
        plt.savefig("figures/province_worst.png")
        plt.show()
        """, language="python")
    st.write('')

    image = Image.open('figures/region_best.png').convert('RGB')
    st.image(image, caption='', width=900, height=600)
    if st.checkbox('Show code', value=False, key="4"):
        st.code("""
        region_count = df_included_schools['school.region'].value_counts()

        best_region_state = dict()

        temp = df_best_regions['school.region'].value_counts()

        for region in temp.keys():
            best_region_state[region] = temp[region] / region_count[region]

        best_region_state = dict(sorted(best_region_state.items(), key=lambda item: item[1], reverse=True))
        df_best_ratios = pd.DataFrame.from_dict(best_region_state.items())
        df_best_ratios.set_index(0)

        # indicates if plotting on the figues or on subplots
        plt.figure(figsize=(18,8)) ## size of the figure

        # the main code to create the graph
        sns.barplot(x=df_best_ratios[1], y=df_best_ratios[0],
                    data=df_best_ratios, palette = 'Blues_d')

        # additional elements that can be customzed
        plt.title("Public Schools with Best Metrics by Region (Elementary)", fontsize=20)
        plt.ylabel("Regions", fontsize=15)
        plt.xlabel("Percent of Schools in Region", fontsize=15)

        # display graph
        plt.savefig("figures/region_best.png")
        plt.show()
        """, language="python")
    st.write('')

    image = Image.open('figures/region_worst.png').convert('RGB')
    st.image(image, caption='', width=900, height=600)
    if st.checkbox('Show code', value=False, key="5"):
        st.code("""
        region_count = df_included_schools['school.region'].value_counts()

        worst_region_state = dict()

        temp = df_worst_regions['school.region'].value_counts()

        for region in temp.keys():
            worst_region_state[region] = temp[region] / region_count[region]

        worst_region_state = dict(sorted(worst_region_state.items(), key=lambda item: item[1], reverse=True))
        df_worst_ratios = pd.DataFrame.from_dict(worst_region_state.items())
        df_worst_ratios.set_index(0)

        # indicates if plotting on the figues or on subplots
        plt.figure(figsize=(18,8)) ## size of the figure

        # the main code to create the graph
        sns.barplot(x=df_best_ratios[1], y=df_best_ratios[0],
                    data=df_best_ratios, palette = 'Blues_d')

        # additional elements that can be customzed
        plt.title("Public Schools with Best Metrics by Region (Elementary)", fontsize=20)
        plt.ylabel("Regions", fontsize=15)
        plt.xlabel("Percent of Schools in Region", fontsize=15)

        # display graph
        plt.savefig("figures/region_best.png")
        plt.show()
        """, language="python")
    st.write('')

def candr():
    caching.clear_cache()
    st.write('')
    st.header('Conclusions and Recommendations')
    st.write('-----------------------------------------------------------------------') 
    st.write('')

    st.subheader('Conclusion:')
    st.markdown('- Regions with high average number of schools in the **best metric group** are **CAR, Region VIII, and Region I**. Conversely, regions with a high average number of schools in the **worst metric group** are **NCR, Region IV-A, and Region XI.**')
    st.markdown('- **Leyte** is the province with the most schools in the **best metric group**, while **Cebu** is the province with most schools in the **worst metric group**.')

    st.write('')

    st.subheader('Recommendations:')
    st.markdown('- Take a look at the **reasons for schools being in the best and worst metric group** (e.g. overpopulation in the area, school density, funding in the region in comparison to its population)')
    st.markdown('- Take a look at **how metric groups affect NAT scores** (how do the metrics affect nat scores - do low metric schools have low nat scores?)')
    st.markdown('- Take a look at how **different clustering algorithms** affect how the schools were clustered based on the metrics')

def contributors():
    caching.clear_cache()
    st.write('')
    st.header('Contributors')
    st.write('-----------------------------------------------------------------------') 
    st.write('')

    st.subheader('Andrei Gabriel Labayan')
    st.markdown('- Email: ')
    st.markdown('- LinkedIn: [https://www.linkedin.com/in/andrei-gabriel-labayan-48a8ba1a4](https://www.linkedin.com/in/andrei-gabriel-labayan-48a8ba1a4)')

    st.subheader('Eric Vincent Magno')
    st.markdown('- Email: [ericvincentmagno@gmail.com](mailto:ericvincentmagno@gmail.com)')
    st.markdown('- LinkedIn: [https://www.linkedin.com/in/ericxmagno/](https://www.linkedin.com/in/ericxmagno/)')

    st.subheader('Justine Paul Padayao')
    st.markdown('- Email: ')
    st.markdown('- LinkedIn: [https://www.linkedin.com/in/justpaulpadayao/](https://www.linkedin.com/in/justpaulpadayao/)')

    st.subheader('Kaye Janelle Yao')
    st.markdown('- Email: ')
    st.markdown('- LinkedIn: [https://www.linkedin.com/in/kaye-janelle-yao/](https://www.linkedin.com/in/kaye-janelle-yao/)')

    st.subheader('Rhey Ann Magcalas - Mentor')
    st.markdown('- Email: ')
    st.markdown('- LinkedIn: [https://www.linkedin.com/in/rhey-ann-magcalas-47541490/](https://www.linkedin.com/in/rhey-ann-magcalas-47541490/)')