import pandas as pd
import streamlit as st

from syml.diagnostool.calculator import data_profiler
from syml.diagnostool.calculator import variability_calculator
from syml.diagnostool.utils import hist_maker
from syml.interract.page_class import BasePageElement


class FieldInspector(BasePageElement):
    def __init__(
        self,
        data=None,
        name="FieldInspector",
    ):
        self.name = name
        self.data = data
        super().__init__()

    def setup(self):
        self.profiled_data = data_profiler(self.data)
        self.actions += [self.basic_summary, self.advanced_analysis]

    def introduction(self):
        st.header("Field Inspector :microscope:")
        st.markdown("""
                    The **Field Inspector** :microscope: will help you understand your data on a technical level.
                    The goal is to provide you with information about the type, the completion, the variability and
                    other characteristics that will help you diagnose the quality of your data.

                    Once you'll have a better understanding of your raw data, **:blue[QIA]** (Quality Improvement Assistant) will help you boost your
                    data coverage, quality and uniformity.

                    Then, with the help of **:orange[ADA]** (Advanced Data Analyst) you will get a deep comprehension of relationships and patterns in your data.
                    """)

    def basic_summary(self):
        st.subheader("Basic summary :mag:")
        st.markdown("""The following table contains a basic summary about your data.
                    You'll see the field completion, the detected data type and the field name.
                    """)

        df = self.profiled_data

        edited_df = st.data_editor(
            df,
            hide_index=True,
            column_config={
                "field names": st.column_config.TextColumn(
                    "field names",
                ),
                "data type": st.column_config.SelectboxColumn(
                    "data type",
                    help="Data is either Continuous (length, amount of money, ...) or Categorical (gender, name of a color, ...)",
                    options=[
                        "continuous",
                        "categorical",
                        "mixed",
                        "unknown",
                    ],
                    required=True,
                ),
                "field completion": st.column_config.ProgressColumn(
                    "field completion",
                    help="percentage of rows that contain a value for each field",
                    format="%.0f",
                    min_value=0,
                    max_value=100,
                ),
                "examples": st.column_config.ListColumn(
                    "examples",
                ),
            },
            disabled=["examples", "field completion", "field names"],
        )

        self.edited_df = edited_df

    def advanced_analysis(self):
        data = self.data
        classification = self.edited_df[["field names", "data type"]].set_index("field names")

        st.subheader("Advanced Analysis :microscope:")
        st.markdown("""The Advanced Analysis section helps you diagnose problems in your raw data.
                    For example, it can happen that you have outliers in your continuous data, or you
                    could have for a categorical variable a very large number of labels due to typos.
                    """)

        variability = variability_calculator(data, classification=classification)

        if "continuous" in variability.keys():
            st.markdown("""
                        #### Continuous Variables
                        Continuous variables are analyzed below.
                        For each field, you have the mean, standard deviation, min-max values and a histogram.
                        """)

            data_hist = hist_maker(data[variability["continuous"].columns])
            table = pd.concat([variability["continuous"].T, data_hist], axis=1)

            st.data_editor(
                table,
                column_config={
                    "values": st.column_config.BarChartColumn(
                        "Histogram",
                        help="Histogram of the values of each field",
                        width="medium",
                    ),
                },
                hide_index=False,
                disabled=True,
            )

        if "categorical" in variability.keys():
            st.markdown("""
                        #### Categorical Variables
                        Categorical variables are analyzed below.
                        For each field the occurrence of each unique label has been counted, then a few statistics are computed :
                        - number of distinct labels
                        - average occurrence of a label
                        - min-max occurrence of label
                        """)

            st.dataframe(variability["categorical"])
