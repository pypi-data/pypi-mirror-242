#!/usr/bin/env python
# coding: utf-8

# # <center>LAB Assignment 3: Hierarchical Data Visualization</center>
# ## <center> - By Bimal Parajuli (20BDS0405) - 11th Oct 2023</center>

# ## <center> TASK: </center>
# Develop the following visualizations using plotly. Create a dataset on your own to visualize the 
# same. Either you can use the existing dataset or create your own dataset or add necessary columns 
# in an existing dataset in achieving the same. 
# 1. Treemap (plotly) (2.5 marks) 
# 2. Sunburst (plotly) (2.5 marks) 
# 3. Network graph (plotly) (2.5 marks) 
# 4. Hierarchical clustering and dendrogram (plotly) (2.5 marks) 
# 

# In[ ]:





# In[1]:


# Import some reqiured packages.

import numpy as np
import pandas as pd

from chart_studio import plotly
import plotly.express as px
import plotly.graph_objects as go

# For interactive plots using plotly
from plotly.offline import iplot


import networkx as nx



# In[2]:


df1 = pd.read_csv('Assignment_3_dataviz_csv1.csv')

# About the dataset:
#     - It is a manually created synthetic dataset that resembles the file system of a computer.
#     - Hierarchy moves from Drive > Folder1 > Folder2 > Folder3... 
#     - Size represents the size of Level3 folder.


# In[3]:


df1.head()


# In[ ]:





# # 1. Suburst Chart

# In[4]:


fig2 = px.sunburst(df1, path=['Drive', 'Folder1', 'Folder2', 'Folder3'], values='Size(in GB)')
fig2.update_layout(title_text="Sunburst Diagram by Bimal Parajuli (20BDS0405)", font_size = 10, height = 700, width = 700)
fig2.show()


# In[ ]:





# # 2. TreeMap

# In[5]:


fig2 = px.treemap(df1, path=['Drive', 'Folder1', 'Folder2', 'Folder3'], values='Size(in GB)')
fig2.update_layout(title_text="TreeMap Diagram by Bimal Parajuli (20BDS0405)", font_size = 10, height = 700, width = 700)
fig2.show()


# Explanation of the above diagram:
# - Different Drives are identified by hue.
# - Hierarchy levels are identified by Saturation.
# - Size of TreeMap boxes correspond to Folders size. 

# In[ ]:





# In[ ]:





# In[ ]:





# # 3. Node Link (Network) Diagrams

# In[6]:


A = list(df1['Folder2'].unique())
B = list(df1['Folder3'].unique())
C = list(df1['Folder1'].unique())
D = list(df1['Drive'].unique())


node_list = set(A + B + C + D)
# node_list


# In[7]:


G = nx.Graph()
for i in node_list:
    G.add_node(i)
for i, j in df1.iterrows():
    G.add_edges_from([(j["Drive"], j["Folder1"])])
    G.add_edges_from([(j["Folder1"], j["Folder2"])])    
    G.add_edges_from([(j["Folder2"], j["Folder3"])])


# In[8]:


pos = nx.spring_layout(G, k = 0.5, iterations = 50)


# In[9]:


for n, p in pos.items():
    G.nodes[n]['pos'] = p


# In[10]:


edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5,color='#888'),
    hoverinfo='none',
    mode='lines')

for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])


# In[11]:


node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='ylorbr',
        reversescale=True,
        color=[],
        size=15,
        colorbar=dict(
            thickness=10,
            title='Folder Link Counts',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=0)))

for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])


# In[12]:


for node, adjacencies in enumerate(G.adjacency()):
    node_trace['marker']['color']+=tuple([len(adjacencies[1])])
    node_info = "File\Folder Name: " + adjacencies[0]
    node_trace['text']+=tuple([node_info])


# In[13]:


fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='Network Link diagram of File-Folder links by Bimal Parajuli (20BDS0405)',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="",
                    showarrow=False,
                    xref="paper", yref="paper") ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

iplot(fig)


# Explanation of the above Link diagrams:
# - Each levels of folder names are represented by network nodes. 
# - Connections represent that one folder is contaned inside another.
# - Level3 Folders are leaf nodes on the graph.
# - Brightness of node is propotional to the number of connections (ie folders with less numberssubfolders tend to be darker)

# ### <center>- By Bimal Parajuli (20BDS0405)  - 11th Oct 2023</center>

# # 4. Hierarchical Clustering and Dendograms

# In[14]:


import plotly.figure_factory as ff

from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram

from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt


# In[15]:


# Dataset: 3 Dimensional Data of sensor Locations.

# About the dataset: 
#     It is a manually created synthetic dataset.
#     Records in dataset represent location of IOT sensors in 3d space using x,y,z coordinates.

df_loc = pd.read_excel('Sensor_locations.xlsx')


# Extract the numeric fields.
df4 = df_loc.iloc[:, 1:]

df_loc.head(3)


# In[ ]:





# ### 4 a. Clustering

# In[16]:


# Train the model to assign each SensorID to corresponding clusters

hc_model = AgglomerativeClustering(n_clusters=4, affinity = "euclidean", linkage="ward")
clusters = hc_model.fit_predict(df4)
df4["cluster"] = clusters
df4.head(3)


# In[17]:


cluster_count = 4


# In[18]:


clusters_list = []
for i in range(cluster_count):
    obj = df4[df4["cluster"] == i]
    clusters_list.append(obj)

# print(clusters_list)


# In[19]:


# Visualizing the clusters in 3d using plotly.

cluster_trace_list = []
cluster_colors = {
    0: "rgb(255,0,0)",
    1: "rgb(0,255,0)",
    2: "rgb(0,0,255)",
    3: "rgb(255,255,0)"
}

for i in range(cluster_count):
    cluster_trace_obj = go.Scatter3d(
        x = clusters_list[i].x_coord,
        y = clusters_list[i].y_coord,
        z = clusters_list[i].z_coord,
        mode = "markers",
        name = "cluster " + str(i),
        marker = dict(
            size = 6,
            color = cluster_colors[i]
        )
    )
    
    cluster_trace_list.append(cluster_trace_obj)


data_plot_hc = cluster_trace_list

layout = go.Layout(
    margin = dict(l = 0,  r =0, b = 0, t = 0))

fig = go.Figure(data = data_plot_hc, layout = layout)
iplot(fig)


# Observations from the above 3d plot:
# - Approximate members are grouped in a same cluster.
# - Different cluster members are represented with Different color.
# - Clusters have 5, 5, 3 and 2 members respectively.

# In[20]:





# ### 4 b. Dendogram Visualization

# In[31]:


# Draw the dendogram by Hierarchical clustering.

plt.figure(figsize=(15, 6), dpi= 280)  
plt.title("IOT clusters Dendogram by Bimal Parajuli (20BDS0405)", fontsize=22)

dg = dendrogram(
    linkage(df_loc[['x_coord', 'y_coord', 'z_coord']], method = 'ward'), 
    labels = df_loc.SensorID.values, 
    color_threshold = 100
)  

plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.xlabel("Sensor IDs")
plt.ylabel("Distance between the sensors / clusters")

plt.show()


# In[ ]:





# # - By Bimal Parajuli (20BDS0405). - 11th Oct 2023

#  

# <center>------ END -----</center>
