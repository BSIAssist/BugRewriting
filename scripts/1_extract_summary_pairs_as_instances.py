from bug_changing.types.summary import SummaryPairs
from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.path_util import PathUtil
from config import DATA_DIR, MOZILLA_PROJ, ECLIPSE_PROJ


def get_rewritten_summary_pair_list(bugs, id_list):
    """
    Args:
        bugs ():
        id_list (): a. [(bug_id, rm_summary_id, added_summary_id), ..., ]
                    b. [bug_id, bug_id, ..., ]

    Returns: [(rm_summary, added_summary), ..., ]

    """
    summary_pair_list = []
    for bug_id in id_list:
        if isinstance(bug_id, tuple):
            bug_id, rm_summary_id, added_summary_id = bug_id
        else:
            rm_summary_id = 0
            added_summary_id = 1
        bug = bugs.get_bug_by_id(bug_id)
        rm_summary = bug.summary_path[rm_summary_id]
        added_summary = bug.summary_path[added_summary_id]
        summary_pair_list.append((rm_summary, added_summary))
    return summary_pair_list


if __name__ == "__main__":
    folder_name = MOZILLA_PROJ
    # folder_name = ECLIPSE_PROJ
    # bugs_filepath = PathUtil.get_bugs_with_summary_reformulation_filepath(folder_name)
    bugs_filepath = PathUtil.get_train_bugs_filepath(folder_name)
    bugs = FileUtil.load_pickle(bugs_filepath)

    # bugs.overall_bugs()

    instance_bug_list = None

    if folder_name == MOZILLA_PROJ:
        instance_bug_list = [[1218099, 1673885, 1096628, 1679552, 697762, 1156695, 1755433, 740304, 944082, 1693854,
                              611659, 1805678, 1682316, 1639575, 1047904, 1294426, 1583398, 1218099, 1606300,
                              1297839, 1684265, 756405, 1121800, 1231097, 1708548, 902486, 1146052, 1747397,
                              677017, 1702198, 1670008, 1096628, 1107941, 1121800, 1279390, 1036856, 1130672, 1218099,
                              1632048, 771205, 1555196, 857040, 921732, 1300525, 1679552, 1521015, 1388414, 1382150,
                              1679552, 1673885, 803770, 923608, 1393563, 581023, 784131, 902486, 1611864, 1201931,
                              902486, 1213421, 1197529, 1302671, 1773879, 1555196, 1521015, 1725890],
                             [(831452, 0, 1), (1744888, 2, 3), (1744888, 1, 2), (551591, 3, 4), (1217216, 1, 2),
                              (831452, 1, 2), (1698580, 1, 2), (1115363, 1, 2), (673785, 1, 2), (1403460, 0, 1),
                              (788430, 0, 1), (1804854, 0, 1), (1217216, 0, 1), (597669, 0, 1), (641322, 1, 2),
                              (1122695, 0, 1), (802656, 0, 1), (883554, 0, 1), (1122695, 0, 1), (1217216, 0, 1),
                              (1403460, 1, 2), (1403460, 0, 1), (1025492, 0, 1), (1403460, 0, 1), (1629639, 0, 1)]]
    else:
        instance_bug_list = [[356190, 560767, 398347, 409637, 613722, 357540, 560060, 569698, 317206, 387529, 571325,
                              427620, 435156, 355918, 396843, 478512, 419219,  318427, 345467, 312867, 328766, 391816,
                              596446, 340771, 428595, 517139, 504349, 342153, 494748, 539445, 399389, 1331213,
                              307165, 319680, 353615],
                             [(390052, 0, 1), (326028, 0, 1), (404912, 0, 1), (468457, 0, 1)]]

    once_bug_ids = instance_bug_list[0]
    more_bug_ids = instance_bug_list[1]

    summary_pairs = []
    for bug_id in once_bug_ids:
        bug = bugs.get_bug_by_id(bug_id)
        if bug is not None:
            if len(bug.summary_path) > 2:
                print(f"more than once: {bug_id}")
            else:
                summary_pairs.append(bug.get_specific_summary_pair())
        else:
            print(f"not in the train bugs: {bug_id}")

    more_bugs = []
    for bug_id in more_bug_ids:
        bug = bugs.get_bug_by_id(bug_id[0])
        if bug is not None:
            if len(bug.summary_path) < 2:
                print(f"once: {bug_id}")
            else:
                summary_pairs.append(bug.get_specific_summary_pair(bug_id[1], bug_id[2]))
        else:
            print(f"not in the train bugs: {bug_id}")

    for summary_pair in list(set(summary_pairs)):
        print(f'{summary_pair.rm_summary.bug.id} {summary_pair.rm_summary.id} {summary_pair.add_summary.id}')

    summary_pairs = SummaryPairs(set(summary_pairs))
    print(len(summary_pairs))
    # print(summary_pairs.get_length())
    summary_pairs = summary_pairs.filter_for_goal_model_instances()
    print(len(summary_pairs))

    instance_summary_pairs_filepath = PathUtil.get_instance_summary_pairs_filepath(folder_name)
    FileUtil.dump_pickle(instance_summary_pairs_filepath,
                         summary_pairs)
