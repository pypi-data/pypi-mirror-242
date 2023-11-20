#!/usr/bin/env python
# coding: utf-8

# ### <center> Assignment 1 - Notebook 2</center>
# ### <center> Bimal Parajuli (20BDS0405) </center>
# ### 2. SF Salaries Exercise

# **Import pandas library. read the Ecommerce Purchases csv file.**

# In[2]:


import pandas as pd


# <br>
# <br>
# <br>
# <br>
# 

# In[4]:


df = pd.read_csv(r'.\Salaries.csv')
df.head()


# In[25]:


df.info()


# <br>
# <br>
# <br>
# <br>
# 

# ##### What is average base pay?

# In[5]:


Base_Pay=df['BasePay'].mean()
print("Average Base Pay: ",Base_Pay)


# <br>
# <br>
# <br>
# <br>
# 

# ##### ** What is the highest amount of OvertimePay in the dataset ? **

# In[6]:


print("Highest Amount of Overtime Pay: ",df['OvertimePay'].max())


# <br>
# <br>
# <br>
# <br>
# 

# ##### What is the job title of JOSEPH DRISCOLL ? Note: Use all caps, otherwise you may get an answer that doesn’t match up (there is also a lowercase Joseph Driscoll). **

# In[7]:


job_title = df[df['EmployeeName']=='JOSEPH DRISCOLL']['JobTitle'].values[0]
print("Required Job Title: ",job_title)


# <br>
# <br>
# <br>
# <br>
# 

# ** How much does JOSEPH DRISCOLL make (including benefits)? **

# In[8]:


total_pay = df[df['EmployeeName']=='JOSEPH DRISCOLL']['TotalPayBenefits'].values[0]
print("Pay of Joseph Driscoll: ",total_pay)


# <br>
# <br>
# <br>
# <br>
# 

# ##### ** What is the name of highest paid person (including benefits)?**

# In[24]:


highest_pay = df["TotalPayBenefits"].max()
highest_paid_person = df[df["TotalPayBenefits"] == highest_pay]

print("The name of the highest paid person is: ", highest_paid_person["EmployeeName"].to_string(index = False), "\n\n")
print(highest_paid_person)


# <br>
# <br>
# <br>
# <br>
# 

# ** What is the name of highest paid person (including benefits)?**

# In[23]:


lowest_pay = df["TotalPayBenefits"].min()
lowest_paid_person = df[df["TotalPayBenefits"] == lowest_pay]


print("The name of the highest paid person is: ", lowest_paid_person["EmployeeName"].to_string(index = False), "\n\n")
print(lowest_paid_person)


# <br>
# <br>
# <br>
# <br>
# 

# ** What was the average (mean) BasePay of all employees per year? **

# In[28]:


avg_basepay_per_year = df.groupby('Year')['BasePay'].mean()
print(avg_basepay_per_year)


# <br>
# <br>
# <br>
# <br>
# 

# ** How many unique job titles are there? **

# In[30]:


unique_job_titles_count = df['JobTitle'].nunique()

print("The number of uinque job titles are: ", unique_job_titles_count)


# <br>
# <br>
# <br>
# <br>
# 

# ** What are the top 5 most common jobs? **

# In[32]:


top_common_jobs = df['JobTitle'].value_counts().head(5)


print(top_common_jobs)


# <br>
# <br>
# <br>
# <br>
# 

# ** How many Job Titles were represented by only one person in 2013? (e.g. Job Titles with only
# one occurence in 2013?) **

# In[33]:


data_2013 = df[df['Year'] == 2013]

job_title_counts = data_2013['JobTitle'].value_counts()

job_titles_one_person = (job_title_counts == 1).sum()

print("Number of job titles represented by only one person in 2013:", job_titles_one_person)


# <br>
# <br>
# <br>
# <br>
# 

# ** How many people have the word Chief in their job title? **

# In[36]:


chief_count = df[df['JobTitle'].str.contains('Chief')]['JobTitle'].count()

print("Number of people with 'Chief' in their job title:", chief_count)


# <br>
# <br>
# <br>
# <br>
# 

# ** Bonus: Is there a correlation between length of the Job Title string and Salary? **

# In[38]:


df['title_len'] = df['JobTitle'].apply(len)

# Calculate the correlation matrix
correlation_matrix = df[['title_len', 'TotalPayBenefits']].corr()

print(correlation_matrix)


# <br>
# <br>
# <br>
# <br>
# 
