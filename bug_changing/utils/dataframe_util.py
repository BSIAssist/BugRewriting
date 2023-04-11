import pandas as pd

from bug_changing.types.placeholder import Placeholder
from config import MOZILLA_PROJ


class DataFrameUtil:

    @staticmethod
    def convert_data_into_dataframe(columns, rows):
        """

        Args:
            columns (): ["列名", "列名", "列名"]
            rows (): [[value, value, value]
                      [value, value, value]
                      [value, value, value]]

        Returns: pd.DataFrame
        """
        df = pd.DataFrame(rows, columns=columns)
        return df

    @staticmethod
    def write_df_into_excel(filepath, df1, sheet_name1, df2=None, sheet_name2=None):
        with pd.ExcelWriter(filepath) as writer:
            df1.to_excel(writer, sheet_name=sheet_name1)
            if df2 and sheet_name2:
                df2.to_excel(writer, sheet_name=sheet_name2)

    @staticmethod
    def get_row_column_from_value(df, value):
        row_column_series = df[df.isin([value])].stack()
        # print(row_column_series.index.tolist())
        # print(type(row_column_series))
        row_column_list = row_column_series.index.tolist()
        # print(row_column_list)
        # print(type(row_column_list))
        return row_column_list
