from bug_changing.types.goal_model import GoalModel
from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.path_util import PathUtil
from config import MOZILLA_PROJ, ECLIPSE_PROJ

if __name__ == "__main__":
    """
    build goal model
    1. get softgoals from Placeholder.SOFTGOAL_LIST
    2. get targets from Placeholder.TARGET_LIST
    3. get actions from Placeholder.ACTION_LIST
    4. add actions into targets
    5. get hard_goals from Placeholder.HARDGOAL_LIST
    6. add hardgoals into softgoals
    7. get instance from mozilla and eclipse:
       a. get hardgoals into summary_pairs
       b. instances into hardgoals
       c. get goal model
    """
    # mozilla_instance_summary_pairs_filepath = PathUtil.get_instance_summary_pairs_filepath(MOZILLA_PROJ)
    mozilla_instance_summary_pairs_filepath = PathUtil.get_instance_summary_pairs_with_desc_labels_filepath(MOZILLA_PROJ)
    mozilla_summary_pairs = FileUtil.load_pickle(mozilla_instance_summary_pairs_filepath)

    eclipse_instance_summary_pairs_filepath = PathUtil.get_instance_summary_pairs_with_desc_labels_filepath(ECLIPSE_PROJ)
    eclipse_summary_pairs = FileUtil.load_pickle(eclipse_instance_summary_pairs_filepath)
    # print(eclipse_summary_pairs.length)
    goal_model, targets, actions = GoalModel.initiate(mozilla_summary_pairs, eclipse_summary_pairs)
    print(goal_model)
    FileUtil.dump_pickle(PathUtil.get_goal_model_filepath(), goal_model)
    FileUtil.dump_pickle(PathUtil.get_targets_filepath(), targets)
    FileUtil.dump_pickle(PathUtil.get_actions_filepath(), actions)

    # FileUtil.dump_pickle(mozilla_instance_summary_pairs_filepath, mozilla_summary_pairs)
    # FileUtil.dump_pickle(eclipse_instance_summary_pairs_filepath, eclipse_summary_pairs)

    # print(goal_model.hard_goals[0].instances.mozilla_instances)
    # print(mozilla_summary_pairs[0])








