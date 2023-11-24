import pandas as pd
from typing import List

def drop_missing_values(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Drop rows with missing values.

    Parameters
    ----------
    data : pd.DataFrame

    Returns
    -------
    data : pd.DataFrame
        DataFrame without missing values.

    Examples
    --------
    >>> from kaggle_enefit.data.preprocessing.utils import drop_missing_values
    >>> data = (
    ...     data
    ...     .pipe(drop_missing_values)
    ... )
    """
    data = data.dropna(how='any')

    return data

def drop_columns(
    data: pd.DataFrame,
    columns: List[str],
) -> pd.DataFrame:
    """Drop rows with missing values.

    Parameters
    ----------
    data : pd.DataFrame
    columns : List[str]

    Returns
    -------
    data : pd.DataFrame
        DataFrame with remove columns.

    Examples
    --------
    >>> from kaggle_enefit.data.preprocessing.utils import drop_missing_values
    >>> data = (
    ...     data
    ...     .pipe(drop_missing_values)
    ... )
    """
    data = data.drop(columns=columns)

    return data