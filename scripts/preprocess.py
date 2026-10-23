"""
Dataset Preprocessing and Baseline Aggregations
Project: Electricity Consumption Analytics and Energy-Saving Recommendation System
AICTE - IBM SkillsBuild Data Analytics with AI Internship 2026
Student: Shani Kumar
Dataset: Individual Household Electric Power Consumption (UCI ML Repository)
Original Source File: household_power_consumption (1).txt
"""

import os
import time
import pandas as pd
import numpy as np

def run_preprocessing():
    start_time = time.time()
    input_file = os.path.join("data", "household_power_consumption.txt")
    
    if not os.path.exists(input_file):
        # Fallback to temp path if not in data folder
        temp_path = r"C:\Users\Shani\AppData\Local\Temp\household_power_consumption (1).txt"
        if os.path.exists(temp_path):
            input_file = temp_path
        else:
            raise FileNotFoundError(f"Dataset not found at {input_file} or {temp_path}")

    print(f"Loading raw dataset from {input_file}...")
    df = pd.read_csv(
        input_file,
        sep=';',
        na_values=['?'],
        dtype={
            'Global_active_power': float,
            'Global_reactive_power': float,
            'Voltage': float,
            'Global_intensity': float,
            'Sub_metering_1': float,
            'Sub_metering_2': float,
            'Sub_metering_3': float
        },
        low_memory=False
    )
    
    total_raw_records = len(df)
    missing_records = df['Global_active_power'].isnull().sum()
    print(f"Successfully loaded {total_raw_records:,} minute-by-minute records.")
    print(f"Detected {missing_records:,} missing records ({missing_records/total_raw_records*100:.2f}%).")

    print("Parsing timestamps and constructing datetime index...")
    # Dataset format is DD/MM/YYYY HH:MM:SS
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
    df.set_index('Datetime', inplace=True)
    df.drop(columns=['Date', 'Time'], inplace=True)

    print("Handling missing values using time-weighted interpolation for continuous physical readings...")
    df_clean = df.interpolate(method='time', limit=60)
    df_clean = df_clean.bfill().ffill()

    print("Computing energy consumption components...")
    # Active power is recorded in kW. For a 1-minute sampling interval:
    # Energy in Wh = kW * 1000 W/kW * (1/60) h = kW * (50/3) Wh
    df_clean['Global_active_energy_Wh'] = df_clean['Global_active_power'] * 1000.0 / 60.0

    # Sub_metering_1: Kitchen (Wh)
    # Sub_metering_2: Laundry room (Wh)
    # Sub_metering_3: Electric water-heater & AC (Wh)
    # Remainder energy (lighting, sockets, personal electronics):
    sub_sum = df_clean['Sub_metering_1'] + df_clean['Sub_metering_2'] + df_clean['Sub_metering_3']
    df_clean['Sub_metering_remainder_Wh'] = np.maximum(0.0, df_clean['Global_active_energy_Wh'] - sub_sum)

    print("Generating Daily Aggregations (kWh and statistical summaries)...")
    daily = df_clean.resample('D').agg({
        'Global_active_power': ['mean', 'max', 'min', 'std'],
        'Global_reactive_power': ['mean', 'sum'],
        'Voltage': 'mean',
        'Global_intensity': 'mean',
        'Global_active_energy_Wh': 'sum',
        'Sub_metering_1': 'sum',
        'Sub_metering_2': 'sum',
        'Sub_metering_3': 'sum',
        'Sub_metering_remainder_Wh': 'sum'
    })

    # Flatten multi-level columns
    daily.columns = ['_'.join(c).strip('_') for c in daily.columns]

    # Convert energy sums from Wh to kWh
    daily['Active_Energy_kWh'] = daily['Global_active_energy_Wh_sum'] / 1000.0
    daily['Sub_metering_1_kWh'] = daily['Sub_metering_1_sum'] / 1000.0
    daily['Sub_metering_2_kWh'] = daily['Sub_metering_2_sum'] / 1000.0
    daily['Sub_metering_3_kWh'] = daily['Sub_metering_3_sum'] / 1000.0
    daily['Sub_metering_remainder_kWh'] = daily['Sub_metering_remainder_Wh_sum'] / 1000.0

    daily.reset_index(inplace=True)
    daily.rename(columns={'Datetime': 'Date'}, inplace=True)
    daily['Date_str'] = daily['Date'].dt.strftime('%Y-%m-%d')
    daily['Year'] = daily['Date'].dt.year
    daily['Month'] = daily['Date'].dt.month
    daily['Month_Name'] = daily['Date'].dt.strftime('%b')
    daily['DayOfWeek'] = daily['Date'].dt.day_name()
    daily['IsWeekend'] = daily['Date'].dt.dayofweek.isin([5, 6]).astype(int)

    daily_csv_path = os.path.join("data", "household_power_daily.csv")
    daily.to_csv(daily_csv_path, index=False)
    print(f"Saved daily aggregates: {daily_csv_path} ({len(daily)} calendar days)")

    print("Generating Diurnal / Hourly Profile (0-23 hours)...")
    df_clean['Hour'] = df_clean.index.hour
    hourly_profile = df_clean.groupby('Hour').agg({
        'Global_active_power': 'mean',
        'Global_reactive_power': 'mean',
        'Voltage': 'mean',
        'Global_intensity': 'mean',
        'Sub_metering_1': 'mean',
        'Sub_metering_2': 'mean',
        'Sub_metering_3': 'mean',
        'Sub_metering_remainder_Wh': 'mean'
    }).reset_index()

    # Convert average minute Wh in that hour to total average Wh in that hour (* 60)
    hourly_profile['Sub_1_Hourly_Wh'] = hourly_profile['Sub_metering_1'] * 60.0
    hourly_profile['Sub_2_Hourly_Wh'] = hourly_profile['Sub_metering_2'] * 60.0
    hourly_profile['Sub_3_Hourly_Wh'] = hourly_profile['Sub_metering_3'] * 60.0
    hourly_profile['Sub_Remainder_Hourly_Wh'] = hourly_profile['Sub_metering_remainder_Wh'] * 60.0
    hourly_profile['Total_Hourly_Wh'] = (
        hourly_profile['Sub_1_Hourly_Wh'] + 
        hourly_profile['Sub_2_Hourly_Wh'] + 
        hourly_profile['Sub_3_Hourly_Wh'] + 
        hourly_profile['Sub_Remainder_Hourly_Wh']
    )

    hourly_csv_path = os.path.join("data", "hourly_profile.csv")
    hourly_profile.to_csv(hourly_csv_path, index=False)
    print(f"Saved hourly profile: {hourly_csv_path}")

    # Generate Monthly Summary
    monthly = daily.groupby(['Year', 'Month', 'Month_Name']).agg({
        'Active_Energy_kWh': ['sum', 'mean', 'count'],
        'Sub_metering_1_kWh': 'sum',
        'Sub_metering_2_kWh': 'sum',
        'Sub_metering_3_kWh': 'sum',
        'Sub_metering_remainder_kWh': 'sum'
    }).reset_index()
    monthly.columns = ['_'.join(c).strip('_') for c in monthly.columns]
    monthly_csv_path = os.path.join("data", "monthly_summary.csv")
    monthly.to_csv(monthly_csv_path, index=False)
    print(f"Saved monthly summary: {monthly_csv_path}")

    total_kwh = daily['Active_Energy_kWh'].sum()
    mean_kwh = daily['Active_Energy_kWh'].mean()
    max_kwh = daily['Active_Energy_kWh'].max()
    max_date = daily.loc[daily['Active_Energy_kWh'].idxmax(), 'Date_str']
    min_kwh = daily['Active_Energy_kWh'].min()
    min_date = daily.loc[daily['Active_Energy_kWh'].idxmin(), 'Date_str']

    s1_tot = daily['Sub_metering_1_kWh'].sum()
    s2_tot = daily['Sub_metering_2_kWh'].sum()
    s3_tot = daily['Sub_metering_3_kWh'].sum()
    rem_tot = daily['Sub_metering_remainder_kWh'].sum()

    print("\n--- DATASET GROUND-TRUTH ANALYTICS ---")
    print(f"Observation Window: {daily['Date_str'].min()} to {daily['Date_str'].max()}")
    print(f"Total Days Monitored: {len(daily)}")
    print(f"Total Cumulative Electricity: {total_kwh:,.2f} kWh")
    print(f"Mean Daily Consumption: {mean_kwh:.2f} kWh/day")
    print(f"Median Daily Consumption: {daily['Active_Energy_kWh'].median():.2f} kWh/day")
    print(f"Standard Deviation: {daily['Active_Energy_kWh'].std():.2f} kWh/day")
    print(f"Highest Single Day: {max_kwh:.2f} kWh on {max_date}")
    print(f"Lowest Single Day: {min_kwh:.2f} kWh on {min_date}")
    print(f"Sub-metering 1 (Kitchen): {s1_tot:,.2f} kWh ({s1_tot/total_kwh*100:.1f}%)")
    print(f"Sub-metering 2 (Laundry): {s2_tot:,.2f} kWh ({s2_tot/total_kwh*100:.1f}%)")
    print(f"Sub-metering 3 (HVAC/Water Heater): {s3_tot:,.2f} kWh ({s3_tot/total_kwh*100:.1f}%)")
    print(f"Remainder (Lighting & Appliances): {rem_tot:,.2f} kWh ({rem_tot/total_kwh*100:.1f}%)")
    print(f"Total execution elapsed time: {time.time()-start_time:.2f} seconds")

if __name__ == "__main__":
    run_preprocessing()
