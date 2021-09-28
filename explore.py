import pandas as pd
import numpy as np
import wrangle as w
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style='white')
sns.set_palette("colorblind")
import sklearn.preprocessing
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

import sklearn.preprocessing
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression, LassoLars, TweedieRegressor
from sklearn.preprocessing import PolynomialFeatures

from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score
from sklearn.feature_selection import f_regression

from scipy import stats




def distros(df):
    for col in (df).columns:
        plt.hist((df)[col])
        plt.title(col)
        plt.show()
        

def explore_univariate(df, variable):
    '''
    explore_univariate will take in a dataframe, and one feature or variable. It graphs a box plot and a distribution 
    of the single variable.
    '''
    #set figure size, font for axis ticks
    plt.figure(figsize=(30,10))
    sns.set(font_scale = 2)
    
    # boxplot and stipplot
    plt.subplot(1, 2, 1)
    ax1= sns.boxplot(x=variable, data=df)
    sns.stripplot(x=variable, data=df)
    plt.xlabel('')
    plt.title('Box Plot', fontsize=30)
    

    
    
    
    # distribution
    plt.subplot(1, 2, 2)
    ax2= sns.histplot(data=df, x=variable, element='step', kde=True)
    plt.xlabel('')
    plt.ylabel('')
    plt.title('Distribution', fontsize=30)
    

    #title
    plt.suptitle(f'{variable}', fontsize = 45)
    plt.tight_layout()
    plt.show()


def logerror_uni(df, variable):
    '''
    explore_univariate will take in a dataframe, and one feature or variable. It graphs a box plot and a distribution 
    of the single variable.
    '''
    #set figure size, font for axis ticks
    plt.figure(figsize=(30,10))
    sns.relplot(variable, df.abs_logerror, data =df)
    plt.title(f'Absolute Log Error and {variable}')

    plt.show()
    

def add_scaled_columns(train, validate, test, scaler, columns_to_scale):
    '''Takes in df and scales the columns inputed and concats them to the dataframe '''    
    # new column names
    new_column_names = [c + '_scaled' for c in columns_to_scale]
    
    # Fit the scaler on the train
    scaler.fit(train[columns_to_scale])
    
    # transform train validate and test
    train = pd.concat([
        train,
        pd.DataFrame(scaler.transform(train[columns_to_scale]), columns=new_column_names, index=train.index),
    ], axis=1)
    
    validate = pd.concat([
        validate,
        pd.DataFrame(scaler.transform(validate[columns_to_scale]), columns=new_column_names, index=validate.index),
    ], axis=1)
    
    
    test = pd.concat([
        test,
        pd.DataFrame(scaler.transform(test[columns_to_scale]), columns=new_column_names, index=test.index),
    ], axis=1)
    
    return train, validate, test

def inertia_graph(X):
    plt.figure(figsize=(9, 6))
    pd.Series({k: KMeans(k).fit(X).inertia_ for k in range(2, 12)}).plot(marker='x')
    plt.xticks(range(2, 12))
    plt.xlabel('k')
    plt.ylabel('inertia')
    plt.title('Change in inertia as k increases')
    
def create_cluster(train, X, k, cluster_name):
    ''' Takes in df, X (dataframe with variables you want to cluster on), k number of clusters,
    and the name you want to name the column (enter column as string)
    It scales the X, calcuates the clusters and return train (with clusters), the Scaled dataframe,
    the scaler and kmeans object and unscaled centroids as a dataframe
    note: train_scaled enter the scaled train dataframe
    for X enter the dataframe of the two features for your cluster
    for k enter number of features
    for cluster_name enter name of the cluster column name you want as a string
    '''
    scaler = MinMaxScaler().fit(X)
    X = pd.DataFrame(scaler.transform(X), columns=X.columns.values).set_index([X.index.values])
    kmeans = KMeans(n_clusters = k, random_state = 66)
    kmeans.fit(X)
    kmeans.predict(X)
    train[cluster_name] = kmeans.predict(X)
    # train_scaled[cluster_name] = 'cluster_' + train_scaled[cluster_name].astype(str)
    centroids = pd.DataFrame(scaler.inverse_transform(kmeans.cluster_centers_), columns=X.columns)
    return train, X, scaler, kmeans, centroids

def plot_clusters(x ,y, cluster_col_name, df , kmeans, scaler, centroids):
    
    """ Takes in x and y (variable names as strings, along with returned objects from previous
    function create_cluster and creates a plot"""
    # set palette to zillow colors
    zpalette = ['#1277e1', '#f3ad35', '#0b449c', '#5289e4', '#c3eafb']

    # set figsize
    plt.figure(figsize=(15, 15))
    
    # scatterplot the clusters 
    sns.scatterplot(x = x, y = y, data = df, hue = cluster_col_name, cmap = zpalette)
    
    # plot the centroids as Xs
    centroids.plot.scatter(y=y, x= x, ax=plt.gca(), alpha=.60, s=500, c='black', marker = 'x')
    
def rmse(algo, X_train, X_validate, y_train, y_validate, target, model_name):
    '''
    This function takes in an algorithm name, X_train, X_validate, y_train, y_validate, target and a model name
    and returns the RMSE score for train and validate dataframes.
    '''

    # enter target and model_name as a string
    # algo is algorithm name, enter with capitals for print statement
    
    # fit the model using the algorithm
    algo.fit(X_train, y_train[target])

    # predict train
    y_train[model_name] = algo.predict(X_train)

    # evaluate: rmse
    rmse_train = mean_squared_error(y_train[target], y_train[model_name])**(1/2)

    # predict validate
    y_validate[model_name] = algo.predict(X_validate)

    # evaluate: rmse
    rmse_validate = mean_squared_error(y_validate[target], y_validate[model_name])**(1/2)

    print("RMSE for", model_name, "using", algo, "\nTraining/In-Sample: ", rmse_train, 
          "\nValidation/Out-of-Sample: ", rmse_validate)
    print()
    
    return rmse_train, rmse_validate

def cols():
    cols = [
     'baths',
     'beds',
     'sqft',
     'latitude',
     'longitude',
     'lotsizesquarefeet',
     'year_built',
     'structuretaxvaluedollarcnt',
     'tax_value',
     'landtaxvaluedollarcnt',
     'tax_amount',
     'logerror',
     'propertylandusedesc',
     'LA',
     'Orange',
     'Ventura',
     'county',
     'acres',
     'abs_logerror',
    'age']
    return cols
