import logging
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Union

import pandas as pd

ColumnsDef = Optional[Union[List, Dict]]


def _check_columns(df: pd.DataFrame, columns: ColumnsDef) -> None:
    if isinstance(columns, list):
        for column in columns:
            assert column in df.columns, f"Column {column} missing from DataFrame. Got {_describe_pd(df)}"
    if isinstance(columns, dict):
        for column, dtype in columns.items():
            assert column in df.columns, f"Column {column} missing from DataFrame. Got {_describe_pd(df)}"
            assert (
                df[column].dtype == dtype
            ), f"Column {column} has wrong dtype. Was {df[column].dtype}, expected {dtype}"


def df_out(columns: ColumnsDef = None) -> Callable:
    """Decorator used to document a function that returns a Pandas DataFrame.
    The return value will be validated in runtime.

    Args:
        columns (ColumnsDef, optional): List or dict that describes expected columns of the DataFrame. Defaults to None.

    Returns:
        Callable: Decorated function
    """

    def wrapper_df_out(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: str, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            assert isinstance(result, pd.DataFrame), f"Wrong return type. Expected pandas dataframe, got {type(result)}"
            if columns:
                _check_columns(result, columns)
            return result

        return wrapper

    return wrapper_df_out


def _get_parameter(name: Optional[str] = None, *args: str, **kwargs: Any) -> pd.DataFrame:
    if not name:
        if len(args) == 0:
            return None
        return args[0]
    return kwargs[name]


def df_in(name: Optional[str] = None, columns: ColumnsDef = None) -> Callable:
    """Decorator used to document a function parameter that is a Pandas DataFrame.
    The parameter will be validated in runtime.

    Args:
        name (Optional[str], optional): Name of the parameter that contains a DataFrame. Defaults to None.
        columns (ColumnsDef, optional): List or dict that describes expected columns of the DataFrame. Defaults to None.

    Returns:
        Callable: Decorated function
    """

    def wrapper_df_out(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: str, **kwargs: Any) -> Any:
            df = _get_parameter(name, *args, **kwargs)
            assert isinstance(
                df, pd.DataFrame
            ), f"Wrong parameter type. Expected Pandas DataFrame, got {type(df).__name__} instead."
            if columns:
                _check_columns(df, columns)
            return func(*args, **kwargs)

        return wrapper

    return wrapper_df_out


def _describe_pd(df: pd.DataFrame, include_dtypes: bool = False) -> str:
    result = f"columns: {list(df.columns)}"
    if include_dtypes:
        readable_dtypes = [dtype.name for dtype in df.dtypes]
        result += f" with dtypes {readable_dtypes}"
    return result


def _log_input(level: int, func_name: str, df: Any, include_dtypes: bool) -> None:
    if isinstance(df, pd.DataFrame):
        logging.log(
            level,
            f"Function {func_name} parameters contained a DataFrame: {_describe_pd(df, include_dtypes)}",
        )


def _log_output(level: int, func_name: str, df: Any, include_dtypes: bool) -> None:
    if isinstance(df, pd.DataFrame):
        logging.log(
            level,
            f"Function {func_name} returned a DataFrame: {_describe_pd(df, include_dtypes)}",
        )


def df_log(level: int = logging.DEBUG, include_dtypes: bool = False) -> Callable:
    """Decorator used to wrap a function that consumes or produces a Pandas DataFrame or both.
    Logs the columns of the consumed and/or produced DataFrame.

    Args:
        level (int, optional): Level of the logging messages produced. Defaults to logging.DEBUG.
        include_dtypes (bool, optional): When set to True, will log also the dtypes of each column. Defaults to False.

    Returns:
        Callable: Decorated function.
    """

    def wrapper_df_log(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: str, **kwargs: Any) -> Any:
            _log_input(level, func.__name__, _get_parameter(None, *args, **kwargs), include_dtypes)
            result = func(*args, **kwargs)
            _log_output(level, func.__name__, result, include_dtypes)

        return wrapper

    return wrapper_df_log
