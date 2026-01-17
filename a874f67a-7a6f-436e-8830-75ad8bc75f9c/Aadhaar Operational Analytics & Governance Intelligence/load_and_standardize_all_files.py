import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Define file groups
enrolment_files = [
    'api_data_aadhar_enrolment_0_500000.csv',
    'api_data_aadhar_enrolment_500000_1000000.csv',
    'api_data_aadhar_enrolment_1000000_1006029.csv'
]

demographic_files = [
    'api_data_aadhar_demographic_0_500000.csv',
    'api_data_aadhar_demographic_500000_1000000.csv',
    'api_data_aadhar_demographic_1000000_1500000.csv',
    'api_data_aadhar_demographic_1500000_2000000.csv',
    'api_data_aadhar_demographic_2000000_2071700.csv'
]

biometric_files = [
    'api_data_aadhar_biometric_0_500000.csv',
    'api_data_aadhar_biometric_500000_1000000.csv',
    'api_data_aadhar_biometric_1000000_1500000.csv',
    'api_data_aadhar_biometric_1500000_1861108.csv'
]

print("=" * 80)
print("LOADING ALL AADHAR DATA FILES")
print("=" * 80)

# Load and combine enrolment data
print("\n📊 Loading Enrolment Files...")
enrolment_dfs = []
for file in enrolment_files:
    df = pd.read_csv(file)
    enrolment_dfs.append(df)
    print(f"  ✓ {file}: {len(df):,} records, {df.shape[1]} columns")

enrolment_data = pd.concat(enrolment_dfs, ignore_index=True)
print(f"\n✓ Combined Enrolment Data: {len(enrolment_data):,} total records")

# Load and combine demographic data
print("\n📊 Loading Demographic Files...")
demographic_dfs = []
for file in demographic_files:
    df = pd.read_csv(file)
    demographic_dfs.append(df)
    print(f"  ✓ {file}: {len(df):,} records, {df.shape[1]} columns")

demographic_data = pd.concat(demographic_dfs, ignore_index=True)
print(f"\n✓ Combined Demographic Data: {len(demographic_data):,} total records")

# Load and combine biometric data
print("\n📊 Loading Biometric Files...")
biometric_dfs = []
for file in biometric_files:
    df = pd.read_csv(file)
    biometric_dfs.append(df)
    print(f"  ✓ {file}: {len(df):,} records, {df.shape[1]} columns")

biometric_data = pd.concat(biometric_dfs, ignore_index=True)
print(f"\n✓ Combined Biometric Data: {len(biometric_data):,} total records")

# Display schemas
print("\n" + "=" * 80)
print("SCHEMA OVERVIEW")
print("=" * 80)

print("\n🔹 Enrolment Data Schema:")
print(enrolment_data.dtypes)
print(f"\nShape: {enrolment_data.shape}")

print("\n🔹 Demographic Data Schema:")
print(demographic_data.dtypes)
print(f"\nShape: {demographic_data.shape}")

print("\n🔹 Biometric Data Schema:")
print(biometric_data.dtypes)
print(f"\nShape: {biometric_data.shape}")

# Preview data
print("\n" + "=" * 80)
print("DATA PREVIEW")
print("=" * 80)

print("\n🔹 Enrolment Data Sample:")
print(enrolment_data.head(3))

print("\n🔹 Demographic Data Sample:")
print(demographic_data.head(3))

print("\n🔹 Biometric Data Sample:")
print(biometric_data.head(3))

print("\n✅ All files loaded successfully!")
