#!/usr/bin/env python
# coding: utf-8

# <center> <h1>LAB Assignment 2.</h1> </center>
# 

# <center> <h4>Data Visualization (CSE3020) ELA -- 
#     Slot L3+L4</h4></center>

# <div margin-left = "300px">
# By:
#     
# - Bimal Parajuli (20BDS0405)
# - Prithak Gajurel (20BCE2921)
# - Sharat PM (20BCE0760)
# 
# </p>

# 

# <h1> 1. Employee Salaries dataset visualizations </h1>

# In[ ]:





# In[171]:


# Import necessary libraries...

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


import seaborn as sns


# In[163]:


# read the salaries.csv data 

data = pd.read_csv("/media/bimal/Drive/Academics/VIT_Academics/7th_sem/DataViz/LAB/Datasets/Salaries.csv")


# In[ ]:





# In[172]:


# View the first 5 entries of dataframe
data.head()


# In[174]:


# Observe the columns of the dataframe before proceeding to analysis.

data.columns


# In[ ]:





# In[175]:


data['Year'].value_counts()


# In[ ]:





# In[ ]:





# ### Task1: Compare average salaries over time.

# **Task Abstraction:**
# The task involves visualizing the average salary for employees from the years 2011 to 2014. To achieve this, we need to group the dataset by the 'Year' attribute and calculate the average salary for each year. Then, we represent these averages as bars on a bar chart, with the x-axis denoting the years (2011, 2012, 2013 and 2014) and the y-axis representing the average salary amount. Each bar's height corresponds to the average salary for a specific year, allowing us to compare salary trends over this three-year period.
# 
# **Justification of Visual Idiom:**
# A bar chart is an effective choice for this task because it helps viewers easily compare the average salary across different years. The discrete nature of the years (2011, 2012, and 2013) makes bar charts suitable, as they provide clear separation between the categories. Additionally, bar charts are well-suited for showing variations and trends over time, making it evident whether the average salary increased, decreased, or remained relatively constant across these years. The bar chart's simplicity and straightforwardness make it a suitable choice for conveying this specific type of data and comparison.
# 
# **Data Columns used:**
# - JobTitle
# - Year

# In[176]:


# Group the data by year and calculate the average salary for each year
average_salary_by_year = data.groupby('Year')['TotalPay'].mean()

# Create a bar plot
plt.figure(figsize=(10, 6))
average_salary_by_year.plot(kind='bar', color='skyblue')
plt.xlabel('Year')
plt.ylabel('Average Salary (in USD)')
plt.title('Average Salary by Year (2011-2014)')

# Add labels to the bars
for index, value in enumerate(average_salary_by_year):
    plt.text(index, value, f'{value:.2f}', ha='center', va='bottom', fontsize=10)

plt.xticks(rotation=32)  
plt.yticks(rotation=23)
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# ### Task 2: Identify and Compare Top 5 professions over years.

# **Task Abstraction:**
# The task involves identifying and visualizing the top 5 professions for the years 2013 and 2014. To accomplish this, we need to filter the dataset by the years 2013 and 2014, count the occurrences of each unique job title within these two years, and select the top 5 job titles with the highest counts. The result will be a pie chart for each of the two years, displaying the distribution of the top 5 job titles in terms of the percentage of employees they represent.
# 
# **Justification of Visual Idiom:**
# A pie chart is a suitable choice for this task because it allows for a clear and concise representation of the distribution of job titles within a specific year. Pie charts are effective for showing the composition of a whole in terms of its parts, making it easy to compare the relative proportions of different job titles. In this case, it enables viewers to quickly grasp the top 5 job titles and their respective contributions to the employee population for each of the two years. The limited number of categories (top 5 job titles) in the dataset makes pie charts an intuitive choice for conveying this information.
# 
# **Data Columns Used:**
# - JobTitle
# - Year

# In[169]:


# Define the years
years = [2013, 2014]

# Create subplots for each year
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
axes = axes.ravel()

