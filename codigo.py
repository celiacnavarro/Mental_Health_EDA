import sys 
from classes import DataInfo

import numpy as np
import pandas as pd
import geopandas as gpd

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

#Primer dataset
disorders = pd.read_csv('data/prevalence-by-mental-and-substance-use-disorder.csv')
a = DataInfo(disorders)
a.clean()
disorders.columns= ['Country', 'Year', 'Schizophrenia', 'Bipolar','ED', 'Anxiety','Drugs', 'Depression','Alcohol']
a_cont = a.dfcont()
a_inc = a.dfincome()

#Segundo dataset
depresion = pd.read_csv('data/share-with-depression.csv')
b = DataInfo(depresion)
b.clean()
depresion.columns= ['Country', 'Year','Dep_prev']
b_cont = b.dfcont()
b_inc = b.dfincome()

#Tercer dataset
depresion_sex = pd.read_csv('data/prevalence-of-depression-males-vs-females.csv')
c = DataInfo(depresion_sex)
c.clean()
depresion_sex.drop(columns=['Continent','Population (historical estimates)'], inplace=True)
depresion_sex.columns= ['Country', 'Year','Male_dep', 'Female_dep']
c_cont = c.dfcont()
c_inc = c.dfincome()

#Cuarto dataset
total = pd.read_csv('data/share-with-mental-and-substance-disorders.csv')
d = DataInfo(total)
d.clean()
total.columns= ['Country', 'Year', 'Total_prev']
d_cont = d.dfcont()
d_inc = d.dfincome()

#Quinto dataset
total_sex = pd.read_csv('data/share-with-mental-or-substance-disorders-by-sex.csv')
e = DataInfo(total_sex)
e.clean()
total_sex.drop(columns=['Continent','Population (historical estimates)'], inplace=True)
total_sex.columns= ['Country', 'Year', 'Male_total', 'Female_total']

# Relacionamos los datasets agrupados por continente
df_cont = pd.merge(a_cont, b_cont)
df_cont = pd.merge(df_cont, c_cont)
df_cont = pd.merge(df_cont, d_cont)

# Relacionados los datasets agrupados por ingresos
df_inc = pd.merge(a_inc, b_inc)
df_inc = pd.merge(df_inc, c_inc)
df_inc = pd.merge(df_inc, d_inc)

#Gráfico de barras por continentes
plot_df = (df_cont
               .groupby('Continent')
               .mean()
               .reset_index()
               .drop(columns=['Year'])
               .melt(id_vars='Continent')
          )


fig = px.bar(plot_df, x='variable', y='value',
             color='Continent', barmode='group',
             title='Salud mental por continentes',
             height=400)

fig.update_layout(    
    yaxis_title='Prevalencia en %',
    font_size=18,
)
fig.show()

# Gráfico de líneas por años

disorders_year = (disorders
     .groupby('Year')
     .sum()
     .reset_index()
)
disorders_year = (disorders_year
                        .melt(id_vars='Year')
                        .rename(columns={'variable':'disorder', 'value':'share'})
                )

fig = px.line(disorders_year, x='Year', y='share', color='disorder', markers=True,
             title='Salud mental a lo largo del tiempo',
             height=400)

fig.update_layout(    
    yaxis_title='Prevalencia en %',
    xaxis_title='Año',
    font_size=18,
)
fig.show()

#Correlaciones entre trastornos mentales

a = disorders.corr()
sns.heatmap(a)

# Prevalencia de trastornos mentales por nivel de ingresos

sns.scatterplot(df_inc, x='Income', y='Total_prev')
plt.xticks(rotation=-45)




