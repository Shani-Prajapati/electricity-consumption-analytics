"""
Generate Analysis Visualizations and Actual Figures for the Project Report and README
Project: Electricity Consumption Analytics and Energy-Saving Recommendation System
AICTE - IBM SkillsBuild Data Analytics with AI Internship 2026
Student: Shani Kumar
"""

import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import numpy as np

# Set clean aesthetic styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

os.makedirs("screenshots", exist_ok=True)

# Load aggregated data
daily_path = os.path.join("data", "household_power_daily.csv")
hourly_path = os.path.join("data", "hourly_profile.csv")
monthly_path = os.path.join("data", "monthly_summary.csv")

daily = pd.read_csv(daily_path)
daily['Date'] = pd.to_datetime(daily['Date'])
hourly = pd.read_csv(hourly_path)
monthly = pd.read_csv(monthly_path)

# -------------------------------------------------------------
# Chart 1: 4-Year Daily Consumption Timeline with Rolling Trend
# -------------------------------------------------------------
print("Generating Chart 1: Daily Consumption Timeline...")
fig, ax = plt.subplots(figsize=(12, 5), dpi=300)
daily_sorted = daily.sort_values('Date').copy()
daily_sorted['Rolling_30D'] = daily_sorted['Active_Energy_kWh'].rolling(window=30, center=True).mean()

ax.plot(daily_sorted['Date'], daily_sorted['Active_Energy_kWh'], color='#90CAF9', alpha=0.55, linewidth=0.8, label='Daily Consumption (kWh)')
ax.plot(daily_sorted['Date'], daily_sorted['Rolling_30D'], color='#1565C0', linewidth=2.2, label='30-Day Moving Average')

# Highlight peak day
max_row = daily_sorted.loc[daily_sorted['Active_Energy_kWh'].idxmax()]
ax.scatter([max_row['Date']], [max_row['Active_Energy_kWh']], color='#D32F2F', s=70, zorder=5, label=f"Max: {max_row['Active_Energy_kWh']:.1f} kWh ({max_row['Date_str']})")
ax.annotate(f"Winter Peak: {max_row['Active_Energy_kWh']:.1f} kWh\n({max_row['Date_str']})", 
            xy=(max_row['Date'], max_row['Active_Energy_kWh']),
            xytext=(max_row['Date'] + pd.Timedelta(days=50), max_row['Active_Energy_kWh'] - 6),
            arrowprops=dict(facecolor='#D32F2F', arrowstyle='->', lw=1.2),
            fontsize=9, fontweight='bold', color='#B71C1C',
            bbox=dict(boxstyle="round,pad=0.3", fc="#FFEBEE", ec="#D32F2F", lw=0.8))

ax.set_title("Household Daily Electricity Consumption (Dec 2006 – Nov 2010)", fontsize=13, fontweight='bold', pad=12, color='#1A237E')
ax.set_xlabel("Date (Observation Timeline)", fontsize=10, fontweight='bold', labelpad=8)
ax.set_ylabel("Active Energy Consumed (kWh/day)", fontsize=10, fontweight='bold', labelpad=8)
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.set_ylim(0, 90)
ax.legend(frameon=True, facecolor='white', framealpha=0.9, loc='upper right')
plt.tight_layout()
fig.savefig(os.path.join("screenshots", "01_daily_consumption_trend.png"), dpi=300)
plt.close(fig)

