"""
  Research Task 4: Polars Python Analytics with Metadata
  The objective for Research task 4 was to replace the Task 3 
  script with one that supports any CSV + metadata.

Polars-based descriptive statistics for three datasets:
- Google Play Store
- Telco Customer Churn
- Video Games Sales

This script loads, cleans, and analyzes each dataset using Polars.
It prints descriptive statistics, value counts, unique counts, and group-wise summaries.
Cleaning steps are performed before analysis for reproducible and accurate results.


Change the paths in the DATASETS list to point to your local CSV files.
"""

import polars as pl

# --- Cleaning functions for each dataset ---

def clean_playstore(df):
    # Clean 'Installs': remove commas and plus, convert to int
    if "Installs" in df.columns:
        df = df.with_columns(
            pl.col("Installs")
            .str.replace_all(",", "")
            .str.replace_all(r"\+", "")
            .cast(pl.Int64, strict=False)
            .alias("Installs")
        )
    # Clean 'Reviews': handle 'M' for millions, convert to int
    if "Reviews" in df.columns:
        df = df.with_columns(
            pl.col("Reviews")
            .str.replace("M", "000000")
            .cast(pl.Int64, strict=False)
            .alias("Reviews")
        )
    # Clean 'Price': remove $ and convert to float
    if "Price" in df.columns:
        df = df.with_columns(
            pl.col("Price")
            .str.replace_all("[$]", "")
            .cast(pl.Float64, strict=False)
            .alias("Price")
        )
    # Strip whitespace from all string columns
    str_cols = [col for col, dtype in zip(df.columns, df.dtypes) if dtype == pl.Utf8]
    if str_cols:
        df = df.with_columns([
            pl.col(c).str.strip_chars().alias(c) for c in str_cols
        ])
    return df

def clean_telco(df):
    # Convert 'SeniorCitizen' to int
    if "SeniorCitizen" in df.columns:
        df = df.with_columns(
            pl.col("SeniorCitizen").cast(pl.Int64, strict=False)
        )
    # Convert 'tenure', 'MonthlyCharges', 'TotalCharges' to float
    for col in ["tenure", "MonthlyCharges", "TotalCharges"]:
        if col in df.columns:
            df = df.with_columns(
                pl.col(col).cast(pl.Float64, strict=False)
            )
    # Strip whitespace from all string columns
    str_cols = [col for col, dtype in zip(df.columns, df.dtypes) if dtype == pl.Utf8]
    if str_cols:
        df = df.with_columns([
            pl.col(c).str.strip_chars().alias(c) for c in str_cols
        ])
    return df

def clean_vgsales(df):
    # Convert numeric columns to float
    num_cols = [
        "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales",
        "Critic_Score", "Critic_Count", "User_Score", "User_Count"
    ]
    for col in num_cols:
        if col in df.columns:
            df = df.with_columns(
                pl.col(col).cast(pl.Float64, strict=False)
            )
    # Convert 'Year_of_Release' to int
    if "Year_of_Release" in df.columns:
        df = df.with_columns(
            pl.col("Year_of_Release").cast(pl.Int64, strict=False)
        )
    # Strip whitespace from all string columns
    str_cols = [col for col, dtype in zip(df.columns, df.dtypes) if dtype == pl.Utf8]
    if str_cols:
        df = df.with_columns([
            pl.col(c).str.strip_chars().alias(c) for c in str_cols
        ])
    return df

# --- Analysis functions for each dataset ---

