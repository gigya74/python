import pandas as pd
import numpy as np
import matplotlib.pyplot as plt   #Data visualisation libraries
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
import statsmodels.api as sm
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

lm = LogisticRegression()


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
#-------------------to predict customers that churn using predictors in X
X = data[['ChargeTotal', 'CustServ Calls','Day Mins','Day Calls', 'Eve Calls','Eve Mins', 'Intl Mins', 'Intl Calls','Night Mins','Night Calls']]
y = data['Churn']

just_dummies = pd.get_dummies(data['Churn'])

step_1 = pd.concat([data, just_dummies], axis=1)
step_1.drop(['Churn', 'c'], inplace=True, axis=1)
#partition dataset into train and test (80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=1234)
#create the model
model = lm.fit(X_train,y_train)


y_pred = lm.predict(X_test)
cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
print(cnf_matrix)

logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())

print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
print("Precision:",metrics.precision_score(y_test, y_pred))
print("Recall:",metrics.recall_score(y_test, y_pred))

# ROC curve
logit_roc_auc = roc_auc_score(y_test, lm.predict(X_test))
fpr, tpr, thresholds = roc_curve(y_test, lm.predict_proba(X_test)[:,1])
plt.figure()
plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % logit_roc_auc)
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Customers that churn')
plt.legend(loc="lower right")
plt.savefig('Log_ROC')
plt.show()