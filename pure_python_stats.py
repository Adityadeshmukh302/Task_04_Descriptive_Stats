"""
Aditya Deshmukh 
Research Task 4: Pure-Python Analytics with Metadata
The obejctive for Research task 4 was to replace the Task 3 pure-Python analytics 
script with one that supports any CSV + metadata.

This script analyzes CSV datasets using metadata.
It calculates summary statistics for numeric and categorical columns,
and can group results by specified columns. It writes a report for each dataset.

- Reads CSV files for three datasets.
- Uses metadata to know which columns are numeric/categorical and how to group.
- Calculates stats like mean, min, max for numbers, and top value for categories.
- Writes results to a text file for each dataset.

Change the paths in the DATASETS list to point to your local CSV files.
"""

import csv
import math
from collections import Counter, defaultdict

# =========================
# Utility Functions
# =========================

def is_number(val):
    """Check if a string can be converted to a float."""
    try:
        float(val)
        return True
    except ValueError:
        return False


def stats_numeric(vals):
    """
    Calculate stats for numeric columns:
    - count, mean, min, max, standard deviation
    """
    nums = [float(x) for x in vals]
    n = len(nums)
    mean = sum(nums) / n if n else 0
    mn = min(nums) if nums else 0
    mx = max(nums) if nums else 0
    var = sum((x - mean) ** 2 for x in nums) / n if n else 0
    std = math.sqrt(var)
    return {
        'count': n,
        'mean': round(mean, 4),
        'min': mn,
        'max': mx,
        'std': round(std, 4)
    }


def stats_categorical(vals):
    """
    Calculate stats for categorical columns:
    - count, number of unique values, most common value, frequency of most common
    """
    cleaned = [v for v in vals if v.strip()]
    ctr = Counter(cleaned)
    count = sum(ctr.values())
    unique = len(ctr)
    top, freq = ctr.most_common(1)[0] if ctr else (None, 0)
    return {
        'count': count,
        'unique': unique,
        'top': top,
        'freq': freq
    }


def summarize_column(col_vals):
    """
    Decide if column is numeric or categorical and summarize.
    """
    non_blank = [v for v in col_vals if v.strip()]
    if non_blank and all(is_number(v) for v in non_blank):
        return stats_numeric(non_blank)
    return stats_categorical(non_blank)


def load_csv(path):
    """
    Load a CSV file and remove rows that are completely blank.
    Returns header and rows.
    """
    with open(path, encoding='utf-8', newline='') as fh:
        reader = csv.reader(fh)
        header = next(reader)
        rows = [row for row in reader if any(cell.strip() for cell in row)]
    return header, rows


def overall_summary(header, rows):
    """
    Calculate summary stats for all columns in the dataset.
    """
    cols = list(zip(*rows))
    return {name: summarize_column(vals) for name, vals in zip(header, cols)}


def grouped_summary(header, rows, keys):
    """
    Group rows by the given keys and calculate summary for each group.
    """
    idxs = [header.index(k) for k in keys]
    buckets = defaultdict(list)
    for row in rows:
        key = tuple(row[i] for i in idxs)
        buckets[key].append(row)
    return {key: overall_summary(header, grp) for key, grp in buckets.items()}


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


def analyze_dataset(name, path, meta):
    """
    Analyze a dataset using its metadata.
    Writes a report file with overall and grouped summaries.
    """
    header, rows = load_csv(path)
    report_file = f"{name.lower().replace(' ', '_')}_report.txt"
    sep = '=' * 60
    print(f"Generating report for {name} -> {report_file}")
    with open(report_file, 'w', encoding='utf-8') as out:
        # Overall summary
        out.write(sep + '\n')
        out.write(f"{name.upper()} - OVERALL SUMMARY\n")
        out.write(sep + '\n')
        overall = overall_summary(header, rows)
        for col, stats in overall.items():
            out.write(f"Column: {col}\n")
            for m, v in stats.items():
                out.write(f"  - {m}: {v}\n")
            out.write('\n')
        # Grouped summaries
        for keys in meta['group_by']:
            out.write(sep + '\n')
            out.write(f"SUMMARY BY {tuple(keys)}\n")
            out.write(sep + '\n')
            grp = grouped_summary(header, rows, keys)
            for key_vals, stats in grp.items():
                out.write(f"{dict(zip(keys, key_vals))}\n")
                for col, col_stats in stats.items():
                    out.write(f"  Column: {col}\n")
                    for m, v in col_stats.items():
                        out.write(f"    - {m}: {v}\n")
                out.write('\n')
    print(f"Done! Check {report_file} for {name} report.")


# Run analysis for each dataset when script is executed
if __name__ == '__main__':
    for ds in DATASETS:
        analyze_dataset(ds['name'], ds['path'], ds['metadata'])
