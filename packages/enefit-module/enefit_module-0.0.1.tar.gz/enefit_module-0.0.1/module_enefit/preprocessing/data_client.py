import pandas as pd

def preprocess_client(
    data_client: pd.DataFrame,
) -> pd.DataFrame:
    """Preprocess client data.

    Parameters
    ----------
    data_client : pd.DataFrame

    Returns
    -------
    client : pd.DataFrame
        client data.

    Examples
    --------
    >>> from kaggle_enefit.data.preprocessing.data_client import preprocess_client
    >>> data_client = preprocess_client(data_client)
    """
    # delete `data_block_id`
    if "data_block_id" in data_client.columns:
        data_client = data_client.drop(
            columns=["data_block_id"]
        )

    data_client = (
        data_client
        # assign `date_adjusted`
        .assign(
            **{
                "date_adjusted": lambda d: pd.to_datetime(
                            pd.to_datetime(d["date"]) + pd.DateOffset(days=2)
                        ).dt.date,
            }
        )
        # astype [train, test]
        .assign(
            **{
                "product_type": lambda d: d["product_type"].astype('int8'),
                "county": lambda d: d["county"].astype('int8'),
                "eic_count": lambda d: d["eic_count"].astype('float64'),
                "installed_capacity": lambda d: d["installed_capacity"].astype('float32'),
                "is_business": lambda d: d["is_business"].astype('int8'),
            }
        )
        # delete `date`
        .drop(columns=["date"])
    )


    return data_client