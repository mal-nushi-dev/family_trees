from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype
)
import pandas as pd
import streamlit as st


class filtered_df:
    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe

    def filter_dataframe(self) -> pd.DataFrame:
        modify = st.checkbox("Add filters")

        if not modify:
            return self.dataframe

        usr_df = self.prepare_dataframe()

        modification_container = st.container()
        with modification_container:
            to_filter_columns = st.multiselect(
                "Filter DataFrame On", usr_df.columns)

        filters = []
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            filters.append(self.get_filter(usr_df, column, right))

        for filter in filters:
            usr_df = usr_df[filter]

        return usr_df

    def prepare_dataframe(self) -> pd.DataFrame:
        usr_df = self.dataframe

        for col in usr_df.columns:
            if is_object_dtype(usr_df[col]):
                try:
                    usr_df[col] = pd.to_datetime(usr_df[col])
                except Exception:
                    pass

            if is_datetime64_any_dtype(usr_df[col]):
                usr_df[col] = usr_df[col].dt.tz_localize(None)

        return usr_df

    def get_filter(self, usr_df: pd.DataFrame, column: str, right):
        dtype = usr_df[column].dtype

        if is_categorical_dtype(dtype) or usr_df[column].nunique() < 10:
            user_cat_input = right.multiselect(
                f"Values for {column}",
                usr_df[column].unique(),
                default=list(usr_df[column].unique()),
            )
            return usr_df[column].isin(user_cat_input)

        elif is_numeric_dtype(dtype):
            _min = float(usr_df[column].min())
            _max = float(usr_df[column].max())
            step = (_max - _min) / 100
            user_num_input = right.slider(
                f"Values for {column}",
                min_value=_min,
                max_value=_max,
                value=(_min, _max),
                step=step,
            )
            return usr_df[column].between(*user_num_input)

        elif is_datetime64_any_dtype(dtype):
            user_date_input = right.date_input(
                f"Values for {column}",
                value=(
                    usr_df[column].min(),
                    usr_df[column].max(),
                ),
            )
            if len(user_date_input) == 2:
                user_date_input = tuple(map(pd.to_datetime, user_date_input))
                start_date, end_date = user_date_input
                return usr_df[column].between(start_date, end_date)

        else:
            user_text_input = right.text_input(
                f"Substring or regex in {column}",
            )
            if user_text_input:
                return usr_df[column].astype(str).str.contains(user_text_input)

        # Default return value
        return pd.Series([True]*len(usr_df))


if __name__ == "__main__":
    pass
