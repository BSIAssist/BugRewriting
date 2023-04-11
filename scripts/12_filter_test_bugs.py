
from tqdm import tqdm
from bug_changing.types.bugs import Bugs
from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.nlp_util import NLPUtil
from bug_changing.utils.path_util import PathUtil
from config import MOZILLA_PROJ, ECLIPSE_PROJ

if __name__ == "__main__":
    """
    filter test bugs by:
    1. bug description length [10, 300] <- draw distribution

    2. filter bugs related to log, stack trace, crash report, assertion failure by 
          a. '```' in desc and ('log:' or 'crash report' or 'stack trace' or 'assertion failure') in desc
          
    # 3. filter bugs related to task, feature (non-bugs) by 
    #     desc not complement to summary: common token number percentage >= 0.7 
    #     (also meet the requirement: a. have description b. filter part of up-to-date)
    """
    # folder_name = MOZILLA_PROJ
    folder_name = ECLIPSE_PROJ
    test_bugs = FileUtil.load_pickle(PathUtil.get_test_bugs_filepath(folder_name))
    print(f"test bugs num: {test_bugs.get_length()}")

    filtered_bugs = test_bugs.filter_bugs_by_desc_tokens_num()
    print(f"filtered bugs num (filtered by desc tokens num): {filtered_bugs.get_length()}")

    filtered_bugs = filtered_bugs.filter_bugs_by_desc_with_log(folder_name)
    print(f"filtered bugs num (filter bugs with log): {filtered_bugs.get_length()}")

    # if folder_name == MOZILLA_PROJ:
    #     print(f"https://bugzilla.mozilla.org/show_bug.cgi?id={bug.id}")
    # else:
    #     print(f"https://bugs.eclipse.org/bugs/show_bug.cgi?id={bug.id}")
    filtered_bugs_filepath = PathUtil.get_filtered_test_bugs_filepath(folder_name)
    FileUtil.dump_pickle(filtered_bugs_filepath, filtered_bugs)
