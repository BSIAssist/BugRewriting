from bug_changing.types.placeholder import Placeholder
from bug_changing.utils.dataframe_util import DataFrameUtil
from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.list_util import ListUtil
from bug_changing.utils.path_util import PathUtil
from config import MOZILLA_PROJ, MOZILLA_URL, ECLIPSE_PROJ, ECLIPSE_URL


def get_summaries_cell_from_summary_list(summary_list):
    summaries_cell = ''
    for index, summary in enumerate(summary_list):
        summaries_cell = summaries_cell + f"{index + 1}: {summary}\n"
    return summaries_cell


def get_manual_evaluation_excel(test_summary_pairs, summaries_list, random_summaries_flag, excel_index, foldername):
    columns = ['SNO', 'Questions', 'Description', 'Type', 'Required', 'Answer Start', 'Answer', 'Answer End', 'Other']
    rows = []
    row_num = 0
    delimiter = '。'
    ranking_cell = f'Top-1{delimiter} Top-2{delimiter} Top-3{delimiter} Top-4{delimiter} Top-5{delimiter} ' \
                   f'Top-6{delimiter} Top-7'
    summaries_num_cell = f'Summary 1{delimiter}Summary 2{delimiter}Summary 3{delimiter}Summary 4{delimiter}' \
                         f'Summary 5{delimiter}Summary 6{delimiter}Summary 7{delimiter}'
    # answer_tuple_list = []

    note_cell = 'Note that if the quality of bug summaries is the same, you can have them ranked equally.'

    # personal info
    row_num = row_num + 1
    row = [row_num, 'Name', 'Please write your name here',
           'TEXT', 'TRUE', '', '', '', '']
    rows.append(row)

    row_num = row_num + 1
    row = [row_num, 'How many bug summaries have you ever written?',
           'If no, fill "0" here\n',
           'TEXT', 'TRUE', '', '', '', '']
    rows.append(row)

    row_num = row_num + 1
    row = [row_num, 'Task: Rank the given bug summaries of the bug report',
           'Bug Report Number: 5\n'
           'Time per Bug Report: 10 ~ 15 minutes\n'
           'Total Time: around 1 hour',
           'TITLE', 'TRUE', '', '', '', '']
    rows.append(row)

    # next section
    row_num = row_num + 1
    row = [row_num, f'No. 1 Bug', '',
           'SECTION', 'FALSE', '', '', '', '']
    rows.append(row)

    for index, test_summary_pair in enumerate(test_summary_pairs):
        # bug_link = f'{MOZILLA_URL}{test_summary_pair.bug.id}'
        # summaries_cell = f'{generation_answers[index].strip()}{delimiter} ' \
        #                  f'{rewriting_answers[index].strip()}{delimiter} ' \
        #                  f'{rewriting_with_hg_answers[index].strip()}{delimiter} ' \
        #                  f'{kg_without_rewritten_instances_answers[index].rewritten_summary.strip()}{delimiter} ' \
        #                  f'{kg_with_rewritten_instances_answers[index].rewritten_summary.strip()}{delimiter} ' \
        #                  f'{test_summary_pair.add_summary.text.strip()}{delimiter}'
        # summary_list = [generation_answers[index].strip(), generation_with_hg_answers[index].strip(),
        #                 rewriting_answers[index].strip(), rewriting_with_hg_answers[index].strip(),
        #                 kg_without_rewritten_instances_answers[index].rewritten_summary.strip(),
        #                 kg_with_rewritten_instances_answers[index].rewritten_summary.strip(),
        #                 test_summary_pair.add_summary.text.strip()]
        summaries = summaries_list[index]
        if random_summaries_flag:
            summaries = ListUtil.random_list(summaries)

        summaries_cell = get_summaries_cell_from_summary_list(summaries)

        # summaries_cell = f'1: {generation_answers[index].strip()}\n' \
        #                  f'2: {generation_with_hg_answers[index].strip()}\n' \
        #                  f'3: {rewriting_answers[index].strip()}\n' \
        #                  f'4: {rewriting_with_hg_answers[index].strip()}\n' \
        #                  f'5: {kg_without_rewritten_instances_answers[index].rewritten_summary.strip()}\n' \
        #                  f'6: {kg_with_rewritten_instances_answers[index].rewritten_summary.strip()}\n' \
        #                  f'7: {test_summary_pair.add_summary.text.strip()}'

        # instruction
        row_num = row_num + 1
        row = [row_num, 'Preparation',
               # f'Please rank the given bug summaries by the following guidelines:\n'
               f'\ta. find and open the corresponding bug description from the "bug_description_{excel_index}" folder for viewing the bug description\n'
               f'\tb. for ease of viewing: if only one screen, please use the split screen function '
               f'(the bug description on the left side and the survey on the right side of the screen) '
               f'and if more than one screen, please put the bug description and the survey into different screens',
               # f'\ta. click the bug link to open the bug report for viewing the bug description\n'
               # f'\tb. for ease of viewing: if only one screen, please use the split screen function '
               # f'(the pop-up bug report on the left side and the survey on the right side of the screen) '
               # f'and if more than one screen, please put the pop-up bug report and the survey into different screens',
               # f'\tc. read the initial bug summary and bug description from the bug report.',
               # f'A good bug summary should be specific, concise and easy-to-understand.',
               'TITLE', 'TRUE', '', '', '', '']
        rows.append(row)

        # task
        row_num = row_num + 1
        row = [row_num, 'Task',
               f'please rank the given bug summaries by the guidelines.\n\n'
               f'The initial bug summary is provided by the bug reporter, which has flaws and need to be further optimized.\n'
               f'The given bug summaries are provided by different approaches.\n\n'
               # f'\ta. generation based on "Bug Description"\n'
               # f'\tb. rewriting based on the "Initial Bug Summary" and "Bug Description"\n\n'
               # f'The given bug summaries are provided through two main sources: \n'
               # f'\ta. generation based on "Bug Description"\n'
               # f'\tb. rewriting based on the "Initial Bug Summary" and "Bug Description"\n\n'
               f'!!! Note that the given bug summaries are in random order, '
               f'please rank them based only on the "Initial Bug Summary", "Bug Description" and the given "Guidelines"!!!',
               'TITLE', 'TRUE', '', '', '', '']
        rows.append(row)

        # bug info
        row_num = row_num + 1
        row = [row_num, 'Bug Report Info',
               # f'Bug Link: {project_url}{test_summary_pair.bug.id}\n'
               f'Initial Bug Summary: {test_summary_pair.rm_summary.text.strip()}\n'
               f'Bug description: shown in the "bug_{index+1}" from "bug_description_{excel_index}" folder',
               # f'Bug description: shown in the "Description" part from the Bug Link',
               'TITLE', 'TRUE', '', '', '', '']
        rows.append(row)

        # specific what
        row_num = row_num + 1
        row = [row_num, f'{Placeholder.SPECIFIC} - what',
               f'A good bug summary should be {Placeholder.SPECIFIC}, which contains what goes wrong to the system or software, '
               f'namely {Placeholder.ACTUAL_BEHAVIOR} '
               f'(the observed behavior of the system or software being reported as having a bug or issue) '
               f'instead of {Placeholder.SUGGESTED_SOLUTION} (the conjecture or proposed fix for the bug).\n\n'
               # f'{Placeholder.SUGGESTED_SOLUTION}: the conjecture or proposed fix for the bug\n'
               # f'{Placeholder.ACTUAL_BEHAVIOR}: the observed behavior of the system or software being reported as having a bug or issue\n\n'

               f'Please rank these bug summaries based on:\n'
               f'\ta. don\'t contain {Placeholder.SUGGESTED_SOLUTION}\n'
               f'\tb. contain {Placeholder.ACTUAL_BEHAVIOR}, as specific as possible\n\n'
               f'Initial Bug Summary: {test_summary_pair.rm_summary.text.strip()}\n\n'
               f'The bug summaries needing to be ranked are as follows:\n{summaries_cell}',
               'TITLE', 'TRUE', f'', f'', '', '']
        rows.append(row)

        row_num = row_num + 1
        row = [row_num, f'Please rank these bug summaries based on "{Placeholder.SPECIFIC} - what"',
               f'{note_cell}',
               'GRID', 'TRUE', f'{summaries_num_cell}', f'{ranking_cell}', '', '']
        rows.append(row)

        # specific when
        row_num = row_num + 1
        row = [row_num, f'{Placeholder.SPECIFIC} - when',
               f'A good bug summary should be {Placeholder.SPECIFIC}, which contains when triggers the bug, namely '
               f'{Placeholder.TRIGGER_ACTION} '
               f'(the brief description of the action or event that causes the bug to occur)\n\n'
               # f'{Placeholder.SUGGESTED_SOLUTION}: the conjecture or proposed fix for the bug\n'
               # f'{Placeholder.ACTUAL_BEHAVIOR}: the observed behavior of the system or software being reported as having a bug or issue\n\n'

               f'Please rank these bug summaries based on:\n'
               f'\ta. if bug description has {Placeholder.TRIGGER_ACTION}, contain {Placeholder.TRIGGER_ACTION}, as specific as possible\n\n'
               f'Initial Bug Summary: {test_summary_pair.rm_summary.text.strip()}\n\n'
               f'The bug summaries needing to be ranked are as follows:\n{summaries_cell}',
               'TITLE', 'TRUE', f'', f'', '', '']
        rows.append(row)

        row_num = row_num + 1
        row = [row_num, f'Please rank these bug summaries based on "{Placeholder.SPECIFIC} - when"',
               f'{note_cell}',
               'GRID', 'TRUE', f'{summaries_num_cell}', f'{ranking_cell}', '', '']
        rows.append(row)
        # row_num = row_num + 1
        # row = [row_num, 'Summaries',
        #        f'{summaries_cell}',
        #        'TITLE', 'TRUE', f'', f'']
        # rows.append(row)
        # specific where
        row_num = row_num + 1
        row = [row_num, f'{Placeholder.SPECIFIC} - where',
               f'A good bug summary should be {Placeholder.SPECIFIC}, which contains where the bug happenes, namely '
               f'{Placeholder.PLATFORM} '
               f'(the specific operating system, hardware, or other environment in which the system or application is being used) '
               f'and {Placeholder.COMPONENT} '
               f'(the specific part or subsystem of the system or application where the issue is occurring).\n\n'

               f'Please rank these bug summaries based on:\n'
               f'\ta. if bug description has {Placeholder.PLATFORM}, contain {Placeholder.PLATFORM}\n'
               f'\tb. if bug description has {Placeholder.COMPONENT}, contain {Placeholder.COMPONENT}\n\n'
               f'Initial Bug Summary: {test_summary_pair.rm_summary.text.strip()}\n\n'
               f'The bug summaries needing to be ranked are as follows:\n{summaries_cell}',
               'TITLE', 'TRUE', f'', f'', '', '']
        rows.append(row)

        row_num = row_num + 1
        row = [row_num, f'Please rank these bug summaries based on "{Placeholder.SPECIFIC} - where"',
               f'{note_cell}',
               'GRID', 'TRUE', f'{summaries_num_cell}', f'{ranking_cell}', '', '']
        rows.append(row)
        # concise
        row_num = row_num + 1
        row = [row_num, f'{Placeholder.CONCISE}',
               f'A good bug summary should be {Placeholder.CONCISE}, '
               f'which includes information all related to the bug itself, namely '
               f'be objective (don\'t use {Placeholder.PERSONAL_PRONOUN} and don\'t include emotional expressions), '
               f'be polite (don\'t use {Placeholder.OFFENCE}), '
               f'be definite (describe the actual situation that occurred, rather than what seems to have happened) '
               f'and be not too lengthy.\n\n'

               f'Please rank these bug summaries based on:\n'
               f'\ta. don\'t contain {Placeholder.PERSONAL_PRONOUN}\n'
               f'\tb. avoid describing {Placeholder.EMOTIONAL_REACTION}\n'
               f'\tc. don\'t use {Placeholder.OFFENCE}\n'
               f'\td. don\'t use {Placeholder.WISHY_WASHY_WORD}\n\n'

               f'Initial Bug Summary: {test_summary_pair.rm_summary.text.strip()}\n\n'
               f'The bug summaries needing to be ranked are as follows:\n{summaries_cell}',
               'TITLE', 'TRUE', f'', f'', '', '']
        rows.append(row)

        row_num = row_num + 1
        row = [row_num, f'Please rank these bug summaries based on "{Placeholder.CONCISE}"',
               f'{note_cell}',
               'GRID', 'TRUE', f'{summaries_num_cell}', f'{ranking_cell}', '', '']
        rows.append(row)
        # easy-to-understand
        row_num = row_num + 1
        row = [row_num, f'{Placeholder.UNDERSTANDABLE}',
               f'A good bug summary should be {Placeholder.UNDERSTANDABLE}, which uses correct spelling and grammar. '
               f'Besides, use declarative sentences instead of interrogative sentences and '
               f'use the present tense instead of the past tense. Be readable.\n\n'
               f'Please rank these bug summaries based on:\n'
               f'\ta. don\'t have {Placeholder.SPELLING_ERROR} and {Placeholder.SYNTAX_ERROR}\n'
               f'\tb. use {Placeholder.DECLARATIVE_STATEMENT}\n'
               f'\tc. use {Placeholder.PRESENT_TENSE}\n\n'

               f'Initial Bug Summary: {test_summary_pair.rm_summary.text.strip()}\n\n'
               f'The bug summaries needing to be ranked are as follows:\n{summaries_cell}',
               'TITLE', 'TRUE', f'', f'', '', '']
        rows.append(row)

        row_num = row_num + 1
        row = [row_num, f'Please rank these bug summaries based on "{Placeholder.UNDERSTANDABLE}"',
               f'{note_cell}',
               'GRID', 'TRUE', f'{summaries_num_cell}', f'{ranking_cell}', '', '']
        rows.append(row)
        # overall
        row_num = row_num + 1
        row = [row_num, 'Overall',
               f'In conclusion, a good bug summary needs to meet many different requirements, '
               f'and these requirements also have different priorities. '
               f'Generally, the priorities are '
               f'{Placeholder.SPECIFIC} > {Placeholder.CONCISE} > {Placeholder.UNDERSTANDABLE}. '
               f'However, this is not absolute, and it still depends on the specific situation.\n\n'
               
               f'Note that you can refer to the previous rankings '
               f'to determine the final overall ranking of bug summaries.\n'
               f'!!! But "must not" simply add these rankings together and calculate the average!!! \n\n'
               
               f'Because the weights of different requirements vary, '
               f'and the quality difference between two bug summaries with adjacent rankings may be significant, '
               f'simply adding and calculating the average cannot take into account these two situations.\n\n'
               # f'The requirements in "{Placeholder.SPECIFIC}" are also different: '
               # f'{Placeholder.SPECIFIC} - what > {Placeholder.SPECIFIC} - when > {Placeholder.SPECIFIC} - where\n\n'
               # 
               # f'Please rank these bug summaries based on the priority:\n'
               # f'\ta. {Placeholder.SPECIFIC} - what\n'
               # f'\tb. {Placeholder.SPECIFIC} - when\n'
               # f'\tc. {Placeholder.SPECIFIC} - where\n'
               # f'\td. {Placeholder.CONCISE}\n'
               # f'\te. {Placeholder.UNDERSTANDABLE}\n\n'
               f'Please rank these bug summaries from an overall perspective:\n\n'
               f'Initial Bug Summary: {test_summary_pair.rm_summary.text.strip()}\n\n'
               f'The bug summaries needing to be ranked are as follows:\n{summaries_cell}',
               'TITLE', 'TRUE', f'', f'', '', '']
        rows.append(row)

        row_num = row_num + 1
        row = [row_num, 'Please rank these bug summaries based on "Overall"',
               f'{note_cell}',
               'GRID', 'TRUE', f'{summaries_num_cell}', f'{ranking_cell}', '', '']
        rows.append(row)

        # after survey

        row_num = row_num + 1
        row = [row_num, 'Are there any parts of the other given summaries that are better than those in the Top-1 '
                        'summary of your overall ranking, which can be used to optimize the Top-1 summary?',
               f'{summaries_cell}', 'MULTIPLE CHOICE', 'TRUE', f'Yes', f'No', '', f'TRUE']
        rows.append(row)

        row_num = row_num + 1
        row = [row_num, 'Can the Top-1 summary of your overall ranking be further optimized?',
               f'Initial Bug Summary: {test_summary_pair.rm_summary.text.strip()}\n\n'
               f'{summaries_cell}',
               'MULTIPLE CHOICE', 'TRUE', f'Yes', f'No', '', f'TRUE']
        rows.append(row)

        # row_num = row_num + 1
        # row = [row_num,
        #        'Please write a bug summary for this bug report combining the advantages of the given bug summaries\n',
        #        f'{summaries_cell}',
        #        'PARAGRAPH', 'TRUE', f'', f'', '']
        # rows.append(row)
        row_num = row_num + 1
        row = [row_num,
               'Please write a bug summary for this bug report',
               f'Initial Bug Summary: {test_summary_pair.rm_summary.text.strip()}\n\n'
               f'{summaries_cell}',
               'PARAGRAPH', 'TRUE', f'', f'', '', '']
        rows.append(row)

        row_num = row_num + 1
        row = [row_num, 'Does the bug summary you wrote refer to and combine the advantages of these given summaries?',
               f'Initial Bug Summary: {test_summary_pair.rm_summary.text.strip()}\n\n'
               f'{summaries_cell}',
               'MULTIPLE CHOICE', 'TRUE', f'Yes', f'No', '', f'TRUE']
        rows.append(row)

        row_num = row_num + 1
        row = [row_num,
               'Does the bug summary you wrote refer to the content from the bug description '
               'but not in the given bug summaries?',
               f'Initial Bug Summary: {test_summary_pair.rm_summary.text.strip()}\n\n'
               f'{summaries_cell}',
               'MULTIPLE CHOICE', 'TRUE', f'Yes', f'No', '', f'TRUE']
        rows.append(row)

        row_num = row_num + 1
        row = [row_num, 'Is the bug summary you wrote better than the Top-1 bug summary of your overall ranking?', f'{summaries_cell}',
               'MULTIPLE CHOICE', 'TRUE', f'Yes', f'No', f'Equal to the Top-1 bug summary', f'TRUE']
        rows.append(row)

        row_num = row_num + 1
        row = [row_num,
               'Which way do you prefer to write the bug summary, with or without these given bug summaries as '
               'reference?',
               f'Initial Bug Summary: {test_summary_pair.rm_summary.text.strip()}\n\n'
               f'{summaries_cell}',
               'MULTIPLE CHOICE', 'TRUE', f'With Reference', f'Without Reference', '', f'TRUE']
        rows.append(row)

        row_num = row_num + 1
        row = [row_num,
               'If writing a bug summary without these given bug summaries as reference, '
               'could you write a bug summary with the same or higher '
               'quality as the Top-1 bug summary of your overall ranking?',
               f'Initial Bug Summary: {test_summary_pair.rm_summary.text.strip()}\n\n'
               f'{summaries_cell}',
               'MULTIPLE CHOICE', 'TRUE', f'Yes', f'No', '', f'TRUE']
        rows.append(row)

        # next section
        if index + 1 + 1 <= len(test_summary_pairs):
            row_num = row_num + 1
            row = [row_num, f'No. {index + 1 + 1} Bug', '',
                   'SECTION', 'FALSE', '', '', '', '']
            rows.append(row)
    row_num = row_num + 1
    row = [row_num, f'Post Survey', '',
           'SECTION', 'FALSE', '', '', '', '']
    rows.append(row)

    row_num = row_num + 1
    row = [row_num, f'Can this survey provide a comprehensive understanding of what makes a good bug summary, '
                    f'and enable one to know how to write a good bug summary?', '',
           'MULTIPLE CHOICE', 'TRUE', 'Yes', 'No', '', f'TRUE']
    rows.append(row)

    # row_num = row_num + 1
    # row = [row_num, f'Can the given summaries help write high-quality bug summaries?', '',
    #        'MULTIPLE CHOICE', 'TRUE', 'Yes', 'No', '', f'TRUE']
    # rows.append(row)

    df = DataFrameUtil.convert_data_into_dataframe(columns, rows)
    # print(PathUtil.get_manual_evaluation_excel_filepath(foldername, excel_index))
    DataFrameUtil.write_df_into_excel(PathUtil.get_manual_evaluation_excel_filepath(foldername, excel_index),
                                      df, f'{foldername}')


