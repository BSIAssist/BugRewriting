from pathlib import Path

from bug_changing.utils.dataframe_util import DataFrameUtil
from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.path_util import PathUtil
import pandas as pd

from config import OUTPUT_DIR, ECLIPSE_PROJ

if __name__ == "__main__":
    # folder_name = MOZILLA_PROJ
    folder_name = ECLIPSE_PROJ
    summary_pairs_filepath = PathUtil.get_instance_summary_pairs_filepath(folder_name)
    summary_pairs = FileUtil.load_pickle(summary_pairs_filepath)

    df = summary_pairs.convert_summary_pairs_into_dataframe(folder_name)
    # df2 = convert_bugs_into_dataframe_from_history(sample_bugs_2, folder_name)
    DataFrameUtil.write_df_into_excel(Path(OUTPUT_DIR, folder_name, f'instance_summary_pairs_labels.xlsx'),
                                      df, folder_name)
    # with pd.ExcelWriter(Path(OUTPUT_DIR, folder_name, f'instance_summary_pairs_labels.xlsx')) as writer:
    #     df.to_excel(writer, sheet_name=f'{folder_name}')

