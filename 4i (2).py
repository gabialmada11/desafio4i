import pandas as pd
import numpy as np
from xlsxwriter.utility import xl_rowcol_to_cell

df = pd.read_excel(r"C:\Users\Gabriela\Downloads\owid-covid-data.xlsx")
#df.head()
len(df)
print(df)


# In[2]:


#pegando as colunas:date, total_deaths, new_deaths
df1 = df[['date','location','total_deaths','new_deaths']]
print(df1)


# In[3]:


#pegando apenas os dados do brasil
df2 = df1.loc[df1['location']=='Brazil']
print(df2)


# In[4]:


#renomeando
df3 = df2.rename(columns = {'date': 'Data', 'total_deaths': 'Total de Mortes', 'new_deaths': 'Novas Mortes no Dia'})
print(df3)


# In[5]:


#mudando formato da data
df3['Data'] = pd.to_datetime(df3.Data, format='%Y-%m-%d')
df3['Data'] = df3['Data'].dt.strftime('%d/%m/%Y')
print(df3)


# In[9]:


#apagando linhas em branco
df4 = df3.dropna(subset=['Total de Mortes'])
df5 = df4.dropna(subset=['Novas Mortes no Dia'])
df5


# In[7]:


import csv

df5.to_csv("tabelaModificada.csv")


# In[1]:


#variacao anual

df5['Variacao Anual do Total de Mortes'] = '-' 
df5['Variacao Anual de Novas Mortes no Dia'] = '-' 


for i,row in df5.iterrows():
    date = row['Data']
    if date[6:] == '2021':
        
        dado_anterior = df5.loc[(df5['Data'])==f'{date[0:2]}/{date[3:5]}/{int(date[6:])-1}']['Total de Mortes']
        if len(dado_anterior) == 1:
            indx = (dado_anterior.index)[0]
            dado_anterior = dado_anterior[indx]
            df5.at[i,'Variacao Anual do Total de Mortes'] = ((row['Total de Mortes']/dado_anterior)-1)*100
            
        dado_anterior = df5.loc[(df5['Data'])==f'{date[0:2]}/{date[3:5]}/{int(date[6:])-1}']['Novas Mortes no Dia']
        if len(dado_anterior) == 1:
            indx = (dado_anterior.index)[0]
            dado_anterior = dado_anterior[indx]
            df5.at[i,'Variacao Anual de Novas Mortes no Dia'] = ((row['Novas Mortes no Dia']/dado_anterior)-1)*100

df6 = df5.reset_index(drop=True) 
df6


# In[12]:


df6.to_csv("variacaoAnual.csv")

