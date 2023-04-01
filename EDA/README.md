# EDA (Exploratory Data Analysis)
This folder contains notebooks for the exploratory data analysis (EDA) of two datasets: artists and songs. The EDA is performed to examine and visualize the data, and obtain information about the distribution, descriptive statistics, outliers, and relationships between variables.

The analysis for each dataset is divided into two sections: data exploration and data cleaning.

## Data exploration
In the data exploration notebooks, the datasets are loaded and an initial inspection is performed to check for missing values, data types, and inconsistencies. Descriptive statistics and visualizations are created to better understand the distribution of the data and identify potential outliers. The results of this analysis help in identifying the quality of data and any issues that need to be addressed during the cleaning process.

## Data cleaning
In the data cleaning notebooks, the identified issues in the data exploration are addressed. This includes handling missing values, correcting data types, removing duplicates, and dealing with outliers. After cleaning the data, a second exploratory data analysis is performed to ensure the quality of data and to verify that the problems identified in the first analysis have been resolved.

The cleaned data is then saved to a new file for future use in modeling or further analysis.

## Folder structure
```
EDA/
  |- artists/
  |  |- artists_data_analysis.ipynb
  |  |- artists_data_cleaning.ipynb
  |- songs/
  |  |- songs_data_analysis.ipynb
  |  |- songs_data_cleaning.ipynb

```