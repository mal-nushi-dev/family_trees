import pandas as pd

# Define data
data = {
    'Column 1': ['Value1', 'Value2', 'Value3'],
    '     Column2': ['Value4', 'Value5', 'Value6'],
    'Column3': ['Value7', 'Value8', 'Value9']
}


class DataFrameManager:
    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.dataframe = dataframe

    def upper_case_columns(self):
        



df = pd.DataFrame(data)
print(df)

print("Renaming df columns to uppercase...")

df.rename(columns=str.upper, inplace=True)

print("Removing whitespaces and replacing spaces with underscores...")
df.columns = df.columns.str.strip().str.replace(' ', '_')
print(df)
