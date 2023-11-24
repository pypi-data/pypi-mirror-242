from typing import Optional
import pandas as pd

def merge_data(
    train: pd.DataFrame,
    client: pd.DataFrame,
    gas_prices: pd.DataFrame,
    electricity_prices: pd.DataFrame,
    historical_weather: pd.DataFrame,
    forecast_weather: pd.DataFrame,
    revealed_targets: Optional[pd.DataFrame] = None,
    verbose: bool = False,
) -> pd.DataFrame:
    """Merge data.

    Parameters
    ----------
    train : pd.DataFrame
    client : pd.DataFrame
    gas_prices : pd.DataFrame
    electricity_prices : pd.DataFrame
    historical_weather : pd.DataFrame
    forecast_weather : pd.DataFrame
    revealed_targets: Optional[pd.DataFrame] = None
    verbose : bool
        If True, print information about the merging process.

    Returns
    -------
    combined_data : pd.DataFrame
        Merged data.

    Examples
    --------
    >>> from kaggle_enefit.data.preprocessing.data_weather import preprocess_historical_weather
    >>> from kaggle_enefit.data.preprocessing.data_weather import preprocess_forecast_weather
    >>> from kaggle_enefit.data.preprocessing.data_train import preprocess_train
    >>> from kaggle_enefit.data.preprocessing.data_price import (
    ...     preprocess_gas_prices,
    ...     preprocess_electricity_prices,
    ... )
    >>> from kaggle_enefit.data.preprocessing.data_client import preprocess_client
    >>> from kaggle_enefit.data.preprocessing.merge import merge_data
    >>>
    >>> historical_weather = preprocess_historical_weather(historical_weather)
    >>> forecast_weather = preprocess_forecast_weather(forecast_weather)
    >>> train = preprocess_train(
    ...     train,
    ...     forecast_weather,
    ...     county_id_to_name_map,
    ... )
    >>> gas_prices = preprocess_gas_prices(gas_prices)
    >>> electricity_prices = preprocess_electricity_prices(electricity_prices)
    >>> client = preprocess_client(client)
    >>>
    >>> combined_data = merge_data(
        train,
        client,
        gas_prices,
        electricity_prices,
        historical_weather,
        forecast_weather,
        verbose
    ... )
    """
    # ---------------------------------------------------------------------------
    # client
    # ---------------------------------------------------------------------------

    combined_data = (
        # merge client to train
        pd.merge(
            train,
            client,
            left_on=['product_type', "county", "is_business", "date"],
            right_on=['product_type', "county", "is_business", "date_adjusted"],
            how='left'
        )
        # CHECK: eic_count의 경우 앞뒤로 채우고 나면 없는 위치는 0이되어서 삭제 test에서 문제 가능성 있음
        # fillna of eic_count, installed_capacity
        .assign(
            **{
                "eic_count": lambda d: d.groupby(['is_consumption', 'prediction_unit_id'], group_keys=False).eic_count.apply(lambda x: x.bfill()),
                "eic_count": lambda d: d.groupby(['is_consumption', 'prediction_unit_id'], group_keys=False).eic_count.apply(lambda x: x.ffill()),
                "installed_capacity": lambda d: d.groupby(['is_consumption', 'prediction_unit_id'], group_keys=False).eic_count.apply(lambda x: x.bfill()),
                "installed_capacity": lambda d: d.groupby(['is_consumption', 'prediction_unit_id'], group_keys=False).eic_count.apply(lambda x: x.ffill()),
            }
        
        )
        .drop(columns=['date_adjusted'])
    )

    # TODO: test 상태에서 빈거 있다면 제대로 채우기 필요
    combined_data = (
        combined_data
        # fillna(0) `eic_count, installed_capacity`
        .assign(
            **{
                "eic_count": lambda d: d['eic_count'].fillna(0),
                "installed_capacity": lambda d: d['installed_capacity'].fillna(0),
            }
        )
    )

    if verbose:
        print("")
        print("Merged: client")
        print(f"#train obs: {len(train)}  |  #merged obs: {len(combined_data)}")

    # ---------------------------------------------------------------------------
    # gas_prices
    # ---------------------------------------------------------------------------

    combined_data = (
        # merge gas_prices to combined_data
        pd.merge(
            combined_data,
            gas_prices,
            left_on=["date"],
            right_on=["date_adjusted"],
            how='left'
        # delete `date_adjusted`
        ).drop(
            columns=['date_adjusted']
        )
    )

    if verbose:
        print("")
        print("Merged: gas_prices")
        print(f"#train obs: {len(train)}  |  #merged obs: {len(combined_data)}")

    # ---------------------------------------------------------------------------
    # electricity_prices
    # ---------------------------------------------------------------------------
    
    combined_data = (
        # merge electricity_prices to combined_data
        pd.merge(
            combined_data,
            electricity_prices,
            left_on=["date", "hour"],
            right_on=["date_adjusted", "hour"],
            how='left'
        )
        # delete `date_adjusted`
        .drop(columns=["date_adjusted"])
        # fill NaN at 3am in target
        .assign(
            **{
                "electricity_euros_per_mwh": lambda d: d.groupby(['date', 'prediction_unit_id', 'is_consumption'], group_keys=False).electricity_euros_per_mwh.apply(lambda x: x.interpolate())
            }
        )
    )

    if verbose:
        print("")
        print("Merged: electricity_prices")
        print(f"#train obs: {len(train)}  |  #merged obs: {len(combined_data)}")

    # ---------------------------------------------------------------------------
    # historical_weather
    # ---------------------------------------------------------------------------

    combined_data = (
        # merge historical_weather to combined_data
        pd.merge(
            combined_data,
            (
                historical_weather
                # assign `date_adjusted, hour_adjusted`
                .assign(
                    **{
                        "date_adjusted": lambda d: pd.to_datetime(
                            d["datetime"] + pd.DateOffset(hours=37)
                        ).dt.date,
                        "hour_adjusted": lambda d: pd.to_datetime(
                            d["datetime"] + pd.DateOffset(hours=37)
                        ).dt.hour
                    }
                )
                # delete `date, hour, datetime`
                .drop(columns=['date','hour','datetime'])
            ),
            left_on=["date", "hour", "county"],
            right_on=["date_adjusted", "hour_adjusted", "county"],
            how='left',
            suffixes=(False, '_hist')
        )
        # delete `date_adjusted, hour_adjusted`
        .drop(columns=['date_adjusted','hour_adjusted'])
    )

    if verbose:
        print("")
        print("Merged: historical_weather")
        print(f"#train obs: {len(train)}  |  #merged obs: {len(combined_data)}")

    # ---------------------------------------------------------------------------
    # forecast_weather
    # ---------------------------------------------------------------------------
    
    combined_data = (
        # merge forecast_weather to combined_data
        pd.merge(
            combined_data,
            forecast_weather,
            left_on=["county", "date", "date", "hour"],
            right_on=["county", "origin_date_adjusted","date_adjusted","hour_adjusted"],
            how="left",
            suffixes=('_hist', '_fore')
        )
        # delete unuse datetimes
        .drop(columns=['date_adjusted','hour_adjusted','forecast_datetime_adjusted','origin_date_adjusted'])
    )

    if verbose:
        print("")
        print("Merged: forecast_weather")
        print(f"#train obs: {len(train)}  |  #merged obs: {len(combined_data)}")

    # ---------------------------------------------------------------------------
    # revealed_target
    # ---------------------------------------------------------------------------
    
    if type(revealed_targets) == pd.DataFrame:
        combined_data = (
            # merge revealed_targets to combined_data
            pd.merge(
                combined_data,
                (
                    revealed_targets
                    .rename(
                        columns={
                            'target': 'revealed_target'
                        }
                    )
                ),
                left_on=["row_id"],
                right_on=["row_id"],
                how="left",
            )
        )

        if verbose:
            print("")
            print("Merged: revealed_targets")
            print(f"#train obs: {len(train)}  |  #merged obs: {len(combined_data)}")
    else:
        combined_data = (
            combined_data
            # assign revealed_targets to combined_data
            .assign(
                **{
                    "revealed_target": lambda d: d.groupby(['prediction_unit_id','is_consumption']).target.shift(48)
                }
            )
        )
        if verbose:
            print("")
            print("Created: revealed_targets")
            print(f"#train obs: {len(train)}  |  #created obs: {len(combined_data)}")

    return combined_data