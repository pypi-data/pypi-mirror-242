#!/usr/bin/env python
# coding: utf-8

# <h1> 2. Ecommerce Purchases dataset visualizations </h1>

# In[ ]:





# In[8]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#load data

# df=pd.read_csv("/media/bimal/Drive/Academics/VIT_Academics/7th_sem/DataViz/LAB/Datasets/Ecommerce Purchases.csv")

df = pd.read_csv("D:/Academics/VIT_Academics/7th_sem/DataViz/LAB/Datasets/Ecommerce Purchases.csv")
df.info()


# In[ ]:





# In[9]:


df.head()


# In[ ]:





# In[ ]:





# ### Task 1: Credit Card Provider Distribution
# 

# 
# Task: 
# 
# The task here is to analyze the distribution of credit card providers (CC Provider) used by customers in the dataset. This involves counting the frequency of each credit card provider to understand which payment methods are commonly used for transactions.
# 
# 
# 
# Visual Idiom Chosen (Pie Chart): 
# 
# A pie chart is chosen as the visual idiom for this task. A pie chart is an effective way to represent the distribution of categories within a dataset. In this case, each credit card provider represents a category, and the size of each "slice" of the pie chart corresponds to the proportion of customers using that provider.
# 
# 
# 
# Justification: 
# 
# Analyzing the distribution of credit card providers is essential because it provides insights into the payment preferences of customers. By visualizing this information, businesses can identify which credit card providers are most popular among their customer base. This information can be valuable for various purposes, such as negotiating partnerships with popular providers or optimizing payment processing systems to accommodate the preferences of the majority of customers.
# 

# In[10]:


# Count the frequency of each credit card provider
cc_provider_counts = df['CC Provider'].value_counts()

# Create a pie chart
plt.figure(figsize=(8, 8))
plt.pie(cc_provider_counts, labels=cc_provider_counts.index, autopct='%1.1f%%', startangle=140)

# Add a title
plt.title("Credit Card Provider Distribution")

# Display the pie chart
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()


# In[ ]:





# In[ ]:





# ### Task 2: Job Title Analysis
# 

# 
# Task: 
# 
# The task involves analyzing the distribution of job titles (Job) among customers in the dataset. This analysis aims to provide insights into the demographics and professions of the customer base, which can be valuable for targeted marketing or product development.
# 
# 
# 
# Visual Idiom Chosen (Bar Chart):
# 
# Bar Chart: A bar chart can be chosen to represent the frequency of each job title. Each job title is plotted on the x-axis, and the corresponding count of customers with that job title is plotted on the y-axis.
# 
# 
# 
# Justification: 
# 
# Analyzing job titles within the customer base provides valuable demographic insights. It can help businesses understand the professional backgrounds of their customers, which may influence their preferences and behaviors. For example, knowing that a significant portion of customers holds job titles related to engineering might suggest an interest in technical products or services. This information can inform targeted marketing strategies and product development efforts to cater to the specific interests and needs of various professional groups within the customer base.

# In[11]:


# Count the frequency of each job title
job_counts = df['Job'].value_counts()

# Select the top N most common job titles to display (optional)
top_n = 10  # You can change this value to show more or fewer job titles
top_job_counts = job_counts.head(top_n)

# Create a bar chart
plt.figure(figsize=(12, 6))
top_job_counts.plot(kind='bar', color='skyblue')

# Add labels and title
plt.xlabel("Job Title")
plt.ylabel("Frequency")
plt.title(f"Top {top_n} Most Common Job Titles")

# Rotate x-axis labels for better readability (optional)
plt.xticks(rotation=45, ha='right')

# Show the bar chart
plt.tight_layout()
plt.show()


# In[ ]:





# In[ ]:





# ### Task 3: Language vs. Browser Usage

# 
# Task: 
# 
# The task involves analyzing the relationship between two categorical variables in the dataset: "Language" and "Browser Info." Specifically, we want to understand how the preferred language of customers relates to the web browsers they use. This involves creating a heatmap that visually represents the frequency of language-browser combinations.
# 
# 
# 
# Visual Idiom Chosen (Heatmap): 
# 
# A heatmap is chosen as the visual idiom for this task. A heatmap is a graphical representation of data where individual values are represented as colors. In this case, each cell in the heatmap represents a language-browser combination, and the color intensity indicates the frequency of that combination. Heatmaps are particularly effective for displaying the relationship between two categorical variables and identifying patterns or trends.
# 
# 
# 
# 
# Justification: 
# 
# Analyzing the relationship between preferred language and web browser usage is valuable for optimizing user experiences, localizing content, ensuring cross-browser compatibility, and tailoring marketing efforts to specific user groups. This analysis helps enhance user satisfaction, engagement, and overall website performance.
# 

# In[31]:


# Extract the browser name from the "Browser Info" column
df['Browser'] = df['Browser Info'].str.split('/').str[0]

# Create a cross-tabulation of Language vs. Browser
cross_tab = pd.crosstab(df['Language'], df['Browser'])

# Set the figure size
plt.figure(figsize=(12, 8))

# Create the heatmap using Seaborn
sns.heatmap(cross_tab, cmap='crest', annot=True, fmt='d', linewidths=.5)

# Set labels and title
plt.xlabel("Browser")
plt.ylabel("Language")
plt.title("Language vs. Browser Usage")

# Show the heatmap
plt.tight_layout()
plt.show()


# In[ ]:





# In[ ]:





# ### Task 4: Purchase Price vs. Job Title (Scatter Plot)
# 

# 
# Task: 
# The task is to explore the relationship between the purchase price (Purchase Price) and the job titles (Job) of the customers in the dataset. Specifically, we want to visualize whether there are any patterns or correlations between the job titles of customers and the amount they spend on purchases.
# 
# 
# Justification: 
# This task is justified because understanding how job titles relate to purchase behavior can be valuable for targeted marketing and product development. For instance, identifying whether customers with certain job titles tend to make higher-value purchases can inform strategies for offering tailored products or promotions to specific professional groups.
# 
# 
# Data Columns Used:
# Purchase Price: Represents the amount spent on purchases.
# Job: Represents the job titles of customers. (only top 10 taken for intelligibility.
# 
# 
# 

# In[28]:


# Get the top 10 most common job titles
top_10_jobs = df['Job'].value_counts().head(10).index

# Filter the dataset to include only the top 10 job titles
filtered_df = df[df['Job'].isin(top_10_jobs)]

# Set the figure size
plt.figure(figsize=(12, 6))

# Create the scatter plot
plt.scatter(filtered_df['Job'], filtered_df['Purchase Price'], alpha=0.5, color='b', marker='o')

# Set labels and title
plt.xlabel("Top 10 Job Titles")
plt.ylabel("Purchase Price")
plt.title("Purchase Price vs. Top 10 Job Titles")

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Show the scatter plot
plt.tight_layout()
plt.show()


# In[ ]:





# In[14]:


cross_tab


# In[ ]:




