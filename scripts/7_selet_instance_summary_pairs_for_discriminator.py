from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.path_util import PathUtil

from config import MOZILLA_PROJ, ECLIPSE_PROJ

if __name__ == "__main__":
    # folder_name = MOZILLA_PROJ
    folder_name = ECLIPSE_PROJ

    summary_pairs = FileUtil.load_pickle(PathUtil.get_instance_summary_pairs_with_desc_labels_filepath(folder_name))
    # summary_pairs.complete_vague_labels()
    # FileUtil.dump_pickle(PathUtil.get_instance_summary_pairs_with_desc_labels_filepath(folder_name),
    #                      summary_pairs)
    print(len(summary_pairs))
    # count = 0
    summary_pair_count_pairs = []
    for summary_pair in summary_pairs:
        count = 0
        if summary_pair.rm_summary.is_actual_behavior_vague:
            count = count + 1
        if summary_pair.rm_summary.is_trigger_action_vague:
            count = count + 1
        if summary_pair.rm_summary.spelling_error:
            count = count + 1
        if summary_pair.rm_summary.syntax_error:
            count = count + 1
        if summary_pair.rm_summary.declarative_statement:
            count = count + 1
        if summary_pair.rm_summary.present_tense:
            count = count + 1
        if summary_pair.rm_summary.personal_pronoun:
            count = count + 1
        if summary_pair.rm_summary.emotional_reaction:
            count = count + 1
        if summary_pair.rm_summary.offensive_words:
            count = count + 1
        if summary_pair.rm_summary.wishy_washy_words:
            count = count + 1
        summary_pair_count_pairs.append((summary_pair, count))
    summary_pair_count_pairs = sorted(summary_pair_count_pairs, key=lambda x: (-x[1]))
    for summary_pair, count in summary_pair_count_pairs:
        print(count)
        print(summary_pair)

            # count = count + 1
            # print(count)
        # print(summary_pair.bug.description)
        # input()
