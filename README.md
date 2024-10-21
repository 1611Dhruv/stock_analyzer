# Financial Data Analysis Platform

## Overview

This Django application serves as a comprehensive financial data analysis platform. It offers functionalities for fetching and analyzing stock data, backtesting trading strategies, and leveraging machine learning for price predictions.

## Features

- Historical stock data retrieval from Alpha Vantage API
- PostgreSQL database for data storage
- Backtesting of simple buy/sell strategies
- Integration of a pre-trained machine learning model for stock price prediction
- Comprehensive report generation

## Prerequisites

- Python 3.x
- pip
- git

## Installation

1. Clone the repository:

   ```bash
   git clone https://[your-repository-url]
   ```

2. Set up the environment variables:
   Create a `.env` file in the project root with the following contents:

   ```
   ALPHA_VANTAGE_API_KEY=[your_api_key]
   DB_URL=[your_psql_database_url]
   DB_USER=[your_psql_username]
   DB_PASSWORD=[your_psql_password]
   ```

3. Install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

## Running the Application

Start the development server:

```bash
python manage.py runserver
```

## API Endpoints

### Financial Data

- `POST /financial_data/add`

  - Add a new stock symbol
  - Expects `symbol` in the request body

- `POST /financial_data/refresh`

  - Refresh data for existing symbols

- `GET /financial_data/data`

  - List available symbols

- `GET /financial_data/data?symbol=<symbol>`
  - Get data for a specific symbol

### Backtesting

- `GET /back_test?format=<pdf|json>&symbol=<symbol>&winsell=<sell_threshold>&winbuy=<buy_threshold>&amt=<initial_amt>`
  - Perform backtesting with specified parameters

### AI Prediction

- `GET /ai_prediction?symbol=<symbol>`
  - Get predicted prices for a symbol

### Reporting

- Access the reporting interface at `/reporting/`
