from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.path_util import PathUtil
from bug_changing.utils.plot_util import PlotUtil
from config import MOZILLA_PROJ, MOZILLA_URL, ECLIPSE_PROJ, ECLIPSE_URL
import pandas as pd
from statistics import mean
import seaborn as sns
import matplotlib.pyplot as plt


def combine_rankings_pair_list(rankings_pair_list):
    rankings_0 = []
    rankings_1 = []
    for rankings_pair in rankings_pair_list:
        print(rankings_pair[0])
        print(rankings_pair[1])
        print("******")
        rankings_0.extend(rankings_pair[0])
        rankings_1.extend(rankings_pair[1])
    print("#################")
    print(rankings_0)
    print(rankings_1)
    return rankings_0, rankings_1


def get_specific_summary_ranking_pairs(rankings_pair_list, specific_summary_index):
    """
    get specific summary ranking pairs, such as
    if specific_summary_index == 4:
        it is kg_without_instances summary ranking_pairs [(ranking_0, ranking_1), ...]
    Args:
        rankings_pair_list ():
        specific_summary_index ():

    Returns:

    """
    specific_ranking_pairs = []
    for index, rankings_pair in enumerate(rankings_pair_list):
        rankings_0 = rankings_pair[0]
        rankings_1 = rankings_pair[1]
        specific_ranking_0 = rankings_0[specific_summary_index]
        specific_ranking_1 = rankings_1[specific_summary_index]
        specific_ranking_pairs.append((specific_ranking_0, specific_ranking_1))
    return specific_ranking_pairs


def get_kg_summary_ranking_pairs(rankings_pair_list):
    """
    @todo: need to change, which have problems on
    if kg_without_instances and kg_with_instances:
        yes
    or
    if kg_without_instances or kg_with_instances:
        yes
    Args:
        rankings_pair_list ():

    Returns:

    """
    kg_summary_ranking_pairs = []
    kg_without_instances_ranking_pairs = get_specific_summary_ranking_pairs(rankings_pair_list, 4)
    kg_with_instances_ranking_pairs = get_specific_summary_ranking_pairs(rankings_pair_list, 5)
    for index, kg_without_instances_ranking_pair in enumerate(kg_without_instances_ranking_pairs):
        kg_with_instances_ranking_pair = kg_with_instances_ranking_pairs[index]
        if kg_without_instances_ranking_pair[0] == 1 or kg_with_instances_ranking_pair[0] == 1:
            kg_ranking_pair_0 = 1
        else:
            kg_ranking_pair_0 = 0
        if kg_without_instances_ranking_pair[1] == 1 or kg_with_instances_ranking_pair[1] == 1:
            kg_ranking_pair_1 = 1
        else:
            kg_ranking_pair_1 = 0
        kg_summary_ranking_pairs.append((kg_ranking_pair_0, kg_ranking_pair_1))
    return kg_summary_ranking_pairs


def calculate_top_1_for_ranking_pairs(specific_ranking_pairs):
    both_top_1 = []
    either_top_1 = []
    neither_top_1 = []
    for index, ranking_pair in enumerate(specific_ranking_pairs):
        ranking_0 = ranking_pair[0]
        ranking_1 = ranking_pair[1]
        if ranking_0 == 1 and ranking_1 == 1:
            both_top_1.append((index, ranking_pair))
        elif ranking_0 == 1 or ranking_1 == 1:
            either_top_1.append((index, ranking_pair))
        else:
            neither_top_1.append((index, ranking_pair))
    print(f"both_top_1: {len(both_top_1)}")
    print(f"either_top_1: {len(either_top_1)}")
    print(f"neither_top_1: {len(neither_top_1)}")


