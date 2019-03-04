import pandas as pd
import numpy as np
import matplotlib.pyplot as plt   #Data visualisation libraries
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
lm = LinearRegression()


filename = 'C:\mine\Churn_Clean_Venkat.csv'
colnames = ['State','Account Length','Intl Plan','VMail Plan','VMail Message','Day Mins','Day Calls',
            'Day Charge','Eve Mins','Eve Calls','Eve Charge','Night Mins','Night Calls','Night Charge','Intl Mins','Intl Calls',
            'Intl Charge','CustServ Calls','Churn','ChargeTotal']
data = pd.read_csv(filename, delimiter=',',names=colnames, skiprows=[0])
data.head()
data.info()
data.describe()
data.columns

#sns.pairplot(data)
data.corr()
#-------------------to predict ChargeTotal using the predictors in X
X = data[['Day Mins', 'Day Calls', 'Eve Calls', 'Intl Mins', 'Intl Calls','Night Mins','Night Calls']]
y = data['ChargeTotal']
#partition dataset into train and test (80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=1234)
#create the model
model = lm.fit(X_train,y_train)
print('Coefficients: \n', lm.coef_) #[ 1.70678612e-01 -1.16220798e-03  4.29964468e-05  2.35744974e-01
 #-2.37437298e-02 -4.79270252e-05  8.38990426e-03]
#y intercept
print(lm.intercept_) #25.738174369162664
# variance score: 1 means perfect prediction
print('Variance score: {}'.format(lm.score(X_test, y_test))) #0.7856638940691193

y_pred = lm.predict(X_test)
#RMSE value
print(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))#4.861495027360198