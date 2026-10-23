# Electricity Consumption Analytics and Energy-Saving Recommendation System

### AICTE | IBM SkillsBuild Data Analytics with AI Internship 2026 | BharatCares
**Student Name:** Shani Kumar  
**Specialization:** B.Tech Computer Science and Engineering (AI & ML and Data Analytics)  
**Certificate Verification Project Submission**  
**Recommended GitHub Repository Name:** `electricity-consumption-analytics`

---

## 1. Project Overview

This project is an end-to-end data analytics and decision-support system designed to analyze residential electrical telemetry, visualize intraday and seasonal consumption patterns, detect statistical outliers, and deliver practical, data-backed energy-saving recommendations.

Rather than relying on synthetic data or high-level monthly utility bills, this platform analyzes **2,075,259 minute-by-minute electrical measurements** collected across **1,442 calendar days** (December 2006 to November 2010). The system provides an interactive Streamlit dashboard featuring multi-granularity time filters, sub-metering circuit disaggregation, configurable utility tariffs, and an interactive "What-If" energy savings simulator.

---

## 2. Problem Statement & Objectives

### Problem Statement
Most residential electricity consumers receive only aggregate monthly utility bills. This retrospective view conceals:
1. **Intraday demand peaks:** When cooking, heating, and laundry simultaneously overload the household supply.
2. **Vampire baseload power:** Continuous power draw during sleeping hours (02:00–05:00) from consumer electronics left on standby.
3. **Sub-circuit ambiguity:** Inability to pinpoint whether high bills originate from kitchen appliances, laundry, or climate control (HVAC).
4. **Lack of actionable advice:** Generic conservation tips fail to quantify financial savings or specify when to shift appliance operation.

### Objectives
- **Data Ingestion & Cleaning:** Ingest 2.07 million rows, handle missing observations (1.25%) using time-weighted interpolation, and parse datetime structures.
- **Physical Engineering Conversion:** Convert minute-level active power (kW) to cumulative energy (kWh) and isolate the unmetered active remainder circuit.
- **Exploratory Data Analysis (EDA):** Quantify longitudinal trends, seasonal variations (winter heating vs. summer baseload), and 24-hour diurnal load profiles.
- **Anomaly Detection:** Implement statistical Interquartile Range (IQR) and Scikit-Learn Isolation Forest methods to flag unusual consumption days with clear cautionary guidance.
- **Predictive Evaluation:** Benchmark an out-of-sample Ridge regression forecaster against naive persistence baselines.
- **Decision Support & Actionable Recommendations:** Deliver empirical recommendations and an interactive savings calculator.

---

## 3. Dataset Source and Specification

- **Dataset Name:** Individual Household Electric Power Consumption
- **Origin / Host:** UCI Machine Learning Repository & Électricité de France (EDF) R&D
- **Original Source URL:** [https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption)
- **Monitored Household:** Sceaux (near Paris, France)
- **Monitoring Timeline:** December 16, 2006 (17:24) to November 26, 2010 (21:02)
- **Original File Provided:** `household_power_consumption (1).txt` (~126.8 MB)

### Attribute Information

| Attribute Name | Unit / Type | Description |
| :--- | :--- | :--- |
| **Date** | String (`DD/MM/YYYY`) | Date of observation |
| **Time** | String (`HH:MM:SS`) | Time of observation (1-minute intervals) |
| **Global_active_power** | Float (`kW`) | Household global minute-averaged active power |
| **Global_reactive_power**| Float (`kW`) | Household global minute-averaged reactive power |
| **Voltage** | Float (`V`) | Minute-averaged supply voltage |
| **Global_intensity** | Float (`A`) | Minute-averaged current intensity |
| **Sub_metering_1** | Float (`Wh`) | Kitchen circuit (dishwasher, microwave, electric oven) |
| **Sub_metering_2** | Float (`Wh`) | Laundry room circuit (washing machine, dryer, fridge, light) |
| **Sub_metering_3** | Float (`Wh`) | Climate control & heating circuit (electric water heater, AC) |

