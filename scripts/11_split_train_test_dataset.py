from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.path_util import PathUtil
from config import MOZILLA_PROJ, ECLIPSE_PROJ

if __name__ == "__main__":
    """
    sort bugs by creation time
    and split bugs into training set and testing set by different ways
    1. split_dataset_by_radio: 80% training dataset and 20% testing dataset
    2. split_dataset_by_creation_time(creation_time="2021-01-01T00:00:00Z")
    """
    folder_name = ECLIPSE_PROJ
    # folder_name = MOZILLA_PROJ
    bugs = FileUtil.load_pickle(PathUtil.get_bugs_with_summary_reformulation_filepath(folder_name))

    # train_bugs, test_bugs = bugs.split_dataset_by_creation_time(creation_time="2021-07-01T00:00:00Z")
    train_bugs, test_bugs = bugs.split_dataset_by_creation_time(creation_time="2021-10-01T00:00:00Z")

    # pc_list = FileUtil.load_pickle(PathUtil.get_pc_filepath())
    # train_bugs, test_bugs = bugs.split_dataset_by_pc_and_creation_time(pc_list)
    # train_bugs, test_bugs = bugs.split_dataset_by_pc(pc_list)

    train_bugs.overall_bugs()
    test_bugs.overall_bugs()
    print(train_bugs.get_length())
    print(test_bugs.get_length())

    train_bugs_filepath = PathUtil.get_train_bugs_filepath(folder_name)
    FileUtil.dump_pickle(train_bugs_filepath, train_bugs)
    test_bugs_filepath = PathUtil.get_test_bugs_filepath(folder_name)
    FileUtil.dump_pickle(test_bugs_filepath, test_bugs)


