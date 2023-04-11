import random

from tqdm import tqdm

from bug_changing.types.goal_model import HardGoals
from bug_changing.types.placeholder import Placeholder
from bug_changing.utils.list_util import ListUtil
from bug_changing.utils.nlp_util import NLPUtil

import pandas as pd
from config import MOZILLA_PROJ, ECLIPSE_PROJ


class Summary:
    def __init__(self, id, bug, text, suggested_solution=None, actual_behavior=None,
                 trigger_action=None,
                 platform=None, component=None,
                 length=None):
        self.id = id
        self.bug = bug
        self.text = text
        self.suggested_solution = suggested_solution
        self.actual_behavior = actual_behavior
        self.trigger_action = trigger_action
        self.platform = platform
        self.component = component
        self.desc_suggested_solution = None
        self.desc_actual_behavior = None
        self.desc_trigger_action = None
        self.desc_platform = None
        self.desc_component = None
        self.is_actual_behavior_vague = None
        self.is_trigger_action_vague = None

        self.spelling_error = None

        self.syntax_error = None
        self.declarative_statement = None
        self.present_tense = None

        self.personal_pronoun = None
        self.emotional_reaction = None
        self.offensive_words = None
        self.wishy_washy_words = None
        self.length = length
        # self.content = content
        # self.structure = structure

    def __eq__(self, other):
        return self.text == other.text

    def __repr__(self):
        return f'{self.id} - {self.bug.id} - {self.text}\n' \
               f'\t{Placeholder.SUGGESTED_SOLUTION}: {self.suggested_solution}\n' \
               f'\t{Placeholder.ACTUAL_BEHAVIOR}: {self.actual_behavior}\n' \
               f'\t{Placeholder.TRIGGER_ACTION}: {self.trigger_action}\n' \
               f'\t{Placeholder.PLATFORM}: {self.platform}\n' \
               f'\t{Placeholder.COMPONENT}: {self.component}\n' \
               f'\t{Placeholder.IS_ACTUAL_BEHAVIOR_VAGUE}: {self.is_actual_behavior_vague}\n' \
               f'\t{Placeholder.IS_TRIGGER_ACTION_VAGUE}: {self.is_trigger_action_vague}\n' \
               f'\t{Placeholder.SPELLING_ERROR}: {self.spelling_error}\n' \
               f'\t{Placeholder.SYNTAX_ERROR}: {self.syntax_error}\n' \
               f'\t{Placeholder.DECLARATIVE_STATEMENT}: {self.declarative_statement}\n' \
               f'\t{Placeholder.PRESENT_TENSE}: {self.present_tense}\n' \
               f'\t{Placeholder.PERSONAL_PRONOUN}: {self.personal_pronoun}\n' \
               f'\t{Placeholder.EMOTIONAL_REACTION}: {self.emotional_reaction}\n' \
               f'\t{Placeholder.OFFENCE}: {self.offensive_words}\n' \
               f'\t{Placeholder.WISHY_WASHY_WORD}: {self.wishy_washy_words}\n'

    def __str__(self):
        return f'{self.id} - {self.bug.id} - {self.text}\n' \
               f'\t{Placeholder.SUGGESTED_SOLUTION}: {self.suggested_solution}\n' \
               f'\t{Placeholder.ACTUAL_BEHAVIOR}: {self.actual_behavior}\n' \
               f'\t{Placeholder.TRIGGER_ACTION}: {self.trigger_action}\n' \
               f'\t{Placeholder.PLATFORM}: {self.platform}\n' \
               f'\t{Placeholder.COMPONENT}: {self.component}\n' \
               f'\t{Placeholder.IS_ACTUAL_BEHAVIOR_VAGUE}: {self.is_actual_behavior_vague}\n' \
               f'\t{Placeholder.IS_TRIGGER_ACTION_VAGUE}: {self.is_trigger_action_vague}\n' \
               f'\t{Placeholder.SPELLING_ERROR}: {self.spelling_error}\n' \
               f'\t{Placeholder.SYNTAX_ERROR}: {self.syntax_error}\n' \
               f'\t{Placeholder.DECLARATIVE_STATEMENT}: {self.declarative_statement}\n' \
               f'\t{Placeholder.PRESENT_TENSE}: {self.present_tense}\n' \
               f'\t{Placeholder.PERSONAL_PRONOUN}: {self.personal_pronoun}\n' \
               f'\t{Placeholder.EMOTIONAL_REACTION}: {self.emotional_reaction}\n' \
               f'\t{Placeholder.OFFENCE}: {self.offensive_words}\n' \
               f'\t{Placeholder.WISHY_WASHY_WORD}: {self.wishy_washy_words}\n'

    def __hash__(self):
        # print(hash(str(self)))
        return hash(str(self))

    @classmethod
    def from_summary(cls, id, bug, text):
        return cls(id, bug, text)

    @staticmethod
    def process_input_label(label):
        if label:
            label = label.strip()
            if label == 'y':
                return True
            elif label == 'n':
                return False
            return label
        else:
            return None

    def initiate_from_labels(self, labels):
        self.suggested_solution = Summary.process_input_label(labels[0])
        self.actual_behavior = Summary.process_input_label(labels[1])
        self.trigger_action = Summary.process_input_label(labels[2])
        self.is_actual_behavior_vague = Summary.process_input_label(labels[3])
        self.is_trigger_action_vague = Summary.process_input_label(labels[4])
        self.platform = Summary.process_input_label(labels[5])
        self.component = Summary.process_input_label(labels[6])
        self.spelling_error = Summary.process_input_label(labels[7])
        self.syntax_error = Summary.process_input_label(labels[8])
        self.declarative_statement = Summary.process_input_label(labels[9])
        self.present_tense = Summary.process_input_label(labels[10])
        self.personal_pronoun = Summary.process_input_label(labels[11])
        self.emotional_reaction = Summary.process_input_label(labels[12])
        self.offensive_words = Summary.process_input_label(labels[13])
        self.wishy_washy_words = Summary.process_input_label(labels[14])

    def initiate_from_desc_labels(self, labels):
        # if labels[6] == 'y':
        self.desc_suggested_solution = Summary.process_input_label(labels[0])
        self.desc_actual_behavior = Summary.process_input_label(labels[1])
        self.desc_trigger_action = Summary.process_input_label(labels[2])
        self.desc_platform = Summary.process_input_label(labels[3])
        self.desc_component = Summary.process_input_label(labels[4])

    def initiate_from_discriminator_labels(self, labels):
        """
        @todo: spelling error, syntax error, ...
        Args:
            labels ():

        Returns:

        """
        # if labels[6] == 'y':
        self.is_actual_behavior_vague = Summary.process_input_label(labels[0])
        self.is_trigger_action_vague = Summary.process_input_label(labels[1])
        # self.desc_trigger_action = Summary.process_input_label(labels[2])
        # self.desc_platform = Summary.process_input_label(labels[3])
        # self.desc_component = Summary.process_input_label(labels[4])
        # return self
        # return None

    def label(self):
        print(f"{Placeholder.SUGGESTED_SOLUTION}: ")
        input_content = input()
        self.suggested_solution = Summary.process_input_label(input_content)
        print(f'{Placeholder.ACTUAL_BEHAVIOR}: ')
        input_content = input()
        self.actual_behavior = Summary.process_input_label(input_content)
        print(f'{Placeholder.TRIGGER_ACTION}: ')
        input_content = input()
        self.trigger_action = Summary.process_input_label(input_content)
        print(f'{Placeholder.PLATFORM}: ')
        input_content = input()
        self.platform = Summary.process_input_label(input_content)
        print(f'{Placeholder.COMPONENT}: ')
        input_content = input()
        self.component = Summary.process_input_label(input_content)
        print(f'{Placeholder.IS_ACTUAL_BEHAVIOR_VAGUE}: ')
        input_content = input()
        self.is_actual_behavior_vague = Summary.process_input_label(input_content)
        print(f'{Placeholder.IS_TRIGGER_ACTION_VAGUE}: ')
        input_content = input()
        self.is_trigger_action_vague = Summary.process_input_label(input_content)
        print(f'{Placeholder.SPELLING_ERROR}: ')
        input_content = input()
        self.spelling_error = Summary.process_input_label(input_content)
        print(f'{Placeholder.SYNTAX_ERROR}: \n')
        input_content = input()
        self.syntax_error = Summary.process_input_label(input_content)
        print(f'{Placeholder.DECLARATIVE_STATEMENT}: ')
        input_content = input()
        self.declarative_statement = Summary.process_input_label(input_content)
        print(f'{Placeholder.PRESENT_TENSE}: ')
        input_content = input()
        self.present_tense = Summary.process_input_label(input_content)
        print(f'{Placeholder.PERSONAL_PRONOUN}: ')
        input_content = input()
        self.personal_pronoun = Summary.process_input_label(input_content)
        print(f'{Placeholder.EMOTIONAL_REACTION}: ')
        input_content = input()
        self.emotional_reaction = Summary.process_input_label(input_content)
        print(f'{Placeholder.OFFENCE}: ')
        input_content = input()
        self.offensive_words = Summary.process_input_label(input_content)
        print(f'{Placeholder.WISHY_WASHY_WORD}: ')
        input_content = input()
        self.wishy_washy_words = Summary.process_input_label(input_content)


