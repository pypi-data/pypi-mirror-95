"""Formats to tranform the data into another format.

Functions:
    | *numpy_array()* converts an array-like data to np.ndarray
    | *array_to_dict()* converts an array to a dictionary where the keys are the unique values of 
    |   the array and the values of the dictionary are the counts of the array values. 
    | *dataframe_to_array()* returns a pandas dataframe from an np.ndarray.
"""

from __future__ import annotations
from typing import Any, Optional, Union

import numpy as np
import pandas as pd

from samplics.utils import checks

from samplics.utils.types import Array, DictStrInt, DictStrNum, Number, Series, StringNumber


def numpy_array(arr: Array) -> np.ndarray:
    """Converts an array-like input data to np.ndarray.

    Args:
        arr (Array): array-like input data.

    Returns:
        np.ndarray: an numpy array
    """

    if not isinstance(arr, np.ndarray):
        arr_np = np.asarray(arr)
        if isinstance(arr, (list, tuple)) and len(arr_np.shape) == 2:
            arr_np = np.transpose(arr_np)
        return arr_np
    else:
        return arr


def array_to_dict(arr: np.ndarray, domain: Optional[np.ndarray] = None) -> DictStrNum:
    """Converts an array to a dictionary where the keys are the unique values of the array and
    the values of the dictionary are the counts of the array values.

    Args:
        arr (np.ndarray): an input area.
        domain (np.ndarray, optional): an array to provide the group associated with the
            observations in arr. If not None, a dictionarry of dictionaries is produced.
            Defaults to None.

    Returns:
        dict[StringNumber, Number]: a dictionary with the unique values of *arr* as keys.
            The values of the dictionary correspond to the counts of the keys in *arr*.
    """

    if domain is None:
        keys, counts = np.unique(numpy_array(arr), return_counts=True)
        out_dict = dict(zip(keys, counts))
    else:
        out_dict = {}
        for d in np.unique(domain):
            arr_d = arr[domain == d]
            keys_d, counts_d = np.unique(numpy_array(arr_d), return_counts=True)
            out_dict[d] = dict(zip(keys_d, counts_d))

    return out_dict


def dataframe_to_array(df: pd.DataFrame) -> np.ndarray:
    """Returns a pandas dataframe from an np.ndarray.

    Args:
        df (pd.DataFrame): a pandas dataframe or series.

    Raises:
        AssertionError: return an exception if data is not a pandas dataframe or series.

    Returns:
        np.ndarray: an numpy array.
    """

    if isinstance(df, pd.Series):
        x_array = df
    elif isinstance(df, pd.DataFrame):
        nb_vars = df.shape[1]
        varlist = df.columns
        x_array = df[varlist[0]]
        if nb_vars > 1:
            for k in range(1, nb_vars):
                x_array = x_array.astype(str) + "_&_" + df[varlist[k]].astype(str)
    else:
        raise AssertionError("The input data is not a pandas dataframe")

    return np.asarray(x_array.to_numpy())


def sample_size_dict(
    sample_size: Union[DictStrInt, int],
    stratification: bool,
    stratum: Array,
) -> Union[DictStrInt, int]:
    if not isinstance(sample_size, dict) and stratification:
        return dict(zip(stratum, np.repeat(sample_size, len(stratum))))
    if isinstance(sample_size, (int, float)) and not stratification:
        return sample_size
    elif isinstance(sample_size, dict):
        return sample_size
    else:
        raise AssertionError


def sample_units(all_units: Array, unique: bool = True) -> np.ndarray:
    all_units = numpy_array(all_units)
    if unique:
        checks.assert_not_unique(all_units)

    return all_units


def dict_to_dataframe(col_names: list[str], *args: Any) -> pd.DataFrame:

    if isinstance(args[0], dict):
        keys = list(args[0].keys())
        number_keys = len(keys)
        values = list()
        for k, arg in enumerate(args):
            argk_keys = list(args[k].keys())
            if not isinstance(arg, dict) or (keys != argk_keys) or number_keys != len(argk_keys):
                raise AssertionError(
                    "All input parameters must be dictionaries with the same keys."
                )

            values.append(list(arg.values()))

        values_df = pd.DataFrame(
            values,
        ).T
        values_df.insert(0, "00", keys)
    else:
        values_df = pd.DataFrame({args})

    values_df.columns = col_names

    return values_df


def remove_nans(excluded_units: Array, *args: Any) -> list:

    excluded_units = numpy_array(excluded_units)
    vars = list()
    for var in args:
        if var is not None and len(var.shape) != 0:
            vars.append(var[~excluded_units])
        else:
            vars.append(None)

    return vars


def fpc_as_dict(stratum: Optional[Array], fpc: Union[Array, Number]) -> Union[DictStrNum, Number]:

    if stratum is not None:
        stratum = numpy_array(stratum)

    if stratum is None and isinstance(fpc, (int, float)):
        return fpc
    elif stratum is not None and isinstance(fpc, (int, float)):
        return dict(zip(stratum, np.repeat(fpc, stratum.shape[0])))
    elif stratum is not None and isinstance(fpc, np.ndarray):
        return dict(zip(stratum, fpc))
    else:
        raise TypeError("stratum and fpc are not compatible!")


def concatenate_series_to_str(row: Series) -> str:
    """concatenate the elements into one string using '_' to separate the elements

    Args:
        row (Array): [description]

    Returns:
        str: [description]
    """
    return "__by__".join([str(c) for c in row])


def numpy_to_dummies(arr: np.ndarray, varsnames: list[str]) -> np.ndarray:

    df = pd.DataFrame(arr.astype(str))
    df.columns = varsnames

    return np.asarray(pd.get_dummies(df, drop_first=True).to_numpy())
