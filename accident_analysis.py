import pandas as pd

# Load dataset
df = pd.read_csv("data/accident_data.csv")

print("Original Dataset Shape:", df.shape)

# Select relevant columns for analysis
columns = [
    "Num_Acc",
    "week_day",
    "state",
    "severity",
    "weather",
    "location",
    "hrmn",
    "lum",
    "vehicle_type",
    "engine_size",
    "driver_sex",
    "driver_age",
    "car_age",
    "casualty_severity",
    "casualty_age"
]

df = df[columns].copy()

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Check duplicate records
print("\nDuplicate Records:", df.duplicated().sum())

# Check data types
print("\nData Types:")
print(df.dtypes)

# Remove duplicate records if any
df = df.drop_duplicates()

# Convert accident time (HHMM) into hour
df["hour"] = df["hrmn"] // 100

# Create time-of-day category
def get_time_period(hour):
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 21:
        return "Evening"
    else:
        return "Night"


df["time_period"] = df["hour"].apply(get_time_period)

# Save cleaned dataset
df.to_csv("data/accident_data_cleaned.csv", index=False)

# Final dataset information
print("\nCleaning completed successfully!")
print("Cleaned Dataset Shape:", df.shape)
print("Cleaned file saved to: data/accident_data_cleaned.csv")

# Basic analysis summary
print("\nBasic Dataset Summary:")
print("Total Accidents:", len(df))
print("Total States:", df["state"].nunique())
print("Average Driver Age:", round(df["driver_age"].mean(), 2))
print("Average Casualty Age:", round(df["casualty_age"].mean(), 2))
print("Average Car Age:", round(df["car_age"].mean(), 2))

print("\nSeverity Distribution:")
print(df["severity"].value_counts())

print("\nWeather Distribution:")
print(df["weather"].value_counts())

print("\nVehicle Type Distribution:")
print(df["vehicle_type"].value_counts())