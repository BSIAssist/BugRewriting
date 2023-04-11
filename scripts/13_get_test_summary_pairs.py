from pathlib import Path

from tqdm import tqdm
from bug_changing.types.bugs import Bugs
from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.nlp_util import NLPUtil
from bug_changing.utils.path_util import PathUtil
from config import DATA_DIR, MOZILLA_PROJ, ECLIPSE_PROJ

if __name__ == "__main__":
    """
    1. get test summary_pairs from filtered_test_bugs.json
    2. filter unchanged summary_pairs by: a. replace structure with '' 
                                b. if rm_summary.text == add_summary.text: remove summary_pair
    3. filter up-to-date summary_pairs by: a. if added tokens not from desc but from comments    
                                           b. if deleted tokens exist in comments    
    """
    # folder_name = MOZILLA_PROJ
    folder_name = ECLIPSE_PROJ
    test_bugs = FileUtil.load_pickle(PathUtil.get_filtered_test_bugs_filepath(folder_name))
    print(f"test bugs num: {test_bugs.get_length()}")

    summary_pairs = test_bugs.get_goal_oriented_summary_pairs()
    print(f"summary_pairs num: {len(summary_pairs)}")
    summary_pairs.remove_tags()
    summary_pairs = summary_pairs.filter_unchanged()
    print(f"summary_pairs num (filter unchanged): {len(summary_pairs)}")

    summary_pairs = summary_pairs.filter_up_to_date()
    print(f"summary_pairs num (filter up-to-date): {len(summary_pairs)}")
    FileUtil.dump_pickle(PathUtil.get_test_summary_pairs_filepath(folder_name), summary_pairs)
