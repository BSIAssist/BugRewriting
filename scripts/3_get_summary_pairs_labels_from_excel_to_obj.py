from pathlib import Path

from bug_changing.types.placeholder import Placeholder
from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.path_util import PathUtil
import pandas as pd
import numpy as np

from config import OUTPUT_DIR, MOZILLA_PROJ, ECLIPSE_PROJ


def convert_summary_pairs_into_dataframe(summary_pairs, folder_name='mozilla'):
    columns = ['bug id', 'bug link', 'summary id', 'summary',
               Placeholder.SUGGESTED_SOLUTION, Placeholder.ACTUAL_BEHAVIOR, Placeholder.TRIGGER_ACTION,
               Placeholder.IS_ACTUAL_BEHAVIOR_VAGUE, Placeholder.IS_TRIGGER_ACTION_VAGUE,
               Placeholder.PLATFORM, Placeholder.COMPONENT,
               Placeholder.SPELLING_ERROR, Placeholder.SYNTAX_ERROR,
               Placeholder.DECLARATIVE_STATEMENT, Placeholder.PRESENT_TENSE,
               Placeholder.PERSONAL_PRONOUN, Placeholder.EMOTIONAL_REACTION,
               Placeholder.OFFENCE, Placeholder.WISHY_WASHY_WORD]

    # for index in range(5):
    #     columns.extend(['change from', 'change what', 'change for'])
    rows = []
    for summary_pair in summary_pairs:
        if folder_name == MOZILLA_PROJ:
            bug_link = f"https://bugzilla.mozilla.org/show_bug.cgi?id={summary_pair.bug.id}"
        else:
            bug_link = f"https://bugs.eclipse.org/bugs/show_bug.cgi?id={summary_pair.bug.id}"

        summaries = [summary_pair.rm_summary, summary_pair.add_summary]
        for summary in summaries:
            row = [summary_pair.bug.id, bug_link, summary.id, summary.text, ]
            for add_column in range(15):
                row.extend([''])
            # row.append('')
            rows.append(row)
    df = pd.DataFrame(rows, columns=columns)
    return df


def get_labels_from_row(row):
    labels = row.values[5:20].tolist()  # [5, 20)
    return labels


if __name__ == "__main__":
    folder_name = MOZILLA_PROJ
    # folder_name = ECLIPSE_PROJ
    summary_pairs_filepath = PathUtil.get_instance_summary_pairs_filepath(folder_name)
    summary_pairs = FileUtil.load_pickle(summary_pairs_filepath)
    # print(summary_pairs)
    summary_pairs.remove_tags()

    df = pd.read_excel(Path(OUTPUT_DIR, folder_name, f'instance_summary_pairs_labels.xlsx'),
                       sheet_name=f'{folder_name}')
    df = df.replace(np.nan, None)

    for index, two_rows in df.groupby(np.arange(len(df)) // 2):
        # print(index)
        first_row = two_rows.iloc[0]
        second_row = two_rows.iloc[1]
        bug_id = int(first_row.values[1])
        rm_summary_id = int(first_row.values[3])
        add_summary_id = int(second_row.values[3])
        summary_pair = summary_pairs.get_summary_pair_by_bug_id_summary_ids(bug_id, rm_summary_id, add_summary_id)
        labels_1 = get_labels_from_row(first_row)
        labels_2 = get_labels_from_row(second_row)
        print(labels_1)
        print(labels_2)
        summary_pair.rm_summary.initiate_from_labels(labels_1)
        summary_pair.add_summary.initiate_from_labels(labels_2)
        print(summary_pair)
        # print(labels_1)
        # print(labels_2)
        # print(type(first_row.values[0:5].tolist()))
        # print(first_row.values[1])
        # print(second_row)
        # print(type(g))
        # input()
    if folder_name == MOZILLA_PROJ:
        bug_id_summary_ids_tuple_list = [(551591, 3, 4),
                                         (1388414, 0, 1), (697762, 0, 1), (1393563, 0, 1), (831452, 0, 1),
                                         (1611864, 0, 1), (641322, 1, 2), (1302671, 0, 1), (1698580, 1, 2)]
    else:
        bug_id_summary_ids_tuple_list = [(478512, 0, 1), (560060, 0, 1), (357540, 0, 1)]
    print(len(summary_pairs))
    summary_pairs = summary_pairs.filter_for_goal_model_instances(bug_id_summary_ids_tuple_list)
    summary_pairs.complete_vague_labels()
    print(len(summary_pairs))
    # print(summary_pairs.get_summary_pair_by_bug_id_summary_ids(1403460, 0, 1))
    FileUtil.dump_pickle(summary_pairs_filepath, summary_pairs)
