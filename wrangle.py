#basic imports
import pandas as pd
import numpy as np
import os

# env import
from env import host, user, password

# train test split import
from sklearn.model_selection import train_test_split



def get_connection(db, username=user, host=host, password=password):
    '''
    Creates a connection URL
    '''
    return f'mysql+pymysql://{username}:{password}@{host}/{db}'
    
def new_zillow_data():
    '''
    Returns zillow into a dataframe
    '''
    sql_query = '''  SELECT *
    FROM properties_2017
    LEFT OUTER JOIN airconditioningtype 
    USING (airconditioningtypeid)
    LEFT OUTER JOIN architecturalstyletype
    USING (architecturalstyletypeid)
    LEFT OUTER JOIN buildingclasstype 
    USING (buildingclasstypeid)
    LEFT OUTER JOIN heatingorsystemtype
    USING (heatingorsystemtypeid)
    LEFT OUTER JOIN predictions_2017
    USING (id)
    INNER JOIN (
    SELECT id, MAX(transactiondate) as last_trans_date 
    FROM predictions_2017
    GROUP BY id
    ) predictions ON predictions.id = properties_2017.id AND predictions_2017.transactiondate = predictions.last_trans_date
    LEFT OUTER JOIN propertylandusetype
    USING(propertylandusetypeid)
    LEFT OUTER JOIN storytype
    ON storytype.storytypeid = properties_2017.storytypeid
    LEFT OUTER JOIN typeconstructiontype
    ON typeconstructiontype.typeconstructiontypeid = properties_2017.typeconstructiontypeid
    JOIN unique_properties
    ON unique_properties.parcelid = properties_2017.parcelid
    WHERE latitude IS NOT NULL and longitude IS NOT NULL; '''
    df = pd.read_sql(sql_query, get_connection('zillow'))
    return df 

def get_zillow_data():
    '''get connection, returns zillow into a dataframe and creates a csv for us'''
    if os.path.isfile('zillow.csv'):
        df = pd.read_csv('zillow.csv', index_col=0)
    else:
        df = new_zillow_data()
        df.to_csv('zillow.csv')
    return df

def drop_nulls(df, prop_req_col = .5 , prop_req_row = .5, inplace = True):
    '''Drops colums and rows with more than 50 % null values'''
    threshold = int(prop_req_col * len(df.index)) 
    df.dropna(axis = 1, thresh = threshold, inplace = True)
    threshold = int(prop_req_row * len(df.columns)) 
    df.dropna(axis = 0, thresh = threshold, inplace = True)
    return df

def remove_outliers(df, k, col_list):
    ''' remove outliers from a list of columns in a dataframe 
        and returns that dataframe
    '''
    
    for col in col_list:

        q1, q3 = df[f'{col}'].quantile([.25, .75])  # get quartiles
        
        iqr = q3 - q1   # calculate interquartile range
        
        upper_bound = q3 + k * iqr   # get upper bound
        lower_bound = q1 - k * iqr   # get lower bound

        # return dataframe without outliers
        
        return df[(df[f'{col}'] > lower_bound) & (df[f'{col}'] < upper_bound)]
    
def get_counties(df):
    '''
    This function will create dummy variables out of the original fips column. 
    And return a dataframe with all of the original columns except regionidcounty.
    We will keep fips column for data validation after making changes. 
    New columns added will be 'LA', 'Orange', and 'Ventura' which are boolean 
    The fips ids are renamed to be the name of the county each represents. 
    '''
    # create dummy vars of fips id
    county_df = pd.get_dummies(df.fips)
    # rename columns by actual county name
    county_df.columns = ['LA', 'Orange', 'Ventura']
    # concatenate the dataframe with the 3 county columns to the original dataframe
    df_dummies = pd.concat([df, county_df], axis = 1)
    # drop regionidcounty and fips columns
    df_dummies = df_dummies.drop(columns = ['regionidcounty'])
    #county column with which county the property is located in
    df_dummies['county'] = df_dummies.fips.apply(lambda x: 'Orange' if x == 6059.0 else 'Los angeles' if x == 6037.0 else 'Ventura')
    #drop fips with county and encoded counties i wont need fips anymore
    df_dummies = df_dummies.drop(columns=['fips'])
    return df_dummies

def remove_outliers_manually(df):
    '''
    #remove outliers in bed(less than zero), bath(less than zero), square feet, & acres
    '''

    return df[((df.bathroomcnt <= 7) & (df.bedroomcnt <= 7) & 
               (df.bathroomcnt > 0) & 
               (df.bedroomcnt > 0) & 
               (df.acres < 15) &
               (df.calculatedfinishedsquarefeet < 10000)&
               (df.taxvaluedollarcnt < 1_500_000))]

