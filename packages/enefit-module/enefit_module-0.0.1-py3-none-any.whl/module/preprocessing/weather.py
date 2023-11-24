import numpy as np
import pandas as pd
# from tqdm.autonotebook import tqdm

from .location import create_positional_columns, calculate_positional_columns

def _make_county_col(
    data: pd.DataFrame,
    num: int
) -> pd.DataFrame:
    """return county dataFrame.

    Parameters
    ----------
    data : pd.DataFrame
    num : int

    Returns
    -------
    data : pd.DataFrame
        DataFrame with county.
    """
    temp = data.copy()
    temp['county'] = num
    return temp

def make_forecast_weather_interpolate(
    county_position: pd.DataFrame,
    data_forecast_weather: pd.DataFrame
) -> pd.DataFrame:
    """return county*all_datetime dataFrame.

    Parameters
    ----------
    county_position: pd.DataFrame,
    data_forecast_weather: pd.DataFrame

    Returns
    -------
    data : pd.DataFrame
        DataFrame with county.
    """

    # fill NaN in forecast_weather
    data_forecast_weather = (
        data_forecast_weather
        .assign(
            **{
                "surface_solar_radiation_downwards": lambda d: d.groupby(
                    ['latitude','longitude'],
                    group_keys=False
                ).surface_solar_radiation_downwards.apply(
                    lambda x:x.interpolate()
                )
            }
        )
        
    )
    # create init of forecaste DateFrame
    fore_info = (
        data_forecast_weather
        .groupby(
            ['date_adjusted','hour_adjusted','hours_ahead']
        ).last().reset_index()[
            ['hours_ahead',
            'date_adjusted',
            'hour_adjusted',
            'origin_datetime',
            'forecast_datetime_adjusted',
            'origin_date_adjusted']
        ]
    )
    # make forecast info for county
    for county_num in range(len(county_position)):
        temp=_make_county_col(fore_info, county_num)
        if county_num == 0:
            fore_info_0=temp.copy()
        else:
            fore_info_0=pd.concat([fore_info_0,temp])

    fore_columns=[
        '10_metre_u_wind_component',
        '10_metre_v_wind_component',
        'temperature',
        'dewpoint',
        'cloudcover_high',
        'cloudcover_low',
        'cloudcover_mid',
        'cloudcover_total',
        'direct_solar_radiation',
        'surface_solar_radiation_downwards',
        'snowfall',
        'total_precipitation'
    ]

    # merge county info with forecast info
    fore_info_0 = (
        pd.merge(
            fore_info_0,
            county_position,
            on='county',
            how='left'
        )
        .drop(columns=['county_name','latitude','longitude'])
        .pipe(create_positional_columns, data_forecast_weather, fore_columns, option='forecast')
        .pipe(calculate_positional_columns, fore_columns)
        .drop(
            columns=[
                'l_top_long',
                'l_top_lat',
                'l_bottom_long',
                'l_bottom_lat',
                'r_top_long',
                'r_top_lat',
                'r_bottom_lat',
                'r_bottom_long',
                'l_top_dist',
                'r_top_dist',
                'l_bottom_dist',
                'r_bottom_dist',
                'origin_datetime'
            ]
        )
    )
    
    return fore_info_0

def make_historical_weather_interpolate(
    county_position: pd.DataFrame,
    data_historical_weather: pd.DataFrame
) -> pd.DataFrame:
    """return county*all_datetime dataFrame.

    Parameters
    ----------
    county_position: pd.DataFrame,
    data_historical_weather: pd.DataFrame

    Returns
    -------
    data : pd.DataFrame
        DataFrame with county.
    """

    # make dataframe with ['datetime'] in historical_weather
    his_info=data_historical_weather.groupby(['date','hour','datetime']).last().reset_index()[['date','hour','datetime']]
    
    # make historical info for county
    for county_num in range(len(county_position)):
        temp=_make_county_col(his_info, county_num)
        if county_num == 0:
            hist_info_0=temp.copy()
        else:
            hist_info_0=pd.concat([hist_info_0,temp])

    hist_columns=[
        'temperature',
        'dewpoint',
        'rain',
        'snowfall',
        'surface_pressure',
        'cloudcover_total',
        'cloudcover_low',
        'cloudcover_mid',
        'cloudcover_high',
        'windspeed_10m',
        'winddirection_10m',
        'shortwave_radiation',
        'direct_solar_radiation',
        'diffuse_radiation'
    ]

    # merge county info with historical info
    hist_info_0 = (
        pd.merge(
            hist_info_0,
            county_position,
            on='county',
            how='left'
        )
        .drop(columns=['county_name','latitude','longitude'])
        .pipe(create_positional_columns, data_historical_weather, hist_columns)
        .pipe(calculate_positional_columns, hist_columns)
        .drop(
            columns=[
                'l_top_long',
                'l_top_lat',
                'l_bottom_long',
                'l_bottom_lat',
                'r_top_long',
                'r_top_lat',
                'r_bottom_lat',
                'r_bottom_long',
                'l_top_dist',
                'r_top_dist',
                'l_bottom_dist',
                'r_bottom_dist'
            ]
        )
    )
    
    return hist_info_0

