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
depresion_sex.dropna(inplace=True)

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
total_sex.dropna(inplace=True)


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
               .drop(columns=['Year', 'Dep_prev', 'Male_dep', 'Female_dep'])
               .melt(id_vars='Continent')
          )


fig = px.bar(plot_df, x='variable', y='value',
             color='Continent', barmode='group',
             title='Salud mental por continentes')

fig.update_layout(    
    yaxis_title='Prevalencia en %',
    xaxis_title='',
    legend_title='Continentes',
    font_size=14,
)
fig.show()

fig.write_image("images/fig1.png")


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
             title="Salud mental a lo largo del tiempo")

fig.update_layout(    
    yaxis_title="Prevalencia en %",
    xaxis_title="Año",
    legend_title='Trastornos mentales',
    font_size=18,
)
fig.show()
fig.write_image("images/fig2.png")


#Correlaciones entre trastornos mentales

a = disorders.corr()
a.drop(columns='Year', inplace=True)
axis_labels = ['Esquizofrenia', 'Bipolar', 'TCA', 'Ansiedad', 'Drogas', 'Depresión', 'Alcohol'] # labels for x-axis
ax = plt.axes()
ax.set_title('Correlación entre trastornos mentales')
plt.xticks(rotation=-45);

heatmap = sns.heatmap(a[1:], ax=ax, xticklabels=axis_labels, yticklabels=axis_labels, annot=True)
plt.show()
fig = heatmap.get_figure()
fig.savefig("images/fig3.png", bbox_inches='tight')

# Prevalencia de trastornos mentales por nivel de ingresos

x_labels = ['Clase alta', 'Clase baja', 'Clase media-baja', 'Clase media-alta'] # labels for x-axis

sns.catplot(x="Income", y="Total_prev", kind="box", data=df_inc);
plt.title('Salud mental y nivel de ingresos')
plt.xticks(ticks=[0,1,2,3],labels=x_labels,rotation=-45)
plt.xlabel('Ingresos')
plt.ylabel('Prevalencia total en %');
plt.savefig('images/fig4.png', bbox_inches='tight')

# Scatterplot de la prevalencia de depresión por continente y género

c_cont.rename(columns={'Male_dep':'Hombres',
                        'Female_dep': 'Mujeres'}, inplace=True)

depsex = (c_cont.drop(columns='Year')
                        .melt(id_vars='Continent')
                        .rename(columns={'variable':'Género', 'value':'share'})
                )

fig, ax = plt.subplots()
ax.set_title('Prevalencia de la depresión por continente y género')
ax.set_xlabel('Continente')
ax.set_ylabel('Prevalencia en %')


plt.xticks(rotation=-40)


sns.scatterplot(data=depsex, x='Continent', y='share', hue='Género', ax=ax)
plt.savefig('images/fig5.png', bbox_inches='tight')




