from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.path_util import PathUtil
from config import MOZILLA_PROJ, MOZILLA_URL, ECLIPSE_PROJ, ECLIPSE_URL


def convert_into_continuous_value(rankings):
    # rankings.sort()
    sorted_rankings = sorted(rankings)
    value_change_dict = dict()
    new_rankings = []
    start = 1
    for index, value in enumerate(sorted_rankings):
        # if index == 0:
        # if value != start:
        value_change_dict[value] = value_change_dict.get(value, start)
        if index < len(sorted_rankings) - 1:
            if value != sorted_rankings[index + 1]:
                start = start + 1
    for value in rankings:
        new_rankings.append(value_change_dict[value])
    # print(f'sorted_rankings:\t{sorted_rankings}')
    # if rankings != new_rankings:
    #     print(f'rankings:\t{rankings}')
    #     print(f'new_rankings:\t{new_rankings}')
    #     print('###############################')
    return new_rankings


def count_equal_value(rankings):
    rankings = convert_into_continuous_value(rankings)
    sorted_rankings = sorted(rankings)
    value_change_dict = dict()
    new_rankings = []
    for index, value in enumerate(sorted_rankings):
        if index == 0:
            value_change_dict[value] = value_change_dict.get(value, value)
        if value != sorted_rankings[index - 1]:
            value_change_dict[value] = value_change_dict.get(value, index + 1)
        else:
            value_change_dict[sorted_rankings[index - 1]] = value_change_dict.get(sorted_rankings[index - 1],
                                                                                  sorted_rankings[index - 1])
            value_change_dict[value] = value_change_dict.get(value, value_change_dict[sorted_rankings[index - 1]])
    for value in rankings:
        new_rankings.append(value_change_dict[value])
    # print(f'sorted_rankings:\t{sorted_rankings}')
    # # if rankings != new_rankings:
    # print(f'rankings:\t{rankings}')
    # print(f'new_rankings:\t{new_rankings}')
    # print('###############################')
    return new_rankings


if __name__ == "__main__":
    # foldername = MOZILLA_PROJ
    foldername = ECLIPSE_PROJ

    # is_continuous_value_flag = True
    is_continuous_value_flag = False

    if foldername == MOZILLA_PROJ:
        project_url = MOZILLA_URL
    else:
        project_url = ECLIPSE_URL

    # test_summary_pairs = FileUtil.load_pickle(
    #     PathUtil.get_sample_summary_pairs_for_manual_evaluation_filepath(foldername))
    # summaries_list = FileUtil.load_pickle(PathUtil.get_sample_summaries_list_for_manual_evaluation_filepath(foldername))
    # print(len(test_summary_pairs))
    # print(len(summaries_list))
    if foldername == MOZILLA_PROJ:
        rankings_pair_list = [([3, 6, 7, 3, 1, 3, 2], [2, 2, 2, 2, 1, 2, 3]),
                              ([3, 2, 1, 1, 1, 4, 2], [4, 3, 2, 2, 1, 4, 2]),
                              ([1, 2, 2, 2, 2, 1, 2], [4, 5, 2, 2, 3, 1, 2]),
                              ([4, 3, 3, 6, 3, 1, 5], [1, 4, 3, 6, 5, 2, 7]),
                              ([1, 1, 3, 1, 2, 1, 4], [2, 3, 4, 2, 1, 2, 4]),

                              ([7, 2, 4, 1, 3, 5, 6], [3, 7, 5, 1, 6, 4, 2]),
                              ([3, 2, 4, 7, 6, 1, 5], [5, 3, 3, 2, 4, 1, 3]),
                              ([4, 4, 3, 5, 1, 6, 2], [5, 5, 4, 2, 4, 1, 3]),
                              ([6, 3, 5, 4, 2, 1, 6], [2, 3, 4, 5, 3, 1, 2]),
                              ([2, 5, 4, 3, 6, 1, 7], [4, 5, 2, 3, 3, 1, 5]),

                              ([2, 6, 3, 4, 4, 5, 1], [1, 7, 4, 2, 5, 6, 3]),
                              ([4, 1, 3, 3, 2, 5, 6], [1, 6, 5, 3, 2, 4, 7]),
                              ([5, 7, 6, 2, 3, 1, 4], [2, 6, 7, 1, 5, 3, 4]),
                              ([5, 3, 6, 4, 2, 1, 7], [3, 2, 4, 3, 1, 2, 4]),
                              ([5, 6, 3, 7, 1, 2, 4], [2, 4, 3, 4, 6, 7, 4]),

                              ([4, 5, 3, 2, 1, 6, 7], [3, 3, 3, 3, 1, 3, 2]),
                              ([2, 4, 6, 3, 7, 1, 5], [3, 3, 3, 3, 1, 2, 3]),
                              ([5, 7, 4, 3, 2, 1, 6], [3, 3, 2, 3, 1, 1, 3]),
                              ([2, 5, 3, 6, 1, 4, 7], [3, 3, 3, 3, 1, 2, 3]),
                              ([6, 4, 2, 5, 3, 1, 7], [2, 2, 3, 3, 3, 1, 3])]
    else:
        rankings_pair_list = [([2, 4, 3, 3, 1, 5, 6], [6, 1, 7, 4, 3, 2, 5]),
                              ([3, 4, 4, 5, 1, 2, 6], [6, 3, 1, 5, 2, 4, 7]),
                              ([2, 5, 6, 4, 3, 1, 2], [2, 4, 5, 6, 3, 1, 5]),
                              ([5, 5, 2, 6, 3, 4, 1], [5, 3, 4, 2, 7, 1, 6]),
                              ([1, 5, 3, 2, 4, 1, 5], [1, 4, 3, 2, 4, 2, 5]),

                              ([1, 1, 2, 2, 6, 2, 2], [3, 5, 4, 6, 1, 2, 7]),
                              ([2, 3, 2, 2, 3, 1, 7], [6, 3, 4, 5, 2, 1, 7]),
                              ([3, 3, 2, 1, 2, 4, 1], [4, 7, 3, 1, 5, 6, 2]),
                              ([3, 3, 3, 2, 3, 1, 6], [3, 7, 5, 4, 1, 2, 6]),
                              ([2, 4, 1, 3, 1, 2, 2], [2, 3, 6, 4, 5, 7, 1])]

    new_rankings_pair_list = []
    for rankings_pair in rankings_pair_list:
        if is_continuous_value_flag:
            rankings_pair_0 = convert_into_continuous_value(rankings_pair[0])
            rankings_pair_1 = convert_into_continuous_value(rankings_pair[1])
            new_rankings_pair_list.append([rankings_pair_0, rankings_pair_1])
        else:
            rankings_pair_0 = count_equal_value(rankings_pair[0])
            rankings_pair_1 = count_equal_value(rankings_pair[1])
            new_rankings_pair_list.append([rankings_pair_0, rankings_pair_1])
    if is_continuous_value_flag:
        FileUtil.dump_pickle(PathUtil.get_manual_evaluation_continuous_rankings_result_filepath(foldername),
                             new_rankings_pair_list)
    else:
        FileUtil.dump_pickle(PathUtil.get_manual_evaluation_count_equal_rankings_result_filepath(foldername),
                             new_rankings_pair_list)
