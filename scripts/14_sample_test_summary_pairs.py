
from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.path_util import PathUtil
from config import MOZILLA_PROJ, ECLIPSE_PROJ

if __name__ == "__main__":
    # folder_name = MOZILLA_PROJ
    folder_name = ECLIPSE_PROJ
    summary_pairs = FileUtil.load_pickle(PathUtil.get_test_summary_pairs_filepath(folder_name))
    print(f"test summary_pairs num: {summary_pairs.get_length()}")

    # sample_num = 337  # mozilla: 2701
    # sample_num = 201  # eclipse: 418

    # sample_num = 318  # mozilla: 1839, ratio = 0.3
    # sample_num = 182  # eclipse: 344, ratio = 0.3

    # sample_num = 333  # mozilla: 2454
    # sample_num = 201  # eclipse: 418

    # sample_num = 264  # mozilla: 839 -> 173
    # sample_num = 246  # eclipse: 246 -> 97

    # sample_num = 247  # mozilla: 688 -> 247 -> 159
    sample_num = 170  # eclipse: 170 -> 63

    sample_summary_pairs = summary_pairs.random_sample_summary_pairs(sample_num)
    print(f"sample summary_pairs num: {sample_summary_pairs.get_length()}")
    FileUtil.dump_pickle(PathUtil.get_test_sample_summary_pairs_filepath(folder_name), sample_summary_pairs)

