from pathlib import Path

from bug_changing.pipelines.evaluator import Discriminator
from bug_changing.types.summary import SummaryPairs
from bug_changing.utils.dataframe_util import DataFrameUtil
from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.path_util import PathUtil

from config import MOZILLA_PROJ, ECLIPSE_PROJ, OUTPUT_DIR

if __name__ == "__main__":
    # folder_name = MOZILLA_PROJ
    folder_name = ECLIPSE_PROJ

    summary_pairs = FileUtil.load_pickle(PathUtil.get_instance_summary_pairs_with_desc_labels_filepath(folder_name))

    discriminator = Discriminator()
    discriminator.get_instances(summary_pairs, folder_name)
    instances = SummaryPairs(discriminator.instances)
    df = instances.convert_summary_pairs_for_discriminator_info_into_dataframe(folder_name)
    DataFrameUtil.write_df_into_excel(Path(OUTPUT_DIR, folder_name, f'instance_summary_pairs_for_discriminator_labels.xlsx'),
                                      df, folder_name)
