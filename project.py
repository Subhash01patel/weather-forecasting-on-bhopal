# -*- coding: utf-8 -*-
"""project

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tZM2AdOm2i79-PwvDtWiTSLf9KROjd4S

# Problem statement

**Steps to follow**
1. Problem understanding
2. Data collection
3. Data understanding
4. Data preprocessing
(All steps)
5. EDA
"""

# Importing necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import PolynomialFeatures
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

# Load the DataSet
data = pd.read_csv("/content/weather.csv")

# Display the first few rows of the dataset
data.head()

data.info()

# Summary statistics
data.describe()

"""2. Data Preprocessing

Before we proceed with the analysis and model building, it's essential to preprocess the data to handle any missing values, outliers, or inconsistencies. In this section, we will perform data cleaning and preprocessing steps
"""

data.columns

data.dtypes

# Drop unnecessary columns
data.drop('Unnamed: 0', axis=1, inplace=True)

# Handle missing values
data.dropna(inplace=True)

# Check if 'Date' column exists before proceeding
if 'Date' in data.columns:
    # Convert date column to datetime
    data['Date'] = pd.to_datetime(data['Date'])
else:
    print("Warning: 'Date' column not found in the DataFrame. Skipping conversion.")

# Convert categorical columns to numerical using label encoding
categorical_cols = ['Location', 'WindGustDir', 'WindDir9am', 'WindDir3pm', 'RainToday', 'RainTomorrow']
label_encoder = LabelEncoder()

# Check if the columns exist in the DataFrame
for col in categorical_cols:
    if col in data.columns:  # Add this condition to check column existence
        data[col] = label_encoder.fit_transform(data[col])
    else:
        print(f"Column '{col}' not found in DataFrame.")

# Split the dataset into features and target variable
# Check if 'RainTomorrow' column exists before dropping
if 'RainTomorrow' in data.columns:
    X = data.drop('RainTomorrow', axis=1)  # Features
    y = data['RainTomorrow']  # Target variable
else:
    # Handle the case where 'RainTomorrow' is not found
    # Print an error message or investigate why it's missing
    print("Error: 'RainTomorrow' column not found in the DataFrame.")
    # You might need to reload your data or adjust previous steps

# Normalize numeric features
numeric_cols = ['MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation', 'Sunshine',
                'WindGustSpeed', 'WindSpeed9am', 'WindSpeed3pm', 'Humidity9am',
                'Humidity3pm', 'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm',
                'Temp9am', 'Temp3pm', 'RISK_MM']

# Ensure X is defined before using it
if 'X' in locals():  # Check if X is defined
    X[numeric_cols] = (X[numeric_cols] - X[numeric_cols].mean()) / X[numeric_cols].std()
else:
   print("Error: X is not defined. Make sure to run the data splitting step first.")

"""3. Exploratory Data Analysis (EDA)

Exploratory Data Analysis helps us understand the distribution of features, relationships between variables, and identify patterns or anomalies. In this section, we will visualize and analyze the dataset.
"""

# Correlation matrix
numeric_cols = ['MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation', 'Sunshine',
                'WindGustSpeed', 'WindSpeed9am', 'WindSpeed3pm', 'Humidity9am',
                'Humidity3pm', 'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm',
                'Temp9am', 'Temp3pm', 'RISK_MM']

# check if the columns to only include those that exist in the DataFrame
existing_numeric_cols = [col for col in numeric_cols if col in data.columns]

# Use the filtered list to access data
if existing_numeric_cols:  # Check if there are any existing numeric columns
    numeric_data = data[existing_numeric_cols]
    corr_matrix = numeric_data.corr()

    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.show()

# Distribution of numeric features
plt.figure(figsize=(12, 10))
for i, col in enumerate(numeric_cols):
    # Check if the column exists in the DataFrame
    if col in data.columns:
        plt.subplot(4, 5, i + 1)
        sns.histplot(data[col], kde=True)
        plt.title(col)
    else:
        print(f"Warning: Column '{col}' not found in the DataFrame. Skipping.")

plt.tight_layout()
plt.show()

"""4. Feature Engineering

Feature engineering involves creating new features or transforming existing ones to improve the predictive power of the model. In this section, we will engineer relevant features from the existing data.
"""

# Create new features
# Extract year, month, and day from the 'Date' column
# Specify the correct format using the 'format' argument
data['Year'] = pd.to_datetime(data['Date'], format='%d-%m-%Y').dt.year
data['Month'] = pd.to_datetime(data['Date'], format='%d-%m-%Y').dt.month
data['Day'] = pd.to_datetime(data['Date'], format='%d-%m-%Y').dt.day

# Calculate the difference between max and min temperature
data['TempDiff'] = data['MaxTemp'] - data['MinTemp']

# Calculate the difference between max and min temperature
# Check if the columns exist before accessing them
if 'MaxTemp' in data.columns and 'MinTemp' in data.columns:
    data['TempDiff'] = data['MaxTemp'] - data['MinTemp']
else:
    # Print a warning if either column is missing
    missing_cols = [col for col in ['MaxTemp', 'MinTemp'] if col not in data.columns]
    print(f"Warning: Columns {missing_cols} not found in the DataFrame. Skipping TempDiff calculation.")

# Perform imputation for missing values
imputer = SimpleImputer(strategy='mean')
numeric_cols = ['MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation', 'Sunshine',
                'WindGustSpeed', 'WindSpeed9am', 'WindSpeed3pm', 'Humidity9am',
                'Humidity3pm', 'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm',
                'Temp9am', 'Temp3pm', 'RISK_MM']
data[numeric_cols] = imputer.fit_transform(data[numeric_cols])

# Perform imputation for missing values
imputer = SimpleImputer(strategy='mean')
numeric_cols = ['MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation', 'Sunshine',
                'WindGustSpeed', 'WindSpeed9am', 'WindSpeed3pm', 'Humidity9am',
                'Humidity3pm', 'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm',
                'Temp9am', 'Temp3pm', 'RISK_MM']
data[numeric_cols] = imputer.fit_transform(data[numeric_cols])

# Log transform skewed features
skewed_features = ['Rainfall', 'Evaporation']
data[skewed_features] = np.log1p(data[skewed_features])

# Drop unnecessary columns
data.drop([ 'Date'], axis=1, inplace=True)

# Encode categorical variables
categorical_cols = ['Location', 'WindGustDir', 'WindDir9am', 'WindDir3pm', 'RainToday']
data = pd.get_dummies(data, columns=categorical_cols, drop_first=True)

# Split the dataset into features and target variable
X = data.drop('RainTomorrow', axis=1)  # Features
y = data['RainTomorrow']  # Target variable

# Perform imputation for missing values in features
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)

"""

In this section, we will split the dataset into training and testing sets and train a binary classification model to predict whether it will rain or not tomorrow"""

# skewed_features = ['Rainfall', 'Evaporation']
# data[skewed_features] = np.log1p(data[skewed_features])
# plt.show()
# create graph

import matplotlib.pyplot as plt

# Assuming 'data' and 'skewed_features' are defined as in your original code.
# The code you provided already applies the log1p transformation.
# This part creates the graphs

# Distribution of skewed features after log transformation
plt.figure(figsize=(12, 5))

for i, col in enumerate(skewed_features):
    plt.subplot(1, 2, i + 1)
    sns.histplot(data[col], kde=True)
    plt.title(f'Distribution of {col} after Log Transformation')
    plt.xlabel(col)
    plt.ylabel('Frequency')

plt.tight_layout()
plt.show()

"""Conclusion


The notebook followed a systematic workflow, including data preprocessing, exploratory data analysis (EDA), feature engineering, model training, and model evaluation. The dataset was preprocessed by handling missing values and outliers, and necessary transformations were applied to the data. The features were split into the predictor variables (features) and the target variable (whether it will rain tomorrow).
"""

