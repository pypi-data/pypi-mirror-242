#!/usr/bin/env python
# coding: utf-8

# ### <center> Assignment 1 - Notebook 1</center>
# ### <center> Bimal Parajuli (20BDS0405) </center>
# ### 1. Ecommerce Purchases Exercise

# **Import pandas library. read the Ecommerce Purchases csv file.**

# In[78]:


import pandas as pd
df = pd.read_csv("./Ecommerce Purchases")


# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>

# #### Check the head of the DataFrame.

# In[50]:


print(df.head())


# 
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>

# ##### How many rows and columns are there?

# In[51]:


rows_count, cols_count = df.shape

print("Number of rows: ",rows_count)
print("Number of columns: ",cols_count)


# In[52]:


df.info()


# 
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>

# #### What is the average Purchase Price?

# In[53]:


purchase_price_avg = df['Purchase Price'].mean()


print("Average Purchase Price is: ", purchase_price_avg)


# 
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>

# #### What were the highest and lowest purchase prices? 

# In[54]:


purchase_price_max = df['Purchase Price'].max()
purchase_price_min = df['Purchase Price'].min()

print("Highest Price is: ", purchase_price_max)
print("Lowest Price is: ", purchase_price_min)


# 
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>

# #### How many people have English ‘en’ as their Language of choice on the website?

# In[55]:


languages_counts = df['Language'].value_counts()
english_counts = languages_counts.get('en')


print("Number of users with 'en' as their language choice are: ",english_counts)


# 
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>

# #### How many people have the job title of “Lawyer” ? 

# In[56]:


jobs_counts = df['Job'].value_counts()
lawyer_count = jobs_counts.get('Lawyer')


print("Number of people with job title of 'Lawyer' is: ", lawyer_count)


# 
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>

# #### How many people made the purchase during the AM and how many people made the purchase during PM ?

# In[57]:


df['AM or PM'].value_counts()


# 
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>

# #### What are the 5 most common Job Titles? 

# In[58]:


jobs_counts = df['Job'].value_counts()
most_common_jobs = job_counts.head(5)


print(most_common_jobs)


# 
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>

# #### Someone made a purchase that came from Lot: “90 WT” , what was the Purchase Price for this transaction?

# In[59]:


data_90WT = df[df['Lot'] == '90 WT']
purchase_price_90WT = data_90WT['Purchase Price']


print("Purchase price of a purchase from Lot 90 was: ", purchase_price_90WT.values[0])


# purchase_price_90WT


# 
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>

# ####  What is the email of the person with the following Credit Card Number: 4926535242672853 

# In[62]:


data_of_selected_record = df[df['Credit Card'] == 4926535242672853]
email_of_sleected_person = data_of_selected_record['Email'].values[0]

print("Email of the person with given CC No is: ",email_of_sleected_person)


# 
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>

# #### How many people have American Express as their Credit Card Provider and made a purchaseabove $95 ?

# In[67]:


amex_records = df[df['CC Provider'] == 'American Express']
amex_records_gt_95 = amex_records[amex_records['Purchase Price'] > 95]

print("Number of people with AMEX cards and purchase above $95 is: ",len(amex_records_gt_95))


# 
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>

# #### How many people have a credit card that expires in 2025?

# In[82]:


df['CC Exp Year'] = df['CC Exp Date'].apply(lambda x: int('20' + x.split('/')[1]))

count_2025_expiry = len(df[df['CC Exp Year'] == 2025])

print("Number of people with credit card expiry in 2025 is:", count_2025_expiry)


# 
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>
# <br>

# #### ** Hard: What are the top 5 most popular email providers/hosts (e.g. gmail.com, yahoo.com, etc…)
# 

# In[88]:


df['Email Domain'] = df['Email'].apply(lambda x: x.split('@')[1])

domain_counts = df['Email Domain'].value_counts()

top_5_providers = domain_counts.head(5)


print("Top 5 most popular email providers are: \n\n", top_5_providers)


# 
