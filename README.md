# Blockhouse Task

## Overview

This repository contains the implementation task required as part of the application process for Blockhouse.

## Technologies Used

- Python
- Django
- PostgreSQL
- Docker
- GitHub Actions

## Setup

### 1. Clone the Repository

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a .env file in the root directory of the project and add your Alpha Vantage

```
API_KEY=YOUR_ALPHA_VANTAGE_API_KEY
```

### 4. Set Up PostgreSQL Database with Docker

Run the following Docker command to start a PostgreSQL database:

```
docker run --name blockhouse \
    -e POSTGRES_USER=admin \
    -e POSTGRES_PASSWORD=muilyang \
    -e POSTGRES_DB=muilyang \
    -p 5432:5432 \
    -d postgres
```

### 5. Apply Database Migrations and Run the Application

Once the PostgreSQL database is up and running, apply the migrations and run the application. The server will run at http://127.0.0.1:8000/.

```
python manage.py migrate
python manage.py runserver
```

## API Documentation

### 1. Add Stock

- Endpoint: POST /financial/add-stock/
- Request Body Example:

```
{
  "symbol": "IBM"
}
```

### 2. Backtest

- Endpoint: POST /financial/backtest/
- Request Body Example:

```
{
  "symbol": "IBM",
  "investmentAmount": 100000,
  "buyMovingAverage": 50,
  "sellMovingAverage": 200
}
```

### 3. Predict

- Endpoint: POST /financial/predict/
- Request Body Example:

```
{
  "symbol": "IBM"
}
```

### 4. Backtest with Report

- Endpoint: POST /financial/backtest-with-report/
- Request Body Example:

```
{
  "symbol": "IBM",
  "investmentAmount": 100000,
  "buyMovingAverage": 50,
  "sellMovingAverage": 200
}
```

### 5. Predict with Report

- Endpoint: POST /financial/predict-with-report/
- Request Body Example:

```
{
  "symbol": "IBM"
}
```