---

## 4. Key Performance Indicators (Empirical Ground Truth)

The following metrics are directly computed from the 1,442 calendar days of observation:

| Metric | Ground-Truth Value | Engineering Significance |
| :--- | :--- | :--- |
| **Total Telemetry Records** | `2,075,259` rows | Minute-by-minute continuous electrical measurements |
| **Missing Telemetry Records**| `25,979` rows (`1.25%`) | Cleaned via time-weighted linear interpolation |
| **Total Monitored Days** | `1,442` calendar days | December 16, 2006 to November 26, 2010 |
| **Total Cumulative Electricity**| `37,846.56 kWh` | Total active energy consumed across 4 years |
| **Mean Daily Consumption** | `26.25 kWh/day` | Average daily residential consumption |
| **Median Daily Consumption**| `25.92 kWh/day` | 50th percentile of daily consumption |
| **Daily Standard Deviation**| `10.16 kWh/day` | Variability driven by weather and day-of-week |
| **Peak Single Day** | `79.56 kWh` (`2006-12-23`) | Pre-Christmas winter peak heating day |
| **Lowest Single Day** | `4.17 kWh` (`2008-08-25`) | Summer holiday / unoccupied dwelling day |
| **Sub-metering 1 (Kitchen)** | `2,299.46 kWh` (`6.1%`) | Microwave, dishwasher, and oven |
| **Sub-metering 2 (Laundry)** | `2,677.99 kWh` (`7.1%`) | Washing machine, dryer, refrigerator |
| **Sub-metering 3 (HVAC/Water)**| `13,421.42 kWh` (`35.5%`)| Electric water heater and space heating |
| **Remainder (Plug/Light Loads)**| `19,448.00 kWh` (`51.4%`)| Television, computers, lighting, and standby power |

---

## 5. Technology Stack

- **Language:** Python >= 3.10 (tested and verified on Python 3.14)
- **Data Manipulation:** `pandas`, `numpy`
- **Interactive Web Dashboard:** `streamlit`
- **Data Visualizations:** `plotly`, `matplotlib`, `seaborn`
- **Machine Learning & Modeling:** `scikit-learn` (Isolation Forest, Ridge Regression)
- **Report Generation:** `python-docx`

---

## 6. Project Directory Structure

```text
AICTE/
├── data/
│   ├── household_power_daily.csv         # Preprocessed 1,442-day daily aggregates (instant load)
│   ├── hourly_profile.csv                # 24-hour diurnal profile by circuit
│   ├── monthly_summary.csv               # Monthly aggregates across 2006-2010
│   └── household_power_consumption.txt   # Raw dataset (downloaded / copied from temp)
├── screenshots/
│   ├── 01_daily_consumption_trend.png    # 4-year daily timeline with 30-day moving average
│   ├── 02_submetering_breakdown.png      # Donut breakdown and monthly stacked bars
│   ├── 03_diurnal_hourly_pattern.png     # 24-hour diurnal demand curve with peak window
│   ├── 04_anomaly_detection_iqr.png      # Statistical IQR distribution and outlier flags
│   └── 05_forecasting_evaluation.png     # 90-day out-of-sample Ridge forecast evaluation
├── scripts/
│   ├── preprocess.py                     # Raw text preprocessing and aggregation pipeline
│   ├── generate_charts.py                # High-resolution chart generation script
│   ├── build_notebook.py                 # Jupyter Notebook generation script
│   └── build_report_docx.py              # Word report compilation script
├── Shani_ElectricityAnalytics.py         # Main Interactive Streamlit Dashboard application
├── Shani_ElectricityAnalytics.ipynb      # Complete exploratory Jupyter Notebook
├── Shani_ElectricityAnalyticsProjectReport.docx  # Complete 20-section Word Project Report
├── requirements.txt                      # Project dependencies
├── README.md                             # Comprehensive project documentation
└── .gitignore                            # Excludes large raw data (>100MB) from git commits
```

