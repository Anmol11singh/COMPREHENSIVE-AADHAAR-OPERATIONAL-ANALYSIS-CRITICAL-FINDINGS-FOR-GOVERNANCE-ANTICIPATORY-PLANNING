import pandas as pd
import numpy as np

print("=" * 80)
print("PARSING DATES AND DERIVING TEMPORAL FEATURES")
print("=" * 80)

# Function to parse dates and add temporal features
def add_temporal_features(df, dataset_name):
    print(f"\n📅 Processing {dataset_name}...")
    
    # Parse date column
    df['Date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Check for parsing errors
    null_dates = df['Date'].isna().sum()
    if null_dates > 0:
        print(f"  ⚠️ Warning: {null_dates:,} records with unparseable dates")
    
    # Derive temporal features
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Quarter'] = df['Date'].dt.quarter
    df['Month_Year'] = df['Date'].dt.to_period('M').astype(str)
    
    # Date range
    date_range = f"{df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}"
    print(f"  ✓ Date range: {date_range}")
    print(f"  ✓ Temporal features derived: Year, Month, Quarter, Month_Year")
    
    return df

# Process all three datasets
enrolment_processed = add_temporal_features(enrolment_data.copy(), "Enrolment Data")
demographic_processed = add_temporal_features(demographic_data.copy(), "Demographic Data")
biometric_processed = add_temporal_features(biometric_data.copy(), "Biometric Data")

# Display temporal feature statistics
print("\n" + "=" * 80)
print("TEMPORAL FEATURE SUMMARY")
print("=" * 80)

print("\n🔹 Enrolment Data Temporal Breakdown:")
print(f"  Years: {sorted(enrolment_processed['Year'].dropna().unique())}")
print(f"  Unique Month-Year combinations: {enrolment_processed['Month_Year'].nunique()}")
print(f"  Records per Quarter:\n{enrolment_processed['Quarter'].value_counts().sort_index()}")

print("\n🔹 Demographic Data Temporal Breakdown:")
print(f"  Years: {sorted(demographic_processed['Year'].dropna().unique())}")
print(f"  Unique Month-Year combinations: {demographic_processed['Month_Year'].nunique()}")
print(f"  Records per Quarter:\n{demographic_processed['Quarter'].value_counts().sort_index()}")

print("\n🔹 Biometric Data Temporal Breakdown:")
print(f"  Years: {sorted(biometric_processed['Year'].dropna().unique())}")
print(f"  Unique Month-Year combinations: {biometric_processed['Month_Year'].nunique()}")
print(f"  Records per Quarter:\n{biometric_processed['Quarter'].value_counts().sort_index()}")

# Show updated schemas
print("\n" + "=" * 80)
print("UPDATED SCHEMAS WITH TEMPORAL FEATURES")
print("=" * 80)

print("\n🔹 Enrolment Data:")
print(enrolment_processed.dtypes)
print(f"Shape: {enrolment_processed.shape}")

print("\n🔹 Demographic Data:")
print(demographic_processed.dtypes)
print(f"Shape: {demographic_processed.shape}")

print("\n🔹 Biometric Data:")
print(biometric_processed.dtypes)
print(f"Shape: {biometric_processed.shape}")

# Sample data preview
print("\n" + "=" * 80)
print("SAMPLE DATA WITH TEMPORAL FEATURES")
print("=" * 80)

print("\n🔹 Enrolment Sample:")
print(enrolment_processed[['date', 'Date', 'Year', 'Month', 'Quarter', 'Month_Year', 'state', 'district']].head(3))

print("\n✅ Date parsing and temporal feature derivation complete!")
