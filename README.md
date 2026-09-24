# Airline OTP & Delay Analysis Pipeline

A Python-based ETL pipeline for processing airline flight-operation data and generating **On-Time Performance (OTP)** and **flight delay analysis** datasets.

The pipeline uses `pandas` and `numpy` to clean operational flight data, apply OTP validation rules, classify departure and arrival delays, enrich flight records with delay-code and station reference data, and generate multiple aggregated CSV datasets for operational reporting and analysis.

---

## Overview

This project processes airline flight-operation records to produce structured datasets for:

* Departure OTP
* Arrival OTP
* Delay classification
* Delay category analysis
* Delay code analysis
* Station-level OTP
* Aircraft/class-level OTP
* Monthly and yearly OTP
* Controllable vs. uncontrollable delay analysis
* Geographic/zone-level OTP analysis
* Detailed flight-level operational data

The pipeline is designed around a folder-based ETL structure:

```text
Input CSV Files
      │
      ▼
Data Cleaning & Formatting
      │
      ▼
Flight Validation
      │
      ├── Departure OTP
      │
      └── Arrival OTP
      │
      ▼
Delay Code & Station Enrichment
      │
      ▼
Aggregation & KPI Calculation
      │
      ▼
Output CSV Files
```

---

## Technology

* **Python**
* **Pandas**
* **NumPy**
* **CSV**
* ETL / data transformation
* Aggregation and KPI calculation

---

## Project Structure

The script expects the following directory structure:

```text
project/
│
├── otp_calculation.py
│
├── input/
│   ├── otp_pandas_try.csv
│   ├── delco_data_try.csv
│   └── station_db.csv
│
└── output/
    └── generated CSV files
```

The script automatically creates the `output/` directory if it does not already exist.

---

## Input Data

### 1. Flight Operation Data

```text
otp_pandas_try.csv
```

This is the primary flight-operation dataset.

The pipeline uses operational fields including:

* Flight date
* Flight type
* Departure station
* Arrival station
* Flight status
* Delay durations
* Delay codes
* Arrival delay information
* Sub-codes associated with delay codes

The script performs data cleansing and converts date and delay fields into formats suitable for calculation.

---

### 2. Delay Code Reference

```text
delco_data_try.csv
```

This reference table provides delay-code classifications used to enrich the operational flight dataset.

The pipeline uses:

* `DlyCodeAsgn`
* `DlyCat`
* `DlyCat2`

to associate individual delay codes with their corresponding delay categories and controllability classifications.

---

### 3. Station Reference

```text
station_db.csv
```

The station reference dataset provides additional information for operational analysis, including:

* Station
* ICAO
* Class
* Town
* Zone

These attributes are merged into the flight dataset to support station-level and zone-level analysis.

---

## OTP Validation Logic

### Flight Validation

A flight is considered valid for OTP calculation when:

```text
TYPE = J or G
AND
ST = 0
```

The script assigns:

```text
val
```

for valid flights and:

```text
not_count
```

for flights excluded from the OTP calculation.

---

## Departure OTP

Departure delay is calculated from:

```text
DLY1 + DLY2 + DLY3 + DLY4
```

A valid flight is classified as:

| Delay        | Classification |
| ------------ | -------------- |
| ≤ 15 minutes | On Time        |
| > 15 minutes | Late           |

This classification is stored in `DelVal`.

### Departure Delay Ranges

Late flights are further classified into:

| Delay Range   |
| ------------- |
| 00:16 - 00:30 |
| 00:31 - 00:59 |
| 01:00 - 01:59 |
| 02:00 - 03:59 |
| > 04:00       |

---

## Arrival OTP

Arrival delay is calculated from:

```text
DLY1Arr + DLY2Arr
```

The same 15-minute OTP threshold is applied:

```text
≤ 15 minutes → On Time
> 15 minutes → Late
```

Arrival delays are also grouped into the same delay-range categories used for departure OTP.

---

## Delay Code Assignment

For delayed flights, the pipeline identifies the delay code associated with the largest delay component among:

```text
DLY1
DLY2
DLY3
DLY4
```

The assigned delay code is then used to retrieve its corresponding category from the delay-code reference table.

The same approach is applied to arrival delay using:

```text
DLY1Arr
DLY2Arr
```

---

## Delay Categories

The pipeline analyzes delay minutes across several operational categories, including:

* Station Handling
* Damage to Aircraft
* Technical
* System
* Flight Operations & Crew
* Weather
* Airport Facilities
* Miscellaneous

It also separates delays into:

* **Controllable**
* **Uncontrollable**

These categories are calculated for both departure and arrival analysis.

---

## Aggregation

The pipeline generates multiple aggregation levels.

### Time-based

* Daily
* Monthly
* Yearly

### Operational dimensions

* Station
* Station class
* Aircraft/ICAO classification
* Delay category
* Delay code
* Zone

For example, daily OTP is calculated from the number of valid flights and the number of flights classified as on-time.

---

## Output

The pipeline generates the following CSV datasets:

| Output                                        | Description                        |
| --------------------------------------------- | ---------------------------------- |
| `otp_per_date_output.csv`                     | Daily departure OTP                |
| `delay_category_output.csv`                   | Daily departure delay categories   |
| `otp_per_month_output.csv`                    | Monthly departure OTP              |
| `delay_category_per_month_output.csv`         | Monthly departure delay categories |
| `otp_per_station_per_month.csv`               | Monthly OTP by station             |
| `otp_per_station_per_date.csv`                | Daily OTP by station               |
| `otp_per_station_class_per_month.csv`         | Monthly OTP by station class       |
| `otp_per_station_class_per_date.csv`          | Daily OTP by station class         |
| `dfs_details.csv`                             | Enriched flight-level dataset      |
| `delay_per_cat_per_time.csv`                  | Delay category by time period      |
| `otp_arr_per_date_output.csv`                 | Daily arrival OTP                  |
| `otp_arr_per_month_output.csv`                | Monthly arrival OTP                |
| `delay_category_arrival_output.csv`           | Daily arrival delay categories     |
| `delay_category_arrival_per_month_output.csv` | Monthly arrival delay categories   |
| `otp_arr_per_station_per_month.csv`           | Monthly arrival OTP by station     |
| `otp_arr_per_station_per_date.csv`            | Daily arrival OTP by station       |
| `delay_category_per_year_output.csv`          | Yearly delay category analysis     |
| `assigned_delay_code_per_month.csv`           | Monthly delay-code analysis        |
| `otpPerFlightZoneMonthly.csv`                 | Monthly OTP by operational zone    |
| `otpPerFlightZoneYearly.csv`                  | Yearly OTP by operational zone     |

The script writes these datasets as semicolon-separated CSV files into the `output/` directory.

---

## How to Run

### 1. Install dependencies

```bash
pip install pandas numpy
```

### 2. Prepare the input directory

Place the required CSV files inside:

```text
input/
```

with the expected filenames:

```text
otp_pandas_try.csv
delco_data_try.csv
station_db.csv
```

### 3. Run the pipeline

```bash
python otp_calculation.py
```

### 4. Check the output

The generated datasets will be available inside:

```text
output/
```

---

## ETL Workflow

The overall processing sequence is:

### 1. Extract

Read the three CSV sources:

```text
Flight Operation Data
Delay Code Reference
Station Reference
```

### 2. Transform

The pipeline:

* Cleans missing values
* Converts dates
* Converts delay durations to minutes
* Normalizes delay-code fields
* Validates flights for OTP calculation
* Calculates total departure delay
* Calculates total arrival delay
* Classifies flights as on-time or late
* Assigns delay codes
* Categorizes delay causes
* Enriches flights with station information
* Calculates OTP percentages
* Aggregates operational metrics

### 3. Load

The processed datasets are exported as CSV files into the `output/` directory.

---

## Example Use Cases

The generated datasets can be used for:

* Daily operational OTP monitoring
* Monthly OTP reporting
* Station performance analysis
* Arrival vs. departure OTP analysis
* Delay root-cause analysis
* Controllable vs. uncontrollable delay monitoring
* Delay-code contribution analysis
* Station/zone performance comparison
* Historical operational trend analysis
* Power BI or other BI dashboard integration
* Further statistical or machine-learning analysis

---

## Notes

This project is designed around a specific airline operational data structure and delay classification methodology.

Therefore, users adapting the pipeline to another airline or data source may need to modify:

* Input column names
* Flight validation rules
* Delay-code mappings
* Station reference structure
* OTP threshold
* Delay categories
* Aggregation dimensions

The current implementation uses a **15-minute threshold** to distinguish on-time and delayed flights.

---

## Future Improvements

Potential improvements to the pipeline include:

* [ ] Separate configuration from processing logic
* [ ] Move input/output paths into a configuration file
* [ ] Add automated data-quality checks
* [ ] Add logging
* [ ] Add exception handling
* [ ] Reduce repetitive aggregation code
* [ ] Modularize the pipeline into functions
* [ ] Add automated testing
* [ ] Add database input/output
* [ ] Add automated scheduling
* [ ] Integrate with BI dashboards
* [ ] Add automated notification when ETL processing fails

---

## Project Purpose

This project demonstrates the application of Python-based ETL and data analysis to real-world airline operational data.

The primary objective is to transform raw flight-operation records into structured operational datasets that can support **OTP monitoring, delay analysis, operational reporting, and further data-driven decision making**.