---

## 7. Installation and Setup Instructions

### Step 1: Clone or Navigate to the Project Folder
Open your terminal or command prompt:
```bash
cd c:\Users\Shani\Desktop\AICTE
```

### Step 2: Create and Activate a Python Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

**On macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Dataset Placement Instructions
The dataset file `household_power_consumption.txt` (or `household_power_consumption (1).txt`) should be placed in the `data/` folder:
- **Location:** `data/household_power_consumption.txt`
- The project already includes `data/household_power_daily.csv` and `data/hourly_profile.csv`, enabling the Streamlit dashboard to launch immediately without processing delays.
- If you wish to re-run the full raw preprocessing pipeline from scratch:
  ```bash
  python scripts/preprocess.py
  ```

### Step 5: Launch the Interactive Dashboard
Run the following command in your terminal:
```bash
streamlit run Shani_ElectricityAnalytics.py
```
The application will open in your default browser at `http://localhost:8501`.

---

## 8. Dashboard Features and Walkthrough

1. **Executive Overview (Tab 1):**
   - High-level KPI cards: Total Consumption (kWh), Daily Average (kWh/day), Estimated Financial Cost, Peak Day Usage, and Lowest Day Usage.
   - Period-over-period percentage delta comparing the selected window to the prior period.
   - Responsive timeline and recent monthly consumption bars.

2. **Consumption Trends (Tab 2):**
   - Interactive smoothing with selectable moving average windows (7, 14, 30, 60 days).
   - Day-of-week and seasonal monthly bar charts revealing weekend spikes and winter surges.
   - Sub-metering overlay toggles.

3. **End-Use & Sub-Metering (Tab 3):**
   - Interactive donut chart showing percentage distribution across Kitchen (6.1%), Laundry (7.1%), HVAC/Water Heating (35.5%), and Remainder (51.4%).
   - Stacked area timeline displaying circuit demand over time.
   - 24-hour diurnal profile highlighting the **19:00–22:00 peak demand window** and **02:00–05:00 off-peak baseload window**.

4. **Unusual Consumption Patterns (Tab 4):**
   - Dual anomaly detection: Statistical Interquartile Range (IQR) rule and Machine Learning (Isolation Forest).
   - Visual outlier scatter plots on the daily timeline.
   - Filterable data table of top anomalous dates with sub-circuit breakdowns.
   - *Clear Cautionary Notice:* Statistical anomalies flag deviations for inspection—they do not prove equipment failure or power theft.

5. **Energy-Saving Recommendations (Tab 5):**
   - Four evidence-based recommendations derived from the actual data findings.
   - Interactive "What-If" energy savings simulator allowing users to adjust standby reduction, HVAC optimization, and load-shifting percentages to estimate monthly and annual cost savings.

6. **Data Quality & Methodology (Tab 6):**
   - Transparent documentation of dataset characteristics, interpolation formulas, physical unit conversions, and known limitations.

---

## 9. Key Findings and Evidence-Based Recommendations

### Empirical Findings:
1. **Winter Space Heating Dominance:** Daily consumption triples from summer baseline (~15–20 kWh/day) to winter peaks (45–60 kWh/day), driven by electric heating.
2. **Significant Nighttime Baseload:** Between 02:00 and 05:00, the household draws ~350 Wh/hour continuously on the unmetered remainder circuit. This accumulates to ~1,277 kWh/year in phantom standby load.
3. **Evening Peak Overload:** Coincidental operation of cooking, laundry, and heating between 19:00 and 22:00 pushes demand to ~2,250 Wh/hour and causes local voltage sags to ~233 V.
4. **Outlier Event Distribution:** 31 days exceeded the statistical upper bound (52.1 kWh/day), all occurring during extreme winter cold spells.