# -------------------------------------------------------------
# Chart 2: Sub-metering Breakdown (Kitchen, Laundry, HVAC, Remainder)
# -------------------------------------------------------------
print("Generating Chart 2: Energy Breakdown Donut Chart...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)

labels = ['Kitchen (Sub 1)', 'Laundry (Sub 2)', 'HVAC / Water Heater (Sub 3)', 'Remainder (Plug Loads/Lighting)']
shares = [
    daily['Sub_metering_1_kWh'].sum(),
    daily['Sub_metering_2_kWh'].sum(),
    daily['Sub_metering_3_kWh'].sum(),
    daily['Sub_metering_remainder_kWh'].sum()
]
colors = ['#FF7043', '#26A69A', '#42A5F5', '#AB47BC']

wedges, texts, autotexts = ax1.pie(
    shares, 
    labels=labels, 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=colors,
    pctdistance=0.75,
    textprops={'fontsize': 9},
    wedgeprops={'width': 0.45, 'edgecolor': 'white', 'linewidth': 2}
)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(9.5)
ax1.set_title("Cumulative End-Use Breakdown (% of 37,846.5 kWh)", fontsize=11, fontweight='bold', pad=10, color='#1A237E')

# Sub-metering monthly stacked bar
monthly_sub = daily.groupby('Month').agg({
    'Sub_metering_1_kWh': 'mean',
    'Sub_metering_2_kWh': 'mean',
    'Sub_metering_3_kWh': 'mean',
    'Sub_metering_remainder_kWh': 'mean'
}).reset_index()

month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
x = np.arange(12)
width = 0.65

p1 = ax2.bar(x, monthly_sub['Sub_metering_1_kWh'], width, label='Kitchen', color='#FF7043')
p2 = ax2.bar(x, monthly_sub['Sub_metering_2_kWh'], width, bottom=monthly_sub['Sub_metering_1_kWh'], label='Laundry', color='#26A69A')
p3 = ax2.bar(x, monthly_sub['Sub_metering_3_kWh'], width, bottom=monthly_sub['Sub_metering_1_kWh'] + monthly_sub['Sub_metering_2_kWh'], label='HVAC/Water Heater', color='#42A5F5')
p4 = ax2.bar(x, monthly_sub['Sub_metering_remainder_kWh'], width, bottom=monthly_sub['Sub_metering_1_kWh'] + monthly_sub['Sub_metering_2_kWh'] + monthly_sub['Sub_metering_3_kWh'], label='Remainder', color='#AB47BC')

ax2.set_title("Average Daily Consumption by Month (kWh/day)", fontsize=11, fontweight='bold', pad=10, color='#1A237E')
ax2.set_xticks(x)
ax2.set_xticklabels(month_names, fontsize=9)
ax2.set_ylabel("Average kWh / Day", fontsize=10, fontweight='bold')
ax2.legend(loc='upper right', fontsize=8.5, frameon=True)

plt.tight_layout()
fig.savefig(os.path.join("screenshots", "02_submetering_breakdown.png"), dpi=300)
plt.close(fig)

# -------------------------------------------------------------
# Chart 3: 24-Hour Diurnal Profile (Peak vs Off-Peak Hours)
# -------------------------------------------------------------
print("Generating Chart 3: 24-Hour Diurnal Demand Profile...")
fig, ax = plt.subplots(figsize=(11, 5), dpi=300)

hours = hourly['Hour']
ax.plot(hours, hourly['Total_Hourly_Wh'], color='#E65100', marker='o', linewidth=2.5, markersize=5, label='Total Hourly Consumption (Wh)')
ax.plot(hours, hourly['Sub_3_Hourly_Wh'], color='#1E88E5', linestyle='--', linewidth=1.8, label='Sub 3: Water Heater & HVAC (Wh)')
ax.plot(hours, hourly['Sub_Remainder_Hourly_Wh'], color='#8E24AA', linestyle=':', linewidth=1.8, label='Remainder: Lighting & Standby (Wh)')
ax.plot(hours, hourly['Sub_1_Hourly_Wh'], color='#D84315', linestyle='-.', linewidth=1.5, label='Sub 1: Kitchen (Wh)')
ax.plot(hours, hourly['Sub_2_Hourly_Wh'], color='#00897B', linestyle='-.', linewidth=1.5, label='Sub 2: Laundry (Wh)')

# Highlight Peak Period (19:00 - 22:00)
ax.axvspan(19, 22, color='#FFCDD2', alpha=0.35, label='Peak Load Window (19:00 - 22:00)')
# Highlight Baseload Period (02:00 - 05:00)
ax.axvspan(2, 5, color='#E1F5FE', alpha=0.35, label='Off-Peak Baseload (02:00 - 05:00)')

ax.set_title("Household 24-Hour Diurnal Load Profile (Average Watt-Hours per Hour)", fontsize=12, fontweight='bold', pad=12, color='#1A237E')
ax.set_xlabel("Hour of the Day (0:00 to 23:00)", fontsize=10, fontweight='bold', labelpad=8)
ax.set_ylabel("Average Energy (Watt-hours / hour)", fontsize=10, fontweight='bold', labelpad=8)
ax.set_xticks(range(0, 24))
ax.set_xlim(-0.5, 23.5)
ax.legend(frameon=True, facecolor='white', loc='upper left', fontsize=8.5)
plt.tight_layout()
fig.savefig(os.path.join("screenshots", "03_diurnal_hourly_pattern.png"), dpi=300)
plt.close(fig)

# -------------------------------------------------------------
# Chart 4: Anomaly Detection (IQR and Statistical Outliers)
# -------------------------------------------------------------
print("Generating Chart 4: Anomaly Detection Distribution...")
q1 = daily['Active_Energy_kWh'].quantile(0.25)
q3 = daily['Active_Energy_kWh'].quantile(0.75)
iqr = q3 - q1
upper_bound = q3 + 1.5 * iqr
lower_bound = max(0, q1 - 1.5 * iqr)

anomalies = daily[daily['Active_Energy_kWh'] > upper_bound].copy()
pct_anom = (len(anomalies) / len(daily)) * 100

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8), dpi=300)

