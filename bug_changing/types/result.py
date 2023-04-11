import os
from pathlib import Path

from bug_changing.types.placeholder import Placeholder
from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.metrics_util import MetricsUtil
from config import MOZILLA_PROJ, OUTPUT_DIR


class ResultDetails:
    def __init__(self):
        self.accuracy = None
        self.right_answers = list()
        self.wrong_answers = list()

    def __repr__(self):
        return f'{self.accuracy}\n'

    def __str__(self):
        return f'{self.accuracy}\n'

    def calculate_accuracy(self):
        sum_count = len(self.right_answers) + len(self.wrong_answers)
        self.accuracy = len(self.right_answers) / sum_count


class ExtractorResult:
    def __init__(self):
        self.suggested_solution = ResultDetails()
        self.actual_behavior = ResultDetails()
        self.trigger_action = ResultDetails()
        self.platform = ResultDetails()
        self.component = ResultDetails()
        self.accuracy = None

    def __repr__(self):
        return f'\t{Placeholder.SUGGESTED_SOLUTION}: {self.suggested_solution}' \
               f'\t{Placeholder.ACTUAL_BEHAVIOR}: {self.actual_behavior}' \
               f'\t{Placeholder.TRIGGER_ACTION}: {self.trigger_action}' \
               f'\t{Placeholder.PLATFORM}: {self.platform}' \
               f'\t{Placeholder.COMPONENT}: {self.component}' \
               f'\tAccuracy: {self.accuracy}'

    def __str__(self):
        return f'\t{Placeholder.SUGGESTED_SOLUTION}: {self.suggested_solution}' \
               f'\t{Placeholder.ACTUAL_BEHAVIOR}: {self.actual_behavior}' \
               f'\t{Placeholder.TRIGGER_ACTION}: {self.trigger_action}' \
               f'\t{Placeholder.PLATFORM}: {self.platform}' \
               f'\t{Placeholder.COMPONENT}: {self.component}' \
               f'\tAccuracy: {self.accuracy}'

    def calculate_accuracy(self):
        right_hit = len(self.suggested_solution.right_answers) + len(self.actual_behavior.right_answers) \
                    + len(self.trigger_action.right_answers) + len(self.platform.right_answers) + \
                    len(self.component.right_answers)
        all_hit = 5 * (len(self.suggested_solution.right_answers) + len(self.suggested_solution.wrong_answers))
        self.accuracy = right_hit / all_hit

    @staticmethod
    def is_right(one_answer, one_groundtruth_answer):
        if one_answer and one_groundtruth_answer:
            return True
        elif one_answer is None and one_groundtruth_answer is None:
            return True
        return False

    def from_answers(self, answers, groundtruth_answers):
        for index, answer in enumerate(answers):
            groundtruth_answer = groundtruth_answers[index]
            if ExtractorResult.is_right(answer.suggested_solution, groundtruth_answer.suggested_solution):
                self.suggested_solution.right_answers.append(answer)
            else:
                self.suggested_solution.wrong_answers.append(answer)
            if ExtractorResult.is_right(answer.actual_behavior, groundtruth_answer.actual_behavior):
                self.actual_behavior.right_answers.append(answer)
            else:
                self.actual_behavior.wrong_answers.append(answer)
            if ExtractorResult.is_right(answer.trigger_action, groundtruth_answer.trigger_action):
                self.trigger_action.right_answers.append(answer)
            else:
                self.trigger_action.wrong_answers.append(answer)
            if ExtractorResult.is_right(answer.platform, groundtruth_answer.platform):
                self.platform.right_answers.append(answer)
            else:
                self.platform.wrong_answers.append(answer)
            if ExtractorResult.is_right(answer.component, groundtruth_answer.component):
                self.component.right_answers.append(answer)
            else:
                self.component.wrong_answers.append(answer)
        self.suggested_solution.calculate_accuracy()
        self.actual_behavior.calculate_accuracy()
        self.trigger_action.calculate_accuracy()
        self.platform.calculate_accuracy()
        self.component.calculate_accuracy()
        self.calculate_accuracy()


class DiscriminatorResult:
    def __init__(self):
        self.is_actual_behavior_vague = ResultDetails()
        self.is_trigger_action_vague = ResultDetails()

        self.spelling_error = ResultDetails()

        self.syntax_error = ResultDetails()
        self.declarative_statement = ResultDetails()
        self.present_tense = ResultDetails()

        self.personal_pronoun = ResultDetails()
        self.emotional_reaction = ResultDetails()
        self.offensive_words = ResultDetails()
        self.wishy_washy_words = ResultDetails()
        self.accuracy = None

    def __repr__(self):
        return f'\t{Placeholder.IS_ACTUAL_BEHAVIOR_VAGUE}: {self.is_actual_behavior_vague}' \
               f'\t{Placeholder.IS_TRIGGER_ACTION_VAGUE}: {self.is_trigger_action_vague}' \
               f'\t{Placeholder.SPELLING_ERROR}: {self.spelling_error}' \
               f'\t{Placeholder.SYNTAX_ERROR}: {self.syntax_error}' \
               f'\t{Placeholder.DECLARATIVE_STATEMENT}: {self.declarative_statement}' \
               f'\t{Placeholder.PRESENT_TENSE}: {self.present_tense}' \
               f'\t{Placeholder.PERSONAL_PRONOUN}: {self.personal_pronoun}' \
               f'\t{Placeholder.EMOTIONAL_REACTION}: {self.emotional_reaction}' \
               f'\t{Placeholder.OFFENCE}: {self.offensive_words}' \
               f'\t{Placeholder.WISHY_WASHY_WORD}: {self.wishy_washy_words}' \
               f'\tAccuracy: {self.accuracy}'

    def __str__(self):
        return f'\t{Placeholder.IS_ACTUAL_BEHAVIOR_VAGUE}: {self.is_actual_behavior_vague}' \
               f'\t{Placeholder.IS_TRIGGER_ACTION_VAGUE}: {self.is_trigger_action_vague}' \
               f'\t{Placeholder.SPELLING_ERROR}: {self.spelling_error}' \
               f'\t{Placeholder.SYNTAX_ERROR}: {self.syntax_error}' \
               f'\t{Placeholder.DECLARATIVE_STATEMENT}: {self.declarative_statement}' \
               f'\t{Placeholder.PRESENT_TENSE}: {self.present_tense}' \
               f'\t{Placeholder.PERSONAL_PRONOUN}: {self.personal_pronoun}' \
               f'\t{Placeholder.EMOTIONAL_REACTION}: {self.emotional_reaction}' \
               f'\t{Placeholder.OFFENCE}: {self.offensive_words}' \
               f'\t{Placeholder.WISHY_WASHY_WORD}: {self.wishy_washy_words}' \
               f'\tAccuracy: {self.accuracy}'

    def calculate_accuracy(self):
        right_hit = len(self.is_actual_behavior_vague.right_answers) + len(self.is_trigger_action_vague.right_answers) + \
                    len(self.spelling_error.right_answers) + len(self.syntax_error.right_answers) + \
                    len(self.declarative_statement.right_answers) + len(self.present_tense.right_answers) + \
                    len(self.personal_pronoun.right_answers) + len(self.emotional_reaction.right_answers) + \
                    len(self.offensive_words.right_answers) + len(self.wishy_washy_words.right_answers)
        all_hit = 10 * (len(self.is_actual_behavior_vague.right_answers) +
                        len(self.is_actual_behavior_vague.wrong_answers))
        self.accuracy = right_hit / all_hit

    @staticmethod
    def is_right(one_answer, one_groundtruth_answer):
        if one_answer and one_groundtruth_answer:
            if one_answer[0] and one_groundtruth_answer[0]:
                return True
            elif one_answer[0] is False and one_groundtruth_answer[0] is False:
                return True
            return False
        return True

    def from_answers(self, answers, groundtruth_answers):
        for index, answer in enumerate(answers):
            groundtruth_answer = groundtruth_answers[index]
            if DiscriminatorResult.is_right(answer.is_actual_behavior_vague,
                                            groundtruth_answer.is_actual_behavior_vague):
                self.is_actual_behavior_vague.right_answers.append(answer)
            else:
                self.is_actual_behavior_vague.wrong_answers.append(answer)
            if DiscriminatorResult.is_right(answer.is_trigger_action_vague, groundtruth_answer.is_trigger_action_vague):
                self.is_trigger_action_vague.right_answers.append(answer)
            else:
                self.is_trigger_action_vague.wrong_answers.append(answer)
            if DiscriminatorResult.is_right(answer.spelling_error, groundtruth_answer.spelling_error):
                self.spelling_error.right_answers.append(answer)
            else:
                self.spelling_error.wrong_answers.append(answer)
            if DiscriminatorResult.is_right(answer.syntax_error, groundtruth_answer.syntax_error):
                self.syntax_error.right_answers.append(answer)
            else:
                self.syntax_error.wrong_answers.append(answer)
            if DiscriminatorResult.is_right(answer.declarative_statement, groundtruth_answer.declarative_statement):
                self.declarative_statement.right_answers.append(answer)
            else:
                self.declarative_statement.wrong_answers.append(answer)
            if DiscriminatorResult.is_right(answer.present_tense, groundtruth_answer.present_tense):
                self.present_tense.right_answers.append(answer)
            else:
                self.present_tense.wrong_answers.append(answer)
            if DiscriminatorResult.is_right(answer.personal_pronoun, groundtruth_answer.personal_pronoun):
                self.personal_pronoun.right_answers.append(answer)
            else:
                self.personal_pronoun.wrong_answers.append(answer)
            if DiscriminatorResult.is_right(answer.emotional_reaction, groundtruth_answer.emotional_reaction):
                self.emotional_reaction.right_answers.append(answer)
            else:
                self.emotional_reaction.wrong_answers.append(answer)
            if DiscriminatorResult.is_right(answer.offensive_words, groundtruth_answer.offensive_words):
                self.offensive_words.right_answers.append(answer)
            else:
                self.offensive_words.wrong_answers.append(answer)
            if DiscriminatorResult.is_right(answer.wishy_washy_words, groundtruth_answer.wishy_washy_words):
                self.wishy_washy_words.right_answers.append(answer)
            else:
                self.wishy_washy_words.wrong_answers.append(answer)

        self.is_actual_behavior_vague.calculate_accuracy()
        self.is_trigger_action_vague.calculate_accuracy()
        self.spelling_error.calculate_accuracy()
        self.syntax_error.calculate_accuracy()
        self.declarative_statement.calculate_accuracy()
        self.present_tense.calculate_accuracy()
        self.personal_pronoun.calculate_accuracy()
        self.emotional_reaction.calculate_accuracy()
        self.offensive_words.calculate_accuracy()
        self.wishy_washy_words.calculate_accuracy()
        self.calculate_accuracy()


class RewriterResult:
    def __init__(self, rouge_list=None, avg_rouge=None, gleu_list=None, avg_gleu=None):
        self.rouges = rouge_list
        self.avg_rouge = avg_rouge
        self.gleus = gleu_list
        self.avg_gleu = avg_gleu

    def __repr__(self):
        # show_str = ''
        # for summary_pair_gleu in self.summary_pair_gleu_list:
        #     show_str = show_str + f"source: {summary_pair_gleu[0].rm_summary.text}\n" \
        #                           f"reference: "
        return f'\tAVG_rouge: {self.avg_rouge}\n' \
               f'\tAVG_GLEU: {self.avg_gleu}\n'

    def __str__(self):
        return f'\tAVG_rouge: {self.avg_rouge}\n' \
               f'\tAVG_GLEU: {self.avg_gleu}\n'

    def from_answers(self, answers, folder_path=Path(OUTPUT_DIR)):
        sources = []
        references = []
        rewritten_answers = []
        # foldername = 'rewrite'
        # prompt_type = 'rewrite_with_length'
        # prompt_type = 'rewrite_with_length_softgoal'
        # prompt_type = 'our_rewrite'
        # folder_path = Path(OUTPUT_DIR, project, foldername, prompt_type)
        # checking if the directory demo_folder2
        # exist or not.
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
        sources_path = Path(folder_path, "sources.txt")
        references_path = Path(folder_path, "references.txt")
        answers_path = Path(folder_path, "answers.txt")

        for answer in answers:
            sources.append(answer.summary_pair.rm_summary.text)
            references.append(answer.summary_pair.add_summary.text)
            rewritten_answers.append(answer.rewritten_summary)
        FileUtil.dump_txt(sources_path, sources)
        FileUtil.dump_txt(references_path, references)
        FileUtil.dump_txt(answers_path, rewritten_answers)
        gleus, avg_gleu = MetricsUtil.gleu(sources_path, references_path, answers_path)
        rouges, avg_rouge = MetricsUtil.rouge(rewritten_answers, references)
        self.rouges = rouges
        self.avg_rouge = avg_rouge
        self.gleus = gleus
        self.avg_gleu = avg_gleu