### Actionable Recommendations:
1. **Eliminate Standby Power:** Switch off entertainment and computer peripheral clusters at night using smart power strips. Saves ~2.4 kWh/day (~876 kWh/year; ₹5,694/year at ₹6.50/kWh).
2. **Shift Laundry Loads:** Schedule washing machines and dryers during off-peak morning hours (09:00–13:00) using timer delays to relieve evening peak grid stress.
3. **Calibrate HVAC Thermostats:** Set water heater temperature to 55°C and reduce winter heating thermostat by 1°C. Saves ~8% of HVAC demand (~1,073 kWh/year; ₹6,974/year).
4. **Audit Pre-Winter Insulation:** Inspect weatherstripping and heating elements before December to prevent runaway energy expenditure during winter peak weeks.

---

## 10. Submission Files Checklist

As specified in the AICTE | IBM SkillsBuild Internship guidelines, the submission consists of four deliverables:

| File Name | Format | Purpose | Status |
| :--- | :--- | :--- | :--- |
| **`Shani_ElectricityAnalytics.py`** | `.py` | Main Interactive Streamlit Dashboard application | Completed & Verified |
| **`Shani_ElectricityAnalytics.ipynb`**| `.ipynb` | Step-by-step exploratory and modeling notebook | Completed & Verified |
| **`requirements.txt`** | `.txt` | List of third-party dependencies with version bounds | Completed & Verified |
| **`Shani_ElectricityAnalyticsProjectReport.docx`** | `.docx` | Complete 20-section academic Word report with embedded figures | Completed & Verified |
| **`README.md`** | `.md` | Comprehensive project setup and documentation | Completed & Verified |

---

## 11. Instructions for GitHub Repository Creation

To submit your project via GitHub:

1. **Create a New Repository on GitHub:**
   - Log in to your GitHub account at [github.com](https://github.com).
   - Click **New Repository** (or **+** in the top right corner).
   - Repository name: `electricity-consumption-analytics`
   - Set visibility to **Public** so internship evaluators can access it.
   - Do **not** initialize with a README, .gitignore, or license (these are already present in your project).
   - Click **Create repository**.

2. **Push Local Files to GitHub:**
   Open PowerShell in your project folder (`c:\Users\Shani\Desktop\AICTE`) and run:
   ```powershell
   git init
   git add .
   git commit -m "Initial commit: Complete AICTE-IBM SkillsBuild Electricity Analytics Project 2026"
   git branch -M main
   git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/electricity-consumption-analytics.git
   git push -u origin main
   ```
   *(Note: The provided `.gitignore` automatically excludes the large raw text file `data/*.txt` so your commit stays lightweight and does not exceed GitHub's 100 MB individual file limit).*

3. **Copy Repository URL for Submission:**
   - Copy your public repository link: `https://github.com/<YOUR_GITHUB_USERNAME>/electricity-consumption-analytics`
   - Paste the link into the internship certificate verification submission form along with the required files.

---

## 12. References and Citations

1. Hébrail, G., & Bérard, A. (2012). *Individual Household Electric Power Consumption Data Set*. UCI Machine Learning Repository. [https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption)
2. Bureau of Energy Efficiency (BEE), Ministry of Power, Government of India. (2024). *Standards & Labeling Program for Energy Efficient Appliances*. [https://beeindia.gov.in](https://beeindia.gov.in)
3. Liu, F. T., Ting, K. M., & Zhou, Z. H. (2008). *Isolation Forest*. In 2008 Eighth IEEE International Conference on Data Mining (pp. 413-422). IEEE.
4. McKinney, W. (2010). *Data Structures for Statistical Computing in Python*. In Proceedings of the 9th Python in Science Conference (pp. 51-56).
5. Streamlit Documentation. (2025). *Building Interactive Data Applications in Python*. [https://docs.streamlit.io](https://docs.streamlit.io)
6. AICTE & IBM SkillsBuild. (2026). *Data Analytics with AI Internship Curriculum & Guidelines*. BharatCares / Edunet Foundation.
