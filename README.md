# What Makes Indonesian Food Commodity Prices Forecastable?

### Evidence from Statistical and Machine Learning Models

## Overview

This project investigates the forecastability of Indonesian food commodity prices using daily price data from the National Strategic Food Price Information Center (PIHPS) from 2021–2025.

The study examines whether commodity-specific time-series characteristics are associated with forecasting performance. Forecastability is evaluated using both a classical statistical model (ARIMA) and a machine learning model (XGBoost).

## Research Questions

* Do Indonesian food commodities differ in their forecastability?
* Which time-series characteristics are associated with forecasting performance?
* How do statistical and machine learning forecasting approaches compare across commodities?
* Is commodity price volatility associated with forecasting difficulty?

## Data

**Source:** National Strategic Food Price Information Center (PIHPS)

**Period:** 2021–2025

**Frequency:** Daily

**Commodities:**

* Rice
* Chicken
* Beef
* Eggs
* Shallots
* Garlic
* Red Chili
* Bird's Eye Chili
* Cooking Oil
* Sugar

## Methodology

### Forecastability Features

For each commodity, the following characteristics were calculated:

* Mean Price
* Standard Deviation (SD)
* Coefficient of Variation (CV)
* Lag-1 Autocorrelation (ACF1)
* Linear Trend

### Forecasting Models

* ARIMA(1,1,1)
* XGBoost

### Evaluation Metric

* Root Mean Squared Error (RMSE)

## Key Findings

* Forecastability varies substantially across commodities.
* XGBoost outperformed ARIMA across all commodities.
* Highly volatile commodities exhibited larger forecasting errors than relatively stable commodities.
* Commodity volatility was positively associated with forecasting error:

  * SD vs RMSE: **r = 0.78**
  * CV vs ARIMA RMSE: **r = 0.72**
  * CV vs XGBoost RMSE: **r = 0.53**
* Autocorrelation and trend showed weak relationships with forecasting performance.

These findings suggest that commodity price variability is an important determinant of forecastability in Indonesian food markets.

## Repository Structure

```text
.
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── forecastability.ipynb
│
├── scripts/
│   └── clean_data.py
│
├── results/
│   ├── figures/
│   └── tables/
│
├── README.md
└── requirements.txt
```

## Installation

```bash
pip install -r requirements.txt
```

## Author

**Firila Najma Wahidah**
Department of Statistics
The University of British Columbia