def analyze_playstore():
    print("\n=== Google Play Store Dataset ===")
    # Load and clean dataset
    df = pl.read_csv(
        "Dataset/googleplaystore.csv",
        infer_schema_length=1000,
        schema_overrides={"Price": pl.Utf8, "Reviews": pl.Utf8, "Installs": pl.Utf8}
    )
    df = clean_playstore(df)
    print("First 5 rows after cleaning:")
    print(df.head())

    # Descriptive statistics for numeric columns
    print("\nDescriptive statistics (numeric columns):")
    print(df.select([
        pl.col("Rating").cast(pl.Float64),
        pl.col("Reviews"),
        pl.col("Price"),
        pl.col("Installs")
    ]).describe())

    # Top categories by app count
    print("\nTop Categories by count:")
    print(df.group_by("Category").count().sort("count", descending=True).select(["Category", "count"]).head(10))

    # Unique content ratings
    print("\nUnique Content Ratings:", df["Content Rating"].n_unique())

    # Average rating by category
    print("\nAverage Rating by Category:")
    print(
        df.group_by("Category")
        .agg(pl.col("Rating").cast(pl.Float64).mean().alias("Avg_Rating"))
        .sort("Avg_Rating", descending=True)
        .head(10)
    )

    # Top 10 most installed apps
    print("\nTop 10 most installed apps:")
    print(df.sort("Installs", descending=True).select(["App", "Installs"]).head(10))

def analyze_telco():
    print("\n=== Telco Customer Churn Dataset ===")
    # Load and clean dataset
    df = pl.read_csv(
        "Dataset/Telco_Customer_Churn.csv",
        infer_schema_length=1000
    )
    df = clean_telco(df)
    print("First 5 rows after cleaning:")
    print(df.head())

    # Descriptive statistics for numeric columns
    print("\nDescriptive statistics (numeric columns):")
    print(df.select([
        pl.col("tenure"),
        pl.col("MonthlyCharges"),
        pl.col("TotalCharges")
    ]).describe())

    # Top contracts by customer count
    print("\nTop Contracts by count:")
    print(df.group_by("Contract").count().sort("count", descending=True).select(["Contract", "count"]).head(10))

    # Unique payment methods
    print("\nUnique Payment Methods:", df["PaymentMethod"].n_unique())

    # Average monthly charges by contract type
    print("\nAverage Monthly Charges by Contract:")
    print(
        df.group_by("Contract")
        .agg(pl.col("MonthlyCharges").mean().alias("Avg_MonthlyCharges"))
        .sort("Avg_MonthlyCharges", descending=True)
        .head(10)
    )

    # Top 10 customers by total charges
    print("\nTop 10 customers by TotalCharges:")
    print(df.sort("TotalCharges", descending=True).select(["customerID", "TotalCharges"]).head(10))

def analyze_vgsales():
    print("\n=== Video Games Sales Dataset ===")
    # Load and clean dataset
    df = pl.read_csv(
        "Dataset/Video_Games_Sales_as_at_22_Dec_2016.csv",
        infer_schema_length=1000
    )
    df = clean_vgsales(df)
    print("First 5 rows after cleaning:")
    print(df.head())

    # Descriptive statistics for numeric columns
    print("\nDescriptive statistics (numeric columns):")
    print(df.select([
        pl.col("NA_Sales"),
        pl.col("EU_Sales"),
        pl.col("JP_Sales"),
        pl.col("Other_Sales"),
        pl.col("Global_Sales"),
        pl.col("Critic_Score"),
        pl.col("User_Score")
    ]).describe())

    # Top genres by game count
    print("\nTop Genres by count:")
    print(df.group_by("Genre").count().sort("count", descending=True).select(["Genre", "count"]).head(10))

    # Unique platforms
    print("\nUnique Platforms:", df["Platform"].n_unique())

    # Average global sales by genre
    print("\nAverage Global Sales by Genre:")
    print(
        df.group_by("Genre")
        .agg(pl.col("Global_Sales").mean().alias("Avg_Global_Sales"))
        .sort("Avg_Global_Sales", descending=True)
        .head(10)
    )

    # Top 10 games by global sales
    print("\nTop 10 games by Global Sales:")
    print(df.sort("Global_Sales", descending=True).select(["Name", "Global_Sales"]).head(10))

# --- Main execution: run all analyses ---
if __name__ == "__main__":
    analyze_playstore()
    analyze_telco()
    analyze_vgsales()