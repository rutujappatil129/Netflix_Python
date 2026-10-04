#!/usr/bin/env python
# coding: utf-8

# In[24]:

import streamlit as st
import pandas as pd
get_ipython().system('pip install matplotlib')
import matplotlib.pyplot as plt


# In[25]:


a=1
b=2
c=a+b


# In[26]:


c


# In[5]:


netflix=pd.read_csv("netflix.csv")


# In[6]:


netflix


# In[7]:


netflix.shape #to read the rows and columns of data


# In[8]:


netflix.info() #tells us all information about dataset


# In[9]:


netflix.isnull().sum() #to find null valuse   # and sum if for dectacting all null values


# In[10]:


netflix.describe() #it shows us that which type of statical value in the data


# In[13]:


netflix.duplicated().sum() #to find the duplicate valuse in the dataset  #sum isfor total values.


# In[14]:


netflix.drop_duplicates()


# In[37]:


netflix['Watch_Date']=pd.to_datetime(netflix['Watch_Date'])


# In[38]:


netflix.dtypes  # for finding out the data types


# In[39]:


netflix.groupby("Region")["Monthly_Revenue"].sum().plot(kind="bar",ylabel="Monthly_Revenue",title="region wise revenew")


# In[32]:


netflix.groupby("Subscription_Plan")["Rating"].sum().plot(kind="pie",title="region wise revenew")


# In[33]:


netflix.groupby("Category")["Monthly_Revenue"].sum().plot(kind="bar",ylabel="Monthly_Revenue",title="region wise revenew")


# In[40]:


netflix["month"]=netflix["Watch_Date"].dt.month_name()


# In[41]:


netflix.groupby("month")["Monthly_Revenue"].sum().plot(kind="bar",ylabel="Monthly_Revenue",title="region wise revenew")


# In[ ]:




