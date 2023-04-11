import random
from pathlib import Path

from bug_changing.types.placeholder import Placeholder
from bug_changing.types.summary import SummaryPairs
from bug_changing.utils.dataframe_util import DataFrameUtil
from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.list_util import ListUtil
from bug_changing.utils.path_util import PathUtil
from config import MOZILLA_PROJ, MOZILLA_URL, ECLIPSE_PROJ, ECLIPSE_URL, OUTPUT_DIR


def sample_summaries(summary_pairs,
                     generation_answers, generation_with_hg_answers,
                     rewriting_answers, rewriting_with_hg_answers,
                     kg_without_rewritten_instances_answers, kg_with_rewritten_instances_answers,
                     sample_num=16, project=MOZILLA_PROJ):
    sample_num_list = random.sample(range(0, len(summary_pairs)), sample_num)
    sample_summary_pairs = []
    summaries_list = []
    for sample_num in sample_num_list:
        summaries = []
        sample_summary_pairs.append(summary_pairs[sample_num])
        summaries.append(generation_answers[sample_num].strip())
        summaries.append(generation_with_hg_answers[sample_num].strip())
        summaries.append(rewriting_answers[sample_num].strip())
        summaries.append(rewriting_with_hg_answers[sample_num].strip())
        summaries.append(kg_without_rewritten_instances_answers[sample_num].rewritten_summary.strip())
        summaries.append(kg_with_rewritten_instances_answers[sample_num].rewritten_summary.strip())
        summaries.append(summary_pairs[sample_num].add_summary.text.strip())
        summaries_list.append(summaries)
    sample_summary_pairs = SummaryPairs(sample_summary_pairs)
    FileUtil.dump_pickle(PathUtil.get_sample_summary_pairs_for_manual_evaluation_filepath(project), sample_summary_pairs)
    FileUtil.dump_pickle(PathUtil.get_sample_summaries_list_for_manual_evaluation_filepath(project), summaries_list)
    return sample_summary_pairs, summaries_list


if __name__ == "__main__":
    # foldername = MOZILLA_PROJ
    foldername = ECLIPSE_PROJ
    # sample_summaries_flag = True
    sample_summaries_num = 10
    random_summaries_flag = True
    # random_summaries_flag = False
    if foldername == MOZILLA_PROJ:
        project_url = MOZILLA_URL
    else:
        project_url = ECLIPSE_URL

    prompt_type = 'generation_with_length'
    generation_answers = FileUtil.load_txt(PathUtil.get_baseline_answers_filepath(prompt_type, foldername))
    prompt_type = 'generation_with_length_hardgoal'
    generation_with_hg_answers = FileUtil.load_txt(PathUtil.get_baseline_answers_filepath(prompt_type, foldername))

    prompt_type = 'rewrite_with_length'
    rewriting_answers = FileUtil.load_txt(PathUtil.get_baseline_answers_filepath(prompt_type, foldername))
    prompt_type = 'rewrite_with_length_hardgoal'
    rewriting_with_hg_answers = FileUtil.load_txt(PathUtil.get_baseline_answers_filepath(prompt_type, foldername))

    prompt_type = 'rewrite_by_kg_extractor_with_instances_discriminator_with_instances_rewrite_question_with_extractor_result'
    kg_without_rewritten_instances_answers = FileUtil.load_pickle(
        PathUtil.get_answers_filepath(foldername, prompt_type))
    prompt_type = 'rewrite_by_kg_extractor_with_instances_discriminator_with_instances_rewriter_with_instances_hard_goal_repeat_num_3_rewrite_question_with_extractor_result'
    kg_with_rewritten_instances_answers = FileUtil.load_pickle(PathUtil.get_answers_filepath(foldername, prompt_type))

    test_summary_pairs = FileUtil.load_pickle(PathUtil.get_test_sample_summary_pairs_with_labels_filepath(foldername))
    # print(len(test_summary_pairs))
    # if sample_summaries_flag:
    test_summary_pairs, summaries_list = \
        sample_summaries(test_summary_pairs, generation_answers, generation_with_hg_answers,
                         rewriting_answers, rewriting_with_hg_answers, kg_without_rewritten_instances_answers,
                         kg_with_rewritten_instances_answers, sample_summaries_num, foldername)

    # summaries_list = FileUtil.load_pickle(PathUtil.get_sample_summaries_list_for_manual_evaluation_filepath(foldername))
    # summary_pairs_list = test_summary_pairs.split_summary_pairs_into_num_parts(3)
    # print(len(summary_pairs_list))
    # summaries_list_list = ListUtil.list_of_groups(summaries_list, 3)
    # print(len(summaries_list_list))
    #
    # for index_i, summary_pairs in enumerate(summary_pairs_list):
    #     for index_j, summary_pair in enumerate(summary_pairs):
    #         print(summary_pair.add_summary.text)
    #         print(summaries_list_list[index_i][index_j])
