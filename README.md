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

This is a place holder for when I have key takeaways and fingings
I will also be placing the graphic that best represents my findings at the placeholder gif below. 

![Random GIF](https://media.giphy.com/media/ZVik7pBtu9dNS/giphy.gif)

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

# Data Science Pipeline
[(Back to top)](#table-of-contents)
<!-- Describe your Data Science Pipeline process -->
Following best practices I documented my progress throughout the project and will provide quick summaries and thoughts here. For a further deep dive visit my (enter explore notebook here) & (enter final notebook here)

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
    I quantified single family homes as properties with a propertylandusetypeid of:
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
- removed outliers from
    - calculatedfinishedsquarefeet
    - bedroomcnt
    - bathroomcnt

### Explore
[(Back to top)](#table-of-contents)
<!-- Describe your explore process -->

### Model
[(Back to top)](#table-of-contents)
<!-- Describe your modeling process -->

### Evaluate
[(Back to top)](#table-of-contents)
<!-- Describe your evaluation process -->


# Conclusion
[(Back to top)](#table-of-contents)
<!-- Wrap up with conclusions and takeaways -->


# Given More Time
[(Back to top)](#table-of-contents)
<!-- LET THEM KNOW WHAT YOU WISH YOU COULD HAVE DONE-->

# Recreate This Project
[(Back to top)](#table-of-contents)
<!-- How can they do what you do?-->

# Footer
[(Back to top)](#table-of-contents)
<!-- LET THEM KNOW WHO YOU ARE (linkedin links) close with a joke. -->

