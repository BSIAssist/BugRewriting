from pathlib import Path

from tqdm import tqdm

from bug_changing.utils.dataframe_util import DataFrameUtil
from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.path_util import PathUtil


from config import MOZILLA_PROJ, ECLIPSE_PROJ, MOZILLA_URL, OUTPUT_DIR

if __name__ == "__main__":
    # folder_name = MOZILLA_PROJ
    folder_name = ECLIPSE_PROJ

    summary_pairs_filepath = PathUtil.get_instance_summary_pairs_filepath(folder_name)
    summary_pairs = FileUtil.load_pickle(summary_pairs_filepath)
    # get the session prompt of extractor
    df = summary_pairs.convert_summary_pairs_desc_info_into_dataframe(folder_name)
    DataFrameUtil.write_df_into_excel(Path(OUTPUT_DIR, folder_name, f'instance_summary_pairs_with_desc_labels.xlsx'),
                                      df, folder_name)

    # print(summary_pairs.get_summary_pair_by_bug_id_summary_ids(1403460, 0, 1))
    # FileUtil.dump_pickle(summary_pairs_filepath, summary_pairs)