class SummaryPair:
    def __init__(self, rm_summary, add_summary):
        self.rm_summary = rm_summary
        self.add_summary = add_summary
        self.bug = rm_summary.bug
        self.hard_goals = HardGoals()

    def __eq__(self, other):
        return self.bug.id == other.bug.id \
               and self.rm_summary.id == other.rm_summary.id \
               and self.add_summary.id == other.add_summary.id

    def __repr__(self):
        output = f'{self.bug.id}:\n\t{self.rm_summary}\n\t{self.add_summary}\n\tHardGoals:'
        if self.hard_goals.hard_goals is not None:
            for hard_goal in self.hard_goals:
                output = output + '\n\t\t' + hard_goal.action.name + '-' + hard_goal.target.name
        return output

    def __str__(self):
        output = f'{self.bug.id}:\n\t{self.rm_summary}\n\t{self.add_summary}\n\tHardGoals:'
        if self.hard_goals.hard_goals is not None:
            for hard_goal in self.hard_goals:
                output = output + '\n\t\t' + hard_goal.action.name + '-' + hard_goal.target.name
        return output

    def __hash__(self):
        # print(hash(str(self)))
        return hash(str(self))

    def remove_tags(self):
        """
        remove tags at the beginning of the summary
        Returns:
        """
        tag = NLPUtil.extract_tag_by_regex(self.rm_summary.text)
        if tag:
            self.rm_summary.text = self.rm_summary.text.replace(tag, "").strip()
        tag = NLPUtil.extract_tag_by_regex(self.add_summary.text)
        if tag:
            self.add_summary.text = self.add_summary.text.replace(tag, "").strip()

    def get_tokens(self):
        rm_tokens = NLPUtil.preprocess(self.rm_summary.text)
        add_tokens = NLPUtil.preprocess(self.add_summary.text)
        # desc_tokens = NLPUtil.preprocess(self.bug.description.text)
        # comments = ''
        # for comment in self.bug.comments:
        #     comments = comments + ' ' + comment.text
        # comments_tokens = NLPUtil.preprocess(comments)
        # return [rm_tokens, add_tokens, desc_tokens, comments_tokens]
        return [rm_tokens, add_tokens]

    def complete_vague_labels(self):
        if self.rm_summary.actual_behavior and self.add_summary.actual_behavior:
            self.rm_summary.is_actual_behavior_vague = True
        else:
            self.rm_summary.is_actual_behavior_vague = False

        if self.rm_summary.trigger_action and self.add_summary.trigger_action:
            self.rm_summary.is_trigger_action_vague = True
        else:
            self.rm_summary.is_trigger_action_vague = False
    # def is_change_from_desc(self, ratio=0.3):
    #     # bug = self.bug
    #     # if MOZILLA_PROJ:
    #     #     print(f"https://bugzilla.mozilla.org/show_bug.cgi?id={bug.id}")
    #     # else:
    #     #     print(f"https://bugs.eclipse.org/bugs/show_bug.cgi?id={bug.id}")
    #     rm_tokens = NLPUtil.preprocess(self.rm_summary.text)
    #     add_tokens = NLPUtil.preprocess(self.add_summary.text)
    #     diff_tokens = set(add_tokens) - set(rm_tokens)
    #     desc_tokens = NLPUtil.preprocess(self.bug.description.text)
    #     # print(rm_tokens)
    #     # print(add_tokens)
    #     # print(diff_tokens)
    #     # print(desc_tokens)
    #     if diff_tokens:
    #         other_tokens = diff_tokens - set(desc_tokens)
    #         # print(other_tokens)
    #         if other_tokens:
    #             radio = len(other_tokens) / len(add_tokens)
    #             # print(radio)
    #             if radio > ratio:
    #                 return False
    #         return True
    #     return True

    def is_change_from_desc(self):
        # bug = self.bug
        # if MOZILLA_PROJ:
        #     print(f"https://bugzilla.mozilla.org/show_bug.cgi?id={bug.id}")
        # else:
        #     print(f"https://bugs.eclipse.org/bugs/show_bug.cgi?id={bug.id}")
        rm_tokens = NLPUtil.preprocess(self.rm_summary.text)
        add_tokens = NLPUtil.preprocess(self.add_summary.text)

        # diff_tokens = set(add_tokens) ^ set(rm_tokens)  # 补集
        diff_add_tokens = set(add_tokens) - set(rm_tokens)
        diff_delete_tokens = set(rm_tokens) - set(add_tokens)
        # comments_tokens =
        # print(rm_tokens)
        # print(add_tokens)
        # print(diff_add_tokens)
        # print(diff_delete_tokens)
        is_from_desc, comments_tokens = self.is_diff_add_tokens_from_desc(diff_add_tokens)
        if is_from_desc:
            is_from_comments, comments_tokens = self.is_change_from_comments(diff_delete_tokens, comments_tokens)
            # print(comments_tokens)
            if is_from_comments is False:
                return True
        return False

    def is_diff_add_tokens_from_desc(self, diff_add_tokens, desc_tokens=None):
        comments_tokens = None
        if diff_add_tokens:
            if desc_tokens is None:
                desc_tokens = NLPUtil.preprocess(self.bug.description.text)
                # print(desc_tokens)
            other_tokens = diff_add_tokens - set(desc_tokens)
            if other_tokens:
                is_from_comments, comments_tokens = self.is_change_from_comments(other_tokens)
                if is_from_comments:
                    return False, comments_tokens
        return True, comments_tokens

    def is_change_from_comments(self, other_tokens, comments_tokens=None):
        if other_tokens:
            if comments_tokens is None:
                comments = ''
                for index, comment in enumerate(self.bug.comments):
                    if index != 0:
                        comments = comments + ' ' + comment.text
                comments_tokens = NLPUtil.preprocess(comments)
            tokens_from_comments = other_tokens.intersection(set(comments_tokens))
            if tokens_from_comments:
                return True, comments_tokens
        return False, comments_tokens

    def get_hard_goals(self, hard_goals, project=MOZILLA_PROJ):
        """
        a. get hard_goals for and into summary_pair.instances
        b. summary_pairs as instance into hard_goals
        Args:
            hard_goals ():
            project ():

        Returns:

        """
        self.hard_goals = HardGoals([])
        # easy to understand
        if self.rm_summary.spelling_error and self.add_summary.spelling_error:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.MODIFY,
                                                                     Placeholder.SPELLING_ERROR)
            self.hard_goals.append(hard_goal)
            # self_hard_goals.append(hard_goal)
            hard_goal.instances.append(self, project)

        if self.rm_summary.syntax_error:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.MODIFY,
                                                                     Placeholder.SYNTAX_ERROR)
            self.hard_goals.append(hard_goal)
            # self_hard_goals.append(hard_goal)
            hard_goal.instances.append(self, project)
        if self.rm_summary.declarative_statement:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.MODIFY,
                                                                     Placeholder.DECLARATIVE_STATEMENT)
            self.hard_goals.append(hard_goal)
            # self_hard_goals.append(hard_goal)
            hard_goal.instances.append(self, project)
        if self.rm_summary.present_tense:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.MODIFY,
                                                                     Placeholder.PRESENT_TENSE)
            self.hard_goals.append(hard_goal)
            # self_hard_goals.append(hard_goal)
            hard_goal.instances.append(self, project)
        # concise
        if self.rm_summary.personal_pronoun:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.DELETE,
                                                                     Placeholder.PERSONAL_PRONOUN)
            self.hard_goals.append(hard_goal)
            # self_hard_goals.append(hard_goal)
            hard_goal.instances.append(self, project)
        if self.rm_summary.emotional_reaction:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.DELETE,
                                                                     Placeholder.EMOTIONAL_REACTION)
            self.hard_goals.append(hard_goal)
            # self_hard_goals.append(hard_goal)
            hard_goal.instances.append(self, project)
        if self.rm_summary.offensive_words:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.DELETE,
                                                                     Placeholder.OFFENCE)
            self.hard_goals.append(hard_goal)
            # self_hard_goals.append(hard_goal)
            hard_goal.instances.append(self, project)
        if self.rm_summary.wishy_washy_words:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.DELETE,
                                                                     Placeholder.WISHY_WASHY_WORD)
            self.hard_goals.append(hard_goal)
            # self_hard_goals.append(hard_goal)
            hard_goal.instances.append(self, project)
        # what
        if self.rm_summary.suggested_solution:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.DELETE,
                                                                     Placeholder.SUGGESTED_SOLUTION)
            self.hard_goals.append(hard_goal)
            # self_hard_goals.append(hard_goal)
            hard_goal.instances.append(self, project)
        if self.rm_summary.actual_behavior is None:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.ADD,
                                                                     Placeholder.ACTUAL_BEHAVIOR)
            self.hard_goals.append(hard_goal)
            # self_hard_goals.append(hard_goal)
            hard_goal.instances.append(self, project)
        elif self.add_summary.actual_behavior is not None:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.MODIFY,
                                                                     Placeholder.ACTUAL_BEHAVIOR)
            self.rm_summary.is_actual_behavior_vague = True
            self.hard_goals.append(hard_goal)
            # self_hard_goals.append(hard_goal)
            hard_goal.instances.append(self, project)
        # when
        if self.rm_summary.trigger_action is None and self.add_summary.trigger_action is not None:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.ADD,
                                                                     Placeholder.TRIGGER_ACTION)
            self.hard_goals.append(hard_goal)
            # self_hard_goals.append(hard_goal)
            hard_goal.instances.append(self, project)
        elif self.rm_summary.trigger_action is not None and self.add_summary.trigger_action is not None:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.MODIFY,
                                                                     Placeholder.TRIGGER_ACTION)
            self.rm_summary.is_trigger_action_vague = True
            self.hard_goals.append(hard_goal)
            # self_hard_goals.append(hard_goal)
            hard_goal.instances.append(self, project)
        # where
        if self.rm_summary.platform is None and self.add_summary.platform is not None:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.ADD,
                                                                     Placeholder.PLATFORM)
            self.hard_goals.append(hard_goal)
            # self_hard_goals.append(hard_goal)
            hard_goal.instances.append(self, project)
        elif self.rm_summary.platform is not None and self.add_summary.platform is False:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.DELETE,
                                                                     Placeholder.PLATFORM)
            self.hard_goals.append(hard_goal)
            # self_hard_goals.append(hard_goal)
            hard_goal.instances.append(self, project)
        if self.rm_summary.component is None and self.add_summary.component is not None:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.ADD,
                                                                     Placeholder.COMPONENT)
            self.hard_goals.append(hard_goal)
            # self_hard_goals.append(hard_goal)
            hard_goal.instances.append(self, project)
        elif self.rm_summary.component is not None and self.add_summary.component is False:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.DELETE,
                                                                     Placeholder.COMPONENT)
            self.hard_goals.append(hard_goal)
            # self_hard_goals.append(hard_goal)
            hard_goal.instances.append(self, project)
        # return self_hard_goals