class Result:
    def __init__(self, answers=None):
        """
        todo: self.discriminator = DiscriminatorResult()  # not test
        todo: self.rewriter = RewriterResult()  # not write
        Args:
            answers ():
        """
        self.answers = answers
        self.extractor = ExtractorResult()
        self.discriminator = DiscriminatorResult()  # not test
        self.rewriter = RewriterResult()  # not write

    def __repr__(self):
        return f"Extractor result: \n{self.extractor}\n" \
               f"Discriminator result: \n{self.discriminator}\n" \
               f"Rewriter result: \n{self.rewriter}\n"

    def __str__(self):
        return f"Extractor result: \n{self.extractor}\n" \
               f"Discriminator result: \n{self.discriminator}\n" \
               f"Rewriter result: \n{self.rewriter}\n"

    @classmethod
    def from_answers(cls, answers, folderpath=None):
        result = cls(answers)
        groundtruth_answers = answers.get_groundtruth_answers_from_summary_pairs()
        # print(groundtruth_answers[0])
        result.extractor.from_answers(answers, groundtruth_answers)
        result.discriminator.from_answers(answers, groundtruth_answers)
        return result


class ManualResult:
    def __init__(self, specific_what=None, specific_when=None, specific_where=None, concise=None,
                 easy_to_understand=None, overall=None):
        self.specific_what = specific_what
        self.specific_when = specific_when
        self.specific_where = specific_where
        self.concise = concise
        self.easy_to_understand = easy_to_understand
        self.overall = overall

    def __repr__(self):
        return f"{Placeholder.SPECIFIC} - what: \n{self.specific_what}\n" \
               f"{Placeholder.SPECIFIC} - when: \n{self.specific_when}\n" \
               f"{Placeholder.SPECIFIC} - where: \n{self.specific_where}\n" \
               f"{Placeholder.CONCISE}: \n{self.concise}\n" \
               f"{Placeholder.UNDERSTANDABLE}: \n{self.easy_to_understand}\n" \
               f"Overall: \n{self.overall}\n"

    def __str__(self):
        return f"{Placeholder.SPECIFIC} - what: \n{self.specific_what}\n" \
               f"{Placeholder.SPECIFIC} - when: \n{self.specific_when}\n" \
               f"{Placeholder.SPECIFIC} - where: \n{self.specific_where}\n" \
               f"{Placeholder.CONCISE}: \n{self.concise}\n" \
               f"{Placeholder.UNDERSTANDABLE}: \n{self.easy_to_understand}\n" \
               f"Overall: \n{self.overall}\n"
