import streamlit as st

from syml.interract.page_class import BasePageElement

from .categorical_qia import CategoricalQIA


class Report(BasePageElement):
    def __init__(self, db, nrows=None) -> None:
        self.db = db
        self.data = self.db.query("SELECT * FROM dataset")
        # TODO: Add a way to get the classification of the data
        super().__init__()

    def setup(self):
        self.setup_child(CategoricalQIA(self.data))

    def introduction(self):
        st.title("Quality Improvement Assistant 🧑🏼‍🔬")

        st.markdown("""
                    **You can do better !**

                    #### Introduction

                    On this page you'll find powerful modules to help you mitigate potential data quality issues, such as :
                    - Badly labeled data
                    - typos in categorical data
                    - missing values
                    - anormal extreme numerical data
                    - ... and many other !
                    """)

    def setup_categorical_qia(self, data):
        classification = self.db.query("SELECT field_names, data_type FROM basic_analysis")
        classification = classification.set_index("field_names")
        data_categ = data[classification["data type"] == "categorical"]
        return CategoricalQIA(data_categ)
