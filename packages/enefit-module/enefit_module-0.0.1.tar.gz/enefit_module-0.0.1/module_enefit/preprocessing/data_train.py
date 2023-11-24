from typing import Dict

import pandas as pd

def preprocess_train(
    data_train: pd.DataFrame,
) -> pd.DataFrame:
    """Preprocess train data.

    Parameters
    ----------
    data_train : pd.DataFrame

    Returns
    -------
    data_train : pd.DataFrame

    Examples
    --------
    >>> from kaggle_enefit.data.preprocessing.data_train import preprocess_train
    >>> data_train = preprocess_train(
    ...     data_train=data_train,
    ... )
    """
    # rename `prediction_datetime`
    if "prediction_datetime" in data_train.columns:
        data_train = data_train.rename(columns={"prediction_datetime": "datetime"})
    
    # assign `target`
    if "target" not in data_train.columns:
        data_train = (
            data_train
            .assign(
                **{
                    "target": lambda d: 0
                }
            )
        )
    
    # delete `data_block_id`
    if "data_block_id" in data_train.columns:
        data_train = data_train.drop(
            columns=["data_block_id"]
        )

    data_train = (
        data_train
        # assign `datetime, date, hour, target`
        .assign(
            **{
                "datetime": lambda d: pd.to_datetime(d["datetime"]),
                "date": lambda d: d["datetime"].dt.date,
                "hour": lambda d: d["datetime"].dt.hour,
                # CHECK: summer time 무시
                "target": data_train.groupby(['is_consumption', 'prediction_unit_id'], group_keys=False).target.apply(lambda x: x.interpolate())
            }
        )
        # astype [train, test]
        .assign(
            **{
                "county": lambda d: d["county"].astype('int8'),
                "is_business": lambda d: d["is_business"].astype('int8'),
                "product_type": lambda d: d["product_type"].astype('int8'),
                "is_consumption": lambda d: d["is_consumption"].astype('int8'),
                "row_id": lambda d: d["row_id"].astype('int32'),
                "prediction_unit_id": lambda d: d["prediction_unit_id"].astype('int16'),
                "target": lambda d: d["target"].astype('float64'),
            }
        )
    )

    return data_train