# Boxplot
sns.boxplot(y=daily['Active_Energy_kWh'], ax=ax1, color='#90CAF9', flierprops={'marker': 'o', 'markersize': 5, 'markerfacecolor': '#D32F2F', 'markeredgecolor': '#D32F2F'})
ax1.axhline(upper_bound, color='#D32F2F', linestyle='--', linewidth=1.5, label=f'Upper Threshold ({upper_bound:.1f} kWh)')
ax1.set_title("Distribution & Outliers (Box Plot)", fontsize=11, fontweight='bold', color='#1A237E')
ax1.set_ylabel("Daily Active Energy (kWh)", fontsize=10, fontweight='bold')
ax1.legend(loc='upper right', fontsize=8.5)

# Histogram / KDE
sns.histplot(daily['Active_Energy_kWh'], kde=True, ax=ax2, color='#1565C0', bins=35)
ax2.axvline(upper_bound, color='#D32F2F', linestyle='--', linewidth=1.5, label=f'Threshold: {upper_bound:.1f} kWh')
ax2.set_title(f"Histogram (IQR Outliers: {len(anomalies)} days / {pct_anom:.1f}%)", fontsize=11, fontweight='bold', color='#1A237E')
ax2.set_xlabel("Daily Active Energy (kWh)", fontsize=10, fontweight='bold')
ax2.set_ylabel("Frequency (Days)", fontsize=10, fontweight='bold')
ax2.legend(loc='upper right', fontsize=8.5)

plt.tight_layout()
fig.savefig(os.path.join("screenshots", "04_anomaly_detection_iqr.png"), dpi=300)
plt.close(fig)

# -------------------------------------------------------------
# Chart 5: Short-Term Forecasting (Baseline vs Ridge Regression)
# -------------------------------------------------------------
print("Generating Chart 5: Chronological Forecast Evaluation...")
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

# Feature engineering for daily time-series
ts_df = daily[['Date', 'Active_Energy_kWh', 'DayOfWeek', 'Month', 'IsWeekend']].copy()
ts_df['Lag_1'] = ts_df['Active_Energy_kWh'].shift(1)
ts_df['Lag_2'] = ts_df['Active_Energy_kWh'].shift(2)
ts_df['Lag_7'] = ts_df['Active_Energy_kWh'].shift(7)
ts_df['Rolling_Mean_7'] = ts_df['Active_Energy_kWh'].shift(1).rolling(7).mean()
ts_df.dropna(inplace=True)

# Train on earlier data, test on last 90 days (chronological split)
test_size = 90
train = ts_df.iloc[:-test_size]
test = ts_df.iloc[-test_size:].copy()

features = ['Lag_1', 'Lag_2', 'Lag_7', 'Rolling_Mean_7', 'Month', 'IsWeekend']
X_train, y_train = train[features], train['Active_Energy_kWh']
X_test, y_test = test[features], test['Active_Energy_kWh']

model = Ridge(alpha=1.0)
model.fit(X_train, y_train)
test['Pred_Ridge'] = model.predict(X_test)
test['Pred_Baseline_Lag7'] = test['Lag_7'] # Naive weekly persistence

mae_ridge = mean_absolute_error(y_test, test['Pred_Ridge'])
rmse_ridge = root_mean_squared_error(y_test, test['Pred_Ridge'])
mae_base = mean_absolute_error(y_test, test['Pred_Baseline_Lag7'])

fig, ax = plt.subplots(figsize=(12, 5), dpi=300)
ax.plot(test['Date'], test['Active_Energy_kWh'], label='Actual Consumption', color='#212121', linewidth=2.0)
ax.plot(test['Date'], test['Pred_Ridge'], label=f'Ridge ML Forecast (MAE: {mae_ridge:.2f} kWh)', color='#1976D2', linestyle='--', linewidth=1.8)
ax.plot(test['Date'], test['Pred_Baseline_Lag7'], label=f'7-Day Baseline (MAE: {mae_base:.2f} kWh)', color='#9E9E9E', linestyle=':', linewidth=1.4)

ax.set_title("90-Day Out-of-Sample Electricity Forecasting (Chronological Holdout)", fontsize=12, fontweight='bold', pad=12, color='#1A237E')
ax.set_xlabel("Date (Test Window: Sep 2010 – Nov 2010)", fontsize=10, fontweight='bold', labelpad=8)
ax.set_ylabel("Daily Active Energy (kWh)", fontsize=10, fontweight='bold', labelpad=8)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax.legend(frameon=True, facecolor='white', loc='upper right')
plt.tight_layout()
fig.savefig(os.path.join("screenshots", "05_forecasting_evaluation.png"), dpi=300)
plt.close(fig)

print("All analysis charts successfully generated in screenshots/ folder!")