def calculate_top_1(rankings_pair_list):
    generation_ranking_pair_list = get_specific_summary_ranking_pairs(rankings_pair_list, 0)
    print('generation_ranking_pair_list')
    calculate_top_1_for_ranking_pairs(generation_ranking_pair_list)
    print('#####################################')
    generation_with_hardgoals_ranking_pair_list = get_specific_summary_ranking_pairs(rankings_pair_list, 1)
    print('generation_with_hardgoals_ranking_pair_list')
    calculate_top_1_for_ranking_pairs(generation_with_hardgoals_ranking_pair_list)
    print('#####################################')
    rewriting_ranking_pair_list = get_specific_summary_ranking_pairs(rankings_pair_list, 2)
    print('rewriting_ranking_pair_list')
    calculate_top_1_for_ranking_pairs(rewriting_ranking_pair_list)
    print('#####################################')
    rewriting_with_hardgoals_ranking_pair_list = get_specific_summary_ranking_pairs(rankings_pair_list, 3)
    print('rewriting_with_hardgoals_ranking_pair_list')
    calculate_top_1_for_ranking_pairs(rewriting_with_hardgoals_ranking_pair_list)
    print('#####################################')
    kg_without_instances_ranking_pair_list = get_specific_summary_ranking_pairs(rankings_pair_list, 4)
    print('kg_without_instances_ranking_pair_list')
    calculate_top_1_for_ranking_pairs(kg_without_instances_ranking_pair_list)
    print('#####################################')
    kg_with_instances_ranking_pair_list = get_specific_summary_ranking_pairs(rankings_pair_list, 5)
    print('kg_with_instances_ranking_pair_list')
    calculate_top_1_for_ranking_pairs(kg_with_instances_ranking_pair_list)
    print('#####################################')
    reference_ranking_pair_list = get_specific_summary_ranking_pairs(rankings_pair_list, 6)
    print('reference_ranking_pair_list')
    calculate_top_1_for_ranking_pairs(reference_ranking_pair_list)
    print('#####################################')


def compare_kgs_with_others(rankings):
    ranking_index_pairs = []
    # print(rankings)
    for index, ranking in enumerate(rankings):
        ranking_index_pairs.append((ranking, index))
    # print(ranking_index_pairs)
    ranking_index_pairs.sort(key=lambda x: x[0])
    # print(ranking_index_pairs)
    # top = set()
    top_1 = set()
    top_2 = set()
    for ranking_index_pair in ranking_index_pairs:
        if ranking_index_pair[0] == 1:
            top_1.add(ranking_index_pair[1])
        if ranking_index_pair[0] == 2:
            top_2.add(ranking_index_pair[1])
    if len(top_1) >= 2:
        top = top_1
    else:
        top = top_1.union(top_2)
    # print(top)
    intersection = top.intersection({4, 5})
    # print(intersection)
    # result = None
    if len(intersection) == 2:
        result = 'Yes'
    elif len(intersection) == 1:
        result = 'Not sure'
    else:
        result = 'No'
    # print(result)
    return result


def calculate_consistency(rankings_pair_list):
    consistency = 0
    for rankings_pair in rankings_pair_list:
        rankings_0 = rankings_pair[0]
        rankings_1 = rankings_pair[1]
        person_0 = compare_kgs_with_others(rankings_0)
        person_1 = compare_kgs_with_others(rankings_1)
        # print("########################")
        if person_0 == person_1:
            consistency = consistency + 1
    print(f"consistency: {consistency}")

    return consistency


def calculate_correlation_coefficient(rankings_pair_list):
    # https://realpython.com/numpy-scipy-pandas-correlation-python/#correlation
    correlation_coefficients_list = []
    for index, rankings_pair in enumerate(rankings_pair_list):
        print(f"ranking pair: {rankings_pair[0]}")
        print(f"ranking pair: {rankings_pair[1]}")
        pearson = pd.Series(rankings_pair[0]).corr(pd.Series(rankings_pair[1]))
        spearman = pd.Series(rankings_pair[0]).corr(pd.Series(rankings_pair[1]), method='spearman')
        kendall = pd.Series(rankings_pair[0]).corr(pd.Series(rankings_pair[1]), method='kendall')
        print(f"pearson: {pearson}")
        print(f"spearman: {spearman}")
        print(f"kendall: {kendall}")
        print('################')
        if index in {4, 9, 14, 19}:
            print("****************************")
        correlation_coefficients_list.append((pearson, spearman, kendall))
    print(len(correlation_coefficients_list))
    pearson_list, spearman_list, kendall_list = zip(*correlation_coefficients_list)
    # PlotUtil.show_boxplot(pearson_list, 'pearson_list')
    # PlotUtil.show_boxplot(spearman_list, 'spearman_list')
    # PlotUtil.show_boxplot(kendall_list, 'kendall_list')

    # print(pearson_list)
    # print(spearman_list)
    # print(kendall_list)
    print(f"mean pearson: {mean(pearson_list)}")
    print(f"mean spearman: {mean(spearman_list)}")
    print(f"mean kendall: {mean(kendall_list)}")
    return correlation_coefficients_list


