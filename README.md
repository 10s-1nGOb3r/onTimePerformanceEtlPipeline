# Airline Operations Analytics ETL Pipeline

A Python-based ETL pipeline for transforming airline flight-operation data into structured datasets for **On-Time Performance (OTP), delay analysis, Scheduled Ground Time (SGT), Actual Ground Time (AGT), and operational performance monitoring**.

The project is designed to process raw airline operational data and convert it into analytical datasets that can be used for operational reporting, KPI monitoring, dashboard development, and further data analysis.

The pipeline currently consists of two main analytical modules:

* **OTP & Delay Analysis**
* **Ground Time Analysis**

---

# Project Overview

Airline operational data contains a large amount of flight-level information that can be difficult to analyze directly.

This project transforms raw operational records into structured datasets through a series of ETL processes:

```text
                    Raw Operational Data
                            │
                            ▼
                    Data Cleansing
                            │
             ┌──────────────┴──────────────┐
             │                             │
             ▼                             ▼
      OTP & Delay Analysis          Ground Time Analysis
             │                             │
             ▼                             ▼
       Delay / OTP KPIs               SGT / AGT KPIs
             │                             │
             └──────────────┬──────────────┘
                            │
                            ▼
                  Aggregated Datasets
                            │
                            ▼
                   CSV Output Files
                            │
                            ▼
                Reporting / BI Analysis
```

---

# Modules

## 1. OTP & Delay Analysis

The OTP module processes airline flight-operation data to calculate:

* Departure OTP
* Arrival OTP
* Delay duration
* Delay ranges
* Delay codes
* Delay categories
* Controllable vs. uncontrollable delays
* Station-level OTP
* Station-class OTP
* Monthly OTP
* Yearly OTP
* Zone-level OTP
* Flight-level operational details

### Flight Validation

A flight is considered valid for OTP calculation when:

```text
TYPE = J or G
AND
ST = 0
```

Valid flights are assigned:

```text
val
```

while excluded flights are assigned:

```text
not_count
```

### Departure OTP

Departure delay is calculated from:

```text
DLY1 + DLY2 + DLY3 + DLY4
```

The OTP classification uses a 15-minute threshold:

| Delay        | Classification |
| ------------ | -------------- |
| ≤ 15 minutes | On Time        |
| > 15 minutes | Late           |

### Arrival OTP

Arrival delay is calculated from:

```text
DLY1Arr + DLY2Arr
```

The same 15-minute threshold is applied.

### Delay Ranges

Delayed flights are grouped into:

* 00:16 - 00:30
* 00:31 - 00:59
* 01:00 - 01:59
* 02:00 - 03:59
* > 04:00

### Delay Code Analysis

The pipeline identifies the delay component with the largest delay duration and uses the corresponding delay code to classify the cause.

Delay categories include:

* Station Handling
* Damage to Aircraft
* Technical
* System
* Flight Operations & Crew
* Weather
* Airport Facilities
* Miscellaneous

The analysis also separates delays into:

* Controllable
* Uncontrollable

---

# 2. Ground Time Analysis

The Ground Time module analyzes aircraft turnaround performance by comparing:

* **Scheduled Ground Time (SGT)**
* **Actual Ground Time (AGT)**

The objective is to identify whether an aircraft's actual ground time was:

```text
< SGT
E SGT
> SGT
```

This allows operational teams to monitor whether aircraft turnaround performance is operating below, at, or above the scheduled ground-time target.

---

## Scheduled Ground Time

Scheduled Ground Time is calculated based on aircraft rotation sequencing.

The aircraft rotation is divided into:

```text
head
body
tail
head&tail
```

The classification is determined after sorting flights by aircraft registration and scheduled block-off time.

The SGT calculation considers the scheduled block-off and previous flight's scheduled or actual block-on information depending on the aircraft rotation and early-landing condition.

---

## Actual Ground Time

Actual Ground Time is calculated using actual block-off and block-on timestamps.

For aircraft rotations, the calculation considers:

* Aircraft registration
* Flight sequence
* Actual block-off
* Actual block-on
* Scheduled block-off
* Previous flight's actual block-on
* Early landing condition

The resulting AGT is then associated with the corresponding flight using a composite key:

```text
DATE + FLT + DEP + ARR
```

## The second script creates this key before merging the SGT and AGT datasets.

## SGT vs AGT Classification

After SGT and AGT are combined, the pipeline compares the two values.

For valid flights:

```text
Actual GT < Scheduled GT
        ↓
      < SGT

Actual GT = Scheduled GT
        ↓
      E SGT

Actual GT > Scheduled GT
        ↓
      > SGT
```

This classification is stored in the `AGT` field.

---

# Data Sources

The project uses CSV-based operational data.

Typical input sources include:

### OTP Module

```text
input/
├── otp_pandas_try.csv
├── delco_data_try.csv
└── station_db.csv
```

### Ground Time Module

```text
input_try/
├── pyActGt_try.csv
└── station_db.csv
```

The Ground Time script reads the operational flight dataset and station reference data from the `input_try` directory.

---

# Technology Stack

* **Python**
* **Pandas**
* **NumPy**
* CSV
* ETL
* Data cleansing
* Data transformation
* Data aggregation
* Operational KPI calculation

---

# Project Structure

A possible repository structure is:

```text
airline-operations-analytics/
│
├── src/
│   ├── otp_analysis.py
│   └── ground_time_analysis.py
│
├── input/
│   ├── otp_pandas_try.csv
│   ├── delco_data_try.csv
│   └── station_db.csv
│
├── input_try/
│   └── pyActGt_try.csv
│
├── output/
│   ├── OTP outputs
│   └── Ground Time outputs
│
├── README.md
├── requirements.txt
└── .gitignore
```

For production or portfolio use, the actual raw airline operational data should not be committed to a public repository. Use anonymized/sample data instead.

---

# ETL Process

## Extract

The scripts read operational CSV files containing flight-operation records and supporting reference data.

```text
CSV
 │
 ├── Flight Operations
 ├── Delay Code Reference
 └── Station Reference
```

---

## Transform

The pipeline performs several transformations.

### Data Cleansing

Examples include:

* Date conversion
* Time conversion
* Missing-value handling
* Data-type conversion
* Delay-minute calculations
* Flight validation
* Aircraft rotation sequencing

The Ground Time module, for example, converts operational date/time fields into pandas datetime objects before calculating ground-time metrics.

### Operational Logic

The pipeline then applies domain-specific business rules.

For OTP:

```text
Flight Validation
        ↓
Delay Calculation
        ↓
OTP Classification
        ↓
Delay Code Assignment
        ↓
Delay Category
```

For Ground Time:

```text
Aircraft Rotation
        ↓
Scheduled Ground Time
        ↓
Actual Ground Time
        ↓
SGT vs AGT Comparison
```

---

# Ground Time Aggregation

The Ground Time module produces several aggregation levels.

### Daily

Ground-time performance is aggregated by date.

Metrics include:

* Total valid flights
* Flights with AGT < SGT
* Flights with AGT = SGT
* Flights with AGT > SGT
* Percentage of each category

The daily aggregation is calculated directly from the classified AGT records.

### Monthly

The same metrics are aggregated by:

* Year
* Month number
* Month name

### Station

Ground-time performance can be analyzed by:

* Station
* Airport town
* Station class

The station reference is merged into the operational dataset before aggregation.

### Class

The pipeline also produces ground-time analysis by station class on both monthly and daily levels.

---

# Output Files

## OTP & Delay Outputs

The OTP module generates datasets including:

```text
otp_per_date_output.csv
delay_category_output.csv
otp_per_month_output.csv
delay_category_per_month_output.csv
otp_per_station_per_month.csv
otp_per_station_per_date.csv
otp_per_station_class_per_month.csv
otp_per_station_class_per_date.csv
dfs_details.csv
delay_per_cat_per_time.csv
otp_arr_per_date_output.csv
otp_arr_per_month_output.csv
delay_category_arrival_output.csv
delay_category_arrival_per_month_output.csv
otp_arr_per_station_per_month.csv
otp_arr_per_station_per_date.csv
delay_category_per_year_output.csv
assigned_delay_code_per_month.csv
otpPerFlightZoneMonthly.csv
otpPerFlightZoneYearly.csv
```

---

## Ground Time Outputs

The Ground Time module generates:

| File                        | Description                  |
| --------------------------- | ---------------------------- |
| `sgtDetails.csv`            | Scheduled Ground Time detail |
| `agtDetails.csv`            | Actual Ground Time detail    |
| `sgtAgtDetails.csv`         | Combined SGT and AGT dataset |
| `agtPerDate.csv`            | Daily AGT performance        |
| `agtPerStationPerDate.csv`  | Daily AGT by station         |
| `agtPerMonth.csv`           | Monthly AGT performance      |
| `agtPerStationPerMonth.csv` | Monthly AGT by station       |
| `agtPerClassPerMonth.csv`   | Monthly AGT by station class |
| `agtPerClassPerDate.csv`    | Daily AGT by station class   |

The Ground Time script explicitly exports these nine datasets as semicolon-separated CSV files.

---

# Example Analytical Questions

The resulting datasets can support questions such as:

### OTP

* What is the daily OTP?
* How is OTP changing month-to-month?
* Which stations contribute most to delays?
* What are the major delay categories?
* How much delay is controllable?
* Which delay codes contribute the most delay minutes?
* How does arrival OTP compare with departure OTP?
* How does OTP vary across operational zones?

### Ground Time

* How frequently does actual ground time exceed scheduled ground time?
* What percentage of flights operate below scheduled ground time?
* Which stations have higher AGT relative to SGT?
* How does ground-time performance change month-to-month?
* How does ground-time performance differ by station class?
* Where are potential turnaround-performance issues concentrated?

---

# Business Use Cases

These datasets can support airline operational functions such as:

* Daily Operations Control
* OTP monitoring
* Delay monitoring
* Turnaround monitoring
* Station performance monitoring
* Operational KPI reporting
* Delay root-cause analysis
* Aircraft rotation analysis
* Operational planning
* Performance dashboards
* Historical trend analysis

The resulting CSV datasets can also be connected to BI tools such as Power BI for visualization and reporting.

---

# Running the Project

## 1. Install Dependencies

```bash
pip install pandas numpy
```

Or install from:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```text
pandas
numpy
```

---

## 2. Prepare Input Data

Place the required CSV files into their corresponding input directories.

For example:

```text
input/
├── otp_pandas_try.csv
├── delco_data_try.csv
└── station_db.csv
```

and:

```text
input_try/
├── pyActGt_try.csv
└── station_db.csv
```

---

## 3. Run the Scripts

Run the OTP module:

```bash
python otp_analysis.py
```

Run the Ground Time module:

```bash
python ground_time_analysis.py
```

The generated datasets will be written to the `output/` directory.

---

# Data Flow Between Modules

Although OTP and Ground Time are separate analytical processes, they use related operational flight information.

```text
                    Flight Operation Data
                            │
             ┌──────────────┴──────────────┐
             │                             │
             ▼                             ▼
       OTP Analysis                 Ground Time Analysis
             │                             │
             ▼                             ▼
      OTP / Delay KPIs              SGT / AGT KPIs
             │                             │
             └──────────────┬──────────────┘
                            │
                            ▼
                   Operational Analytics
                            │
                            ▼
                     BI / Reporting
```

Together, these modules provide two different views of airline operational performance:

```text
OTP
│
└── Did the flight operate on time?

Ground Time
│
└── Did the aircraft spend the expected amount
    of time on the ground between flights?
```

---

# Data Quality & Validation Considerations

Because these pipelines depend on operational flight data, the quality of the input data can directly affect the resulting KPIs.

Important validation areas include:

* Missing timestamps
* Invalid flight records
* Incorrect station codes
* Missing aircraft registration
* Incorrect delay values
* Duplicate flight records
* Inconsistent date/time formats
* Missing delay-code mappings
* Missing station-reference mappings
* Aircraft rotation sequencing

For Ground Time analysis, the sequence of flights for each aircraft is particularly important because the SGT and AGT calculations depend on aircraft rotation order.

---

# Current Limitations

The current implementation is designed around a specific airline operational data structure.

Users adapting the project to another airline or data source may need to modify:

* Column names
* Input filenames
* Flight validation rules
* OTP threshold
* Delay-code mapping
* Station reference structure
* Aircraft rotation logic
* Ground-time business rules
* Aggregation requirements

The current OTP implementation uses a **15-minute threshold** for OTP classification.

The Ground Time implementation uses the project's existing SGT/AGT business logic and aircraft rotation methodology.

---

# Future Improvements

Potential improvements include:

* [ ] Separate configuration from processing logic
* [ ] Move input/output paths into configuration files
* [ ] Modularize repeated transformation logic
* [ ] Add automated data-quality validation
* [ ] Add logging
* [ ] Add exception handling
* [ ] Add unit tests
* [ ] Add database connectivity
* [ ] Add automated ETL scheduling
* [ ] Add automated failure notifications
* [ ] Add incremental processing
* [ ] Add Power BI integration
* [ ] Add data dictionary
* [ ] Add sample/anonymized datasets
* [ ] Add pipeline documentation
* [ ] Containerize the ETL environment

---

# Project Purpose

This project demonstrates the use of Python and data-engineering techniques to transform airline operational data into structured analytical datasets.

Rather than treating the operational data as a single reporting table, the project separates different operational questions into analytical pipelines:

```text
Flight Operations
       │
       ├───────────────┐
       │               │
       ▼               ▼
     OTP            Ground Time
       │               │
       ▼               ▼
    Delays          SGT vs AGT
       │               │
       └───────┬───────┘
               ▼
      Operational Analytics
```

The resulting datasets can be used as a foundation for **operational reporting, KPI monitoring, BI dashboards, statistical analysis, and future data-science initiatives**.
