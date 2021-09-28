<!-- Add banner here -->
![Banner](https://github.com/brandon-sharpe/Zillow-Clustering-Project/blob/main/Zillow.gif)

# Zillow Clustering Project

<!-- Add buttons here -->

![GitHub release (latest by date including pre-releases)](https://img.shields.io/badge/release-draft-yellow)
![GitHub last commit](https://img.shields.io/badge/last%20commit-Sep%202021-green)

<!-- Describe your project in brief -->
The Zestimate is a powerful tool used by zillow to predict the final sale price of realestate. My goal for this project is to identify whats driving error between the Zestimate and the final sale prices. To accomplish this goal I will be utilizing clustering and regression models. I will present my findings via a notebook walkthrough to my datascience team.   



# Executive Summary
<!-- Add a demo for your project -->

Goal of this project was to find what was driving log error.

I failed to beat the baseline model RMSE of .15

My best model was an OLS model with an RMSE of .161 on unseen data

The clusters I created where ineffective given more time I'd like to do more engineering.



# Table of contents
<!-- Add a table of contents for your project -->

- [Project Title](#project-title)
- [Executive Summary](#executive-summary)
- [Table of contents](#table-of-contents)
- [Data Dictionary](#data-dictionary)
- [Data Science Pipeline](#data-science-pipline)
    - [Acquire](#acquire)
    - [Prepare](#prepare)
    - [Explore](#explore)
    - [Model](#model)
    - [Evaluate](#evaluate)
- [Conclusion](#conclusion)
- [Given More Time](#given-more-time)
- [Recreate This Project](#recreate-this-project)
- [Footer](#footer)

# Data Dictionary
[(Back to top)](#table-of-contents)
<!-- Drop that sweet sweet dictionary here-->

| Feature                    | Datatype                | Definition   |
|:---------------------------|:------------------------|:-------------|
| parcelid                   | 55513 non-null: int64   |individual id for unique properties|
| baths                      | 55513 non-null: float64 |# of bathrooms a property has|
| beds                       | 55513 non-null: float64 |# of bedrooms a property has|
| sqft                       | 55513 non-null: float64 |calculated square footage of home|
| latitude                   | 55513 non-null: float64 |where the porperty is located in refrence to latitude|
| longitude                  | 55513 non-null: float64 |where the porperty is located in refrence to  longitude|
| lotsizesquarefeet          | 55513 non-null: float64 |the square footage of the land the propety resides on|
| regionidcity               | 55513 non-null: object  |unique identifier for cities the property is in|
| regionidzip                | 55513 non-null: object  |uniques identifier for the zip code the propert resides in|
| year_built                 | 55513 non-null: float64 |year the property was built|
| structuretaxvaluedollarcnt | 55513 non-null: float64 |the estimated tax value of the property itself|
| tax_value                  | 55513 non-null: float64 |the estimated tax value of the property|
| landtaxvaluedollarcnt      | 55513 non-null: float64 |the estimated tax value of the land the property is on|
| tax_amount                 | 55513 non-null: float64 |How much the owner of the property must pay this year|
| logerror                   | 55513 non-null: float64 |The target of this project (error produced in predictions)|
| transactiondate            | 55513 non-null: object  |Date property was sold|
| propertylandusedesc        | 55513 non-null: object  |What the property is listed as ex.(Single family)|
| LA                         | 55513 non-null: uint8   |Whether or not the propert resides in LA county|
| Orange                     | 55513 non-null: uint8   |Whether or not the propert resides in Orange county|
| Ventura                    | 55513 non-null: uint8   |Whether or not the propert resides in Ventura county|
| county                     | 55513 non-null: object  |The county the resident resides in|
| acres                      | 55513 non-null: float64 |How many acres the property encompasses|

# Data Science Pipeline
[(Back to top)](#table-of-contents)
<!-- Describe your Data Science Pipeline process -->
Following best practices I documented my progress throughout the project and will provide quick summaries and thoughts here. For a further deep dive please visit my final notebook or take a look at the planning that took place for this project using trello (https://trello.com/b/HxywACZ5)

### Acquire
[(Back to top)](#table-of-contents)
<!-- Describe your acquire process -->
The data was acquired from the Codeup MySQL server using the zillow database. I pulled every property from the properties_2017 table (later in prepare I will filter this down further) and joined the following tables:

- airconditioningtype (for labeling purposes)
- architecturalstyletype (for labeling purposes)
- buildingclasstype (for labeling purposes)
- heatingorsystemtype (for labeling purposes)
- predictions_2017 (for logerror which will be our target)(( I also filtered by transaction date and parcel id to handle duplicates))

My goal with this acquisition was to give me as much data as possible moving foward.
At this point our data has
* *77614 rows*
* *74 columns*

(for a dive into the acquire funtions refer to (insert link to wrangle.py here))

### Prepare
[(Back to top)](#table-of-contents)
<!-- Describe your prepare process -->
Performed the following on my acquired data.

- dropped null values from columns and rows which had less than 50% of the values.
- dropped all data from properties that where not single value homes
    - I quantified single family homes as properties with a propertylandusetypeid of:
        - 261	Single Family Residential
        - 262	Rural Residence
        - 263	Mobile Home
        - 264	Townhouse
        - 265	Cluster Home
        - 268	Row House
        - 273	Bungalow
        - 275	Manufactured, Modular, Prefabricated Homes
        - 276	Patio Home
        - 279	Inferred Single Family Residential
- dropped the duplicated columns pulled over from the sql inquiry
- removed outliers by upper and lower iqr fences from
    - calculatedfinishedsquarefeet
    - bedroomcnt
    - bathroomcnt
- Further removed outliers manually with the following conditions
    - bathroom count or bedroom count greater than 6 
    - bathroom coutnt or bedroom count less than 1 
    - properties with greater than 15 acres
    - properties with a square footage above 10,000
- Drops columns I have deemed irellivant
    - id because its a usless and duplicated
    - heatingorsystemtypeid because it was missing about 20k values to much to fill
    - heatingorsystemdesc because it was missing about 20k values to much to fill
    - propertylandusetypeid is useless to me after the dropping irrelevant data earlier
    - buildingqualitytypeid because it was missing about 20k values to much to fill
    - rawcensustractandblock useless data to me
    - unitcnt is useless to me after the dropping irrelevant data earlier
    - propertyzoningdesc because it was missing about 20k values to much to fill
    - censustractandblock isn't useful to me
    - calculatedbathnbr data is inconsistent 
    - finishedsquarefeet12 calculatedsquarefeet is a better metric
    - fullbathcnt redundant to bathroom count
    - assessmentyear values are all 2016
    - propertylandusetypeid because the data was filtered already. 
    - roomcnt because it is inconsistent with data
- Created boolean columns for county
- Replace fips with county column for exploration purposes.
- Filled null values in the following columns
    - year
    - regionidcity with mode (want to possibly use this as a feature to determine price variation between cities)
    - regionidzip with mode (same as above possibly more accurate than fips)
- Dropped remaining null values
-Created an Acres column. (Im assuming property size is relevant in log error, further exploration is needed.)
- Renamed several columns for readability, may update more later.

At this point our data has
* *55513 rows*
* *22 columns*

We will now split our data into train, validate, and split.


### Explore
[(Back to top)](#table-of-contents)
<!-- Describe your explore process -->
Hypothesis: Location plays a role in log error

Hypothesis: Age Plays a role in log error

Hypothesis: Tax Value plays a role in log error



Its time to Explore.
** I thought it may be more productive to use absolute log error for my product, Looking back this was a mistake as thats not what the original metric was.

* Age appears tobe a driver of log error
* As does Tax Value
* longitude and latitude appear to be as well i would like to combine these.
* Created a cluster combining latitutude and longitude does not seem to hold any value, stsastical test do not support the use 
* Created another cluster of tax value and latitude, I wanted to see if more expensive houses along the cost created a higher mean log error. This proved to make non effective  clusters when driving for abs log error.
* Created another cluster of age and tax value, I wanted to see the correlation of age and tax value on the abs log error. Proved to be ineffective. 
    
### Model
[(Back to top)](#table-of-contents)
<!-- Describe your modeling process -->
Created a rfe model to produce the best features selected all bt my clusters which where at the bottom. 

Created a baseline
RSME to beat: .15

RMSE a OLS linear reagreation model
Training/In-Sample:  0.159
Validation/Out-of-Sample:  0.149
This is a little to close to baseline

RMSE Lasso/Lars linear reagreation model
Training/In-Sample:  0.159
Validation/Out-of-Sample:  0.149

RMSE for TweedieRegressor
Training/In-Sample:  0.159
Validation/Out-of-Sample:  0.149

RMSE for 2nd Degree Polynomial
Training/In-Sample:  0.15
Validation/Out-of-Sample:  0.149

### Evaluate
[(Back to top)](#table-of-contents)
<!-- Describe your evaluation process -->
Most of these models where within .0002 or less of each other.

I chose to use the best perfoming model which was the OLS

RMSE for OLS Model
Training/In-Sample:  0.1597255269835122 
Validation/Out-of-Sample:  0.14950052346348475 
Test/Out-of-Sample:  0.16146151424220911
I could not beat baseline


# Conclusion
[(Back to top)](#table-of-contents)
<!-- Wrap up with conclusions and takeaways -->

Our model was not able to beat the baseline rmse of .15 

It scored an rmse of .161

Our clusters where not benefiecal to the process with rfe putting almost every created cluster at the bottom

The following where the drivers rfe picked
- 'LA',
- 'Orange',
- 'Ventura',
- 'sqft_scaled',
- 'beds_scaled',
- 'baths_scaled',
- 'year_built_scaled',
- 'latitude_scaled',
- 'longitude_scaled',
- 'acres_scaled',
- 'age_scaled',
- 'structuretaxvaluedollarcnt_scaled'

Moving foward my recommendation is to continue using the current models until such a time I can create substaintial clusters. 

# Given More Time
[(Back to top)](#table-of-contents)
<!-- LET THEM KNOW WHAT YOU WISH YOU COULD HAVE DONE-->

- I'd spend more time engineering effective clusters, maybe throwing more than 2 variables into a cluster at a time
- I'd also like to break the models down to a per county bases and try to establish effective neighborhood clusters


# Recreate This Project
[(Back to top)](#table-of-contents)
<!-- How can they do what you do?-->
You can recreate this project by downloading my wrangle, and explore and this notebook and using your own env file to acess the sql database.


# Footer
[(Back to top)](#table-of-contents)
<!-- LET THEM KNOW WHO YOU ARE (linkedin links) close with a joke. -->

If you have anyquestions please feel free to reach out to me.
