from pathlib import Path

from tqdm import tqdm
from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.path_util import PathUtil
import Levenshtein as lv
import pandas as pd

from config import OUTPUT_DIR


def display_bugs_with_summary_reformulation(bugs, folder_name='mozilla'):
    print(f"\tbug num: {bugs.get_length()}")
    for bug in tqdm(bugs, ascii=True):
        if folder_name == 'mozilla':
            print(f"\t\thttps://bugzilla.mozilla.org/show_bug.cgi?id={bug.id}")
        elif folder_name == 'eclipse':
            print(f"\t\thttps://bugs.eclipse.org/bugs/show_bug.cgi?id={bug.id}")
        print(f"\t\tbug type: {bug.type}")
        # print(f"\t\t\tinitial summary: {bug.summary_path[0]}")
        # print(f"\t\t\tfinal   summary: {bug.summary_path[-1]}")
        # print(f'\t\t\tadded tokens: {tokens}')
        # print('\n')
        for history in bug.history_list:
            for change in history.changes:
                if change.field_name == 'summary':
                    if history.who == bug.reporter and history.who == bug.assignee:
                        print(f'\t\t\treporter & assignee (change summary): {history.who}')
                    elif history.who == bug.reporter:
                        print(f'\t\t\treporter (change summary): {history.who}')
                    elif history.who == bug.assignee:
                        print(f'\t\t\tassignee (change summary): {history.who}')
                    else:
                        print(f'\t\t\tparticipant (change summary): {history.who}')
                    if bug.closed_time and history.when_hardgoals > bug.closed_time:
                        print(f'\t\t\tsummary changed after closing the bug')
                    elif bug.closed_time and history.when_hardgoals == bug.closed_time:
                        print(f'\t\t\tsummary changed when closing the bug')
                    print(f'\t\t\tremoved summary: {change.removed}')
                    print(f'\t\t\tadded   summary: {change.added}')
                    edit_distance = lv.distance(change.added, change.removed)
                    print(f'\t\t\tedit   distance: {edit_distance}')
                    for comment in bug.comments:
                        if comment.creation_time == history.when_hardgoals and comment.author == history.who:
                            print(f'\t\t\tcomment: {comment.text}')
                    print('\n')


def convert_bugs_into_dataframe(bugs, folder_name='mozilla'):
    columns = ['bugID', 'removed summary id', 'bug link', 'removed summary', 'added summary', 'edit distance',
               'up to date']

    for index in range(5):
        columns.extend(['change from', 'change what', 'change for'])
    rows = []
    for bug in bugs:
        if folder_name == 'mozilla':
            bug_link = f"https://bugzilla.mozilla.org/show_bug.cgi?id={bug.id}"
        else:
            bug_link = f"https://bugs.eclipse.org/bugs/show_bug.cgi?id={bug.id}"
        for index, summary in enumerate(bug.summary_path):
            if index != len(bug.summary_path) - 1:
                next_summary = bug.summary_path[index + 1]
                edit_distance = lv.distance(summary.text, next_summary.text)
                row = [bug.id, summary.id, bug_link, summary.text, next_summary.text, edit_distance]
                for add_column in range(5):
                    row.extend(['', '', ''])
                row.append('')
                rows.append(row)
    df = pd.DataFrame(rows, columns=columns)
    return df


def convert_bugs_into_dataframe_from_history(bugs, folder_name='mozilla'):
    columns = ['bugID', 'rm_sum_id', 'bug_link', 'who', 'when', 'sync_comment', 'rm_summary',
               'add_summary', 'edit distance', 'up to date']
    for _ in range(5):
        columns.extend(['change from', 'change what', 'change for'])
    rows = []
    for bug in bugs:

        if folder_name == 'mozilla':
            bug_link = f"https://bugzilla.mozilla.org/show_bug.cgi?id={bug.id}"
        else:
            bug_link = f"https://bugs.eclipse.org/bugs/show_bug.cgi?id={bug.id}"
        summary_index = 0
        for history in bug.history_list:
            for change in history.changes:
                if change.field_name == 'summary':
                    when = ''
                    row = []
                    if history.who == bug.reporter and history.who == bug.assignee:
                        who = 'reporter & assignee'
                    elif history.who == bug.reporter:
                        who = 'reporter'
                    elif history.who == bug.assignee:
                        who = 'assignee'
                    else:
                        who = 'participant'
                    if bug.closed_time and history.when > bug.closed_time:
                        when = 'after closing'
                    elif bug.closed_time and history.when == bug.closed_time:
                        when = 'when closing'
                    removed_summary = change.removed
                    added_summary = change.added
                    edit_distance = lv.distance(added_summary, removed_summary)
                    sync_comment = ''
                    for comment in bug.comments:
                        if comment.creation_time == history.when and comment.author == history.who:
                            sync_comment = comment.text

                    row.extend([bug.id, summary_index, bug_link, who, when, sync_comment,
                                removed_summary, added_summary, edit_distance])

                    for _ in range(5):
                        row.extend(['', '', ''])
                    row.append('')
                    rows.append(row)
                    summary_index = summary_index + 1

        # rows.append(row)
    df = pd.DataFrame(rows, columns=columns)
    return df


if __name__ == "__main__":
    folder_name = 'mozilla'  # 382
    # folder_name = 'eclipse'  # 380

    bugs = FileUtil.load_pickle(PathUtil.get_bugs_with_summary_reformulation_filepath(folder_name))
    # bugs = bugs.get_summary_reformulation_bugs()

    sample_num = 380
    sample_bugs = bugs.random_sample_bugs(sample_num)
    sample_bugs_1, sample_bugs_2 = sample_bugs.split_dataset_by_summary_rewritten_num(rewritten_num=2)
    # print(f"sample bugs with once summary rewriting: {sample_bugs_1.get_length()}")
    # print(f"sample bugs with more than once summary rewriting: {sample_bugs_2.get_length()}")
    # display_bugs_with_summary_reformulation(sample_bugs, folder_name)

    df1 = convert_bugs_into_dataframe_from_history(sample_bugs_1, folder_name)
    df2 = convert_bugs_into_dataframe_from_history(sample_bugs_2, folder_name)
    with pd.ExcelWriter(Path(OUTPUT_DIR, folder_name, f'empirical_dataset.xlsx')) as writer:
        df1.to_excel(writer, sheet_name=f'once_{sample_bugs_1.get_length()}')
        df2.to_excel(writer, sheet_name=f'more_than_once_{sample_bugs_2.get_length()}')
    # df.to_excel(Path(OUTPUT_DIR, f'empirical_{folder_name}_dataset.xlsx'), sheet_name='more_than_once')

    FileUtil.dump_pickle(Path(OUTPUT_DIR, folder_name, 'empirical_sample_bugs.json'), sample_bugs)

    # df1 = convert_bugs_into_dataframe(sample_bugs_1)
    # df2 = convert_bugs_into_dataframe(sample_bugs_2)
    # with pd.ExcelWriter(Path(OUTPUT_DIR, folder_name, f'empirical_dataset_test.xlsx')) as writer:
    #     df1.to_excel(writer, sheet_name='once')
    #     df2.to_excel(writer, sheet_name='more_than_once')
