from typing import Optional

import pandas as pd

from .location import county_positioning
from .weather import make_historical_weather_interpolate, make_forecast_weather_interpolate

def preprocess_historical_weather(
    data_historical_weather: pd.DataFrame,
    option: Optional[str]= None
) -> pd.DataFrame:
    """Preprocess historical weather data.

    Parameters
    ----------
    data_historical_weather : pd.DataFrame
    option : Optional['insert_county']

    Returns
    -------
    data_historical_weather : pd.DataFrame

    Examples
    --------
    >>> from kaggle_enefit.data.preprocessing.data_weather import preprocess_historical_weather
    >>> data_historical_weather = preprocess_historical_weather(
    ...     data_historical_weather=data_historical_weather,
    ...     option=None
    ... )
    """
    # delete `data_block_id`
    if "data_block_id" in data_historical_weather.columns:
        data_historical_weather = data_historical_weather.drop(
            columns=["data_block_id"]
        )
        
    data_historical_weather = (
        data_historical_weather
        # assign `datetime, date, hour`
        .assign(
            **{
                "datetime": lambda d: pd.to_datetime(d["datetime"]),
                "date": lambda d: d["datetime"].dt.date,
                "hour": lambda d: d["datetime"].dt.hour,
            }
        )
        # astype [train, test]
        .assign(
            **{
                "temperature": lambda d: d["temperature"].astype('float64'),
                "dewpoint": lambda d: d["dewpoint"].astype('float64'),
                "rain": lambda d: d["rain"].astype('float64'),
                "snowfall": lambda d: d["snowfall"].astype('float64'),
                "surface_pressure": lambda d: d["surface_pressure"].astype('float64'),
                "cloudcover_total": lambda d: d["cloudcover_total"].astype('float64'),
                "cloudcover_low": lambda d: d["cloudcover_low"].astype('float64'),
                "cloudcover_mid": lambda d: d["cloudcover_mid"].astype('float64'),
                "cloudcover_high": lambda d: d["cloudcover_high"].astype('float64'),
                "windspeed_10m": lambda d: d["windspeed_10m"].astype('float64'),
                "winddirection_10m": lambda d: d["winddirection_10m"].astype('float64'),
                "shortwave_radiation": lambda d: d["shortwave_radiation"].astype('float64'),
                "direct_solar_radiation": lambda d: d["direct_solar_radiation"].astype('float64'),
                "diffuse_radiation": lambda d: d["diffuse_radiation"].astype('float64'),
                "latitude": lambda d: d["latitude"].astype('float64'),
                "longitude": lambda d: d["longitude"].astype('float64'),
            }
        )
    )

    # merge to county
    if option == 'insert_county':
        data_historical_weather = (
            data_historical_weather
            .pipe(county_positioning)
            .pipe(make_historical_weather_interpolate, data_historical_weather)
        )


    return data_historical_weather


def preprocess_forecast_weather(
    data_forecast_weather: pd.DataFrame,
    option: Optional[str] = None
) -> pd.DataFrame:
    """Preprocess forecast weather data.

    Parameters
    ----------
    data_forecast_weather : pd.DataFrame
    option : Optional['insert_county']

    Returns
    -------
    data_forecast_weather : pd.DataFrame

    Examples
    --------
    >>> from kaggle_enefit.data.preprocessing.data_weather import preprocess_forecast_weather
    >>> data_forecast_weather = preprocess_forecast_weather(data_forecast_weather)
    """
    # delete `data_block_id`
    if "data_block_id" in data_forecast_weather.columns:
        data_forecast_weather = data_forecast_weather.drop(
            columns=["data_block_id"]
        )

    data_forecast_weather = (
        data_forecast_weather
        # assign `forecast_datetime_adjusted, date_adjusted, hour_adjusted, origin_datetime_adjusted, origin_date_adjusted`
        .assign(
            **{
                "forecast_datetime_adjusted": lambda d:
                    pd.to_datetime(d["forecast_datetime"]) + pd.DateOffset(hours=2),
                "date_adjusted": lambda d: d["forecast_datetime_adjusted"].dt.date,
                "hour_adjusted": lambda d: d["forecast_datetime_adjusted"].dt.hour,
                "origin_datetime_adjusted": lambda d:
                    pd.to_datetime(d["origin_datetime"]) + pd.DateOffset(days=1),
                "origin_date_adjusted": lambda d: d["origin_datetime_adjusted"].dt.date,
            }
        )
        # astype [train, test]
        .assign(
            **{
                "temperature": lambda d: d["temperature"].astype('float64'),
                "dewpoint": lambda d: d["dewpoint"].astype('float64'),
                "cloudcover_high": lambda d: d["cloudcover_high"].astype('float64'),
                "cloudcover_low": lambda d: d["cloudcover_low"].astype('float64'),
                "cloudcover_mid": lambda d: d["cloudcover_mid"].astype('float64'),
                "cloudcover_total": lambda d: d["cloudcover_total"].astype('float64'),
                "10_metre_u_wind_component": lambda d: d["10_metre_u_wind_component"].astype('float64'),
                "10_metre_v_wind_component": lambda d: d["10_metre_v_wind_component"].astype('float64'),
                "direct_solar_radiation": lambda d: d["direct_solar_radiation"].astype('float64'),
                "surface_solar_radiation_downwards": lambda d: d["surface_solar_radiation_downwards"].astype('float64'),
                "snowfall": lambda d: d["snowfall"].astype('float64'),
                "total_precipitation": lambda d: d["total_precipitation"].astype('float64'),
                "hours_ahead": lambda d: d["hours_ahead"].astype('int8'),
                "latitude": lambda d: d["latitude"].astype('float64'),
                "longitude": lambda d: d["longitude"].astype('float64'),
            }
        )
        # delete `forecast_datetime, origin_datetime_adjusted`
        .drop(columns=["forecast_datetime", "origin_datetime_adjusted"])
    )

    # merge to county
    if option == 'insert_county':
        data_forecast_weather = (
            data_forecast_weather
            .pipe(county_positioning)
            .pipe(make_forecast_weather_interpolate, data_forecast_weather)
        )

    return data_forecast_weather