def evaluate(project):
    is_continuous_value_flag = True
    # is_continuous_value_flag = False

    if is_continuous_value_flag:
        rankings_pair_list = FileUtil.load_pickle(
            PathUtil.get_manual_evaluation_continuous_rankings_result_filepath(project))
    else:
        rankings_pair_list = FileUtil.load_pickle(
            PathUtil.get_manual_evaluation_count_equal_rankings_result_filepath(project))
    # rankings_0, rankings_1 = combine_rankings_pair_list(rankings_pair_list)
    # pearson = pd.Series(rankings_0).corr(pd.Series(rankings_1))
    # spearman = pd.Series(rankings_0).corr(pd.Series(rankings_1), method='spearman')
    # kendall = pd.Series(rankings_0).corr(pd.Series(rankings_1), method='kendall')
    # print(pearson)
    # print(spearman)
    # print(kendall)

    correlation_coefficients_list = calculate_correlation_coefficient(rankings_pair_list)

    calculate_top_1(rankings_pair_list)

    consistency = calculate_consistency(rankings_pair_list)
    return correlation_coefficients_list


def get_list_for_df(one_list, tag):
    tag_df = [tag] * len(one_list)
    return tag_df
    # for _ in one_list:
    #     tag_df.append(tag)


def construct_df_for_boxplot(mozilla_correlation_coefficients_list, eclipse_correlation_coefficients_list):
    category_list = []
    value_category_list = []
    value_list = []
    for pearson, spearson, kendall in mozilla_correlation_coefficients_list:
        category_list.append('Mozilla')
        value_category_list.append('Pearson')
        value_list.append(pearson)

        category_list.append('Mozilla')
        value_category_list.append('Spearman')
        value_list.append(spearson)

        category_list.append('Mozilla')
        value_category_list.append('Kendall')
        value_list.append(kendall)
    for pearson, spearson, kendall in eclipse_correlation_coefficients_list:
        category_list.append('Eclipse')
        value_category_list.append('Pearson')
        value_list.append(pearson)

        category_list.append('Eclipse')
        value_category_list.append('Spearman')
        value_list.append(spearson)

        category_list.append('Eclipse')
        value_category_list.append('Kendall')
        value_list.append(kendall)
    data = {'Project': category_list,
            'Correlation Coefficient': value_category_list,
            'Value': value_list
            }
    df = pd.DataFrame(data)
    return df


if __name__ == "__main__":
    foldername = MOZILLA_PROJ
    mozilla_correlation_coefficients_list = evaluate(foldername)
    foldername = ECLIPSE_PROJ
    eclipse_correlation_coefficients_list = evaluate(foldername)

    result_df = construct_df_for_boxplot(mozilla_correlation_coefficients_list, eclipse_correlation_coefficients_list)
    print(result_df)
    # result_df.plot.box()
    # plt.grid(linestyle="--", alpha=0.3)
    # plt.show()
    my_colors = ["#FF7B7B", "#DAF7A6", "#74E9D7"]
    sns.set(rc={'figure.figsize': (6, 2.8)})
    custom = {"axes.edgecolor": "black", "grid.linestyle": ":", "grid.color": "grey"}
    sns.set_style("whitegrid", rc=custom)
    # sns.set(font_scale=1.5)
    boxplot = sns.boxplot(data=result_df, orient="h", width=0.6, palette=my_colors, x='Value', y='Project',
                          hue='Correlation Coefficient')
    boxplot.set(xlabel=None, ylabel=None)
    # plt.setp(boxplot.get_legend().get_texts(), fontsize='10')  # for legend text
    # plt.setp(boxplot.get_legend().get_title(), fontsize='32')  # for legend title
    plt.legend(loc='best', fontsize="x-small")
    # plt.ylim(5, 50)
    # plt.tight_layout()
    # sns.set(rc={"figure.figsize": (5, 1)})
    # plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1, wspace=0.2)
    # plt.grid(True)
    # plt.show()
    plt.savefig("correlation_coefficient_boxplot.pdf", bbox_inches="tight")

    # result_df = pd.concat([mozilla_df, eclipse_df], axis=1)
    # print(result_df)
    # kg_ranking_pair_list = get_kg_summary_ranking_pairs(rankings_pair_list)
    # print(kg_without_instances_ranking_pair_list)
    # print(len(kg_without_instances_ranking_pair_list))
    # print(kg_with_instances_ranking_pair2list)
    # print(len(kg_with_instances_ranking_pair_list))
    # print(kg_ranking_pair_list)
    # print(len(kg_ranking_pair_list))
    # print('kg_ranking_pair_list')
    # calculate_top_1(kg_ranking_pair_list)
