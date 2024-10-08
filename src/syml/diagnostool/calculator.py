import pandas as pd
import streamlit as st

from .utils import categorical_variability
from .utils import classify_columns
from .utils import continuous_variability
from .utils import sampler


@st.cache_data
def data_profiler(data):
    """
    This function is responsible for profiling the raw data given to syml.

    It returns basic information about the data, for each field :
     - detected type (continuous, categorical or unknown)
     - percentage of completion
     - variance
     - ...

    Args:
        data (pd.DataFrame): the raw  data to be profiled.

    Returns:
        pd.DataFrame: The result of the profiling.
    """
    field_data = pd.Series(data.columns, name="field names")
    field_type = classify_columns(data).reset_index(drop=True)
    fillage_data = 100 * pd.Series([data[col].notna().sum() / len(data) for col in field_data], name="field completion")
    examples = data.apply(sampler, args=(10,), axis=0).T.reset_index(drop=True)
    examples.columns = ["examples"]

    df = pd.concat([field_data, field_type, fillage_data, examples], axis=1)

    return df


def variability_calculator(df: pd.DataFrame, classification=None):
    if classification is None:
        classification = classify_columns(df)
    classification = pd.DataFrame(classification)

    variability = {}

    if "continuous" in classification.values:
        continous_cols = df[classification[classification["data type"] == "continuous"].index]
        continuous_var = continuous_variability(continous_cols)
        variability["continuous"] = continuous_var

    if "categorical" in classification.values:
        categorical_cols = df[classification[classification["data type"] == "categorical"].index]
        categorical_var = categorical_variability(categorical_cols)
        variability["categorical"] = categorical_var

    return variability
