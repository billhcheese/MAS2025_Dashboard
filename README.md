# Metro Atlanta Speaks (MAS) 2025 Dashboard

An interactive Streamlit dashboard for exploring the Metro Atlanta Speaks Survey results. This dashboard provides comprehensive visualizations and insights from the region's largest survey of perceptions and attitudes.

## Overview

The Metro Atlanta Speaks Survey is conducted by the Atlanta Regional Commission (ARC) in collaboration with Kennesaw State University's A.L. Burruss Institute of Public Service & Research. Since 2013, this survey has been taking the pulse of metro Atlanta residents to inform the region's planning and decision-making.

This dashboard allows users to:
- Explore regional survey trends over time
- Analyze responses by demographic groups
- View key findings on topics including transportation, housing, economy, workforce, and quality of life
- Compare responses across different demographic segments

## Features

### 📊 Metro Summary Dashboard
- Regional-level survey results with interactive visualizations
- Year-over-year trend analysis
- Explore responses to questions about:
  - Housing affordability
  - Transportation and traffic solutions
  - Economic conditions
  - Workforce development
  - Artificial Intelligence impact
  - Climate change
  - Quality of life

### 👥 Demographic Breakdown
- Analyze survey responses by demographic groups including:
  - Gender
  - Race/Ethnicity
  - Age groups
  - Income levels
  - Education levels
  - Home ownership status
  - Geographic location (county level)
- Compare responses across different demographic segments

### ❓ FAQ
- Comprehensive answers to common questions about the survey methodology
- Information about survey coverage and statistical significance
- Contact information for additional inquiries

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup

1. Clone or download this repository

2. Navigate to the Streamlit_App directory:
   ```bash
   cd Streamlit_App
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To launch the dashboard locally:

```bash
streamlit run MAS25_app.py
```

The application will open in your default web browser at `http://localhost:8501`

## Project Structure

```
Streamlit_App/
├── MAS25_app.py              # Main application entry point
├── Metro_Summary.py           # Regional summary dashboard page
├── Demographic_Breakdown.py   # Demographic analysis page
├── FAQ.py                     # Frequently asked questions page
├── requirements.txt           # Python package dependencies
├── Assets/                    # Image and logo files
│   ├── metro-atl-speaks.svg
│   ├── logo-with-text.svg
│   └── Fw_ltnUt_400x400.png
└── Data/                      # Survey data files
    └── MAS_Dashboard_Records_2025_Updated.parquet
```

## Data

The dashboard uses survey data stored in Parquet format for optimal performance:
- **File**: `Data/MAS_Dashboard_Records_2025_Updated.parquet`
- **Format**: Apache Parquet
- **Content**: Cleaned and processed survey responses from multiple years

## Dependencies

- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **altair**: Interactive visualization library

See `requirements.txt` for specific version information.

## Survey Coverage

The dashboard includes survey data from the following years:
- 2016, 2017, 2018, 2019, 2020, 2021, 2023, 2024, 2025

**Note**: The survey was not conducted in 2022.

The survey covers the 11 counties of the Atlanta Regional Commission area plus the City of Atlanta.

## Statistical Significance

- Regional results: Margin of error (MOE) under 2%, typically under 1.5%
- Core counties and City of Atlanta: MOE ranges from 3% to 5%
- Smaller suburban/exurban counties: MOE ranges from 5% to 7%

## Usage Tips

1. **Downloading Graphics**: Hover over any chart and click the "..." menu to download visualizations
2. **Exploring Data**: Use dropdown menus to filter by question, year, and demographic groups
3. **Year Comparison**: Note that not all questions were asked every year
4. **Sample Sizes**: Some demographic groups may not be displayed if sample sizes are too small for statistical confidence

## Contact

For questions about the survey or dashboard:
- **Contact**: Bill Huang
- **Email**: bhuang@atlantaregional.org
- **Website**: [Metro Atlanta Speaks Survey](https://atlantaregional.org/what-we-do/research-and-data/metro-atlanta-speaks-survey-report/)

## About ARC

The Atlanta Regional Commission (ARC) is the regional planning and intergovernmental coordination agency for the 11-county Atlanta metropolitan area. ARC works to promote a more livable region through planning, funding, and facilitating programs in areas such as transportation, environmental quality, aging services, and workforce development.

## License

While we encourage all to make use of ARC published data, do note the Creative Commons Attribution 4.0 International license agreement. In short, users are free to use data provided the source is credited.

This is a human-readable summary of (and not a substitute for) the full license and disclaimer.

You are free to:

Share — copy and redistribute the material in any medium or format
Adapt — remix, transform, and build upon the material for any purpose, even commercially.
Provided these terms are met:

Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
Please see best practices for attribution that may prove useful.

No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

Notices:
You do not have to comply with the license for elements of the material in the public domain or where your use is permitted by an applicable exception of limitation. 

Disclaimer:
No warranties are given. The license may not give you all of the permissions necessary for your intended use. For example, other rights such as publicity, privacy, or moral rights may limit how you use the material.

---

*Dashboard developed for the Atlanta Regional Commission*

