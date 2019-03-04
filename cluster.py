import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from sklearn.preprocessing import MinMaxScaler

from sklearn.preprocessing import scale


# The kmeans algorithm is implemented in the scikits-learn library
from sklearn.cluster import KMeans
from sklearn.metrics import  silhouette_score
def replace_q(x):
    '''used by clean_data function to remove question marks from dataset'''
    if x.strip() == '?':
        return np.nan
    else:
        return x

def clean_data():
    '''
    imports and cleans data set

    INPUTS: None

    OUTPUTS:
        pandas dataframe of cleaned data
        list - categorical data columns
        list - continuous data columns
    '''
    cols = ['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal','num']
    
    url="C:/Users/venkat/Desktop/ufa/coursework/sem-2/Dr Beth/knn_clustering/HeartDisease_Cleaveland - Copy.csv"
    df = pd.read_csv(url, index_col=False, names=cols, header=None)

    #replace '?' with 'np.nan' for now to avoid errors in eda
    #cast dtypes as float
    df['ca'] = df['ca'].apply(replace_q).astype('float64')
    df['thal'] = df['thal'].apply(replace_q).astype('float64')

    #drop rows with nans for now. only looses 6 rows. consider filling with mean values in future
    df.dropna(inplace=True)

    #separate categorical variables from continuous
    cat_var = [col for col in df.columns.tolist() if len(df[col].unique()) <=5]
    cont_var = [col for col in df.columns.tolist() if len(df[col].unique()) > 5]

    #map booleans to predictor column see eda for details on why
    df['num'] = df['num'] > 0
    df['num'] = df['num'].map({False: 0, True: 1})
    return df, cat_var, cont_var

dataframe, cat_var, cont_var = clean_data()
#print(A)

print("-----------------------------------------")
scaler = MinMaxScaler()
dataframe[dataframe.columns] = scaler.fit_transform(dataframe[dataframe.columns])
#A = scale(A.values, axis=0)
print(dataframe)
A = dataframe.copy(deep=True)
#A = pd.read_csv("C:/Users/venkat/Desktop/ufa/coursework/sem-2/Dr Beth/knn_clustering/A.csv")
for k in range(2, 11):
    # Create a kmeans model on our data, using k clusters.  random_state helps ensure that the algorithm returns the same results each time.
    kmeans_model = KMeans(n_clusters=k, random_state=1).fit(A.iloc[:, :])

    # These are our fitted labels for clusters -- the first cluster has label 0, and the second has label 1.
    labels = kmeans_model.labels_

    # Sum of distances of samples to their closest cluster center
    interia = kmeans_model.inertia_
    print("k:", k, " cost:", interia)


    #------------------------------------------------------------------------
    # Initialize the clusterer with n_clusters value and a random generator
    # seed of 10 for reproducibility.



    # The silhouette_score gives the average value for all the samples.
    # This gives a perspective into the density and separation of the formed
    # clusters


    score = silhouette_score(A, labels, metric='euclidean')
    print("For n_clusters = {}, silhouette score is {})".format(k, score))