def train_validate_test_split(df, target, seed=66):
    '''
    This function takes in a dataframe, the name of the target variable
    (for stratification purposes), and an integer for a setting a seed
    and splits the data into train, validate and test. 
    The function returns, in this order, train, validate and test dataframes. 
    '''
    train_validate, test = train_test_split(df, test_size=0.2, 
                                            random_state=seed)
    train, validate = train_test_split(train_validate, test_size=0.3, 
                                       random_state=seed)
    
    # split train into X (dataframe, drop target) & y (series, keep target only)
    X_train = train.drop(columns=[target])
    y_train = train[target]
    
    # split validate into X (dataframe, drop target) & y (series, keep target only)
    X_validate = validate.drop(columns=[target])
    y_validate = validate[target]
    
    # split test into X (dataframe, drop target) & y (series, keep target only)
    X_test = test.drop(columns=[target])
    y_test = test[target]
    
    return train, validate, test

def xysplit(train,validate,test,target):
    # split train into X (dataframe, drop target) & y (series, keep target only)
    X_train = train.drop(columns=[target])
    y_train = train[target]
    
    # split validate into X (dataframe, drop target) & y (series, keep target only)
    X_validate = validate.drop(columns=[target])
    y_validate = validate[target]
    
    # split test into X (dataframe, drop target) & y (series, keep target only)
    X_test = test.drop(columns=[target])
    y_test = test[target]
    return X_train, y_train, X_validate, y_validate, X_test, y_test


def prep_zillow():
    '''Removes all outlieirs from the function via remove_outliers and remove_outliers_2,
    drops all irelevant columns, drops items from column and rows with less than 50% value. Fills remaining null values, 
    Drops duplicated columns brought in from MySQL. '''
    
    # brings in data from sql or csv file
    df = get_zillow_data()
    
    # Drops duplicated columns from MySql
    df = df.loc[:,~df.columns.duplicated()]
    
    # Ensures we are only bringing in single use properties
    single_use_codes = [261, 262, 263, 264, 265, 268, 273,275, 276, 279]
    df = df[df['propertylandusetypeid'].isin(single_use_codes)]
    
    # Drops null rows and columns that have less than have more nulls than threshhold (50%)
    df = drop_nulls(df, prop_req_col = .5 , prop_req_row = .5, inplace = True)
    

    dropcols = ['id',
            'heatingorsystemtypeid',
            'propertycountylandusecode',
            'buildingqualitytypeid',
            'rawcensustractandblock',
            'unitcnt',
            'propertyzoningdesc',
            'heatingorsystemdesc',
            'censustractandblock',
            'calculatedbathnbr',
            'finishedsquarefeet12',
            'fullbathcnt',
            'assessmentyear',
            'propertylandusetypeid',
            'parcelid.1',
            'id.1',
            'parcelid.2',
            'roomcnt',
            'last_trans_date',
            'regionidcity',
            'regionidzip',
            'transactiondate']
    
    # Drops columns I have deemed irellivant
     # - id because its a usless and duplicated
     # - heatingorsystemtypeid because it was missing about 20k values to much to fill
     # - heatingorsystemdesc because it was missing about 20k values to much to fill
     # - propertylandusetypeid is useless to me after the dropping irrelevant data earlier
     # - buildingqualitytypeid because it was missing about 20k values to much to fill
     # - rawcensustractandblock useless data to me
     # - unitcnt is useless to me after the dropping irrelevant data earlier
     # - propertyzoningdesc because it was missing about 20k values to much to fill
     # - censustractandblock isn't useful to me
     # - calculatedbathnbr data is inconsistent 
     # - finishedsquarefeet12 calculatedsquarefeet is a better metric
     # - fullbathcnt redundant to bathroom count
     # - assessmentyear values are all 2016
     # - propertylandusetypeid because the data was filtered already. 
    df = df.drop(columns=dropcols)
    
    
    # Creats 3 new boolean columns out of fips labeling counties
    df = get_counties(df)
    
    
    # Filling nulls in yearbuilt with 2017
    df['yearbuilt'].fillna(2017, inplace = True)
    # Dropped about a thousand values here no eal good way to determine land size
    df.dropna(subset=['lotsizesquarefeet'], inplace = True)
    # Drop remaining nulls
    df = df.dropna()
    
    
    # Added an acres column, When I previously explored this data I had noticed some anomolies
    df['acres'] = df.lotsizesquarefeet/43560
    
    # Removes properties with 0 beds or baths, properties with greater than 15 acres of property, more than 6 bedrooms or bathrroms and mre than 10000 sqft
    df = remove_outliers_manually(df)
    
    #rename the columns
    df = df.rename(columns={
                            'calculatedfinishedsquarefeet': 'sqft',
                            'bathroomcnt': 'baths',
                            'bedroomcnt': 'beds',
                            'taxvaluedollarcnt':'tax_value',
                            'yearbuilt':'year_built',
                            'taxamount': 'tax_amount'
        
    })
    df['abs_logerror']= df.logerror.abs()
    df['age']=2017-df.year_built
    # Splits data into train, validate, test, X_train, y_train, X_validate, y_validate, X_test, and y_test
    train, validate, test = train_validate_test_split(df,'logerror', seed=66)
    return train, validate, test

