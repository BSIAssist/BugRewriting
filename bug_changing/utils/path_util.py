import os
from pathlib import Path

from config import DATA_DIR, METRICS_DIR, OUTPUT_DIR, MODEL_DIR, ROOT_DIR, MOZILLA_PROJ


class PathUtil:

    # @staticmethod
    # def get_specified_product_component_bugs_filepath(product_component_pair):
    #     return DATA_DIR / Path("product_component_bugs") / \
    #            Path(product_component_pair.product + "_" + product_component_pair.component + "_" + "bugs.json")
    #
    # @staticmethod
    # def get_specified_product_components_bugs_filepath(folder_name, product_component_pair_list, bugs_type='filtered'):
    #     pc_names = ''
    #     for pc in product_component_pair_list:
    #         pc_names = pc_names + pc.product + '_' + pc.component
    #     specified_product_components_bugs_dir = DATA_DIR / Path(folder_name, pc_names)
    #     # if not exists this dir, create it
    #     specified_product_components_bugs_dir.mkdir(exist_ok=True, parents=True)
    #     return specified_product_components_bugs_dir / Path(f"{bugs_type}_bugs.json")

    @staticmethod
    def get_bugs_filepath(folder_name=MOZILLA_PROJ):
        return DATA_DIR / Path(folder_name, "bugs.json")

    @staticmethod
    def get_test_bugs_filepath(folder_name=MOZILLA_PROJ):
        return DATA_DIR / Path(folder_name, "test_bugs.json")

    @staticmethod
    def get_filtered_test_bugs_filepath(folder_name=MOZILLA_PROJ):
        return DATA_DIR / Path(folder_name, "filtered_test_bugs.json")

    # @staticmethod
    # def get_tossed_test_bugs_filepath(folder_name="mozilla"):
    #     return DATA_DIR / Path(folder_name, "tossed_test_bugs.json")
    #
    # @staticmethod
    # def get_untossed_test_bugs_filepath(folder_name="mozilla"):
    #     return DATA_DIR / Path(folder_name, "untossed_test_bugs.json")

    @staticmethod
    def get_train_bugs_filepath(folder_name=MOZILLA_PROJ):
        return DATA_DIR / Path(folder_name, "train_bugs.json")

    @staticmethod
    def get_val_bugs_filepath(folder_name=MOZILLA_PROJ):
        return DATA_DIR / Path(folder_name, "val_bugs.json")

    @staticmethod
    def get_filtered_bugs_filepath(folder_name=MOZILLA_PROJ):
        return DATA_DIR / Path(folder_name, "filtered_bugs.json")

    @staticmethod
    def get_bugs_with_summary_reformulation_filepath(folder_name=MOZILLA_PROJ):
        return DATA_DIR / Path(folder_name, "bugs_with_summary_reformulation.json")

    @staticmethod
    def get_pc_filepath(folder_name=MOZILLA_PROJ):
        return DATA_DIR / Path(folder_name, "product_component.json")

    @staticmethod
    def get_instance_summary_pairs_filepath(folder_name=MOZILLA_PROJ):
        return DATA_DIR / Path(folder_name, "instance_summary_pairs.json")

    @staticmethod
    def get_instance_summary_pairs_with_desc_labels_filepath(folder_name=MOZILLA_PROJ):
        return DATA_DIR / Path(folder_name, "instance_summary_pairs_with_desc_labels.json")

    @staticmethod
    def get_test_summary_pairs_filepath(folder_name=MOZILLA_PROJ):
        return DATA_DIR / Path(folder_name, "test_summary_pairs.json")

    @staticmethod
    def get_test_sample_summary_pairs_filepath(folder_name=MOZILLA_PROJ):
        return DATA_DIR / Path(folder_name, "test_sample_summary_pairs.json")

    @staticmethod
    def get_test_sample_summary_pairs_with_labels_filepath(folder_name=MOZILLA_PROJ):
        return DATA_DIR / Path(folder_name, "test_sample_summary_pairs_with_labels.json")

    @staticmethod
    def get_goal_model_filepath():
        return DATA_DIR / Path("goal_model.json")

    @staticmethod
    def get_targets_filepath():
        return DATA_DIR / Path("targets.json")

    @staticmethod
    def get_actions_filepath():
        return DATA_DIR / Path("actions.json")

    @staticmethod
    def get_baseline_answers_filepath(prompt_type, project):
        return OUTPUT_DIR / Path(project, f"{prompt_type}_answers.txt")

    @staticmethod
    def get_answers_filepath(project, prompt_type):
        folder_path = OUTPUT_DIR / Path(project, prompt_type)
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
        return Path(folder_path, "answers.json")

    @staticmethod
    def get_raw_answers_filepath(project, prompt_type):
        folder_path = OUTPUT_DIR / Path(project, prompt_type)
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
        return Path(folder_path, "raw_answers.json")

    @staticmethod
    def get_result_filepath(project, prompt_type):
        folder_path = OUTPUT_DIR / Path(project, prompt_type)
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
        return Path(folder_path, "result.json")

    @staticmethod
    def get_sample_summary_pairs_for_manual_evaluation_filepath(project):
        folder_path = OUTPUT_DIR / Path(project, 'manual_evaluation')
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
        return Path(folder_path, "sample_summary_pairs.json")

    @staticmethod
    def get_sample_summaries_list_for_manual_evaluation_filepath(project):
        folder_path = OUTPUT_DIR / Path(project, 'manual_evaluation')
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
        return Path(folder_path, "sample_summaries_list.json")

    @staticmethod
    def get_manual_evaluation_excel_filepath(project, index):
        folder_path = OUTPUT_DIR / Path(project, f'manual_evaluation')
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
        return Path(folder_path, f"manual_evaluation_{index}.xlsx")

    @staticmethod
    def get_manual_evaluation_responses_excel_filepath(project, index):
        folder_path = OUTPUT_DIR / Path(project, f'manual_evaluation')
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
        return Path(folder_path, f"manual_evaluation_{index} (Responses).xlsx")

    @staticmethod
    def get_manual_evaluation_continuous_rankings_result_filepath(project):
        folder_path = OUTPUT_DIR / Path(project, f'manual_evaluation')
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
        return Path(folder_path, f"continuous_rankings_result.json")

    @staticmethod
    def get_manual_evaluation_count_equal_rankings_result_filepath(project):
        folder_path = OUTPUT_DIR / Path(project, f'manual_evaluation')
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
        return Path(folder_path, f"count_equal_rankings_result.json")

    # @staticmethod
    # def get_pc_adjacency_matrix_filepath():
    #     return DATA_DIR / Path("product_component_adjacency_matrix.json")

    # @staticmethod
    # def get_pc_with_topics_filepath():
    #     return DATA_DIR / Path("product_component_with_topics.json")

    # @staticmethod
    # def get_concept_set_filepath():
    #     return DATA_DIR / Path("concept_set.json")

    # @staticmethod
    # def get_bugbug_pair_outputs_filepath():
    #     return METRICS_DIR / Path("bugbug", "test_bugs_top10_pair_outputs.json")

    # @staticmethod
    # def get_bugbug_top10_outputs_filepath():
    #     return METRICS_DIR / Path("bugbug", "test_bugs_metrics_top10.json")

    # @staticmethod
    # def get_bugbug_metrics_filepath():
    #     return METRICS_DIR / Path("bugbug", "test_bugs_metrics.json")

    # @staticmethod
    # def get_bugbug_tossed_metrics_filepath():
    #     return METRICS_DIR / Path("bugbug", "tossed_test_bugs_metrics.json")
    #
    # @staticmethod
    # def get_bugbug_untossed_metrics_filepath():
    #     return METRICS_DIR / Path("bugbug", "untossed_test_bugs_metrics.json")
    #
    # @staticmethod
    # def get_bugbug_result_filepath():
    #     return METRICS_DIR / Path("bugbug", "result.json")
    #
    # @staticmethod
    # def get_bugbug_tossed_result_filepath():
    #     return METRICS_DIR / Path("bugbug", "tossed_result.json")
    #
    # @staticmethod
    # def get_bugbug_untossed_result_filepath():
    #     return METRICS_DIR / Path("bugbug", "untossed_result.json")

    # @staticmethod
    # def get_bugbug_with_tossing_graph_metrics_filepath():
    #     return METRICS_DIR / Path("bugbug_with_tossing_graph", "metrics_with_tossing_graph.json")
    #
    # @staticmethod
    # def get_bugbug_with_tossing_graph_tossed_metrics_filepath():
    #     return METRICS_DIR / Path("bugbug_with_tossing_graph", "tossed_metrics_with_tossing_graph.json")
    #
    # @staticmethod
    # def get_bugbug_with_tossing_graph_untossed_metrics_filepath():
    #     return METRICS_DIR / Path("bugbug_with_tossing_graph", "untossed_metrics_with_tossing_graph.json")
    #
    # @staticmethod
    # def get_bugbug_with_tossing_graph_result_filepath():
    #     return METRICS_DIR / Path("bugbug_with_tossing_graph", "result.json")
    #
    # @staticmethod
    # def get_bugbug_with_tossing_graph_tossed_result_filepath():
    #     return METRICS_DIR / Path("bugbug_with_tossing_graph", "tossed_result.json")
    #
    # @staticmethod
    # def get_bugbug_with_tossing_graph_untossed_result_filepath():
    #     return METRICS_DIR / Path("bugbug_with_tossing_graph", "untossed_result.json")

    # @staticmethod
    # def get_our_metrics_ablation_filepath(ablation):
    #     return METRICS_DIR / Path("our_approach", f"metrics_{ablation}.json")
    #
    # @staticmethod
    # def get_our_metrics_filepath():
    #     return METRICS_DIR / Path("our_approach", "metrics.json")
    #
    # @staticmethod
    # def get_our_tossed_metrics_filepath():
    #     return METRICS_DIR / Path("our_approach", "tossed_metrics.json")
    #
    # @staticmethod
    # def get_our_untossed_metrics_filepath():
    #     return METRICS_DIR / Path("our_approach", "untossed_metrics.json")
    #
    # @staticmethod
    # def get_our_result_ablation_filepath(ablation):
    #     return METRICS_DIR / Path("our_approach", f"result_{ablation}.json")
    #
    # @staticmethod
    # def get_our_result_filepath():
    #     return METRICS_DIR / Path("our_approach", "result.json")
    #
    # @staticmethod
    # def get_our_untossed_result_filepath():
    #     return METRICS_DIR / Path("our_approach", "untossed_result.json")
    #
    # @staticmethod
    # def get_our_tossed_result_filepath():
    #     return METRICS_DIR / Path("our_approach", "tossed_result.json")
    #
    # @staticmethod
    # def get_our_approach_metrics_with_tossing_graph_filepath():
    #     return METRICS_DIR / Path("our_approach", "metrics_with_tossing_graph.json")
    #
    # @staticmethod
    # def get_feature_vector_train_filepath():
    #     return OUTPUT_DIR / Path("feature_vector_train.txt")
    #
    # @staticmethod
    # def get_feature_vector_test_filepath():
    #     return OUTPUT_DIR / Path("feature_vector_test.txt")
    #
    # @staticmethod
    # def get_feature_vector_score_filepath():
    #     return OUTPUT_DIR / Path("feature_vector_score.json")
    #
    # @staticmethod
    # def load_lambdaMart_model_filepath():
    #     return MODEL_DIR / Path("lambdaMart_model.json")
    #
    # @staticmethod
    # def load_lda_model_filepath():
    #     return MODEL_DIR / Path("lda.model")
    #
    # @staticmethod
    # def load_fasttext_model_filepath():
    #     return MODEL_DIR / Path("wiki.en", FASTTEXT_MODEL_NAME)
    #
    # @staticmethod
    # def load_bert_model_filepath():
    #     return MODEL_DIR / Path("bert_classifier_model")
    #
    # @staticmethod
    # def get_fig_filepath(folder_name, fig_name):
    #     figs_dir = ROOT_DIR / Path('figs')
    #     figs_dir.mkdir(exist_ok=True, parents=True)
    #     folder_name_dir = figs_dir / Path(folder_name)
    #     folder_name_dir.mkdir(exist_ok=True, parents=True)
    #     return folder_name_dir / Path(fig_name)
