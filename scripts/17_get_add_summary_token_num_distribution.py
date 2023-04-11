from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.nlp_util import NLPUtil
from bug_changing.utils.path_util import PathUtil
from config import MOZILLA_PROJ, ECLIPSE_PROJ
import matplotlib.pyplot as plt
import pandas as pd


def get_box_plot_data(labels, bp):
    rows_list = []

    for i in range(len(labels)):
        dict1 = {}
        dict1['label'] = labels[i]
        dict1['lower_whisker'] = bp['whiskers'][i * 2].get_ydata()[1]
        dict1['lower_quartile'] = bp['boxes'][i].get_ydata()[1]
        dict1['median'] = bp['medians'][i].get_ydata()[1]
        dict1['upper_quartile'] = bp['boxes'][i].get_ydata()[2]
        dict1['upper_whisker'] = bp['whiskers'][(i * 2) + 1].get_ydata()[1]
        rows_list.append(dict1)

    return pd.DataFrame(rows_list)


if __name__ == "__main__":
    # folder_name = MOZILLA_PROJ
    folder_name = ECLIPSE_PROJ

    # summary_pairs = FileUtil.load_pickle(PathUtil.get_instance_summary_pairs_filepath(folder_name))
    # print(len(summary_pairs))
    train_bugs = FileUtil.load_pickle(PathUtil.get_train_bugs_filepath(folder_name))
    print(train_bugs.get_length())

    add_summary_list = []
    # for summary_pair in summary_pairs:
    #     add_summary = summary_pair.add_summary.text
    #     add_summary_list.append(add_summary)
    for bug in train_bugs:
        add_summary_list.append(bug.summary_path[-1].text)

    token_num_list = list()
    for add_summary in add_summary_list:
        add_summary_token_num = NLPUtil.calculate_token_num(add_summary)
        # print(f"{add_summary}: {add_summary_token_num}")
        token_num_list.append(add_summary_token_num)

    # np.random.seed(42)
    # x = np.random.normal(size=1000)

    # plt.hist(token_num_list, density=True, bins=1)  # density=False would make counts
    # plt.ylabel('Count')
    # plt.xlabel('TokenNum')
    # plt.show()
    # plt.boxplot(token_num_list)
    bp = plt.boxplot(token_num_list)
    print(len(add_summary_list))
    labels = ['token_num_list']
    value_data = get_box_plot_data(labels, bp)
    # Convert the whole dataframe as a string and display
    print(value_data.to_string())
    # for key, value in value_dict_list.items():
    #     print(f"{key}: {value}")

    plt.show()