class SummaryPairs:
    def __init__(self, summary_pairs=None):
        self.summary_pairs = summary_pairs
        # self.length = len(self.summary_pairs)

    def __iter__(self):
        for summary_pair in self.summary_pairs:
            yield summary_pair

    def __getitem__(self, index):
        return self.summary_pairs[index]

    def __len__(self):
        return len(self.summary_pairs)

    # def get_length(self):
    #     return len(self.summary_pairs)

    def remove_by_id(self, bug_id, rm_summary_id=0, add_summary_id=1):
        for index, summary_pair in enumerate(self.summary_pairs):
            if summary_pair.bug.id == bug_id \
                    and summary_pair.rm_summary.id == rm_summary_id \
                    and summary_pair.add_summary.id == add_summary_id:
                # print(summary_pair)
                del self.summary_pairs[index]
                break

    def complete_vague_labels(self):
        for summary_pair in self.summary_pairs:
            summary_pair.complete_vague_labels()
            # print(summary_pair)

    def get_token_idf_dict(self):
        corpus = []
        summary_pair_nested_tokens_list = []
        for summary_pair in tqdm(self.summary_pairs, ascii=True):
            tokens_list = summary_pair.get_tokens()
            summary_pair_nested_tokens_list.append(tokens_list)
            tokens = ListUtil.flatten_list_of_groups(tokens_list)
            # print(tokens)
            corpus.append(tokens)
        word_idf_dict = NLPUtil.get_word_idf_dict(corpus)
        return word_idf_dict, summary_pair_nested_tokens_list

    def filter_unchanged(self):
        """
        mozilla:
            test bugs num: 2168
            summary_pairs num: 2621
        eclipse:
            test bugs num: 446
            summary_pairs num: 501
        1. if summary_pair.rm_summary.text == summary_pair.add_summary.text: remove
                                                     [mozilla, summary_pairs num: 2454]
                                                     [eclipse, summary_pairs num: 418]
        Returns:
        """
        filtered_summary_pairs = []
        for summary_pair in tqdm(self.summary_pairs, ascii=True):
            if summary_pair.rm_summary.text != summary_pair.add_summary.text:
                filtered_summary_pairs.append(summary_pair)
            # else:
            #     print(f"https://bugzilla.mozilla.org/show_bug.cgi?id={summary_pair.bug.id}")
            #     print(summary_pair.rm_summary.text)
            #     print(summary_pair.add_summary.text)
        return SummaryPairs(filtered_summary_pairs)

    def filter_up_to_date(self):
        """
        Returns:
        """

        filtered_summary_pairs = []
        for summary_pair in tqdm(self.summary_pairs, ascii=True):
            if summary_pair.is_change_from_desc():
                filtered_summary_pairs.append(summary_pair)
            # else:
            #     if MOZILLA_PROJ:
            #         print(f"https://bugzilla.mozilla.org/show_bug.cgi?id={summary_pair.bug.id}")
            #     else:
            #         print(f"https://bugs.eclipse.org/bugs/show_bug.cgi?id={summary_pair.bug.id}")

        return SummaryPairs(filtered_summary_pairs)

    def filter_for_goal_model_instances(self, bug_id_summary_ids_tuple_list=None):
        """
        1. description length [10, 500]
        # 2. replace structure with null
        Returns:
        """
        filtered_summary_pairs = []
        for summary_pair in self.summary_pairs:
            if bug_id_summary_ids_tuple_list:
                if (summary_pair.bug.id, summary_pair.rm_summary.id, summary_pair.add_summary.id) \
                        in bug_id_summary_ids_tuple_list:
                    continue
            bug = summary_pair.bug
            if 10 <= NLPUtil.calculate_token_num(bug.description.text) <= 500:
                filtered_summary_pairs.append(summary_pair)
            else:
                print(NLPUtil.calculate_token_num(bug.description.text))
                print(summary_pair)
        return SummaryPairs(filtered_summary_pairs)

    def random_sample_summary_pairs(self, sample_num=384):
        sample_summary_pairs = []
        sample_num_list = random.sample(range(0, len(self)), sample_num)
        for sample_num in sample_num_list:
            sample_summary_pairs.append(self.summary_pairs[sample_num])
        return SummaryPairs(sample_summary_pairs)

    def get_summary_pair_by_bug_id_summary_ids(self, bug_id, rm_summary_id, add_summary_id):
        for summary_pair in self.summary_pairs:
            if summary_pair.bug.id == bug_id and \
                    summary_pair.rm_summary.id == rm_summary_id and \
                    summary_pair.add_summary.id == add_summary_id:
                return summary_pair
        return None

    def get_summary_pair_by_bug_id_summary_texts(self, bug_id, rm_summary_text, add_summary_text):
        for summary_pair in self.summary_pairs:
            if summary_pair.bug.id == bug_id and \
                    summary_pair.rm_summary.text == rm_summary_text and \
                    summary_pair.add_summary.text == add_summary_text:
                return summary_pair

    def get_summary_pairs_by_bug_id(self, bug_id):
        summary_pairs = []
        for summary_pair in self.summary_pairs:
            if summary_pair.bug.id == bug_id:
                summary_pairs.append(summary_pair)
        return SummaryPairs(summary_pairs)

    def get_hard_goals(self, hard_goals, project=MOZILLA_PROJ):
        for summary_pair in self.summary_pairs:
            summary_pair.get_hard_goals(hard_goals, project)

    def remove_tags(self):
        for summary_pair in self.summary_pairs:
            summary_pair.remove_tags()

    def convert_summary_pairs_into_dataframe(self, folder_name=MOZILLA_PROJ):
        columns = ['bug id', 'bug link', 'summary id', 'summary',
                   Placeholder.SUGGESTED_SOLUTION, Placeholder.ACTUAL_BEHAVIOR, Placeholder.TRIGGER_ACTION,
                   Placeholder.IS_ACTUAL_BEHAVIOR_VAGUE, Placeholder.IS_TRIGGER_ACTION_VAGUE,
                   Placeholder.PLATFORM, Placeholder.COMPONENT,
                   Placeholder.SPELLING_ERROR, Placeholder.SYNTAX_ERROR,
                   Placeholder.DECLARATIVE_STATEMENT, Placeholder.PRESENT_TENSE,
                   Placeholder.PERSONAL_PRONOUN, Placeholder.EMOTIONAL_REACTION,
                   Placeholder.OFFENCE, Placeholder.WISHY_WASHY_WORD]

        # for index in range(5):
        #     columns.extend(['change from', 'change what', 'change for'])
        rows = []
        for summary_pair in self.summary_pairs:
            if folder_name == MOZILLA_PROJ:
                bug_link = f"https://bugzilla.mozilla.org/show_bug.cgi?id={summary_pair.bug.id}"
            else:
                bug_link = f"https://bugs.eclipse.org/bugs/show_bug.cgi?id={summary_pair.bug.id}"

            summaries = [summary_pair.rm_summary, summary_pair.add_summary]
            for summary in summaries:
                row = [summary_pair.bug.id, bug_link, summary.id, summary.text, ]
                for add_column in range(15):
                    row.extend([''])
                # row.append('')
                rows.append(row)
        df = pd.DataFrame(rows, columns=columns)
        return df

    def convert_summary_pairs_desc_info_into_dataframe(self, folder_name=MOZILLA_PROJ):
        columns = ['bug id', 'bug link', 'summary',
                   Placeholder.SUGGESTED_SOLUTION, Placeholder.ACTUAL_BEHAVIOR, Placeholder.TRIGGER_ACTION,
                   Placeholder.PLATFORM, Placeholder.COMPONENT]

        # for index in range(5):
        #     columns.extend(['change from', 'change what', 'change for'])
        rows = []
        for summary_pair in self.summary_pairs:
            if folder_name == MOZILLA_PROJ:
                bug_link = f"https://bugzilla.mozilla.org/show_bug.cgi?id={summary_pair.bug.id}"
            else:
                bug_link = f"https://bugs.eclipse.org/bugs/show_bug.cgi?id={summary_pair.bug.id}"

            summary_list = [summary_pair.rm_summary, summary_pair.add_summary]
            for summary in summary_list:
                row = [summary.bug.id, bug_link, summary.text,
                       summary.desc_suggested_solution,
                       summary.desc_actual_behavior,
                       summary.desc_trigger_action,
                       summary.desc_platform,
                       summary.desc_component]

                rows.append(row)
        df = pd.DataFrame(rows, columns=columns)
        return df

    def convert_summary_pairs_for_discriminator_info_into_dataframe(self, folder_name=MOZILLA_PROJ):
        columns = ['bug id', 'summary id', 'bug link', 'summary',
                   f'is {Placeholder.ACTUAL_BEHAVIOR} vague', f'is {Placeholder.TRIGGER_ACTION} vague',
                   Placeholder.SPELLING_ERROR, Placeholder.SYNTAX_ERROR, Placeholder.DECLARATIVE_STATEMENT,
                   Placeholder.PRESENT_TENSE, Placeholder.PERSONAL_PRONOUN, Placeholder.EMOTIONAL_REACTION,
                   Placeholder.OFFENCE, Placeholder.WISHY_WASHY_WORD]

        # for index in range(5):
        #     columns.extend(['change from', 'change what', 'change for'])
        rows = []
        for summary_pair in self.summary_pairs:
            if folder_name == MOZILLA_PROJ:
                bug_link = f"https://bugzilla.mozilla.org/show_bug.cgi?id={summary_pair.bug.id}"
            else:
                bug_link = f"https://bugs.eclipse.org/bugs/show_bug.cgi?id={summary_pair.bug.id}"

            summary_list = [summary_pair.rm_summary, summary_pair.add_summary]
            for summary in summary_list:
                row = [summary.bug.id, summary.id, bug_link, summary.text,
                       summary.is_actual_behavior_vague, summary.is_trigger_action_vague,
                       summary.spelling_error, summary.syntax_error, summary.declarative_statement,
                       summary.present_tense, summary.personal_pronoun, summary.emotional_reaction,
                       summary.offensive_words, summary.wishy_washy_words]

                rows.append(row)
        df = pd.DataFrame(rows, columns=columns)
        return df

    def split_summary_pairs_by_children_list_len(self, num):
        summary_pairs_list = ListUtil.list_of_groups(self.summary_pairs, num)
        # for summary_pairs in summary_pairs_list:
        #     summary_pairs = SummaryPairs(summary_pairs)
        return summary_pairs_list

    # def random_summaries(self, generation_summaries, generation_with_hardgoals_summaries,
    #                      rewritten_summaries, rewritten_with_hardgoals_summaries,
    #                      kg_without_instances_summaries, kg_with_instances_summaries,
    #                      reference_summaries):
    #     for index, summary_pair in enumerate(self.summary_pairs):

