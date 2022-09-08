#!/usr/bin/env python
# coding: utf-8

# # Scenario 1

# In[1]:


import pandas as pd
import numpy as np
import random as rd
import seaborn as sns 
import matplotlib.pyplot as plt
import datetime as dt
import warnings
warnings.filterwarnings('ignore')

import plotly.express as px


# In[2]:


customer = pd.read_csv("customer.csv")


# In[3]:


customer


# In[4]:


customer.head(10)


# In[5]:


customer.ndim


# In[6]:


customer.shape


# In[7]:


customer.columns


# In[8]:


customer["Age"]= 2015-customer["Year_Birth"]


# In[9]:


customer


# In[10]:


customer.describe()


# In[11]:


customer.isnull().sum()


# In[12]:


plt.figure(figsize=(10,6))
sns.heatmap(customer.isnull(),
            cmap="YlGnBu",
            cbar_kws={'label': 'Missing Data'},yticklabels='')


# In[13]:


customer


# In[14]:


customer=customer.dropna()


# # Scenario 2

# In[15]:


customer.isnull().sum()


# In[16]:


customer['Dt_Customer'] = pd.to_datetime(customer['Dt_Customer'])
customer['Month_Customer'] = 12.0 * (2015 - customer.Dt_Customer.dt.year ) + (customer.Dt_Customer.dt.month-1)


# In[17]:


customer


# In[18]:


customer["TotalSpendings"]=customer["MntGoldProds"]+customer["MntMeatProducts"]+customer["MntFishProducts"]+customer["MntSweetProducts"]


# In[19]:


customer


# In[20]:


customer.loc[(customer["Age"]<=19),"AgeGroup"]="Teen"
customer.loc[(customer["Age"]>=20) & (customer["Age"]<=39),"AgeGroup"]="Adults"
customer.loc[(customer["Age"]>=40) & (customer["Age"]<=59),"AgeGroup"]="Middle age Adults"
customer.loc[(customer["Age"]>=60),"AgeGroup"]="senior"


# In[21]:


customer


# In[22]:


customer["Children"]=customer["Teenhome"]+customer["Kidhome"]


# In[23]:


customer.drop(columns=["Teenhome","Kidhome"])


# In[24]:


customer.Marital_Status = customer.Marital_Status.replace({"Together":"Married",
                                                          "Married": "Married",
                                                          "Divorced":"Single",
                                                          "Widow":"Single",
                                                          "Alone":"Single",
                                                          "Absurd":"Single",
                                                          "YOLO":"Single"})


# In[25]:


customer


# In[26]:


plt.figure(figsize=(5,4))
sns.boxplot(y=customer.Age);
plt.ylabel('Age', fontsize=10)


# In[27]:


customer.Age.describe()


# In[28]:


Q1=38
Q3=56
IQR=Q3-Q1
upper=Q3+1.5*IQR
lower=Q1-1.5*IQR
upper


# In[29]:


customer=customer.drop(customer[customer['Age'] > 83].index, inplace = False)


# In[30]:


plt.figure(figsize=(5,4))
sns.boxplot(y=customer.Age);
plt.ylabel('Age', fontsize=10)


# In[31]:


customer.Income.describe()


# In[32]:


Q1=35340
Q3=68487
IQR=Q3-Q1
upper=Q3+1.5*IQR
upper


# In[33]:


customer=customer.drop(customer[customer['Income'] >118207.5 ].index, inplace = False)


# In[34]:


plt.figure(figsize=(5,4))
sns.boxplot(y=customer.Income);
plt.ylabel('income', fontsize=20)


# In[35]:


customer.shape


# In[36]:


customer


# # Scenario 3

# 
# # Exploratory Data Analysis
# 
Marital Status
# In[37]:


maritalstatus = customer.Marital_Status.value_counts()

fig = px.pie(maritalstatus, 
             values = maritalstatus.values, 
             names = maritalstatus.index,
             color_discrete_sequence=px.colors.sequential.RdBu)
