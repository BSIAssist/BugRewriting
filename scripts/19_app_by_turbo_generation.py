import openai

from bug_changing.pipelines.app import App
from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.llm_util import LLMUtil
from bug_changing.utils.path_util import PathUtil
from config import MOZILLA_PROJ, ECLIPSE_PROJ, MOZILLA_SUMMARY_LEN, ECLIPSE_SUMMARY_LEN

if __name__ == "__main__":
    # foldername = MOZILLA_PROJ
    foldername = ECLIPSE_PROJ

    # prompt_type = 'generation'
    # prompt_type = 'generation_with_length'
    # prompt_type = 'generation_with_length_softgoal'
    prompt_type = 'generation_with_length_hardgoal'

    openai.api_key = LLMUtil.OPENAI_API_KEY
    test_summary_pairs = FileUtil.load_pickle(PathUtil.get_test_sample_summary_pairs_with_labels_filepath(foldername))
    app = App()

    answers = app.process_by_turbo_generation(test_summary_pairs, prompt_type, foldername)

    FileUtil.dump_txt(PathUtil.get_baseline_answers_filepath(prompt_type, foldername), answers)

    # result = Result.from_answers(answers)
    # print(result)
    #
    # FileUtil.dump_pickle(PathUtil.get_result_filepath(foldername), result)
