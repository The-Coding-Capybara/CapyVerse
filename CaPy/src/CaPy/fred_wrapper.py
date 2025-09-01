import pandas as pd
import requests
from fredapi import Fred
from typing import List

def fetch_fred_series(
        tickers: List[str],
        start_date: str,
        end_date: str,
        api_key: str
) -> pd.DataFrame:
    """
    Fetch multiple FRED time series and return as a DataFrame.

    Parameters:
        tickers (List[str]): List of FRED series IDs.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        api_key (str): Your FRED API key.

    Returns:
        pd.DataFrame: DataFrame with dates as index and each ticker as a column.
    """
    base_url = "https://api.stlouisfed.org/fred/series/observations"
    df_all = pd.DataFrame()

    for ticker in tickers:
        params = {
            'series_id': ticker,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': start_date,
            'observation_end': end_date,
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()['observations']
        dates = [obs['date'] for obs in data]
        values = [float(obs['value']) if obs['value'] != '.' else None for obs in data]

        df = pd.DataFrame({ticker: values}, index=pd.to_datetime(dates))
        df_all = pd.concat([df_all, df], axis=1)

    return df_all.sort_index()