if __name__ == "__main__":
    foldername = MOZILLA_PROJ
    # foldername = ECLIPSE_PROJ
    # sample_summaries_flag = True
    # sample_summaries_num = 15
    children_sample_num = 5
    random_summaries_flag = True
    # random_summaries_flag = False
    if foldername == MOZILLA_PROJ:
        project_url = MOZILLA_URL
    else:
        project_url = ECLIPSE_URL

    test_summary_pairs = FileUtil.load_pickle(
        PathUtil.get_sample_summary_pairs_for_manual_evaluation_filepath(foldername))
    summaries_list = FileUtil.load_pickle(PathUtil.get_sample_summaries_list_for_manual_evaluation_filepath(foldername))

    summary_pairs_list = test_summary_pairs.split_summary_pairs_by_children_list_len(children_sample_num)
    # print(len(summary_pairs_list))
    summaries_list_list = ListUtil.list_of_groups(summaries_list, children_sample_num)
    # print(len(summaries_list_list))

    for index_i, summary_pairs in enumerate(summary_pairs_list):
        # print(index_i)
        summaries_list = summaries_list_list[index_i]
        get_manual_evaluation_excel(summary_pairs, summaries_list, random_summaries_flag, index_i, foldername)
    # answer_tuple_list.append((generation_answers[index].strip(),
    #                           rewriting_answers[index].strip(), rewriting_with_hg_answers[index].strip(),
    #                           kg_without_rewritten_instances_answers[index].rewritten_summary.strip(),
    #                           kg_with_rewritten_instances_answers[index].rewritten_summary.strip(),
    #                           test_summary_pair.add_summary.text.strip()))
    # print(generation_answers[index].strip())
    # print(rewriting_answers[index].strip())
    # print(rewriting_with_hg_answers[index].strip())
    # print(kg_without_rewritten_instances_answers[index].rewritten_summary.strip())
    # print(kg_with_rewritten_instances_answers[index].rewritten_summary.strip())
    # print(test_summary_pair.add_summary.text.strip())
    # input()
