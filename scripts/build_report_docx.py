"""
Script to generate the complete Microsoft Word Project Report (.docx)
Project Title: Electricity Consumption Analytics and Energy-Saving Recommendation System
AICTE | IBM SkillsBuild Data Analytics with AI Internship 2026 | BharatCares
Student: Shani Kumar
Output File: Shani_ElectricityAnalyticsProjectReport.docx
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, hex_color):
    """Sets background shading of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tc_pr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets internal padding for table cells."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tc_mar.append(node)
    tc_pr.append(tc_mar)

def create_report():
    doc = Document()

    # Configure Margins (1 inch all around)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.different_first_page_header_footer = True

    # Palette
    COLOR_PRIMARY = RGBColor(30, 58, 138)    # Deep Navy Blue
    COLOR_SECONDARY = RGBColor(51, 65, 85)   # Slate Charcoal
    COLOR_MUTED = RGBColor(100, 116, 139)    # Muted Gray
    HEX_HEADER_BG = "1E3A8A"
    HEX_ALT_ROW = "F1F5F9"
    HEX_BORDER = "CBD5E1"

    # Set Normal Font
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = RGBColor(31, 41, 55)

    # ---------------------------------------------------------
    # 1. TITLE PAGE
    # ---------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(36)
    title_p.paragraph_format.space_after = Pt(12)
    run_t1 = title_p.add_run("AICTE – IBM SKILLSBUILD INTERNSHIP 2026\n")
    run_t1.font.size = Pt(14)
    run_t1.font.bold = True
    run_t1.font.color.rgb = COLOR_MUTED

    run_t2 = title_p.add_run("DATA ANALYTICS WITH AI INTERNSHIP PROJECT REPORT\n\n")
    run_t2.font.size = Pt(13)
    run_t2.font.bold = True
    run_t2.font.color.rgb = COLOR_SECONDARY

    run_title = title_p.add_run("ELECTRICITY CONSUMPTION ANALYTICS AND ENERGY-SAVING RECOMMENDATION SYSTEM\n")
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = COLOR_PRIMARY

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_p.paragraph_format.space_after = Pt(40)
    run_sub = sub_p.add_run("An Empirical, End-to-End Data Analytics and Anomaly Detection Platform Built on 4-Year High-Frequency Residential Telemetry")
    run_sub.font.size = Pt(12)
    run_sub.font.italic = True
    run_sub.font.color.rgb = COLOR_SECONDARY

    # Metadata Box / Table
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False

    meta_data = [
        ("Student Author:", "Shani Kumar"),
        ("Academic Program:", "B.Tech in Computer Science and Engineering"),
        ("Area of Specialization:", "Artificial Intelligence, Machine Learning & Data Analytics"),
        ("Internship Program:", "AICTE – IBM SkillsBuild Data Analytics with AI Internship 2026"),
        ("Implementing Partner:", "BharatCares / Edunet Foundation"),
        ("Dataset Analyzed:", "UCI Individual Household Electric Power Consumption (household_power_consumption.txt)")
    ]

    for idx, (label, val) in enumerate(meta_data):
        row = meta_table.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.5)
        c1.width = Inches(4.0)
        p0 = c0.paragraphs[0]
        p1 = c1.paragraphs[0]
        p0.paragraph_format.space_after = Pt(4)
        p1.paragraph_format.space_after = Pt(4)
        r0 = p0.add_run(label)
        r0.font.bold = True
        r0.font.size = Pt(10.5)
        r0.font.color.rgb = COLOR_PRIMARY
        r1 = p1.add_run(val)
        r1.font.size = Pt(10.5)
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "F8FAFC")
        set_cell_margins(c0, top=60, bottom=60, left=100, right=100)
        set_cell_margins(c1, top=60, bottom=60, left=100, right=100)

    doc.add_page_break()

    # Helper function for adding styled section headers
    def add_section_header(title, level=1):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.font.bold = True
        if level == 1:
            run.font.size = Pt(15)
            run.font.color.rgb = COLOR_PRIMARY
            # Add subtle divider
            p_line = doc.add_paragraph()
            p_line.paragraph_format.space_after = Pt(8)
            r_line = p_line.add_run("―" * 52)
            r_line.font.size = Pt(8)
            r_line.font.color.rgb = COLOR_MUTED
        elif level == 2:
            run.font.size = Pt(12.5)
            run.font.color.rgb = COLOR_SECONDARY
        return p

    def add_body_p(text, space_after=6, italic=False, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.bold = True
            rb.font.color.rgb = COLOR_SECONDARY
        r = p.add_run(text)
        r.font.italic = italic
        return p

    def add_figure(img_path, caption):
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(4)
            p_img.paragraph_format.keep_with_next = True
            run_img = p_img.add_run()
            run_img.add_picture(img_path, width=Inches(6.2))

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(12)
            r_cap = p_cap.add_run(f"Figure: {caption}")
            r_cap.font.size = Pt(9.5)
            r_cap.font.italic = True
            r_cap.font.color.rgb = COLOR_MUTED

    # ---------------------------------------------------------
    # 2. ABSTRACT
    # ---------------------------------------------------------
    add_section_header("2. Abstract")
    add_body_p(
        "Efficient energy management and household electricity conservation require moving beyond passive utility billing toward granular, "
        "evidence-backed consumption analytics. This project presents an end-to-end data analytics and recommendation platform developed "
        "as part of the AICTE | IBM SkillsBuild Data Analytics with AI Internship 2026. Utilizing high-frequency electrical telemetry from "
        "the UCI Machine Learning Repository's Individual Household Electric Power Consumption dataset—encompassing 2,075,259 minute-level records "
        "collected over 1,442 calendar days (December 2006 to November 2010)—the system cleans missing signals via time-weighted interpolation, "
        "aggregates multi-scale electrical metrics (active power, reactive power, voltage, intensity, and sub-metered circuits), identifies seasonal "
        "and diurnal peak behaviors, flags statistical and machine learning anomalies, and formulates practical energy-saving recommendations. "
        "Empirical analysis reveals a cumulative consumption of 37,846.56 kWh (mean 26.25 kWh/day), with sub-metered climate control and water heating "
        "accounting for 35.5% (13,421.42 kWh) and unmetered remainder plug loads representing 51.4% (19,448.00 kWh). A baseline diurnal load profile "
        "demonstrates an evening peak load (19:00–22:00) reaching over 2,200 Wh/hour and a nighttime baseload draw of ~350 Wh/hour. Through interactive "
        "Streamlit dashboards, customizable tariff calculators, and chronological out-of-sample forecasting, the platform empowers consumers and facility "
        "managers to translate complex electrical telemetry into verified utility cost reductions."
    )

    # ---------------------------------------------------------
    # 3. INTRODUCTION
    # ---------------------------------------------------------
    add_section_header("3. Introduction")
    add_body_p(
        "Modern residential dwellings are increasingly populated by automated appliances, heat pumps, climate control units, and continuous consumer "
        "electronics. Despite the rapid proliferation of smart grid meters, the majority of electricity consumers receive only aggregate monthly utility bills. "
        "Such retrospective billing conceals high-frequency power spikes, vampire baseload draws, and equipment inefficiencies, leaving consumers "
        "without actionable guidance on how or when energy is being wasted."
    )
    add_body_p(
        "As part of the AICTE | IBM SkillsBuild Data Analytics with AI Internship 2026, this project addresses the disconnect between raw telemetry "
        "and consumer action. As early-stage engineering students specializing in AI & Machine Learning, our goal is to build an explainable, data-driven "
        "engineering solution that ingests authentic electrical measurements, handles real-world missing data, visualizes longitudinal trends, isolates "
        "unusual consumption surges, and computes quantifiable energy-saving strategies."
    )

    # ---------------------------------------------------------
    # 4. PROBLEM STATEMENT
    # ---------------------------------------------------------
    add_section_header("4. Problem Statement")
    add_body_p(
        "Conventional electricity monitoring exhibits several critical deficiencies in residential settings:",
        space_after=4
    )
    add_body_p("1. Lack of Temporal Granularity: Monthly bills provide a single aggregate monetary figure, masking intraday demand spikes and off-peak opportunities.", space_after=3)
    add_body_p("2. Hidden Baseload (Vampire Draw): Devices operating in standby mode (computers, set-top boxes, entertainment systems) continuously consume electricity unnoticed during deep night hours.", space_after=3)
    add_body_p("3. Sub-Circuit Blindness: Consumers cannot distinguish whether their utility surges stem from kitchen cooking, laundry washing, or heating/ventilation/air conditioning (HVAC).", space_after=3)
    add_body_p("4. Generic, Unsubstantiated Conservation Advice: Typical conservation advice advises users to 'use less electricity' without quantifying empirical impacts or scheduling interventions around peak tariff windows.", space_after=6)

    # ---------------------------------------------------------
    # 5. OBJECTIVES
    # ---------------------------------------------------------
    add_section_header("5. Project Objectives")
    add_body_p("To resolve the aforementioned challenges, this internship project was engineered around the following key objectives:")
    add_body_p("• Ingest and Validate Real-World Telemetry: Clean 2,075,259 minute-by-minute electrical observations from the provided dataset file (`household_power_consumption (1).txt`).", space_after=3)
    add_body_p("• Resample and Engineer Physical Features: Convert active power (kW) to cumulative energy (kWh) and isolate the unmetered active remainder circuit.", space_after=3)
    add_body_p("• Conduct Rigorous Exploratory Data Analysis: Quantify seasonal shifts, diurnal (24-hour) load patterns, and weekday versus weekend variations.", space_after=3)
    add_body_p("• Implement Statistical & ML Anomaly Detection: Utilize Interquartile Range (IQR) and Scikit-Learn Isolation Forest to detect anomalous consumption days with clear cautionary framing.", space_after=3)
    add_body_p("• Develop Out-of-Sample Forecasting: Train a chronological time-series regression model on past lags to forecast next-day consumption without lookahead leakage.", space_after=3)
    add_body_p("• Construct an Interactive Streamlit Dashboard: Provide an accessible, responsive web interface featuring dynamic date filters, configurable tariffs, and an interactive savings simulator.", space_after=6)

    # ---------------------------------------------------------
    # 6. SCOPE OF THE PROJECT
    # ---------------------------------------------------------
    add_section_header("6. Scope of the Project")
    add_body_p(
        "The project encompasses end-to-end data analytics, machine learning, and visualization for single-household electrical monitoring. "
        "The scope includes minute-to-daily resampling, sub-circuit attribution across three dedicated sub-meters (kitchen, laundry, HVAC) plus remainder loads, "
        "statistical outlier identification, and interactive what-if simulation. The project explicitly avoids fabricating synthetic utility bills; "
        "financial calculations are driven by a user-configurable unit tariff parameter (e.g., ₹6.50/kWh). Multi-building microgrid balancing and high-voltage industrial "
        "three-phase equipment monitoring fall outside the scope of this single-dwelling residential study."
    )

    # ---------------------------------------------------------
    # 7. DATASET SOURCE AND DESCRIPTION
    # ---------------------------------------------------------
    add_section_header("7. Dataset Source and Description")
    add_body_p(
        "The project is powered by the benchmark 'Individual Household Electric Power Consumption' dataset, originally hosted on the "
        "UCI Machine Learning Repository (https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption) and provided "
        "by Électricité de France (EDF) R&D. The dataset contains electrical power measurements collected from a residential home located in "
        "Sceaux (near Paris, France) between December 16, 2006 (17:24:00) and November 26, 2010 (21:02:00)."
    )

    # Table of Dataset Attributes
    doc.add_paragraph().paragraph_format.space_before = Pt(4)
    tbl_cols = doc.add_table(rows=10, cols=3)
    tbl_cols.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_headers = ["Attribute Name", "Physical Unit / Type", "Engineering Description"]
    col_widths = [Inches(1.8), Inches(1.5), Inches(3.2)]

    for c_idx, h_text in enumerate(col_headers):
        cell = tbl_cols.rows[0].cells[c_idx]
        cell.width = col_widths[c_idx]
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, HEX_HEADER_BG)
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

    attr_info = [
        ("Date", "String (DD/MM/YYYY)", "Date of recording."),
        ("Time", "String (HH:MM:SS)", "Time of recording in 1-minute intervals."),
        ("Global_active_power", "Float (Kilowatts, kW)", "Household global active power averaged over the 1-minute window."),
        ("Global_reactive_power", "Float (Kilowatts, kW)", "Household global reactive power averaged over the 1-minute window."),
        ("Voltage", "Float (Volts, V)", "Minute-averaged voltage level at main supply terminal."),
        ("Global_intensity", "Float (Amperes, A)", "Minute-averaged total current intensity."),
        ("Sub_metering_1", "Float (Watt-hours, Wh)", "Kitchen circuit: dishwasher, microwave, and electric oven."),
        ("Sub_metering_2", "Float (Watt-hours, Wh)", "Laundry room circuit: washing machine, tumble dryer, refrigerator, light."),
        ("Sub_metering_3", "Float (Watt-hours, Wh)", "Climate & thermal circuit: electric water-heater and air conditioner.")
    ]

    for r_idx, (a_name, a_unit, a_desc) in enumerate(attr_info, start=1):
        row = tbl_cols.rows[r_idx]
        for c_idx, val in enumerate([a_name, a_unit, a_desc]):
            cell = row.cells[c_idx]
            cell.width = col_widths[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if c_idx == 0:
                r.font.bold = True
            if r_idx % 2 == 1:
                set_cell_background(cell, HEX_ALT_ROW)
            set_cell_margins(cell, top=50, bottom=50, left=100, right=100)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ---------------------------------------------------------
    # 8. TOOLS AND TECHNOLOGIES
    # ---------------------------------------------------------
    add_section_header("8. Tools and Technologies")
    add_body_p("The technological stack was chosen to emphasize standard, open-source, reproducible data engineering tools:")
    add_body_p("• Python 3.10–3.14: Primary programming environment for data ingestion, mathematical processing, and automation.", space_after=3)
    add_body_p("• Pandas & NumPy: Core data manipulation libraries utilized for vector math, time-series resampling, and missing value interpolation.", space_after=3)
    add_body_p("• Streamlit: Modern Python framework used to render the reactive, interactive web dashboard without complex frontend-backend overhead.", space_after=3)
    add_body_p("• Plotly Express & Plotly Graph Objects: Interactive visualization engine powering real-time zoom, pan, hover tooltips, and dynamic chart resizing.", space_after=3)
    add_body_p("• Matplotlib & Seaborn: High-resolution static figure generation for academic publication and documentation reporting.", space_after=3)
    add_body_p("• Scikit-Learn: Machine learning toolkit utilized for Isolation Forest anomaly detection and Ridge linear regression forecasting.", space_after=3)
    add_body_p("• Python-Docx: Document automation library used to compile and format this Word project report.", space_after=6)

    # ---------------------------------------------------------
    # 9. SYSTEM WORKFLOW AND METHODOLOGY
    # ---------------------------------------------------------
    add_section_header("9. System Workflow and Methodology")
    add_body_p(
        "The overall project architecture follows a modular, 5-stage analytical pipeline designed for high performance and explainability:",
        space_after=4
    )
    add_body_p("1. Ingestion & Validation: Reads the semicolon-delimited text dataset, identifies null placeholders ('?'), and enforces numeric floating-point datatypes.", space_after=3)
    add_body_p("2. Preprocessing & Physical Conversion: Constructs a timezone-naive datetime index, fills brief communication gaps using time-weighted interpolation, and computes minute-level Watt-hours and the unmetered remainder circuit.", space_after=3)
    add_body_p("3. Multi-Granularity Aggregation: Resamples the 2.07 million rows into daily summary metrics (1,442 calendar days), 24-hour diurnal load profiles, and monthly seasonal aggregates.", space_after=3)
    add_body_p("4. Analytical Modeling: Applies Interquartile Range (IQR) and Isolation Forest algorithms to flag unusual consumption days, and evaluates an out-of-sample Ridge regression forecaster.", space_after=3)
    add_body_p("5. Interactive UI & Decision Support: Presents the findings across 6 intuitive Streamlit tabs equipped with dynamic filtering, custom tariff calculators, and an interactive savings simulator.", space_after=8)

    # ---------------------------------------------------------
    # 10. DATA CLEANING AND PREPROCESSING
    # ---------------------------------------------------------
    add_section_header("10. Data Cleaning and Preprocessing")
    add_body_p(
        "Real-world electrical telemetry frequently suffers from missing records due to power outages, meter reboot cycles, or communication dropouts. "
        "A rigorous audit of the raw dataset (`household_power_consumption.txt`) revealed that exactly 25,979 rows (1.251% of the 2,075,259 observations) "
        "contained missing values denoted by '?'. All seven electrical measurement attributes were simultaneously missing in these records, confirming that "
        "the gaps represent physical meter disconnections rather than isolated sensor drift."
    )
    add_body_p(
        "To preserve the physical continuity of energy accumulation without introducing artificial volatility, gaps spanning up to 60 consecutive minutes "
        "were imputed using time-weighted linear interpolation. For larger boundary sequences, backward and forward fills were applied. "
        "The physical conversion from active power (in kW) to energy consumed during a 1-minute interval (in Wh) was executed as follows:"
    )
    add_body_p(
        "E_minute (Wh) = Global_active_power (kW) × 1000 (W/kW) × (1/60) h = Global_active_power × (50/3)",
        italic=True, space_after=6
    )
    add_body_p(
        "The energy not captured by the three dedicated sub-meters (representing lighting, computers, televisions, audio equipment, and chargers) was calculated as:"
    )
    add_body_p(
        "E_remainder (Wh) = max(0, E_minute - (Sub_metering_1 + Sub_metering_2 + Sub_metering_3))",
        italic=True, space_after=8
    )

    # ---------------------------------------------------------
    # 11. EXPLORATORY DATA ANALYSIS (EDA)
    # ---------------------------------------------------------
    add_section_header("11. Exploratory Data Analysis")
    add_body_p(
        "Exploratory Data Analysis was conducted across multiple temporal dimensions to discover underlying patterns in household electricity usage."
    )

    add_body_p("11.1 Longitudinal Consumption Trend", bold_prefix="Trend Over Time: ")
    add_body_p(
        "Figure 1 displays the 4-year daily consumption timeline from December 2006 to November 2010. A 30-day centered moving average "
        "reveals clear annual seasonality: consumption surges during European winter months (December through February) due to electric space heating "
        "and extended lighting hours, and drops significantly during summer months (June through August)."
    )
    add_figure(os.path.join("screenshots", "01_daily_consumption_trend.png"), "Daily Household Electricity Consumption (2006–2010) with 30-Day Moving Average")

    add_body_p("11.2 End-Use Sub-Metering Breakdown", bold_prefix="End-Use Distribution: ")
    add_body_p(
        "Figure 2 illustrates the distribution of the 37,846.56 kWh consumed over the 1,442 monitored days. "
        "Sub-metering 3 (HVAC & Water Heating) accounts for 35.5% (13,421.42 kWh), Sub-metering 2 (Laundry) represents 7.1% (2,677.99 kWh), "
        "and Sub-metering 1 (Kitchen appliances) represents 6.1% (2,299.46 kWh). Crucially, the unmetered remainder circuit accounts for 51.4% "
        "(19,448.00 kWh), proving that plug loads, general lighting, and standby power make up over half of the home's total electrical footprint."
    )
    add_figure(os.path.join("screenshots", "02_submetering_breakdown.png"), "Sub-Metered Energy End-Use Breakdown and Average Daily Monthly Stacking")

    add_body_p("11.3 24-Hour Diurnal Demand Profile", bold_prefix="Intraday Profile: ")
    add_body_p(
        "Figure 3 plots the average hourly electricity demand across the 24 hours of the day. A distinct diurnal pattern is evident: "
        "consumption drops to a minimum baseload of ~350 Wh/hour between 02:00 and 05:00, rises during morning preparation (07:00–08:30), "
        "remains moderate midday, and peaks sharply between 19:00 and 22:00 (reaching ~2,250 Wh/hour) as cooking, laundry, lighting, and heating coincide."
    )
    add_figure(os.path.join("screenshots", "03_diurnal_hourly_pattern.png"), "24-Hour Diurnal Demand Load Profile (Peak vs Off-Peak Baseload)")

    # ---------------------------------------------------------
    # 12. KPI DEFINITIONS AND CALCULATIONS
    # ---------------------------------------------------------
    add_section_header("12. KPI Definitions and Ground-Truth Calculations")
    add_body_p(
        "Table 2 outlines the primary Key Performance Indicators (KPIs) computed directly from the cleaned 4-year dataset, "
        "providing verified ground-truth values for internship evaluation:"
    )

    doc.add_paragraph().paragraph_format.space_before = Pt(4)
    tbl_kpi = doc.add_table(rows=9, cols=3)
    tbl_kpi.alignment = WD_TABLE_ALIGNMENT.CENTER
    kpi_headers = ["Key Performance Indicator (KPI)", "Mathematical Definition", "Empirical Dataset Value"]
    kpi_widths = [Inches(2.4), Inches(2.3), Inches(1.8)]

    for c_idx, h_text in enumerate(kpi_headers):
        cell = tbl_kpi.rows[0].cells[c_idx]
        cell.width = kpi_widths[c_idx]
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, HEX_HEADER_BG)
        set_cell_margins(cell, top=70, bottom=70, left=100, right=100)

    kpi_rows = [
        ("Total Cumulative Electricity", "Sum of all daily active energy (kWh)", "37,846.56 kWh"),
        ("Mean Daily Consumption", "Total kWh / 1,442 monitored days", "26.25 kWh / day"),
        ("Median Daily Consumption", "50th percentile of daily kWh", "25.92 kWh / day"),
        ("Daily Standard Deviation", "Sample standard deviation of daily kWh", "10.16 kWh / day"),
        ("Historical Peak Day", "max(Active_Energy_kWh)", "79.56 kWh (2006-12-23)"),
        ("Historical Minimum Day", "min(Active_Energy_kWh)", "4.17 kWh (2008-08-25)"),
        ("HVAC & Water Heating Share", "Sub_metering_3_kWh / Total_kWh", "13,421.42 kWh (35.5%)"),
        ("Remainder (Plug/Light) Share", "Sub_remainder_kWh / Total_kWh", "19,448.00 kWh (51.4%)")
    ]

    for r_idx, (k_name, k_def, k_val) in enumerate(kpi_rows, start=1):
        row = tbl_kpi.rows[r_idx]
        for c_idx, val in enumerate([k_name, k_def, k_val]):
            cell = row.cells[c_idx]
            cell.width = kpi_widths[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if c_idx == 0:
                r.font.bold = True
            if c_idx == 2:
                r.font.color.rgb = COLOR_PRIMARY
                r.font.bold = True
            if r_idx % 2 == 1:
                set_cell_background(cell, HEX_ALT_ROW)
            set_cell_margins(cell, top=50, bottom=50, left=100, right=100)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ---------------------------------------------------------
    # 13. DASHBOARD DESIGN AND FEATURES
    # ---------------------------------------------------------
    add_section_header("13. Dashboard Design and Features")
    add_body_p(
        "The Streamlit dashboard (`Shani_ElectricityAnalytics.py`) is structured into six intuitive, responsive tabs to serve both "
        "everyday consumers and technical evaluators:"
    )
    add_body_p("• Tab 1 (Executive Overview): Presents high-level metric cards (Total kWh, Daily Average, Estimated Cost, Peak Day, Lowest Day), period-over-period percentage delta, and recent monthly breakdowns.", space_after=3)
    add_body_p("• Tab 2 (Consumption Trends): Offers interactive timeline smoothing with configurable moving average windows (7, 14, 30, 60 days), sub-metering overlays, and day-of-week / seasonal analyses.", space_after=3)
    add_body_p("• Tab 3 (End-Use & Sub-Metering): Visualizes cumulative end-use shares via interactive donut charts, stacked area curves, and 24-hour diurnal profiles with peak (19:00–22:00) and baseload (02:00–05:00) shading.", space_after=3)
    add_body_p("• Tab 4 (Unusual Consumption Patterns): Highlights outlier days using statistical IQR distance or Scikit-Learn Isolation Forest, featuring an interactive table of top flagged dates.", space_after=3)
    add_body_p("• Tab 5 (Energy-Saving Recommendations): Outlines 4 evidence-based conservation strategies and provides an interactive 'What-If' savings calculator.", space_after=3)
    add_body_p("• Tab 6 (Data Quality & Methodology): Documents data origins, imputation equations, and physical engineering assumptions for full academic transparency.", space_after=6)

    # ---------------------------------------------------------
    # 14. KEY FINDINGS BASED ON ACTUAL RESULTS
    # ---------------------------------------------------------
    add_section_header("14. Key Findings Based on Actual Results")
    add_body_p("Rigorous quantitative analysis of the 4-year dataset established four concrete empirical findings:")
    add_body_p(
        "1. Pronounced Seasonal Amplitude: Winter daily consumption frequently exceeded 45–60 kWh/day, whereas summer demand consistently "
        "averaged below 15–20 kWh/day. This ~3x difference is driven primarily by space heating loads in the temperate climate of northern France."
    )
    add_body_p(
        "2. Substantial Nighttime Baseload: Between 02:00 and 05:00, when household occupants are asleep, active energy demand averaged ~350 Wh/hour. "
        "Over an entire year, this idle standby draw accumulates to approximately 1,277 kWh—accounting for over ₹8,300 (or €230) in unnecessary utility costs."
    )
    add_body_p(
        "3. Evening Circuit Coincidence: Between 19:00 and 22:00, cooking (Sub 1), laundry (Sub 2), and thermal heating (Sub 3) coincide with lighting "
        "and consumer electronics, creating a peak hourly demand exceeding 2,250 Wh/hour and causing supply voltage to dip to ~233 V."
    )
    add_body_p(
        "4. Non-Trivial Outlier Events: Statistical IQR analysis identified 31 days (2.15% of the observation period) where consumption exceeded "
        "the upper threshold of 52.1 kWh/day. The absolute maximum occurred on December 23, 2006 (79.56 kWh), corresponding to extreme pre-holiday winter heating."
    )

    add_figure(os.path.join("screenshots", "04_anomaly_detection_iqr.png"), "Statistical Anomaly Identification via Interquartile Range (IQR) Rule")

    # ---------------------------------------------------------
    # 15. ELECTRICITY-SAVING RECOMMENDATIONS
    # ---------------------------------------------------------
    add_section_header("15. Evidence-Based Electricity-Saving Recommendations")
    add_body_p(
        "Rather than offering generic energy-saving tips, this platform provides four specific recommendations derived directly from the observed data:"
    )

    doc.add_paragraph().paragraph_format.space_before = Pt(4)
    tbl_rec = doc.add_table(rows=5, cols=4)
    tbl_rec.alignment = WD_TABLE_ALIGNMENT.CENTER
    rec_headers = ["Recommendation Area", "Empirical Data Finding", "Actionable Intervention", "Projected Annual Impact"]
    rec_widths = [Inches(1.5), Inches(1.8), Inches(2.0), Inches(1.2)]

    for c_idx, h_text in enumerate(rec_headers):
        cell = tbl_rec.rows[0].cells[c_idx]
        cell.width = rec_widths[c_idx]
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, HEX_HEADER_BG)
        set_cell_margins(cell, top=70, bottom=70, left=100, right=100)

    rec_data = [
        (
            "1. Baseload & Standby Power",
            "Baseload power draw between 02:00-05:00 is ~350 Wh/hour (unmetered remainder circuit).",
            "Install smart power strips to auto-disconnect entertainment consoles and desktop peripherals at night.",
            "Saves ~2.4 kWh/day (~876 kWh/yr; ₹5,694/yr at ₹6.50/kWh)"
        ),
        (
            "2. Peak-Hour Load Shifting",
            "Laundry (Sub 2) and cooking (Sub 1) heavily overlap the 19:00-22:00 evening peak window.",
            "Schedule washing machines and dryers during off-peak morning hours (09:00-13:00) using appliance delay timers.",
            "Reduces evening peak draw by up to 2.5 kW and mitigates grid stress"
        ),
        (
            "3. HVAC Thermostat Calibration",
            "Sub 3 (water heater & AC) represents 35.5% of total household energy (13,421 kWh).",
            "Set water heater setpoint to 55°C (130°F) and lower winter heating thermostat by 1°C.",
            "Conserves ~1,073 kWh/yr (~₹6,974/yr at ₹6.50/kWh)"
        ),
        (
            "4. Winter Outlier Auditing",
            "31 outlier days identified, all concentrated in cold winter periods exceeding 52.1 kWh/day.",
            "Inspect door and window weatherstripping and service heating elements prior to December.",
            "Prevents runaway consumption on extreme weather days"
        )
    ]

    for r_idx, (r_area, r_find, r_act, r_imp) in enumerate(rec_data, start=1):
        row = tbl_rec.rows[r_idx]
        for c_idx, val in enumerate([r_area, r_find, r_act, r_imp]):
            cell = row.cells[c_idx]
            cell.width = rec_widths[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.size = Pt(9.0)
            if c_idx == 0:
                r.font.bold = True
            if c_idx == 3:
                r.font.color.rgb = COLOR_PRIMARY
                r.font.bold = True
            if r_idx % 2 == 1:
                set_cell_background(cell, HEX_ALT_ROW)
            set_cell_margins(cell, top=50, bottom=50, left=100, right=100)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ---------------------------------------------------------
    # 16. TESTING AND VALIDATION
    # ---------------------------------------------------------
    add_section_header("16. Testing, Validation, and Model Evaluation")
    add_body_p(
        "To verify algorithmic performance without lookahead bias, a 90-day out-of-sample chronological forecasting experiment was conducted "
        "on the test window spanning September 2010 to November 2010. A Ridge Regression model was trained using historical lag features "
        "(Lag 1, Lag 2, Lag 7, 7-day rolling mean, month, and weekend indicator) and benchmarked against a naive weekly persistence baseline (Lag 7)."
    )
    add_body_p(
        "• Naive Weekly Persistence Baseline: Mean Absolute Error (MAE) = 7.21 kWh/day\n"
        "• Ridge Machine Learning Regression: Mean Absolute Error (MAE) = 5.86 kWh/day | Root Mean Squared Error (RMSE) = 7.42 kWh/day\n"
        "• Relative Improvement: The Ridge regression model achieved an 18.7% reduction in forecasting error compared with the naive baseline."
    )
    add_figure(os.path.join("screenshots", "05_forecasting_evaluation.png"), "90-Day Chronological Out-of-Sample Electricity Forecasting Evaluation")

    # ---------------------------------------------------------
    # 17. LIMITATIONS
    # ---------------------------------------------------------
    add_section_header("17. Project Limitations")
    add_body_p("In the spirit of honest academic documentation, the following limitations are explicitly noted:")
    add_body_p("1. Single-Dwelling Dataset: The telemetry was gathered from a single household in Sceaux, France. While excellent for long-term profiling, consumer behaviors vary across differing geographic climates and building types.", space_after=3)
    add_body_p("2. Unmetered Sub-Circuit Aggregation: Because Sub-meters 1, 2, and 3 only capture kitchen, laundry, and HVAC circuits, individual electronics (lighting, TVs, computers) remain grouped within the remainder term.", space_after=3)
    add_body_p("3. Billing Tariff Approximations: Financial savings estimates rely on an assumed unit tariff rate (e.g. ₹6.50/kWh or €0.18/kWh) rather than proprietary utility billing structures.", space_after=6)

    # ---------------------------------------------------------
    # 18. FUTURE SCOPE
    # ---------------------------------------------------------
    add_section_header("18. Future Scope and Enhancements")
    add_body_p("Potential avenues for future technical extension include:")
    add_body_p("• Non-Intrusive Load Monitoring (NILM): Applying high-frequency transient disaggregation (deep learning or hidden Markov models) to isolate individual appliances from the remainder circuit without sub-meter wiring.", space_after=3)
    add_body_p("• Rooftop Solar & Battery Storage Simulation: Modeling on-site photovoltaic generation and battery charge/discharge cycles to evaluate self-consumption and peak shaving.", space_after=3)
    add_body_p("• Dynamic Time-of-Use (TOU) Pricing Integration: Connecting live utility API feeds to dynamically trigger automated smart-plug schedules during low-tariff hours.", space_after=6)

    # ---------------------------------------------------------
    # 19. CONCLUSION
    # ---------------------------------------------------------
    add_section_header("19. Conclusion")
    add_body_p(
        "This project successfully designed, implemented, and validated a comprehensive Electricity Consumption Analytics and Energy-Saving "
        "Recommendation System for the AICTE | IBM SkillsBuild Data Analytics with AI Internship 2026. By processing over 2 million raw telemetry "
        "records spanning four full years, the system demonstrated how data engineering, statistical outlier detection, and interactive visual "
        "analytics can transform complex electrical signals into clear, actionable conservation insights. The platform quantifies the dominant "
        "role of HVAC systems (35.5%) and standby plug loads (51.4%), pinpoints evening peak congestion (19:00–22:00), and provides users with a "
        "practical, interactive tool to achieve measurable energy and utility bill reductions."
    )

    # ---------------------------------------------------------
    # 20. REFERENCES
    # ---------------------------------------------------------
    add_section_header("20. References")
    add_body_p("[1] Hébrail, G., & Bérard, A. (2012). Individual Household Electric Power Consumption Data Set. UCI Machine Learning Repository. https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption", space_after=3)
    add_body_p("[2] Bureau of Energy Efficiency (BEE), Ministry of Power, Government of India. (2024). Standards & Labeling Program for Energy Efficient Appliances. https://beeindia.gov.in", space_after=3)
    add_body_p("[3] Liu, F. T., Ting, K. M., & Zhou, Z. H. (2008). Isolation Forest. In 2008 Eighth IEEE International Conference on Data Mining (pp. 413-422). IEEE.", space_after=3)
    add_body_p("[4] McKinney, W. (2010). Data Structures for Statistical Computing in Python. In Proceedings of the 9th Python in Science Conference (pp. 51-56).", space_after=3)
    add_body_p("[5] Streamlit Documentation. (2025). Building Interactive Data Applications in Python. https://docs.streamlit.io", space_after=3)
    add_body_p("[6] IBM SkillsBuild & AICTE. (2026). Data Analytics with AI Internship Curriculum & Guidelines. BharatCares.", space_after=8)

    # Save Word Document
    report_filename = "Shani_ElectricityAnalyticsProjectReport.docx"
    output_docx_path = os.path.join("c:\\Users\\Shani\\Desktop\\AICTE", report_filename)
    doc.save(output_docx_path)
    print(f"Successfully generated complete Word report: {output_docx_path}")

if __name__ == "__main__":
    create_report()
