import openai
from chatgpt_wrapper import ChatGPT
from tqdm import tqdm

from bug_changing.pipelines.evaluator import Extractor
from bug_changing.types.summary import SummaryPairs
from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.llm_util import LLMUtil
from bug_changing.utils.path_util import PathUtil


from config import OUTPUT_DIR, MOZILLA_PROJ, ECLIPSE_PROJ


if __name__ == "__main__":
    openai.api_key = LLMUtil.OPENAI_API_KEY
    # folder_name = MOZILLA_PROJ
    folder_name = ECLIPSE_PROJ
    extractor = Extractor()
    # bot = ChatGPT()

    all_targets = FileUtil.load_pickle(PathUtil.get_targets_filepath())
    goal_model = FileUtil.load_pickle(PathUtil.get_goal_model_filepath())

    summary_pairs_filepath = PathUtil.get_instance_summary_pairs_filepath(folder_name)
    summary_pairs = FileUtil.load_pickle(summary_pairs_filepath)
    # summary_pair = summary_pairs.get_summary_pair_by_bug_id_summary_ids(1725890, 0, 1)
    # summary_pairs = SummaryPairs([summary_pair])
    # get the session prompt of extractor
    # extractor.get_session_prompt(all_targets)
    # LLMUtil.SESSION_PROMPT = extractor.session_prompt
    # ans_list = []
    # raw_answer_list = []
    for index, summary_pair in tqdm(enumerate(summary_pairs), ascii=True):
        ans, raw_answer = extractor.extract_info_from_desc(summary_pair.bug.description,
                                                           summary_pairs, all_targets,
                                                           folder_name, with_instances=True)
        summary_pair.rm_summary.desc_suggested_solution = ans[0]
        summary_pair.rm_summary.desc_actual_behavior = ans[1]
        summary_pair.rm_summary.desc_trigger_action = ans[2]
        summary_pair.rm_summary.desc_platform = ans[3]
        summary_pair.rm_summary.desc_component = ans[4]
        print(f"{index}: {raw_answer}")
        # input()
    # print(summary_pairs.get_summary_pair_by_bug_id_summary_ids(1403460, 0, 1))
    FileUtil.dump_pickle(summary_pairs_filepath, summary_pairs)
