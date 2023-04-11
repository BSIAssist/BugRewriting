from pathlib import Path

from tqdm import tqdm
from bug_changing.types.bugs import Bugs
from bug_changing.utils.dataframe_util import DataFrameUtil
from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.nlp_util import NLPUtil
from bug_changing.utils.path_util import PathUtil
from config import DATA_DIR, MOZILLA_PROJ, ECLIPSE_PROJ, OUTPUT_DIR

if __name__ == "__main__":
    """
    put test_sample_summary_pairs into excel for labeling
    """
    # folder_name = MOZILLA_PROJ
    folder_name = ECLIPSE_PROJ

    summary_pairs = FileUtil.load_pickle(PathUtil.get_test_sample_summary_pairs_filepath(folder_name))
    df = summary_pairs.convert_summary_pairs_into_dataframe(folder_name)
    # df2 = convert_bugs_into_dataframe_from_history(sample_bugs_2, folder_name)
    DataFrameUtil.write_df_into_excel(Path(OUTPUT_DIR, folder_name, f'test_sample_summary_pairs_labels.xlsx'),
                                      df, folder_name)