fig.update_traces(textposition='inside', textinfo='percent+label', 
                  marker = dict(line = dict(color = 'white', width = 4)))
fig.show()  

INSIGHT2/3 OF the customers live with patner while 1/3 stays single 
# # Average Spendings: Marital Status Wise

# In[38]:


maritalspending = customer.groupby('Marital_Status')['TotalSpendings'].mean().sort_values(ascending=False)
maritalspending_df = pd.DataFrame(list(maritalspending.items()), columns=['Marital Status', 'Average Spending'])

plt.figure(figsize=(13,5))
sns.barplot(data = maritalspending_df, x="Average Spending", y="Marital Status", palette='rocket');

plt.xticks( fontsize=12)
plt.yticks( fontsize=12)
plt.xlabel('Average Spending', fontsize=13, labelpad=13)
plt.ylabel('Marital Status', fontsize=13, labelpad=13);


# In[39]:


sns.boxplot(x="Marital_Status", y="TotalSpendings", data=customer, palette='rocket')

INSIGHTalthoug minority, single persons spend more than person living with patner
# # Education Level

# In[40]:


education = customer.Education.value_counts()

fig = px.pie(education, 
             values = education.values, 
             names = education.index,
             color_discrete_sequence=px.colors.sequential.RdBu)
fig.update_traces(textposition='inside', textinfo='percent+label', 
                  marker = dict(line = dict(color = 'white', width = 2)))
fig.show()

INSIGHT Half of the clients are graduates of the University
There are more clients who have PhD degrees than customers who have a Master's degree
# # Child Status

# In[41]:


children = customer.Children.value_counts()

fig = px.pie(children, 
             values = children.values, 
             names = children.index,
             color_discrete_sequence=px.colors.sequential.RdBu)
fig.update_traces(textposition='inside', textinfo='percent+label', 
                  marker = dict(line = dict(color = 'white', width = 2)))
fig.show()

INSIGHTAbout 50% of customers only have one child
28% of customers have no children at home while 19% of them have 2 children
# # Average Spendings: Child Status Wise

# In[42]:


childrenspending = customer.groupby('Children')['TotalSpendings'].mean().sort_values(ascending=False)
childrenspending_df = pd.DataFrame(list(childrenspending.items()), columns=['No. of Children', 'Average Spending'])

plt.figure(figsize=(10,5))

sns.barplot(data=childrenspending_df,  x="No. of Children", y="Average Spending", palette='rocket_r');
plt.xticks( fontsize=12)
plt.yticks( fontsize=12)
plt.xlabel('No. of Children', fontsize=13, labelpad=13)
plt.ylabel('Average Spending', fontsize=13, labelpad=13);

INSIGHTCustomers who don't have children at home spend more than customers who have 1 child.
The customer has 1 child withdrawal higher than the customer has 2 and 3 children.
# # Age Distribution of Customers

# In[43]:


plt.figure(figsize=(10,5))
ax = sns.histplot(data = customer.Age, color='salmon')
ax.set(title = "Age Distribution of Customers");
plt.xticks( fontsize=12)
plt.yticks( fontsize=12)
plt.xlabel('Age ', fontsize=13, labelpad=13)
plt.ylabel('Counts', fontsize=13, labelpad=13);

INSIGHTThe age of customers is almost normally distributed, with the vast majority of customers between the ages of 40 and 60.
# # Relationship: Income vs Spendings

# In[44]:


plt.figure(figsize=(20,10))


sns.scatterplot(x=customer.Income, y=customer.TotalSpendings, s=100, color='black');

plt.xticks( fontsize=16)
plt.yticks( fontsize=16)
plt.xlabel('Income', fontsize=20, labelpad=20)
plt.ylabel('Spendings', fontsize=20, labelpad=20);

INSIGHTThe relationship is linear. Customers with higher salaries spend more
# # Most Bought Products

# In[45]:


products = customer[['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']]
product_means = products.mean(axis=0).sort_values(ascending=False)
product_means_df = pd.DataFrame(list(product_means.items()), columns=['Product', 'Average Spending'])

plt.figure(figsize=(15,10))
plt.title('Average Spending on Products')
sns.barplot(data=product_means_df, x='Product', y='Average Spending', palette='rocket_r');
plt.xlabel('Product', fontsize=20, labelpad=20)
plt.ylabel('Average Spending', fontsize=20, labelpad=20);

INSIGHTGrape and Meat Products are the most famous products among customers
Candy and Fruit are not often bought
# # Scenario 4

# In[46]:


X = customer.drop(['ID', 'Year_Birth', 'Education', 'Marital_Status', 'Kidhome', 'Teenhome', 'MntWines', 'MntFruits','MntMeatProducts',
                          'MntFishProducts', 'MntSweetProducts', 'MntGoldProds','Dt_Customer', 'Z_CostContact',
                          'Z_Revenue', 'Recency', 'NumDealsPurchases', 'NumWebPurchases','NumCatalogPurchases',
                          'NumStorePurchases', 'NumWebVisitsMonth', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5',
                          'AcceptedCmp1', 'AcceptedCmp2', 'Complain',  'Response', 'AgeGroup'], axis=1)


# In[47]:


X.info()


# # Optimum Clusters Using Elbow Method

# In[48]:


from sklearn.cluster import KMeans

options = range(2,9)
inertias = []

for n_clusters in options:
    model = KMeans(n_clusters, random_state=42).fit(X)
    inertias.append(model.inertia_)

plt.figure(figsize=(20,10))    
plt.title("No. of clusters vs. Inertia")
plt.plot(options, inertias, '-o', color = 'black')
plt.xticks( fontsize=16)
plt.yticks( fontsize=16)
plt.xlabel('No. of Clusters (K)', fontsize=20, labelpad=20)
plt.ylabel('Inertia', fontsize=20, labelpad=20);


# In[60]:


model = KMeans(n_clusters=4, init='k-means++', random_state=42).fit(X)

import joblib
joblib.dump(model,'customer.pkl')

preds = model.predict(X)

customer_kmeans = X.copy()
customer_kmeans['clusters'] = preds


# # Clusters Identification

# In[50]:


#Income
plt.figure(figsize=(20,10))

sns.boxplot(data=customer_kmeans, x='clusters', y = 'Income',palette='rocket_r');
plt.xlabel('Clusters', fontsize=20, labelpad=20)
plt.ylabel('Income', fontsize=30, labelpad=20);


# In[51]:


#Total Spending
plt.figure(figsize=(20,10))

sns.boxplot(data=customer_kmeans, x='clusters', y = 'TotalSpendings',palette='rocket_r');
plt.xlabel('Clusters', fontsize=20, labelpad=20)
plt.ylabel('Spendings', fontsize=30, labelpad=20);


# In[52]:


#Month Since Customer
plt.figure(figsize=(20,10))

sns.boxplot(data=customer_kmeans, x='clusters', y = 'Month_Customer',palette='rocket_r');
plt.xlabel('Clusters', fontsize=20, labelpad=20)
plt.ylabel('Month Since Customer', fontsize=30, labelpad=20);


# In[53]:


plt.figure(figsize=(20,10))

sns.boxplot(data=customer_kmeans, x='clusters', y = 'Age',palette='rocket_r');
plt.xlabel('Clusters', fontsize=20, labelpad=20)
plt.ylabel('Age', fontsize=30, labelpad=20);


# In[54]:


plt.figure(figsize=(20,10))

sns.boxplot(data=customer_kmeans, x='clusters', y = 'Children',palette='rocket_r');
plt.xlabel('Clusters', fontsize=20, labelpad=20)
plt.ylabel('No. of Children', fontsize=50, labelpad=20);


# # Data Exploration: Clusters Based

# In[55]:


customer_kmeans.clusters = customer_kmeans.clusters.replace({1: 'first group',
                                                             2: 'second group',
                                                             3: 'third group',
                                                             0: 'zero group'})

customer['clusters'] = customer_kmeans.clusters


# In[56]:


customer


# saving the trained model

# In[58]:





# In[ ]:




