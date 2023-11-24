from typing import List, Optional

import numpy as np
import pandas as pd

# from tqdm.autonotebook import tqdm

def county_positioning(
    weather_data: pd.DataFrame,
) -> pd.DataFrame:
    """Assign location to each county.

    Parameters
    ----------
    weather_data : pd.DataFrame

    Returns
    -------
    data : pd.DataFrame
        DataFrame with location assigned to each county.
    """
    # location is from google map (manually)
    name_to_location_map = {
        "HARJUMAA": [59.37564599072755, 24.76634160396904],
        "HIIUMAA": [58.933990104765385, 22.592611630193417],
        "IDA-VIRUMAA": [59.260027110999104, 27.424623084957503],
        "JÄRVAMAA": [58.93141428698745, 25.61492605120901],
        "JÕGEVAMAA": [58.75129581441412, 26.396217935199086],
        "LÄÄNE-VIRUMAA": [59.351855094338006, 26.358582291361408],
        "LÄÄNEMAA": [58.971844103963996, 23.865264807862204],
        "PÄRNUMAA": [58.529730512924466, 24.390625023202976],
        "PÕLVAMAA": [58.115278626639046, 27.210355429168683],
        "RAPLAMAA": [59.001783512075306, 24.800546663034282],
        "SAAREMAA": [58.40187275691764, 22.473957776666857],
        "TARTUMAA": [58.38464096871995, 26.742185601931066],
        "UNKNOWN": [58.65, 24.95], # "UNKNOWN" 지역 : 가운데 값 사용
        "VALGAMAA": [57.910997459035016, 26.161956297267043],
        "VILJANDIMAA": [58.362156921790586, 25.589748513576247],
        "VÕRUMAA": [57.84391746680313, 27.00999868536037],
    }
    # create county info dataFrame
    county_info=pd.DataFrame()
    for idx, (county, region_coord) in enumerate(name_to_location_map.items()):
        temp = pd.DataFrame({'county' : [idx],'county_name' : [county], 'latitude' : [region_coord[0]], 'longitude' : [region_coord[1]]})
        county_info = pd.concat([county_info,temp], axis = 0)

    county_info = (
        county_info
        .pipe(county_latitude_generator, weather_data)
        .pipe(county_longitude_generator, weather_data)
        # assign 4 position
        .assign(
            **{
                "l_top_long": lambda d: d["left_longitude"],
                "l_top_lat": lambda d: d["top_latitude"],
                "r_top_long": lambda d: d["right_longitude"],
                "r_top_lat": lambda d: d["top_latitude"],
                "l_bottom_long": lambda d: d["left_longitude"],
                "l_bottom_lat": lambda d: d["bottom_latitude"],
                "r_bottom_long": lambda d: d["right_longitude"],
                "r_bottom_lat": lambda d: d["bottom_latitude"],
            }
        )
        # assign 4 position distance
        .assign(
            **{
                "l_top_dist": lambda d: (
                    (d["top_latitude"]+d["latitude"])**2+
                    (d["left_longitude"]+d["longitude"])**2
                )**0.5,
                "r_top_dist": lambda d: (
                    (d["top_latitude"]+d["latitude"])**2+
                    (d["right_longitude"]+d["longitude"])**2
                )**0.5,
                "l_bottom_dist": lambda d: (
                    (d["bottom_latitude"]+d["latitude"])**2+
                    (d["left_longitude"]+d["longitude"])**2
                )**0.5,
                "r_bottom_dist": lambda d: (
                    (d["bottom_latitude"]+d["latitude"])**2+
                    (d["right_longitude"]+d["longitude"])**2
                )**0.5,
            }
        )
        # drop unnecessary columns
        .drop(columns=['bottom_latitude','top_latitude','left_longitude','right_longitude'])
        .reset_index(drop=True)
    )

    return county_info

def county_latitude_generator(
    county_info: pd.DataFrame,
    weather_data: pd.DataFrame,
) -> pd.DataFrame:
    """Generate latitude location to each county.

    Parameters
    ----------
    county_info : pd.DataFrame
    weather_data : pd.DataFrame

    Returns
    -------
    data : pd.DataFrame
        DataFrame with county add latitude data.
    """
    # 4점의 latitude 매칭
    latitudes=pd.DataFrame(weather_data.groupby('latitude').first().index)
    latitudes['latitude_copy']=latitudes.latitude

    county_info = (
        pd.merge_asof(
            county_info.sort_values('latitude'),
            latitudes.rename(columns={'latitude_copy':'bottom_latitude'}), 
            on='latitude'
        )
    )
    county_info = (
        pd.merge_asof(
            county_info.sort_values('latitude'),
            latitudes.rename(columns={'latitude_copy':'top_latitude'}),
            on='latitude',
            direction='forward'
        )
    )
    return county_info

def county_longitude_generator(
    county_info: pd.DataFrame,
    weather_data: pd.DataFrame,
) -> pd.DataFrame:
    """Generate longitude location to each county.

    Parameters
    ----------
    county_info : pd.DataFrame
    weather_data : pd.DataFrame

    Returns
    -------
    data : pd.DataFrame
        DataFrame with county add longitude data.
    """
    # 4점의 longitude 매칭
    longitudes=pd.DataFrame(weather_data.groupby('longitude').first().index)
    longitudes['longitude_copy']=longitudes.longitude

    county_info = (
        pd.merge_asof(
            county_info.sort_values('longitude'),
            longitudes.rename(columns={'longitude_copy':'left_longitude'}), 
            on='longitude'
        )
    )
    county_info = (
        pd.merge_asof(
            county_info.sort_values('longitude'),
            longitudes.rename(columns={'longitude_copy':'right_longitude'}),
            on='longitude',
            direction='forward'
        )
    )
    return county_info

def create_positional_columns(
    weather_info: pd.DataFrame,
    data_weather: pd.DataFrame,
    weather_columns: List,
    option: Optional[str]= None,
) -> pd.DataFrame:
    """Generate longitude location to each county.

    Parameters
    ----------
    weather_info : pd.DataFrame
    data_weather: pd.DataFrame
    weather_columns : List
    option: Optional['forecast']

    Returns
    -------
    data : pd.DataFrame
        DataFrame with created positional columns data.
    """
    position_columns=[
        'l_top_',
        'r_top_',
        'l_bottom_',
        'r_bottom_',
    ]
    # print("==== creating weather position data ====")
    # for col in tqdm(weather_columns):
    for col in weather_columns:
        for pos in (position_columns):
            if option == 'forecast':
                data_weather_col = [col,'origin_datetime','latitude','longitude','date_adjusted','hour_adjusted']
                merge_on = [f'{pos}lat',f'{pos}long','date_adjusted','hour_adjusted','origin_datetime']
            else:
                data_weather_col = [col,'datetime','latitude','longitude','date','hour']
                merge_on = [f'{pos}lat',f'{pos}long','date','hour','datetime']
            weather_info = (
                # create positional columns
                pd.merge(
                    weather_info,
                    data_weather[data_weather_col].rename(
                    columns={
                        'latitude': f'{pos}lat',
                        'longitude': f'{pos}long',
                        col: f'{pos}{col}'
                    }
                ),
                on=merge_on,
                how='left'
                )
            )

    return weather_info

def calculate_positional_columns(
    weather_info: pd.DataFrame,
    weather_columns: List,
) -> pd.DataFrame:
    """Generate longitude location to each county.

    Parameters
    ----------
    weather_info : pd.DataFrame
    weather_columns : List

    Returns
    -------
    data : pd.DataFrame
        DataFrame with created positional columns data.
    """
    for col in weather_columns:
        # calculate the weather value
        weather_info[col]=(
            (weather_info['l_top_'+col]/weather_info['l_top_dist'])+
            (weather_info['r_top_'+col]/weather_info['r_top_dist'])+
            (weather_info['l_bottom_'+col]/weather_info['l_bottom_dist'])+
            (weather_info['r_bottom_'+col]/weather_info['r_bottom_dist'])
        ) / (
            (1/weather_info['l_top_dist'])+
            (1/weather_info['r_top_dist'])+
            (1/weather_info['l_bottom_dist'])+
            (1/weather_info['r_bottom_dist'])
        )
        # drop calculated weather value
        weather_info = (
            weather_info
            .drop(
                columns=['l_top_'+col,
                    'r_top_'+col,
                    'l_bottom_'+col,
                    'r_bottom_'+col
                ]
            )
        )

    return weather_info