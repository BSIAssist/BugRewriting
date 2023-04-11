from pathlib import Path

from bug_changing.types.summary import SummaryPairs
from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.path_util import PathUtil
import pandas as pd
import numpy as np

from config import OUTPUT_DIR, MOZILLA_PROJ, ECLIPSE_PROJ


def get_labels_from_row(row, begin_index, end_add_1_index):
    labels = row.values[begin_index:end_add_1_index].tolist()  # [begin_index, end_add_1_index)
    return labels


if __name__ == "__main__":
    # folder_name = MOZILLA_PROJ
    folder_name = ECLIPSE_PROJ
    summary_pairs_filepath = PathUtil.get_instance_summary_pairs_filepath(folder_name)
    summary_pairs = FileUtil.load_pickle(summary_pairs_filepath)
    print(len(summary_pairs))
    # summary_pairs.remove_tags()

    df = pd.read_excel(Path(OUTPUT_DIR, folder_name, f'instance_summary_pairs_with_desc_labels.xlsx'),
                       sheet_name=f'{folder_name}')
    df = df.replace(np.nan, None)
    filtered_summary_pairs = []
    for index, two_rows in df.groupby(np.arange(len(df)) // 2):
        # print(index)
        first_row = two_rows.iloc[0]
        second_row = two_rows.iloc[1]
        bug_id = int(first_row.values[1])
        print(bug_id)
        rm_summary_text = str(first_row.values[3])
        add_summary_text = str(second_row.values[3])
        print(rm_summary_text)
        print(add_summary_text)
        summary_pair = summary_pairs.get_summary_pair_by_bug_id_summary_texts(bug_id,
                                                                              rm_summary_text, add_summary_text)

        labels_1 = get_labels_from_row(first_row, 4, 11)
        labels_2 = get_labels_from_row(second_row, 4, 11)
        print(labels_1)
        print(labels_2)
        # summary_pair.add_summary.initiate_from_desc_labels(labels_2)

        print(summary_pair.bug.id)
        summary_pair.rm_summary.initiate_from_desc_labels(labels_1)
        if labels_1[6] == 'y':
            filtered_summary_pairs.append(summary_pair)
            # print(initiated_summary_pair)
        # print(labels_1)
        # print(labels_2)
        # print(type(first_row.values[0:5].tolist()))
        # print(first_row.values[1])
        # print(second_row)
        # print(type(g))
        # input()
    filtered_summary_pairs = SummaryPairs(filtered_summary_pairs)
    print(len(filtered_summary_pairs))
    # print(summary_pairs.get_summary_pair_by_bug_id_summary_ids(1403460, 0, 1))
    filtered_summary_pairs.complete_vague_labels()
    FileUtil.dump_pickle(PathUtil.get_instance_summary_pairs_with_desc_labels_filepath(folder_name),
                         filtered_summary_pairs)
