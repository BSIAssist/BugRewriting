from bug_changing.types.answer import Answer, QA
from bug_changing.types.goal_model import HardGoals
from bug_changing.types.placeholder import Placeholder
from bug_changing.types.summary import SummaryPairs
from bug_changing.utils.llm_util import LLMUtil
from config import MOZILLA_PROJ, MOZILLA_SUMMARY_LEN, ECLIPSE_PROJ, ECLIPSE_SUMMARY_LEN


class Rewriter:
    def __init__(self):
        self.session_prompt = None
        self.hard_goals = None
        self.instances = None
        # self.session_prompt = None  # all about instances
        self.question_for_evaluated_answer = None
        # "The rewritten bug summary is one-sentence and satisfies the given conditions.\n"

        self.rewrite_prompt = "Please rewrite the bug summary based on the bug description by the following conditions:\n"
        self.rewritten_prompt = 'The rewritten summary: '

    def get_session_prompt(self, summary_len=None):
        """
        based on self.instances
        Returns:

        """
        self.session_prompt = f"I'm a bug summary rewriter. " \
                              f"I can rewrite the bug summary based on the bug description. " \
                              f"The rewritten bug summary is around {summary_len} words and " \
                              f"satisfies the given conditions.\n"

    @staticmethod
    def get_instance_intersection_diff_hardgoals_num_tuple_list(hardgoals, project=MOZILLA_PROJ):
        """
        return [(instance, intersection_hg_num, diff_hg_num), ... ,]
        """
        if hardgoals:
            instances = list()
            for hard_goal in hardgoals:
                if project == MOZILLA_PROJ:
                    instances_in_one_hg = hard_goal.instances.mozilla_instances
                else:
                    instances_in_one_hg = hard_goal.instances.eclipse_instances
                instances.extend(instances_in_one_hg)
            instances = set(instances)
            instance_hd_intersection_num_hd_diff_num_tuples = []
            for instance in instances:
                hd_intersection_num = len(set(instance.hard_goals).intersection(set(hardgoals)))
                hd_diff_num = len(set(instance.hard_goals) - set(hardgoals))
                instance_hd_intersection_num_hd_diff_num_tuples.append((instance, hd_intersection_num, hd_diff_num))
            if instance_hd_intersection_num_hd_diff_num_tuples:
                instance_hd_intersection_num_hd_diff_num_tuples = sorted(
                    instance_hd_intersection_num_hd_diff_num_tuples, key=lambda x: (-x[1], x[2]))
            return instance_hd_intersection_num_hd_diff_num_tuples

    def get_instances_by_hard_goal_repeat_num(self, hard_goal_repeat_num=2, project=MOZILLA_PROJ):
        final_instances = []
        hard_goal_num_dict = dict()
        update_hard_goals_flag = False
        if self.hard_goals:
            hard_goals = set(self.hard_goals)
            instance_hd_intersection_num_hd_diff_num_tuples = Rewriter.get_instance_intersection_diff_hardgoals_num_tuple_list(
                hard_goals, project)
            if instance_hd_intersection_num_hd_diff_num_tuples:
                index = 0
                while True:
                    if instance_hd_intersection_num_hd_diff_num_tuples:
                        # print(index)
                        # print(len(instance_hd_intersection_num_hd_diff_num_tuples))
                        instance = instance_hd_intersection_num_hd_diff_num_tuples[index][0]
                        if instance not in final_instances:
                            intersection_hgs = set(instance.hard_goals).intersection(hard_goals)
                            if intersection_hgs:
                                final_instances.append(instance)
                                for hard_goal in intersection_hgs:
                                    hard_goal_num_dict[hard_goal] = hard_goal_num_dict.get(hard_goal, 0) + 1
                                    if hard_goal_num_dict[hard_goal] >= hard_goal_repeat_num:
                                        hard_goals = hard_goals - {hard_goal}
                                        update_hard_goals_flag = True
                                if update_hard_goals_flag and hard_goals:
                                    # instances = set(instances) - set(final_instances)
                                    instance_hd_intersection_num_hd_diff_num_tuples = Rewriter.get_instance_intersection_diff_hardgoals_num_tuple_list(
                                        hard_goals, project)
                                    update_hard_goals_flag = False
                                    index = -1

                            else:
                                break
                        index = index + 1
                        if index >= len(instance_hd_intersection_num_hd_diff_num_tuples):
                            break
                    else:
                        break
        if final_instances:
            self.instances = final_instances
            return self.instances

    def get_instances(self, project=MOZILLA_PROJ):
        """
        based on self.hard_goals
        Args:
            project ():

        Returns:

        """
        instances, diff_hardgoals = self.get_subset_instances(project)
        # print(f"get subset instances: {len(instances)} {instances}")
        # print(f"diff_hardgoals: {len(diff_hardgoals)} {diff_hardgoals}")
        diff_instances = self.get_diff_instances(diff_hardgoals, project)
        # print(f"diff_instances: {len(diff_instances)} {diff_instances}")
        instances.extend(diff_instances)
        self.instances = SummaryPairs(instances)

    def get_subset_instances(self, project=MOZILLA_PROJ):
        """
        hardgoals = [a, b, c]
        subset_instance's hardgoals is equal to or subset of hardgoals
        Args:
            project ():

        Returns: [instance, instance, ...]
        """
        # self.instances = None
        # instance_hardgoal_num_dict = dict()
        instance_hardgoal_num_list = []
        if self.hard_goals:
            for hard_goal in self.hard_goals:
                if project == MOZILLA_PROJ:
                    instances = hard_goal.instances.mozilla_instances
                else:
                    instances = hard_goal.instances.eclipse_instances
                if instances:
                    for instance in instances:
                        # remove this restriction
                        if len(set(instance.hard_goals.hard_goals).union(set(self.hard_goals.hard_goals))) <= len(
                                self.hard_goals):
                            hardgoal_num = len(
                                set(instance.hard_goals.hard_goals).intersection(set(self.hard_goals.hard_goals)))
                            instance_hardgoal_num_list.append((instance, hardgoal_num))
                            # dict[instance] = instance_hardgoal_num_dict.get(instance, hardgoal_num)

            instance_hardgoal_num_list = sorted(instance_hardgoal_num_list, key=lambda x: -x[1])
        # print(instance_hardgoal_num_list)
        instances = []
        diff_hardgoals = None
        if len(instance_hardgoal_num_list) == 0:
            diff_hardgoals = set(self.hard_goals.hard_goals)
            return instances, diff_hardgoals
        # if instance_hardgoal_num_list:
        for index, instance_hardgoal_num in enumerate(instance_hardgoal_num_list):
            instance = instance_hardgoal_num[0]
            hardgoal_num = instance_hardgoal_num[1]
            if hardgoal_num == len(self.hard_goals):
                return [instance], diff_hardgoals
            else:
                if index == 0:
                    instances.append(instance)
                    diff_hardgoals = set(self.hard_goals.hard_goals) - set(instance.hard_goals)
                elif set(instance.hard_goals).intersection(diff_hardgoals):
                    instances.append(instance)
                    diff_hardgoals = diff_hardgoals - set(instance.hard_goals)
                    if len(diff_hardgoals) == 0:
                        return instances, diff_hardgoals
        return instances, diff_hardgoals

    def get_diff_instances(self, diff_hardgoals, project=MOZILLA_PROJ):
        """
        diff_hardgoals = [a, b, c]
        diff_instance's hardgoal = [a, d, e] has intersection with diff_hardgoals and also has the difference
                                             we try to make the intersection the more the better
                                                            the difference the less the better
        Args:
            diff_hardgoals ():
            project ():

        Returns: [diff_instance, diff_instance, ...]

        """
        instance_hardgoal_num_tuple_list = []
        # instance_hardgoal_num_list = None
        if diff_hardgoals:
            for hard_goal in diff_hardgoals:
                if project == MOZILLA_PROJ:
                    instances = hard_goal.instances.mozilla_instances
                else:
                    instances = hard_goal.instances.eclipse_instances
                if instances:
                    for instance in instances:
                        intersection_hardgoal_num = len(
                            set(instance.hard_goals.hard_goals).intersection(set(self.hard_goals.hard_goals)))
                        instance_hardgoal_num = len(instance.hard_goals)
                        instance_hardgoal_num_tuple_list.append((instance,
                                                                 intersection_hardgoal_num,
                                                                 instance_hardgoal_num))
            if instance_hardgoal_num_tuple_list:
                instance_hardgoal_num_tuple_list = sorted(instance_hardgoal_num_tuple_list, key=lambda x: (-x[1], x[2]))
        # print(instance_hardgoal_num_list)
        instances = []
        # rest_diff_hardgoals = None
        if instance_hardgoal_num_tuple_list:
            for instance_hardgoal_num_tuple in instance_hardgoal_num_tuple_list:
                instance = instance_hardgoal_num_tuple[0]
                if set(instance.hard_goals.hard_goals).intersection(set(diff_hardgoals)):
                    instances.append(instance)
                    diff_hardgoals = set(diff_hardgoals) - set(instance.hard_goals.hard_goals)
                    if len(diff_hardgoals) == 0:
                        break
        return instances

    def add_instances_into_chat_log(self):
        # self.get_instances(answer, goal_model, project)
        if self.instances:
            for instance in self.instances:
                # question = ''
                # question = question + f"Bug summary: {instance.rm_summary.text}\n"
                # question = question + f"Bug description: {Placeholder.TAG_DESCRIPTION[0]}{instance.bug.description.text}{Placeholder.TAG_DESCRIPTION[1]}\n"
                # question = question + self.rewrite_prompt
                # prompt = instance.hard_goals.generate_prompt()
                # question = question + prompt
                # question = question + self.rewritten_prompt
                question = self.question_from_evaluated_answer(instance, instance.rm_summary, False)
                answer = instance.add_summary.text
                LLMUtil.CHAT_LOG = LLMUtil.append_interaction_to_chat_log(question, answer, LLMUtil.CHAT_LOG)
            # question = question + f"\nAI: {instance.add_summary.text}\n"
        # self.session_prompt = question

    def convert_instances_into_prompt(self, rewrite_question_with_extrator_result=True):
        # self.get_instances(answer, goal_model, project)
        instance_prompt = ''
        if self.instances:
            for instance in self.instances:
                # instance_prompt = instance_prompt + self.session_prompt
                # instance_prompt = instance_prompt + f"Bug summary: {instance.rm_summary.text}\n"
                # instance_prompt = instance_prompt + f"Bug description: {Placeholder.TAG_DESCRIPTION[0]}{instance.bug.description.text}{Placeholder.TAG_DESCRIPTION[1]}\n"
                # instance_prompt = instance_prompt + self.rewrite_prompt
                # prompt = instance.hard_goals.generate_prompt()
                # instance_prompt = instance_prompt + prompt
                # instance_prompt = instance_prompt + self.rewritten_prompt
                instance_prompt = instance_prompt + self.question_from_evaluated_answer(instance, instance.rm_summary,
                                                                                        False,
                                                                                        rewrite_question_with_extrator_result)
                answer = instance.add_summary.text
                instance_prompt = instance_prompt + '\n' + answer + '\n\n'
        return instance_prompt

    def get_hard_goals(self, answer, goal_model):
        """
        @todo: self.hard_goals = HardGoals([])  # initiate: why must add [] ?
        Args:
            answer ():
            goal_model ():

        Returns:

        """
        self.hard_goals = HardGoals([])  # initiate: why must add [] ?
        hard_goals = goal_model.hard_goals
        if answer.suggested_solution is not None:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.DELETE,
                                                                     Placeholder.SUGGESTED_SOLUTION)
            self.hard_goals.append(hard_goal)
        if answer.actual_behavior is None and answer.desc_actual_behavior is not None:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.ADD,
                                                                     Placeholder.ACTUAL_BEHAVIOR)
            self.hard_goals.append(hard_goal)
        if answer.trigger_action is None and answer.desc_trigger_action is not None:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.ADD,
                                                                     Placeholder.TRIGGER_ACTION)
            self.hard_goals.append(hard_goal)
        if answer.platform is None and answer.desc_platform is not None:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.ADD,
                                                                     Placeholder.PLATFORM)
            self.hard_goals.append(hard_goal)
        if answer.component is None and answer.desc_component is not None:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.ADD,
                                                                     Placeholder.COMPONENT)
            self.hard_goals.append(hard_goal)
        if answer.is_actual_behavior_vague and answer.is_actual_behavior_vague[0]:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.MODIFY,
                                                                     Placeholder.ACTUAL_BEHAVIOR)
            self.hard_goals.append(hard_goal)
        if answer.is_trigger_action_vague and answer.is_trigger_action_vague[0]:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.MODIFY,
                                                                     Placeholder.TRIGGER_ACTION)
            self.hard_goals.append(hard_goal)
        if answer.spelling_error and answer.spelling_error[0]:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.MODIFY,
                                                                     Placeholder.SPELLING_ERROR)
            self.hard_goals.append(hard_goal)
        if answer.syntax_error and answer.syntax_error[0]:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.MODIFY,
                                                                     Placeholder.SYNTAX_ERROR)
            self.hard_goals.append(hard_goal)
        if answer.declarative_statement and answer.declarative_statement[0]:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.MODIFY,
                                                                     Placeholder.DECLARATIVE_STATEMENT)
            self.hard_goals.append(hard_goal)
        if answer.present_tense and not answer.present_tense[0]:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.MODIFY,
                                                                     Placeholder.PRESENT_TENSE)
            self.hard_goals.append(hard_goal)
        if answer.personal_pronoun and answer.personal_pronoun[0]:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.DELETE,
                                                                     Placeholder.PERSONAL_PRONOUN)
            self.hard_goals.append(hard_goal)
        if answer.emotional_reaction and not answer.emotional_reaction[0]:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.DELETE,
                                                                     Placeholder.EMOTIONAL_REACTION)
            self.hard_goals.append(hard_goal)
        if answer.offensive_words and answer.offensive_words[0]:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.DELETE,
                                                                     Placeholder.OFFENCE)
            self.hard_goals.append(hard_goal)
        if answer.wishy_washy_words and answer.wishy_washy_words[0]:
            hard_goal = hard_goals.get_hardgoal_by_action_and_target(Placeholder.DELETE,
                                                                     Placeholder.WISHY_WASHY_WORD)
            self.hard_goals.append(hard_goal)
        # return self.hard_goals

    def question_from_evaluated_answer(self, summary_pair, answer_or_instance_rm_summary=None, is_answer=True,
                                       rewrite_question_with_extrator_result=True):
        """
        based on self.hard_goals
        Returns:

        """
        # question = ''
        # question = question + self.session_prompt
        # if answer is None:
        question = f'Bug summary: {summary_pair.rm_summary.text}\n' \
                   f'Bug description: {Placeholder.TAG_DESCRIPTION[0]}{summary_pair.bug.description.text}{Placeholder.TAG_DESCRIPTION[1]}\n'
        # else:
        #     question = question + f'Bug summary: {summary_pair.rm_summary.text}\n' \
        #                           f'Bug description: {Placeholder.TAG_DESCRIPTION[0]}{summary_pair.bug.description.text}{Placeholder.TAG_DESCRIPTION[1]}\n\n' \
        #                           f'{Placeholder.SUGGESTED_SOLUTION} in the bug summary: {answer.suggested_solution}\n' \
        #                           f'{Placeholder.ACTUAL_BEHAVIOR} in the bug summary: {answer.actual_behavior}\n' \
        #                           f'{Placeholder.TRIGGER_ACTION} in the bug summary: {answer.trigger_action}\n' \
        #                           f'{Placeholder.PLATFORM} in the bug summary: {answer.platform}\n' \
        #                           f'{Placeholder.COMPONENT} in the bug summary: {answer.component}\n\n' \
        #                           f'{Placeholder.SUGGESTED_SOLUTION} in the bug description: {answer.desc_suggested_solution}\n' \
        #                           f'{Placeholder.ACTUAL_BEHAVIOR} in the bug description: {answer.desc_actual_behavior}\n' \
        #                           f'{Placeholder.TRIGGER_ACTION} in the bug description: {answer.desc_trigger_action}\n' \
        #                           f'{Placeholder.PLATFORM} in the bug description: {answer.desc_platform}\n' \
        #                           f'{Placeholder.COMPONENT} in the bug description: {answer.desc_component}\n'
        question = question + self.rewrite_prompt
        # prompt = self.hard_goals.generate_prompt()
        if is_answer:
            if rewrite_question_with_extrator_result:
                prompt = self.hard_goals.generate_prompt_with_extrator_result(answer_or_instance_rm_summary)
            else:
                prompt = self.hard_goals.generate_prompt()

        else:
            if rewrite_question_with_extrator_result:
                prompt = summary_pair.hard_goals.generate_prompt_with_extrator_result(answer_or_instance_rm_summary)
            else:
                prompt = summary_pair.hard_goals.generate_prompt()
        question = question + prompt
        question = question + self.rewritten_prompt
        self.question_for_evaluated_answer = question

        # question = f'Bug summary: {summary_pair.rm_summary.text}\n' \
        #            f'Bug description: <DESCRIPTION>{summary_pair.bug.description.text}</DESCRIPTION>\n'
        # question = question + self.rewrite_prompt
        # prompt = self.hard_goals.generate_prompt()
        # question = question + prompt
        # question = question + self.rewritten_prompt
        # self.question_for_evaluated_answer = question
        return self.question_for_evaluated_answer

    def convert_instances_into_qa_pairs(self, rewrite_question_with_extrator_result):
        qa_pairs = []
        if self.instances:
            for instance in self.instances:
                self.question_from_evaluated_answer(instance, instance.rm_summary, False,
                                                    rewrite_question_with_extrator_result)
                answer = instance.add_summary.text
                qa_pairs.append((self.question_for_evaluated_answer, answer))
        return qa_pairs

    def get_initial_messages(self, answer, goal_model, hard_goal_repeat_num, rewrite_question_with_extrator_result, project=MOZILLA_PROJ,
                             with_instances=True):
        """

        Args:
            answer ():
            goal_model ():
            hard_goal_repeat_num ():
            rewrite_question_with_extrator_result ():
            project ():
            with_instances ():

        Returns: messages contains 'session_prompt' and 'instances'
        """
        summary_len = None
        if project == MOZILLA_PROJ:
            summary_len = MOZILLA_SUMMARY_LEN
        elif project == ECLIPSE_PROJ:
            summary_len = ECLIPSE_SUMMARY_LEN
        self.get_session_prompt(summary_len)
        qa_pairs = None
        self.hard_goals = []
        self.instances = []
        if answer is not None:
            self.get_hard_goals(answer, goal_model)
            if with_instances:
                self.get_instances_by_hard_goal_repeat_num(hard_goal_repeat_num, project)
                qa_pairs = self.convert_instances_into_qa_pairs(rewrite_question_with_extrator_result)
        messages = LLMUtil.get_messages_for_turbo(self.session_prompt, qa_pairs)
        return messages

    def rewrite(self, summary_pair, answer, raw_answer, goal_model, project, with_instances=True,
                hard_goal_repeat_num=2, rewrite_question_with_extrator_result=True):
        """

        Args:
            rewrite_question_with_extrator_result ():
            hard_goal_repeat_num ():
            project ():
            goal_model ():
            summary_pair ():
            answer ():
            raw_answer ():
            with_instances (): if True: with instances
                                    else: without instances

        Returns:

        """
        # question = self.question_for_evaluated_answer
        # LLMUtil.CHAT_LOG = LLMUtil.change_chat_log_by_raw_answer(raw_answer)
        # print(len(self.hard_goals))

            # print(len(self.hard_goals))
            # if with_instances:
            #     # self.get_instances(project)
            #     self.get_instances_by_hard_goal_repeat_num(2)
        messages = self.get_initial_messages(answer, goal_model, hard_goal_repeat_num,
                                             rewrite_question_with_extrator_result, project,
                                             with_instances)
        self.question_from_evaluated_answer(summary_pair, answer, True, rewrite_question_with_extrator_result)
        messages = LLMUtil.add_role_content_dict_into_messages(LLMUtil.ROLE_USER,
                                                               self.question_for_evaluated_answer, messages)
        ans = LLMUtil.ask_turbo(messages)
        messages = LLMUtil.add_role_content_dict_into_messages(LLMUtil.ROLE_ASSISTANT, ans, messages)
        LLMUtil.show_messages(messages)

        # if llm is None:
        #     LLMUtil.CHAT_LOG = None
        #     if with_instances:
        #         self.add_instances_into_chat_log()
        #     self.question_from_evaluated_answer(summary_pair, answer, True, rewrite_question_with_extrator_result)
        #     question, ans = LLMUtil.question_answer(self.question_for_evaluated_answer)
        # else:
        #     if with_instances:
        #         instances_prompt = self.convert_instances_into_prompt(rewrite_question_with_extrator_result)
        #         self.question_from_evaluated_answer(summary_pair, answer, True, rewrite_question_with_extrator_result)
        #         question = instances_prompt + self.question_for_evaluated_answer
        #     else:
        #         self.question_from_evaluated_answer(summary_pair, answer, True, rewrite_question_with_extrator_result)
        #         question = self.question_for_evaluated_answer
        #     ans = llm.ask_davinci(question)
        #     if LLMUtil.reach_chatgpt_limited_request(ans, summary_pair):
        #         return None, None
        # question = self.question_for_evaluated_answer
        raw_answer.rewriter = QA(self.question_for_evaluated_answer, ans)
        ans = ans.replace('\n', ' ').replace('\r', '')
        answer.rewritten_summary = ans
        return answer, raw_answer
