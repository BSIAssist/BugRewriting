from pathlib import Path

from bug_changing.types.placeholder import Placeholder
from bug_changing.types.summary import SummaryPairs
from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.path_util import PathUtil
import pandas as pd
import numpy as np

from config import OUTPUT_DIR, MOZILLA_PROJ, ECLIPSE_PROJ


def get_labels_from_row(row):
    labels = row.values[5:20].tolist()  # [5, 20)
    return labels


if __name__ == "__main__":
    folder_name = MOZILLA_PROJ
    # folder_name = ECLIPSE_PROJ
    summary_pairs_filepath = PathUtil.get_test_sample_summary_pairs_filepath(folder_name)
    summary_pairs = FileUtil.load_pickle(summary_pairs_filepath)
    print(len(summary_pairs))
    summary_pairs.remove_tags()

    df = pd.read_excel(Path(OUTPUT_DIR, folder_name, f'test_sample_summary_pairs_labels.xlsx'),
                       sheet_name=f'{folder_name}')
    df = df.replace(np.nan, None)
    test_sample_summary_pairs_with_labels = []
    for index, two_rows in df.groupby(np.arange(len(df)) // 2):
        # print(index)
        first_row = two_rows.iloc[0]
        second_row = two_rows.iloc[1]
        bug_id = int(first_row.values[1])
        rm_summary_id = int(first_row.values[3])
        add_summary_id = int(second_row.values[3])
        # print(f"{first_row.values[20]}\t{first_row.values[21]}")
        # print(f"{second_row.values[20]}\t{second_row.values[21]}")
        # others and notes
        if first_row.values[20] is None and first_row.values[21] is None:
            summary_pair = summary_pairs.get_summary_pair_by_bug_id_summary_ids(bug_id, rm_summary_id, add_summary_id)
            if summary_pair is not None:
                labels_1 = get_labels_from_row(first_row)
                labels_2 = get_labels_from_row(second_row)
                # print(labels_1)
                # print(labels_2)
                summary_pair.rm_summary.initiate_from_labels(labels_1)
                summary_pair.add_summary.initiate_from_labels(labels_2)
                test_sample_summary_pairs_with_labels.append(summary_pair)
                # print(summary_pair)
        # else:
        #     summary_pairs.remove_by_id(bug_id, rm_summary_id, add_summary_id)
    test_sample_summary_pairs_with_labels = SummaryPairs(test_sample_summary_pairs_with_labels)
    test_sample_summary_pairs_with_labels.complete_vague_labels()
    print(len(test_sample_summary_pairs_with_labels))
    summary_pairs_filepath = PathUtil.get_test_sample_summary_pairs_with_labels_filepath(folder_name)
    FileUtil.dump_pickle(summary_pairs_filepath, test_sample_summary_pairs_with_labels)
