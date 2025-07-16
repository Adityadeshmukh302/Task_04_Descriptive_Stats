# Aditya Deshmukh 
# Research Task 4: Pure-Python Analytics with Metadata
# The obejctive for Research task 4 was to replace the Task 3 pandas 
# script with one that supports any CSV + metadata.
# ============================================================
# This script analyzes multiple datasets using pandas.
# It loads each dataset, cleans it, and generates summary statistics.
# For each dataset, it creates a text report with:
#   - Overall numeric and categorical summaries
#   - Grouped statistics based on specified columns
# The datasets and their metadata (column types, groupings) are defined at the top.


# Change the paths in the DATASETS list to point to your local CSV files.
# ============================================================

import pandas as pd

# =========================
# Metadata for Datasets
# =========================
DATASETS = [
    {
        'name': 'Telco Customer Churn',
        'path': 'Dataset/Telco_Customer_Churn.csv',
        'metadata': {
            'numeric': ['tenure', 'MonthlyCharges', 'TotalCharges'],
            'categorical': ['gender', 'Contract', 'PaymentMethod', 'Churn'],
            'group_by': [['Contract'], ['Contract', 'gender']]
        }
    },
    {
        'name': 'Google Play Store Apps',
        'path': 'Dataset/googleplaystore.csv',
        'metadata': {
            'numeric': ['Rating', 'Reviews', 'Size', 'Installs'],
            'categorical': ['Category', 'Type', 'Content Rating'],
            'group_by': [['Category'], ['Category', 'Type']]
        }
    },
    {
        'name': 'Video Game Sales',
        'path': 'Dataset/Video_Games_Sales_as_at_22_Dec_2016.csv',
        'metadata': {
            'numeric': ['Global_Sales', 'Critic_Score', 'User_Score'],
            'categorical': ['Platform', 'Genre', 'Publisher'],
            'group_by': [['Platform'], ['Genre', 'Platform']]
        }
    }
]

# =========================
# Helper Functions
# =========================

def load_and_clean(path):
    """
    Loads a CSV file, replaces empty strings with NA, and drops rows that are all NA.
    Returns a cleaned DataFrame.
    """
    df = pd.read_csv(path)
    df = df.replace(r'^\s*$', pd.NA, regex=True)
    df = df.dropna(how='all')
    return df


def overall_stats(df, numeric_cols, categorical_cols, out):
    """
    Writes overall summary statistics for numeric and categorical columns to the output file.
    """
    out.write('='*60 + '\n')
    out.write('OVERALL SUMMARY\n')
    out.write('='*60 + '\n')
    # Numeric columns summary
    out.write('Numeric columns (describe):\n')
    stats_num = df[numeric_cols].describe().T.round(4)
    out.write(stats_num.to_string() + '\n\n')
    # Categorical columns summary
    out.write('Categorical columns (unique / top values):\n')
    for col in categorical_cols:
        out.write(f"-- {col} --\n")
        out.write(f"Unique: {df[col].nunique(dropna=True)}\n")
        vc = df[col].value_counts(dropna=True).head(5)
        out.write(vc.to_string() + '\n\n')


def grouped_stats(df, keys, numeric_cols, categorical_cols, out):
    """
    Writes grouped summary statistics for numeric and categorical columns to the output file.
    Groups are defined by the 'keys' columns.
    """
    out.write('='*60 + '\n')
    out.write(f"STATS GROUPED BY {tuple(keys)}\n")
    out.write('='*60 + '\n')
    grouped = df.groupby(keys)
    for name, grp in grouped:
        out.write(f"Group = {name}\n")
        # Numeric columns summary for group
        stats_num = grp[numeric_cols].describe().T.round(4)
        out.write(stats_num.to_string() + '\n')
        # Categorical columns summary for group
        for col in categorical_cols:
            out.write(f"  {col} - Unique: {grp[col].nunique(dropna=True)} | Top 5:\n")
            vc = grp[col].value_counts(dropna=True).head(5)
            out.write('    ' + vc.to_string().replace('\n', '\n    ') + '\n')
        out.write('\n')


def analyze_dataset_pd(name, path, meta):
    """
    Loads, cleans, and analyzes a dataset.
    Writes overall and grouped statistics to a text report file.
    """
    df = load_and_clean(path)
    report_file = f"{name.lower().replace(' ', '_')}_pandas_report.txt"
    print(f"Generating pandas report for {name} -> {report_file}")
    with open(report_file, 'w', encoding='utf-8') as out:
        overall_stats(df, meta['numeric'], meta['categorical'], out)
        for keys in meta['group_by']:
            grouped_stats(df, keys, meta['numeric'], meta['categorical'], out)
    print(f"Done! Check {report_file} for {name} pandas report.")


if __name__ == '__main__':
    # Loop through each dataset and generate its report
    for ds in DATASETS:
        analyze_dataset_pd(ds['name'], ds['path'], ds['metadata'])
