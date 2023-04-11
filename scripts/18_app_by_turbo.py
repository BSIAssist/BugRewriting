import openai

from bug_changing.pipelines.app import App
from bug_changing.types.result import Result
from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.llm_util import LLMUtil
from bug_changing.utils.path_util import PathUtil
from config import MOZILLA_PROJ, ECLIPSE_PROJ

if __name__ == "__main__":
    # foldername = MOZILLA_PROJ
    foldername = ECLIPSE_PROJ

    openai.api_key = LLMUtil.OPENAI_API_KEY
    instance_summary_pairs = FileUtil.load_pickle(PathUtil.get_instance_summary_pairs_with_desc_labels_filepath(foldername))
    test_summary_pairs = FileUtil.load_pickle(PathUtil.get_test_sample_summary_pairs_with_labels_filepath(foldername))
    all_targets = FileUtil.load_pickle(PathUtil.get_targets_filepath())
    goal_model = FileUtil.load_pickle(PathUtil.get_goal_model_filepath())
    # bugs = FileUtil.load_pickle(PathUtil.get_bugs_with_summary_reformulation_filepath(foldername))
    # bugs = FileUtil.load_pickle(PathUtil.get_train_bugs_filepath(foldername))
    # bugs = FileUtil.load_pickle(PathUtil.get_test_bugs_filepath(foldername))

    app = App()
    # app.process(test_summary_pairs[0:2], instance_summary_pairs, all_targets, goal_model, foldername,
    #             extractor_with_instances=True, rewriter_with_instances=False)

    extractor_with_instances = True
    discriminator_with_instances = True
    rewriter_with_instances = True
    hard_goal_repeat_num = 3
    rewrite_question_with_extractor_result = True

    answers, raw_answers = app.process(test_summary_pairs, instance_summary_pairs, all_targets, goal_model,
                                       foldername, extractor_with_instances=extractor_with_instances,
                                       discriminator_with_instances=discriminator_with_instances,
                                       rewriter_with_instances=rewriter_with_instances,
                                       hard_goal_repeat_num=hard_goal_repeat_num,
                                       rewrite_question_with_extractor_result=rewrite_question_with_extractor_result)

    prompt_type = 'rewrite_by_kg'
    if extractor_with_instances:
        prompt_type = prompt_type + f"_extractor_with_instances"
    if discriminator_with_instances:
        prompt_type = prompt_type + f"_discriminator_with_instances"
    if rewriter_with_instances:
        prompt_type = prompt_type + f"_rewriter_with_instances_hard_goal_repeat_num_{hard_goal_repeat_num}"
    if rewrite_question_with_extractor_result:
        prompt_type = prompt_type + f"_rewrite_question_with_extractor_result"

    FileUtil.dump_pickle(PathUtil.get_answers_filepath(foldername, prompt_type), answers)
    FileUtil.dump_pickle(PathUtil.get_raw_answers_filepath(foldername, prompt_type), raw_answers)

    result = Result.from_answers(answers)
    print(result)

    FileUtil.dump_pickle(PathUtil.get_result_filepath(foldername, prompt_type), result)