for i, year in enumerate(years):
    # Filter the data for the current year
    data_year = data[data['Year'] == year]
    
    # Get the top 5 job titles by count in the current year
    top_5_job_titles = data_year['JobTitle'].value_counts().head(5).index.tolist()
    
    # Calculate the percentage of each job title among all employees in the current year
    percentage_labels = []
    for title in top_5_job_titles:
        title_count = len(data_year[data_year['JobTitle'] == title])
        total_count_year = len(data_year)
        percentage = (title_count / total_count_year) * 100
        percentage_labels.append(f"{title} ({percentage:.2f}%)")
    
    # Create a pie chart for the current year
    axes[i].pie(data_year['JobTitle'].value_counts().head(5), labels=percentage_labels, autopct='', startangle=140)
    axes[i].set_title(f"Top 5 Job Titles by count in {year}")
    axes[i].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    axes[i].legend(labels=top_5_job_titles, loc='lower center')
# Adjust layout
plt.tight_layout()

# Show the pie charts
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# ### Task 3: Discover how OtherPay varies with BasePay

# **Task Abstraction:**
# The task involves examining the relationship between 'OtherPay' and 'BasePay' for the top 300 special nurses in the year 2013. To accomplish this, we need to filter the dataset to include only records for special nurses in 2013, select the top 300 records, and then create a scatter plot. In the scatter plot, 'BasePay' values will be plotted on the x-axis, and 'OtherPay' values will be plotted on the y-axis for these selected records. This visualization aims to reveal any patterns or correlations between 'OtherPay' and 'BasePay' for this specific group of employees and year.
# 
# **Justification of Visual Idiom:**
# A scatter chart is the appropriate choice for this task because it allows us to explore the relationship between two continuous variables, 'OtherPay' and 'BasePay,' for a subset of data. Scatter plots are ideal for visualizing the distribution of data points and identifying trends or clusters in the data. In this case, we are interested in understanding how 'OtherPay' varies concerning 'BasePay' for a specific group of employees (top 300 special nurses) in a particular year (2013). Scatter plots provide a clear and intuitive way to observe any patterns or anomalies in the data and are commonly used for exploratory data analysis.
# 
# **Columns Used:**
# - BasePay
# - OtherPay
# - Year

# In[181]:


# Filter the data for special nurses in the year 2013
special_nurses_2013 = data[ (data['OtherPay'] != 0) & (data['JobTitle'] == 'Special Nurse') & (data['Year'] == 2013)].sort_values(by='OtherPay', ascending = False).head(300)

# Extract 'BasePay' and 'OtherPay' columns
basepay = special_nurses_2013['BasePay']
otherpay = special_nurses_2013['OtherPay']

# Create a scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(basepay, otherpay)
plt.title("Scatter Plot of BasePay vs. OtherPay for Special Nurses (2013)")
plt.xlabel("BasePay (in USD)")
plt.ylabel("OtherPay (in USD)")

# Show the scatter plot
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# ### Task 4: Present the correlation coefficient of different types of pay.

# **Task Abstraction:**
# The task involves assessing the correlations between various types of pays (specifically, 'BasePay,' 'OvertimePay,' 'OtherPay,' 'Benefits,' 'TotalPay,' and 'TotalPayBenefits') in the dataset. To achieve this, we need to calculate the correlation coefficients between these pairs of variables, resulting in a correlation matrix. This matrix provides a systematic overview of how these variables relate to each other, with values ranging from -1 (perfect negative correlation) to 1 (perfect positive correlation), indicating the strength and direction of the relationships.
# 
# **Justification of Visual Idiom:**
# A heatmap is the appropriate choice for this task because it effectively visualizes the correlation matrix. Heatmaps use color to represent the magnitude and direction of correlations between variables, making it easy to identify patterns and relationships in a large dataset. In this case, the heatmap will quickly convey which pairs of pay types are positively correlated, negatively correlated, or have no significant correlation. It provides an at-a-glance understanding of the interdependencies between different pay-related attributes, making it a valuable tool for data exploration and identifying potential areas of interest or further analysis. Heatmaps are widely used for visualizing correlation matrices due to their ability to simplify complex relationships and support data-driven decision-making.
# 
# **Columns Used:**
# - BasePay
# - OvertimePay
# - OtherPay
# - Benefits
# - TotalPay
# - TotalPayBenefits

# In[155]:


numeric_data = data[['BasePay', 'OvertimePay', 'OtherPay', 'Benefits', 'TotalPay', 'TotalPayBenefits']]
f,ax = plt.subplots(figsize=(5, 5))
sns.heatmap(numeric_data.corr(), annot=True, linewidths=.5, fmt= '.1f',ax=ax)


# In[ ]:





# In[ ]:





# In[ ]:




