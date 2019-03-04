#https://www.kaggle.com/fabijanbajo/heart-disease-prediction

#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
#get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


#import dataset while naming columns
cols = ['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal','num']
url="C:/Users/venkat/Desktop/ufa/coursework/sem-2/Dr Beth/knn_clustering/HeartDisease_Cleaveland - Copy.csv"
df = pd.read_csv(url, index_col=False, names=cols, header=None)


# In[3]:


df.head()


# In[4]:


df.describe()


# In[5]:


df.info()


# In[7]:


#investigate object datatypes
print(df['ca'].unique())
print(df['thal'].unique())


# In[9]:


#replace '?' with 'np.nan' for now to avoid errors in eda
#cast dtypes as float
def clean(x):
    if x.strip() == '?':
        return np.nan
    else:
        return x

df['ca'] = df['ca'].apply(clean).astype('float64')
df['thal'] = df['thal'].apply(clean).astype('float64')
print(df['ca'].unique())
print(df['thal'].unique())


# In[10]:


df.info()


# In[12]:


df.dropna(inplace=True)
print(df.shape)


# In[14]:


for col in df.columns.tolist():
    print(col, len(df[col].unique()))


# In[17]:


#separate categorical variables from continuous
cat_var = [col for col in df.columns.tolist() if len(df[col].unique()) <=5]
print(len(cat_var))
cont_var = [col for col in df.columns.tolist() if len(df[col].unique()) > 5]
print(len(cont_var))


# In[18]:


#explore distributions of continuous variables
fig, axes = plt.subplots(3,2, figsize=(12,10))
for i, ax in enumerate(axes.flatten()):
    column_name = cont_var[i]
    ax.hist(df[column_name])
    ax.set_title(column_name)

plt.tightlayout()


# In[19]:


fig, axes = plt.subplots(2, 5, figsize=(12,10))
for i, ax in enumerate(axes.flatten()):
    column_name = cat_var[i]
    ax.hist(df[column_name])
    ax.set_title(column_name)

plt.tightlayout()


# In[20]:


#closer look at predictor column for class imbalance
float(df[df['num'] > 0].shape[0]) / df['num'].shape[0]


# In[21]:


df.head()


# In[22]:


fig, (ax1, ax2) = plt.subplots(1,2, figsize=(8, 4))
ax1.hist(df['num'])
ax1.set_title('Predictor Column')

#change predictor ('num') col to boolean
df['num'] = df['num'] > 0
df['num'] = df['num'].map({False: 0, True: 1})

ax2.hist(df['num'])
ax2.set_title('Predictor Column Cleaned')
plt.xticks([0,1], ['No Heart Disease', 'Heart Disease'])
plt.tight_layout()
plt.savefig('predictor_column.png')


# In[23]:


#covariance matrix for looking into dimensionality reduction
from sklearn.preprocessing import scale
cdf = df.copy()
cdf.pop('num')
cdf = pd.DataFrame(scale(cdf.values), columns=cdf.columns.tolist())
cdf.cov()


# In[25]:


#identify higher correlation values
for col in cdf.columns.tolist():
    mask = cdf.cov()[col].argsort()
    print(col, cdf.cov()[col][mask][-2])
mask = cdf.cov() > 0.3
mask


# In[26]:


df.corr()


# In[ ]:




