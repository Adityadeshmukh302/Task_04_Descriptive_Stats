# Task 04: Descriptive Statistics System

## Overview

This project demonstrates reproducible descriptive statistics and data cleaning for three real-world datasets using **Pure Python**, **Pandas**, and **Polars**.  
It is part of Research Task 4, which compares base Python, Pandas, and Polars approaches for data summarization and analysis.

**Datasets analyzed:**
- Google Play Store Apps
https://www.kaggle.com/datasets/lava18/google-play-store-apps
- Telco Customer Churn
https://www.kaggle.com/datasets/blastchar/telco-customer-churn
- Video Games Sales
https://www.kaggle.com/datasets/rush4ratio/video-game-sales-with-ratings

All data cleaning is performed before analysis to ensure accuracy and reproducibility.

---

## How to Run

1. **Install dependencies**  
   You need Python 3.10+ and the following libraries:
   ```bash
   pip install polars pandas
   ```

2. **Place datasets**  
   Download and place the following files in the `Dataset_task4` folder:
   - `googleplaystore.csv`
   - `Telco_Customer_Churn.csv`
   - `Video_Games_Sales_as_at_22_Dec_2016.csv`

3. **Run the scripts**
   - **Pure Python:**  
     ```bash
     python src/pure_python_stats.py
     ```
   - **Pandas:**  
     ```bash
     python src/pandas_stats_task4.py
     ```
   - **Polars:**  
     ```bash
     python src/polars2new.py
     ```

---

## What the Code Does

### Pure Python (`pure_python_stats.py`)
- Loads each dataset using only the standard library (`csv`).
- Cleans columns and converts types manually.
- Computes count, mean, min, max, and (optionally) standard deviation for numeric columns.
- For categorical columns: computes unique value counts and most frequent values.
- Performs group-wise analysis (e.g., by contract, category, genre).

### Pandas (`pandas_stats_task4.py`)
- Loads each dataset using Pandas.
- Cleans columns using vectorized string and numeric operations.
- Uses `DataFrame.describe()` for numeric summaries.
- Uses `value_counts()` and `nunique()` for categorical summaries.
- Performs group-wise analysis using `groupby()`.

### Polars (`polars2new.py`)
- Loads each dataset using Polars.
- Cleans columns using efficient string and type operations.
- Uses `DataFrame.describe()` for numeric summaries.
- Uses `group_by().count()` and `.n_unique()` for categorical summaries.
- Performs group-wise analysis using `group_by()`.

---

## Data Cleaning Steps

- **Remove unwanted characters** (e.g., `$`, `,`, `+`, whitespace)
- **Convert columns to correct types** (e.g., string to int/float)
- **Handle missing values** (e.g., treat `tbd` as null)
- **Standardize categorical values** (e.g., strip whitespace)

---

## Findings & Output Summary

### 1. Google Play Store

- **Descriptive statistics** show average app rating, review counts, price, and installs.
- **Top Categories:** Most apps are in "Family", "Game", and "Tools".
- **Unique Content Ratings:** Several, with "Everyone" being most common.
- **Average Rating by Category:** Some categories (e.g., "Events", "Education") have higher average ratings.
- **Top Installed Apps:** The most installed apps have tens of millions of installs.

**Sample Output:**
```
=== Google Play Store Dataset ===
First 5 rows after cleaning:
...
Descriptive statistics (numeric columns):
...
Top Categories by count:
...
Unique Content Ratings: 6
Average Rating by Category:
...
Top 10 most installed apps:
...
```

### 2. Telco Customer Churn

- **Descriptive statistics** show tenure, monthly charges, and total charges.
- **Top Contracts:** "Month-to-month" is the most common contract type.
- **Unique Payment Methods:** Multiple, with "Electronic check" and "Mailed check" common.
- **Average Monthly Charges by Contract:** Longer contracts tend to have lower average monthly charges.
- **Top Customers by Total Charges:** Some customers have paid thousands in total charges.

**Sample Output:**
```
=== Telco Customer Churn Dataset ===
First 5 rows after cleaning:
...
Descriptive statistics (numeric columns):
...
Top Contracts by count:
...
Unique Payment Methods: 4
Average Monthly Charges by Contract:
...
Top 10 customers by TotalCharges:
...
```

### 3. Video Games Sales

- **Descriptive statistics** show sales across regions, critic/user scores.
- **Top Genres:** "Action", "Sports", and "Role-Playing" are most common.
- **Unique Platforms:** Many, with "PS2", "DS", "PS3", "Wii" among the most frequent.
- **Average Global Sales by Genre:** "Sports" and "Platform" genres have highest average global sales.
- **Top Games by Global Sales:** "Wii Sports", "Super Mario Bros.", and "Mario Kart Wii" are top sellers.

**Sample Output:**
```
=== Video Games Sales Dataset ===
First 5 rows after cleaning:
...
Descriptive statistics (numeric columns):
...
Top Genres by count:
...
Unique Platforms: 31
Average Global Sales by Genre:
...
Top 10 games by Global Sales:
...
```

---

## Insights & Recommendations

- **Polars is fast and memory-efficient** for large datasets, with syntax similar to Pandas.
- **Pandas is more familiar for most analysts** and has a rich ecosystem for visualization.
- **Pure Python is flexible but verbose and slow** for large datasets.
- **Data cleaning is crucial** for accurate analysis (e.g., converting strings to numbers, handling missing values).
- **Group-wise summaries** help uncover trends (e.g., which contract types or genres perform best).
- **For reproducible research:** Always clean data before analysis and document your steps.

---

