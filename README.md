# 🌍 South Africa Opportunity Monitor

### Exploring youth unemployment, internet access and economic development across Africa

A reproducible **data analytics and visualisation project** built with **Python, Pandas, SQL, Plotly and Streamlit**. The dashboard explores socioeconomic indicators for **South Africa, Botswana, Namibia, Kenya and Nigeria**, helping users compare country-level trends and understand differences in economic context.

> **Data transparency:** The repository includes **synthetic demonstration data** for testing. Its demo values are invented and **must not be interpreted as actual statistics**. Switch to the **Live World Bank API** option in the dashboard, or run `python pipeline.py --real`, to retrieve published indicator data.

## 📊 Dashboard preview

These preview charts were generated with **synthetic demonstration data**:

![Youth unemployment trends — synthetic demo data](reports/youth_unemployment.png)

![Internet access trends — synthetic demo data](reports/internet_access.png)

## 🎯 Project objectives

- Compare youth unemployment trends across five African countries.
- Track access to the internet and examine digital inclusion.
- Explore GDP per capita and overall unemployment indicators.
- Use reproducible data processing and data-quality checks.
- Visualise trends in an interactive dashboard.
- Practice responsible interpretation of official socioeconomic data.

## 🛠️ Technologies

| Technology | Purpose |
|---|---|
| Python | Data processing and automation |
| Pandas & NumPy | Cleaning, validation, transformation and analysis |
| World Bank Indicators API & Requests | Downloading published socioeconomic data |
| Streamlit & Plotly | Interactive dashboard and charts |
| Matplotlib | Report-ready PNG visualisations |
| SQL | Additional exploratory analysis queries |
| Pytest | Automated tests |

## 🌐 Data sources

**Primary source:** [World Bank Indicators API](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392)

| Indicator | World Bank code |
|---|---|
| Youth unemployment (% of labour force ages 15–24; modelled ILO estimate) | `SL.UEM.1524.ZS` |
| Individuals using the internet (% of population) | `IT.NET.USER.ZS` |
| GDP per capita (current US$) | `NY.GDP.PCAP.CD` |
| Total unemployment (% of total labour force; modelled ILO estimate) | `SL.UEM.TOTL.ZS` |

**Countries:** South Africa (`ZAF`), Botswana (`BWA`), Namibia (`NAM`), Kenya (`KEN`) and Nigeria (`NGA`).

The analysis requests **2005–2025**, subject to data availability. Not every country or indicator has a published observation for every year. Published values may be revised by the source.

## 🚀 Installation and usage

**Requirements:** Python 3.10+ and an internet connection for live World Bank data.

### 1. Download the repository

```bash
git clone https://github.com/lemowkay/africa-monitor.git
cd africa-monitor
```

> If the Python files are inside a nested `03-south-africa-opportunity-monitor` folder, `cd` into that folder before running the following commands. Run `dir` (Windows) or `ls` to find the folder containing `pipeline.py` and `requirements.txt`.

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Generate demo analysis and charts

```bash
python pipeline.py --demo
```

Demo mode is offline and creates **fictional** sample observations and output files.

### 4. Launch the interactive dashboard

```bash
python -m streamlit run app.py
```

Open the local URL displayed by Streamlit (usually `http://localhost:8501`). Select **Synthetic demonstration** or **Live World Bank API** in the dashboard sidebar.

### 5. Analyse published World Bank data

```bash
python pipeline.py --real
```

This requires internet access and saves a local copy of the downloaded observations to `data/world_bank_real.csv`. The API may be unavailable or have missing observations.

### 6. Run automated tests

```bash
python -m pytest -q
```

## 📂 Project structure

```text
03-south-africa-opportunity-monitor/
├── app.py                    # Interactive Streamlit dashboard
├── pipeline.py               # Data ingestion, validation, analysis, charts
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── data/
│   └── demo_indicators.csv   # Synthetic example observations
├── outputs/
│   ├── data_quality.csv
│   ├── indicator_observations.csv
│   ├── latest_by_indicator.csv
│   ├── latest_joint_year.csv
│   └── kpis.csv
├── reports/
│   ├── internet_access.png
│   └── youth_unemployment.png
├── sql/
│   └── analysis.sql
└── tests/
    └── test_pipeline.py
```

*Files and folders shown are relative to the Python project directory. Additional `sql_query_*.csv` results may be included when the portfolio's SQL runner is used.*

## 🔎 Analytics workflow

1. **Collect:** Download indicator observations from the World Bank API, or load clearly labelled synthetic data.
2. **Validate:** Check required columns, remove invalid/missing records and handle duplicate country-year-indicator combinations.
3. **Transform:** Convert observations into a tidy table, compute latest-available values, and align shared years where comparisons require it.
4. **Analyse:** Compare historical trajectories, latest observations and country-level patterns.
5. **Visualise:** Export PNG reports and display interactive Streamlit charts.
6. **Test:** Run Pytest checks on demonstration data, API parsing and range validation.

## 📈 Dashboard functionality

- Country multi-select to compare one or several countries.
- Indicator selector for unemployment, internet use or GDP per capita.
- Interactive historical line charts.
- Latest available observation tables.
- Same-year scatter plot for internet use and youth unemployment where matching data is available.
- Data-quality and methodology panel.
- Clear visual labels distinguishing synthetic and live source data.

## ⚠️ Responsible interpretation

- **Synthetic values are not findings:** The included demo charts illustrate functionality only.
- **Different latest years:** Each country and indicator may have a different latest observation date.
- **Different denominators:** Youth unemployment is calculated relative to the youth labour force; internet usage is measured relative to the population.
- **Correlation is not causation:** Country-level association between internet use and youth unemployment does not prove that one causes the other.
- **Current-dollar GDP:** GDP per capita in current US dollars is not inflation-adjusted and is not a measure of real economic growth.
- **Not a job forecast:** These indicators describe broad economic context; they do not measure individual job vacancies or predict employment outcomes.

## 🚧 Future improvements

- Expand coverage to additional African countries.
- Add metadata for indicator release dates and observation gaps.
- Publish a dashboard with live API access.
- Add downloadable filtered results and more SQL-based analyses.
- Develop clear, source-backed insight summaries using real observations.

## 💼 Skills demonstrated

**Data analysis · Data cleaning · Data quality · API integration · Exploratory data analysis · Time-series visualisation · SQL · Dashboard development · Reproducible workflows · Responsible interpretation**

## 📚 Reference

[World Bank — API Basic Call Structures](https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structures)

---

**Portfolio project by [lemowkay](https://github.com/lemowkay)**
