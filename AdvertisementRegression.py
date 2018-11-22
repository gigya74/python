#!/usr/bin/env python
# coding: utf-8

# In[1]:


# our usual first step: get the modules loaded.
import pandas as pd
import numpy as np
import scipy as sp
import statsmodels.api as sm
import statsmodels.formula.api as smf
import seaborn as sns
sns.set_style("whitegrid")
sns.set_context("notebook", font_scale=1, rc={"lines.linewidth": 2,'font.family': [u'times']})
import matplotlib.pylab as plt
#get_ipython().run_line_magic('matplotlib', 'inline')
plt.style.use('seaborn-whitegrid')
plt.rc('text', usetex = False)
plt.rc('font', family = 'serif')
plt.rc('xtick', labelsize = 10)
plt.rc('ytick', labelsize = 10)
plt.rc('font', size = 12)
plt.rc('figure', figsize = (12, 5))


# In[2]:


advertising = pd.read_csv('Advertising.csv', usecols=[1,2,3,4])


# In[3]:


advertising.info()


# In[4]:


advertising.describe()


# In[5]:


sns.pairplot(data=advertising,
                  y_vars=['Sales'],
                  x_vars=['TV', 'Radio', 'Newspaper'])


# In[6]:


sp.stats.pearsonr(advertising.TV, advertising.Sales) #correlation and its p-value


# In[7]:


advertising.corr() #correlation matrix


# In[8]:


# Draw a correlation heatmap
corrmat = advertising.corr()
sns.heatmap(corrmat, square = True, cmap="YlGnBu")


# In[9]:


TVSales=sns.jointplot(x="TV", y="Sales", data=advertising)
TVSales.savefig("TVSales.pdf")


# In[10]:


RadioSales=sns.jointplot(advertising.Radio, advertising.Sales)
RadioSales.savefig("RadioSales.pdf")


# In[11]:


NPSales=sns.jointplot(advertising.Newspaper, advertising.Sales)
NPSales.savefig("NPSales.pdf")


# In[12]:


TVreg=sns.lmplot("TV", "Sales", advertising, order=1, ci=95, scatter_kws={'color':'r'})
plt.savefig("TVreg.pdf")


# In[13]:


Radioreg=sns.lmplot("Radio", "Sales", data=advertising,order=1, ci=95, scatter_kws={'color':'b'})
plt.savefig("Radioreg.pdf")


# In[14]:


NPreg=sns.lmplot("Newspaper", "Sales", advertising, order=1, ci=95, scatter_kws={'color':'b'})
plt.savefig("NPreg.pdf")


# In[15]:


#TV regression using sklearn library

import sklearn.linear_model as sklm
from sklearn.metrics import mean_squared_error, r2_score
Tvreg=sklm.LinearRegression()
X=advertising.TV.values.reshape(200,1) #Sklearn expects it in this array format
Y=advertising.Sales
Tvreg.fit(X, Y)
print('Intercept:', Tvreg.intercept_)
print('Beta 1:', Tvreg.coef_)
Sales_predict=Tvreg.fit(X, Y).predict(X)
MSE=mean_squared_error(Y, Sales_predict)
R2=r2_score(Y, Sales_predict)
print("Mean Squared Error:", MSE)
print("R-Squared:", R2)


# In[16]:


formula='Sales ~ TV'
model = smf.ols(formula, data=advertising)
Tvreg1 = model.fit()
Tvreg1.summary()


# In[17]:


X2 = advertising.TV
X3 = sm.add_constant(X2)  # Adds a constant term to the predictor
est = sm.OLS(advertising.Sales, X3) # Creates an object OLS estimator
Tvreg2 = est.fit()
Tvreg2.summary()


# In[18]:


formula='Sales ~ TV + Radio + Newspaper'
model = smf.ols(formula, data=advertising)
Salesreg = model.fit()
Salesreg.summary()


# In[19]:


import sklearn.linear_model as sklm
from sklearn.metrics import mean_squared_error, r2_score
salesreg2 = sklm.LinearRegression()
X = advertising[['TV', 'Radio']].as_matrix()
y = advertising.Sales
salesreg2.fit(X,y)
print('Intercept:', salesreg2.intercept_)
print('TV:', salesreg2.coef_[0])
print('Radio:', salesreg2.coef_[1])
Sales_predict2=salesreg2.fit(X, y).predict(X)
MSE=mean_squared_error(y, Sales_predict2)
R2=r2_score(y, Sales_predict2)
print("Mean Squared Error:", MSE)
print("R-Squared:", R2)


# In[20]:


# let's use the min/max values of TV and Radio for setting up the grid for plotting.
advertising[['TV', 'Radio']].describe()


# In[21]:


# Create a coordinate grid
TV = np.arange(0,300)
Radio = np.arange(0,50)

B1, B2 = np.meshgrid(TV, Radio, indexing='xy')
Z = np.zeros((Radio.size, TV.size))
for (i,j),v in np.ndenumerate(Z):
        Z[i,j] =(salesreg2.intercept_ + B1[i,j]*salesreg2.coef_[0] + B2[i,j]*salesreg2.coef_[1])


# In[28]:


# Create plot
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure(figsize=(10,6))
fig.suptitle('Regression: Sales ~ TV + Radio', fontsize=20)

ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(B1, B2, Z, rstride=10, cstride=5, alpha=0.4)
ax.scatter3D(advertising.TV, advertising.Radio, advertising.Sales, c='r')

ax.set_xlabel('TV')
ax.set_xlim(0,300)
ax.set_ylabel('Radio')
ax.set_ylim(ymin=0)
ax.set_zlabel('Sales')
fig.savefig("salestvradio.pdf")


# In[ ]:




