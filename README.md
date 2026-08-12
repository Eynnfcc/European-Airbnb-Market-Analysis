# 🏠 European Airbnb Market Analysis

An end-to-end data analytics project analyzing Airbnb listings across major European cities using **Python, SQL, and Power BI**.

The project follows a **Bronze → Silver → Gold data pipeline** to transform raw Airbnb datasets into clean, analysis-ready data and an interactive Power BI dashboard.

---

## 📊 Power BI Dashboard

![European Airbnb Market Dashboard](europe%20airbnb.png)

The dashboard provides an interactive overview of Airbnb pricing and guest experience across European cities.

### Dashboard KPIs

- 💶 Average Price
- 💰 Median Price
- ⭐ Average Guest Satisfaction
- 🏠 Total Listings

### Dashboard Analysis

The dashboard compares:

- Average price by city
- Average price by room type
- Weekday vs weekend pricing
- Different European Airbnb markets

Interactive filters allow analysis by:

- City
- Day Type
- Room Type

---

## 🏙️ Cities Analyzed

The dataset contains Airbnb listings from:

- Amsterdam
- Athens
- Barcelona
- Berlin
- Budapest
- Lisbon
- London
- Paris
- Rome
- Vienna

Each city contains separate **weekday** and **weekend** datasets.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data pipeline and processing |
| Pandas | Data cleaning and transformation |
| SQL | Data querying and analysis |
| Power BI | Data modeling and dashboard development |
| DAX | KPI measures and calculations |
| GitHub | Version control and project documentation |

---

## 🔄 Data Pipeline

The project uses a three-layer data processing architecture:

### 🥉 Bronze Layer — Raw Data Processing

`bronzelayer.py`

The Bronze layer handles the original Airbnb datasets and prepares the raw data for further processing.

The source data contains separate CSV files for each city and day type.

**Input:**

```text
Amsterdam Weekdays
Amsterdam Weekends
Athens Weekdays
Athens Weekends
...
Vienna Weekdays
Vienna Weekends
```

---

### 🥈 Silver Layer — Data Cleaning

`silverlayer.py`

The Silver layer cleans and standardizes the Airbnb data.

Processing includes:

- Loading datasets from multiple European cities
- Identifying the city from each dataset
- Identifying weekday/weekend records
- Removing duplicate records
- Standardizing the datasets
- Combining the data into a master dataset
- Preparing clean data for analysis

---

### 🥇 Gold Layer — Analytics Preparation

`goldlayer.py`

The Gold layer prepares the cleaned data for analytical use.

This layer produces analysis-ready data that can be used for:

- SQL analysis
- KPI calculations
- Business intelligence
- Power BI visualization

---

## 🗄️ SQL Analysis

SQL is used to query the processed Airbnb data and investigate important business questions.

Examples include:

- Which European cities have the highest average Airbnb prices?
- How do average prices differ between cities?
- Are Airbnb listings more expensive on weekends or weekdays?
- Which room types are the most expensive?
- How does pricing vary across different accommodation types?

---

## 📈 Power BI Analysis

The processed data is loaded into Power BI to create an interactive market analysis dashboard.

DAX measures are used to calculate important metrics including:

```text
Average Price
Median Price
Average Guest Satisfaction
Total Listings
```

The dashboard allows users to dynamically filter the analysis and compare different segments of the European Airbnb market.

---

## 💡 Key Insights

The analysis reveals several interesting patterns:

- Amsterdam has one of the highest average Airbnb prices in the analyzed dataset.
- Airbnb pricing differs significantly between European cities.
- Entire homes/apartments have higher average prices than private and shared rooms.
- Weekend and weekday pricing can be compared directly through the dashboard.
- City, room type, and day type filters allow users to investigate individual market segments.

---

## 📁 Project Structure

```text
European-Airbnb-Market-Analysis/
│
├── dataset/
│   ├── amsterdam_weekdays.csv
│   ├── amsterdam_weekends.csv
│   ├── athens_weekdays.csv
│   ├── athens_weekends.csv
│   ├── barcelona_weekdays.csv
│   ├── barcelona_weekends.csv
│   ├── berlin_weekdays.csv
│   ├── berlin_weekends.csv
│   ├── budapest_weekdays.csv
│   ├── budapest_weekends.csv
│   ├── lisbon_weekdays.csv
│   ├── lisbon_weekends.csv
│   ├── london_weekdays.csv
│   ├── london_weekends.csv
│   ├── paris_weekdays.csv
│   ├── paris_weekends.csv
│   ├── rome_weekdays.csv
│   ├── rome_weekends.csv
│   ├── vienna_weekdays.csv
│   └── vienna_weekends.csv
│
├── bronzelayer.py
├── silverlayer.py
├── goldlayer.py
│
├── sql/
│   └── SQL analysis files
│
├── europe airbnb.png
├── Power BI dashboard
└── README.md
```

---

## 🎯 Project Objective

The goal of this project is to demonstrate a complete data analytics workflow:

**Raw Data → Data Engineering → Data Cleaning → SQL Analysis → Data Modeling → Power BI Dashboard**

The project shows how raw datasets from multiple sources can be transformed into useful business insights through a structured analytics pipeline.

---

## 👤 Author

**Eyad Hassan**

Data Analytics Project  
Python • SQL • Power BI
