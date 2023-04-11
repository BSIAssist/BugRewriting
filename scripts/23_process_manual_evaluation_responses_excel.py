import re

from bug_changing.types.placeholder import Placeholder
from bug_changing.utils.dataframe_util import DataFrameUtil
from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.list_util import ListUtil
from bug_changing.utils.path_util import PathUtil
from config import MOZILLA_PROJ, MOZILLA_URL, ECLIPSE_PROJ, ECLIPSE_URL, OUTPUT_DIR

import pandas as pd


def get_summaries_from_manual_evaluation_excel(manual_evaluation_df, row_column_list, index_j):
    row, column = row_column_list[index_j]
    column = manual_evaluation_df.columns[list(manual_evaluation_df.columns).index(column) + 1]
    value = manual_evaluation_df.iloc[row][column]
    return value


def convert_summaries_from_manual_evaluation_excel_into_list(summaries):
    summaries = summaries.strip().splitlines()
    summary_list = []
    for summary in summaries:
        summary = str(re.sub(r'^\d:', '', summary)).strip()
        summary_list.append(summary)
    return summary_list


def convert_top_n_into_num(top_n):
    top_n = top_n.strip()
    n = int(top_n.replace('Top-', ''))
    return n


def get_rankings_from_manual_evaluation_response_excel(manual_evaluation_responses_df, index_j):
    if index_j == 0:
        rankings = manual_evaluation_responses_df.loc[:,
                   'Please rank these bug summaries based on "specific - what" [Summary 1]':'Please rank these bug summaries based on "Overall" [Summary 7]']
    else:
        rankings = manual_evaluation_responses_df.loc[:,
                   f'Please rank these bug summaries based on "specific - what" [Summary 1].{index_j}':f'Please rank these bug summaries based on "Overall" [Summary 7].{index_j}']
    rankings = rankings.reset_index()  # make sure indexes pair with number of rows
    numbers_list = []
    for index, row in rankings.iterrows():
        numbers = []
        row = row.values.tolist()[1:]
        for top_n in row:
            numbers.append(convert_top_n_into_num(top_n))
        numbers_list.append(numbers)
        # print(row)
        # print(numbers)
        # print(type(row))
    return numbers_list


def combine_summaries_numbers_list(summaries, numbers_list):
    if len(numbers_list) == 2:
        # [number pair, number pair, number pair, ..., ]
        numbers = ListUtil.zip_two_lists(numbers_list[0], numbers_list[1])
    else:
        # elif len(numbers_list) == 1:
        # [number, number, ..., ]
        numbers = numbers_list[0]
    children_numbers_list = ListUtil.list_of_groups(numbers, len(summaries))
    # result = {f'{Placeholder.SPECIFIC}-what': None,
    #                f'{Placeholder.SPECIFIC}-when': None,
    #                f'{Placeholder.SPECIFIC}-where': None,
    #                f'{Placeholder.CONCISE}': None,
    #                f'{Placeholder.UNDERSTANDABLE}': None,
    #                'Overall': None}
    summary_rank_pairs_list = []
    for index, children_numbers in enumerate(children_numbers_list):
        summary_rank_pairs_list.append(ListUtil.zip_two_lists(summaries, children_numbers))
    return summary_rank_pairs_list


def sort_summary_rank_pairs_list_by_regular_order_summaries(summary_rank_pairs_list, regular_order_summaries):
    sorted_list = []
    for summary_rank_pairs in summary_rank_pairs_list:
        sorted_list.append(ListUtil.sort_pair_list_by_specific_order(summary_rank_pairs, regular_order_summaries, 0))
    return sorted_list


if __name__ == "__main__":
    # foldername = MOZILLA_PROJ
    foldername = ECLIPSE_PROJ
    # sample_summaries_num = 15
    children_sample_num = 5
    if foldername == MOZILLA_PROJ:
        project_url = MOZILLA_URL
    else:
        project_url = ECLIPSE_URL

    # test_summary_pairs = FileUtil.load_pickle(
    #     PathUtil.get_sample_summary_pairs_for_manual_evaluation_filepath(foldername))
    summaries_list = FileUtil.load_pickle(PathUtil.get_sample_summaries_list_for_manual_evaluation_filepath(foldername))

    # summary_pairs_list = test_summary_pairs.split_summary_pairs_by_children_list_len(children_sample_num)
    # print(len(summary_pairs_list))
    summaries_list_list = ListUtil.list_of_groups(summaries_list, children_sample_num)
    # print(len(summaries_list_list))

    for index_i, summaries_list in enumerate(summaries_list_list):
        manual_evaluation_responses_df = pd.read_excel(
            PathUtil.get_manual_evaluation_responses_excel_filepath(foldername, index_i),
            sheet_name=f'Form Responses {index_i + 1}')
        manual_evaluation_df = pd.read_excel(
            PathUtil.get_manual_evaluation_excel_filepath(foldername, index_i),
            sheet_name=f'{foldername}')

        summaries_row_column_list = DataFrameUtil.get_row_column_from_value(manual_evaluation_df,
                                                                            'Are there any parts of the other given summaries that are better than those in the Top-1 summary of your overall ranking, which can be used to optimize the Top-1 summary?')
        # print(manual_evaluation_responses_df.columns)
        # print(manual_evaluation_responses_df.loc[:, 'Please rank these bug summaries based on "specific - what" [Summary 1]':'Please rank these bug summaries based on "Overall" [Summary 7]'])
        # summary_pairs = summary_pairs_list[index]
        # print(index_i)
        for index_j, regular_order_summaries in enumerate(summaries_list):
            # get summaries in excel order
            summaries = get_summaries_from_manual_evaluation_excel(manual_evaluation_df, summaries_row_column_list,
                                                                   index_j)
            summaries = convert_summaries_from_manual_evaluation_excel_into_list(summaries)
            print(summaries)
            # print(type(summaries))
            # print(manual_evaluation_responses_df['Please rank these bug summaries based on "specific - what" [Summary 1]'].iloc[:, index_j])
            # get rankings
            numbers_list = get_rankings_from_manual_evaluation_response_excel(manual_evaluation_responses_df, index_j)
            print(numbers_list)
            summary_number_pairs_list = combine_summaries_numbers_list(summaries, numbers_list)
            summary_number_pairs_list = sort_summary_rank_pairs_list_by_regular_order_summaries(summary_number_pairs_list, regular_order_summaries)
            for summary_number_pairs in summary_number_pairs_list:
                for inner_index, summary_number_pair in enumerate(summary_number_pairs):
                    # print(f"regular: {regular_order_summaries[inner_index]}")
                    # print(f"result: {summary_number_pair}")
                    print(f"{summary_number_pair[0]}\t{summary_number_pair[1][0]}\t{summary_number_pair[1][1]}")
                print("#######################")
            print("**********************************************************************")
        input()
