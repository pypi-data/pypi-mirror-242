#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Bimal parajuli
# 20BDS0405



# LAB Assignment 4


# In[2]:


import pandas as pd
import numpy as np


# In[3]:


import plotly.express as px
import plotly.graph_objects as go


# In[ ]:





# In[4]:


import matplotlib.pyplot as plt
import geopandas as gpd


# In[ ]:





# In[5]:


import mapscaler as ms
from shapely import wkt
# import geoplot as gplt


# In[6]:


df_ = pd.read_csv('USArrests.csv')


# In[7]:


df_['UrbanPop'].mean()


# In[8]:


df_.head()


# In[ ]:





# In[9]:


state_codes_df_ = pd.read_csv('https://raw.githubusercontent.com/jasonong/List-of-US-States/master/states.csv')
state_codes_df_.head()


# In[10]:


state_codes_df_.rename(columns = {'State': 'State_', 'Abbreviation': 'StateCode'}, inplace=True)
state_codes_df_.head()


# In[ ]:





# In[11]:


df = pd.merge(df_, state_codes_df_, left_on = "State", right_on = "State_").drop('State_', axis=1)


# In[12]:


df.head()


# In[ ]:





# ## Visualization of 1st Attribute: UrbanPop

# In[14]:


fig = go.Figure(data=go.Choropleth(
    locations=df['StateCode'], # Spatial coordinates
    z = df['UrbanPop'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Greens',
    colorbar_title = "% of Urban Population",
))

fig.update_layout(
    title_text = 'United States urban Population Distribution by states',
    geo_scope='usa', # limite map scope to USA
)

fig.show()


# In[ ]:





# ## Visualization of 2nd Attribute: Assault

# In[14]:


fig = go.Figure(data=go.Choropleth(
    locations=df['StateCode'], # Spatial coordinates
    z = df['Assault'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "Assault Rate",
))

fig.update_layout(
    title_text = 'Cases of Assaults Distribution by states in the USA',
    geo_scope='usa', # limite map scope to USA
)

fig.show()


# In[ ]:





# ## Visualization of 3rd Attribute: Murder

# In[15]:


fig = go.Figure(data=go.Choropleth(
    locations=df['StateCode'], # Spatial coordinates
    z = df['Murder'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Blues',
    colorbar_title = "Murder Rate",
))

fig.update_layout(
    title_text = 'Murder Cases Distribution by states in the USA',
    geo_scope='usa', # limite map scope to USA
)

fig.show()


# In[ ]:





# In[161]:


states_ = geopandas.read_file('shapedata/cb_2022_us_state_20m.shp')
states_ = states[['geometry', 'STUSPS', 'NAME']]
type(states_)


# In[162]:


states_.head(3)


# In[163]:


states.crs


# In[164]:


states_ = states_.to_crs("EPSG:3395")


# In[208]:


# fig = plt.figure()
 
# fig.set_figheight(10)
# fig.set_figwidth(10)
# states_.plot()


# In[209]:


# states_.boundary.plot()


# In[172]:


state = pd.merge(states_, df[['StateCode', 'Assault']], left_on = "STUSPS", right_on="StateCode").drop('STUSPS', axis=1)


# In[211]:


state_tmp = state
state_tmp.head(3)


# In[ ]:





# In[ ]:





# In[212]:


ss = ms.ShapeScaler()
scaled_df = ss.scale_map(state_tmp, 'Assault',map_vel=.001, group_vel=.15, verbose=True)


# In[ ]:





# In[215]:


state_data1 = ms.MapLoader().fetch_states()['df']


# In[217]:


data = pd.read_csv('USArrests.csv')


# In[223]:


world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
usa = world[world['name'] == 'United States']
# Create a new column for scaled Murder values (adjust scale factor as needed)
usa['murder'] = data['Murder']


# In[216]:


# Visualizing Murder


# In[222]:


# Plot the cartogram map for the United States
fig, ax = plt.subplots(figsize=(12, 8))
usa.boundary.plot(ax=ax)
usa.plot(column='murder', colorscale='Blues', legend=True, ax=ax)
plt.title("US States Cartogram - Murder Rates")
plt.show()


# In[224]:





# In[ ]:





# In[236]:


# Visualizing Assault


# In[225]:


# Create a new column for scaled Murder values (adjust scale factor as needed)
usa['assault'] = data['Assault']


# In[226]:


# Plot the cartogram map for the United States wrt assault
fig, ax = plt.subplots(figsize=(12, 8))
usa.boundary.plot(ax=ax)
usa.plot(column='assault', colorscale='Grayscale', legend=True, ax=ax)
plt.show()


# In[228]:





# In[ ]:





# In[235]:


# Visualizing rape


# In[230]:


# Create a new column for scaled Murder values (adjust scale factor as needed)
usa['rape'] = data['Rape']


# In[231]:


# Plot the cartogram map for the United States wrt assault
fig, ax = plt.subplots(figsize=(12, 8))
usa.boundary.plot(ax=ax)
usa.plot(column='rape', colorscale='Grayscale', legend=True, ax=ax)
plt.show()


# In[232]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[234]:


# Challenging exercise:


# In[ ]:


https://drive.google.com/file/d/1vjL115EYOeRPotjKPQGYHp-8adGmAic3/view?usp=sharing


# In[ ]:


# Bimal Parajuli (20BDS0405)

