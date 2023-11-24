from pathlib import Path
from typing import Union

import pandas as pd


def preprocess_gas_prices(
    data_gas_prices: pd.DataFrame,
) -> pd.DataFrame:
    """Read gas prices.

    Parameters
    ----------
    data_gas_prices : pd.DataFrame

    Returns
    -------
    data_gas_prices : pd.DataFrame

    Examples
    --------
    >>> from kaggle_enefit.data.preprocessing.data_price import preprocess_gas_prices
    >>> data_gas_prices = pd.DataFrame(
    ...     {
    ...         "forecast_date": ["2020-01-01", "2020-01-02"],
    ...         "origin_date": ["2020-01-01", "2020-01-02"],
    ...         "gas_price": [0, 1],
    ...     }
    ... )
    >>> preprocess_gas_prices(
    ...     data_gas_prices=data_gas_prices,
    ... )
        date_forecast_gas_prices    origin_date  gas_price
    0                 2020-01-01     2020-01-01          0
    1                 2020-01-02     2020-01-02          1
    """
    # delete `data_block_id`
    if "data_block_id" in data_gas_prices.columns:
        data_gas_prices = data_gas_prices.drop(
            columns=["data_block_id"]
        )

    data_gas_prices = (
        data_gas_prices
        # assign `date_adjusted`
        .assign(
            **{
                "date_adjusted": lambda d: pd.to_datetime(
                    pd.to_datetime(d["forecast_date"]) + pd.DateOffset(days=1)
                ).dt.date,
            }
        )
        # astype [train, test]
        .assign(
            **{
                "lowest_price_per_mwh": lambda d: d["lowest_price_per_mwh"].astype('float32'),
                "highest_price_per_mwh": lambda d: d["highest_price_per_mwh"].astype('float32'),
            }
        )
        # delete `forecast_date, origin_date`
        .drop(columns=["forecast_date", "origin_date"])
        # rename `lowest_price_per_mwh, highest_price_per_mwh`
        .rename(columns={
            "lowest_price_per_mwh": "lowest_gas_price_per_mwh",
            "highest_price_per_mwh": "highest_gas_price_per_mwh"
        })
    )

    return data_gas_prices


def preprocess_electricity_prices(
    data_electricity_prices: Union[str, Path],
) -> pd.DataFrame:
    """Preprocess electricity prices.

    Parameters
    ----------
    data_electricity_prices : pd.DataFrame

    Returns
    -------
    data_electricity_prices : pd.DataFrame

    Examples
    --------
    >>> from kaggle_enefit.data.preprocessing.data_price import preprocess_electricity_prices
    >>> data_electricity_prices = preprocess_electricity_prices(data_electricity_prices)
    """
    # delete `data_block_id`
    if "data_block_id" in data_electricity_prices.columns:
        data_electricity_prices = data_electricity_prices.drop(
            columns=["data_block_id"]
        )

    data_electricity_prices = (
        data_electricity_prices
        # assign `date_adjusted, hour`
        .assign(
            **{
                "date_adjusted": lambda d: pd.to_datetime(
                    pd.to_datetime(d["forecast_date"]) + pd.DateOffset(days=1)
                ).dt.date,
                "hour": lambda d: pd.to_datetime(d["forecast_date"]).dt.hour,
            }
        )
        # astype [train, test]
        .assign(
            **{
                "euros_per_mwh": lambda d: d["euros_per_mwh"].astype('float64'),
            }
        )
        # delete `forecast_date, origin_date`
        .drop(columns=["forecast_date", "origin_date"])
        # rename `euros_per_mwh`
        .rename(columns={
            "euros_per_mwh": "electricity_euros_per_mwh"
        })
    )

    return data_electricity_prices