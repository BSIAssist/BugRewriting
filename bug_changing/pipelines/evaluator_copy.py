import time

from bug_changing.types.answer import Answer, RawAnswer, QA
from bug_changing.types.goal_model import Targets
from bug_changing.types.placeholder import Placeholder
from bug_changing.utils.llm_util import LLMUtil
from config import MOZILLA_PROJ


class Evaluator:
    def __init__(self):
        self.extractor = Extractor()
        self.discriminator = Discriminator()

    # def change_chat_log_by_raw_answer(self, raw_answer):
    #     chat_log = None
    #     summary_question = self.extractor.summary_question
    #     summary_answer = raw_answer.extractor_summary.answer
    #     chat_log = LLMUtil.append_interaction_to_chat_log(summary_question, summary_answer, chat_log)
    #     desc_question = self.extractor.desc_question
    #     desc_answer = raw_answer.extractor_desc.answer
    #     chat_log = LLMUtil.append_interaction_to_chat_log(desc_question, desc_answer, chat_log)
    #     if raw_answer.discriminator:
    #         discriminator_question = self.discriminator.vague_understandable_concise_question
    #         discriminator_answer = raw_answer.discriminator.answer
    #         chat_log = LLMUtil.append_interaction_to_chat_log(discriminator_question, discriminator_answer, chat_log)
    #     return chat_log

    def change_chat_log_by_raw_answer(self, raw_answer):
        # chat_log = None
        chat_log = f"The {Placeholder.SUGGESTED_SOLUTION}, {Placeholder.ACTUAL_BEHAVIOR}, " \
                   f"{Placeholder.TRIGGER_ACTION}, {Placeholder.PLATFORM}, {Placeholder.COMPONENT} " \
                   f"in the Bug Summary: \n{raw_answer.extractor_summary.answer}\n" \
                   f"The {Placeholder.SUGGESTED_SOLUTION}, {Placeholder.ACTUAL_BEHAVIOR}, " \
                   f"{Placeholder.TRIGGER_ACTION}, {Placeholder.PLATFORM}, {Placeholder.COMPONENT} " \
                   f"in the Bug Description: \n{raw_answer.extractor_desc.answer}"
        # summary_question = self.extractor.summary_question
        # summary_answer = raw_answer.extractor_summary.answer
        # chat_log = LLMUtil.append_interaction_to_chat_log(summary_question, summary_answer, chat_log)
        # desc_question = self.extractor.desc_question
        # desc_answer = raw_answer.extractor_desc.answer
        # chat_log = LLMUtil.append_interaction_to_chat_log(desc_question, desc_answer, chat_log)
        if raw_answer.discriminator:
            discriminator_question = self.discriminator.vague_understandable_concise_question
            discriminator_answer = raw_answer.discriminator.answer
            chat_log = LLMUtil.append_interaction_to_chat_log(discriminator_question, discriminator_answer, chat_log)
        return chat_log

    def evaluate(self, summary_pair, llm=None):
        answer, raw_answer = self.extractor.extract_info_from_summary_pair(summary_pair, llm)
        if llm is None:
            LLMUtil.SESSION_PROMPT = None
            LLMUtil.CHAT_LOG = None
            # LLMUtil.CHAT_LOG = self.change_chat_log_by_raw_answer(raw_answer)
        time.sleep(5)
        # print(raw_answer)
        answer, raw_answer = self.discriminator.discriminate_info_from_ans(summary_pair, answer, raw_answer, llm)

        return answer, raw_answer

    def evaluate_rewritten_text(self, answer):
        pass


class Extractor:
    def __init__(self):
        self.system_role = 'system'
        self.question_role = 'user'
        self.answer_role = 'extractor'
        self.targets = None  # suggested solution, ..., component
        self.session_prompt = None  # a. only explanations of targets b. explanations of targets and instances
        self.instances = None
        self.summary_question = None
        self.desc_question = None

    def get_targets(self, all_targets, target_names=None):
        if target_names is None:
            target_names = [Placeholder.SUGGESTED_SOLUTION, Placeholder.ACTUAL_BEHAVIOR, Placeholder.TRIGGER_ACTION,
                            Placeholder.PLATFORM, Placeholder.COMPONENT]
        self.targets = []
        for target_name in target_names:
            target = all_targets.get_target_by_name(target_name)
            self.targets.append(target)

    def get_instances(self, summary_pairs, project=MOZILLA_PROJ):
        """
        Mozilla: suggested solution(1); actual behavior(5); trigger action(3); platform(2); component(3)
        (1115363, 1, 2): suggested solution
        https://bugzilla.mozilla.org/show_bug.cgi?id=1115363
        1	Storage Inspector's variables view should be selectable
            Storage Inspector's variables view should be selectable
        (1213421, 0, 1): actual behavior; trigger action; platform; component
        https://bugzilla.mozilla.org/show_bug.cgi?id=1213421
        0	Setting long body text in notification causes text to wrap on Win 10
            Setting long body text in notification causes text to wrap
            Setting long body text in notification
            on Win 10	 in notification
        (1300525, 0, 1): actual behavior; trigger action
        https://bugzilla.mozilla.org/show_bug.cgi?id=1300525
        0	After selecting a zoom level, navigation keys scroll through pdf levels, not through pages
            navigation keys scroll through pdf levels, not through pages
            After selecting a zoom level
        (1122695, 0, 1): actual behavior; trigger action
        https://bugzilla.mozilla.org/show_bug.cgi?id=1122695
        0	Error message misleading and missing "View Certificate" button when site uses SHA-1 certificate
            Error message misleading and missing "View Certificate" button
            when site uses SHA-1 certificate
        (1403460, 0, 1): actual behavior; platform; component
        https://bugzilla.mozilla.org/show_bug.cgi?id=1403460
        0	Clipboard loading bug in Firefox with Mac OS High Sierra
            Clipboard loading bug
            with Mac OS High Sierra	    in Firefox
        (677017, 0, 1): actual behavior; component
        https://bugzilla.mozilla.org/show_bug.cgi?id=677017
        0	incorrect domain highlighted in URL bar
            incorrect domain highlighted in URL bar
            in URL bar

        Eclipse: suggested solution(1); actual behavior(4); trigger action(2); platform(1); component(2)
        (318427, 0, 1): suggested solution
        https://bugs.eclipse.org/bugs/show_bug.cgi?id=318427
        0	ToolTip Support
            ToolTip Support
        (517139, 0, 1): actual behavior; trigger action
        https://bugs.eclipse.org/bugs/show_bug.cgi?id=517139
        0	Double click to initialize diagram does not make the double node disappear
            Double click to initialize diagram does not make the double node disappear
            Double click to initialize diagram
        (396843, 0, 1): actual behavior; trigger action; component
        https://bugs.eclipse.org/bugs/show_bug.cgi?id=396843
        0	DataSets from a Library AND Report are not possible when they use a DataSources from a Library
            DataSets from a Library AND Report are not possible
            when they use a DataSources from a Library
            from a Library
        (504349, 0, 1): actual behavior; platform
        https://bugs.eclipse.org/bugs/show_bug.cgi?id=504349
        0	Editor text display/ scrolling glitches with Windows 10
            Editor text display/ scrolling glitches with Windows 10
            Windows 10
        (494748, 0, 1): actual behavior; component
        https://bugs.eclipse.org/bugs/show_bug.cgi?id=494748
        0	Overly verbose Marketplace Client in "Report Bug or Enhancement Dialog"
            Overly verbose Marketplace Client in "Report Bug or Enhancement Dialog"
            in "Report Bug or Enhancement Dialog"
        Args:
            summary_pairs ():
            project ():

        Returns:

        """
        self.instances = []
        if project == MOZILLA_PROJ:
            bug_id_summary_ids_list = [(1115363, 1, 2), (1213421, 0, 1), (1300525, 0, 1),
                                       (1122695, 0, 1), (1403460, 0, 1), (677017, 0, 1)]
        else:
            bug_id_summary_ids_list = [(318427, 0, 1), (517139, 0, 1), (396843, 0, 1),
                                       (504349, 0, 1), (494748, 0, 1)]
        for bug_id_summary_ids in bug_id_summary_ids_list:
            instance = summary_pairs.get_summary_pair_by_bug_id_summary_ids(bug_id_summary_ids[0],
                                                                            bug_id_summary_ids[1],
                                                                            bug_id_summary_ids[2])
            self.instances.append(instance)

    def convert_instances_into_qa_pairs(self):
        qa_pairs = []
        if self.instances:
            for instance in self.instances:
                self.question_for_summary(instance.rm_summary)
                question = self.summary_question
                answer = f"{Placeholder.SUGGESTED_SOLUTION}: {instance.rm_summary.suggested_solution}\n" \
                         f"{Placeholder.ACTUAL_BEHAVIOR}: {instance.rm_summary.actual_behavior}\n" \
                         f"{Placeholder.TRIGGER_ACTION}: {instance.rm_summary.trigger_action}\n" \
                         f"{Placeholder.PLATFORM}: {instance.rm_summary.platform}\n" \
                         f"{Placeholder.COMPONENT}: {instance.rm_summary.component}\n\n"
                qa_pairs.append((question, answer))
        return qa_pairs

    def convert_instances_into_prompts(self):
        instance_prompts = None
        if self.instances:
            instance_prompts = []
            for instance in self.instances:
                self.question_for_summary(instance.rm_summary)
                question = self.summary_question
                answer = f"{Placeholder.SUGGESTED_SOLUTION}: {instance.rm_summary.suggested_solution}\n" \
                         f"{Placeholder.ACTUAL_BEHAVIOR}: {instance.rm_summary.actual_behavior}\n" \
                         f"{Placeholder.TRIGGER_ACTION}: {instance.rm_summary.trigger_action}\n" \
                         f"{Placeholder.PLATFORM}: {instance.rm_summary.platform}\n" \
                         f"{Placeholder.COMPONENT}: {instance.rm_summary.component}\n\n"
                instance = question + answer
                instance_prompts.append(instance)
        return instance_prompts

    def get_session_prompt(self, all_targets):
        self.session_prompt = f"I am a text {self.answer_role}. " \
                              "I can extract specific parts directly from a given bug report. " \
                              "All extracted parts are the substring of the bug report. " \
                              "If a specific part doesn't exist in the bug report, I will response with 'None'." \
                              "The specific parts are as follows:\n"
        self.get_targets(all_targets)
        for target in self.targets:
            target_intro = f"\t{target.name}: {target.explanation}\n"
            self.session_prompt = self.session_prompt + target_intro
        # target_intro = f"{Placeholder.SUGGESTED_SOLUTION}: the conjecture or proposed fix for the bug\n" \
        #                f"{Placeholder.ACTUAL_BEHAVIOR}: the observed behavior of the system or software being reported as having a bug or issue\n" \
        #                f"{Placeholder.TRIGGER_ACTION}: the brief description of the action or event that causes the bug to occur\n" \
        #                f"{Placeholder.PLATFORM}: platform-level where the issue is occurring, platform is the specific operating system, hardware, or other environment in which the system or application is being used\n" \
        #                f"{Placeholder.COMPONENT}: component-level where the issue is occurring, component is the specific part or subsystem of the system or application in which the issue is occurring\n\n"
        # self.session_prompt = self.session_prompt + target_intro

    # def get_session_prompt(self, all_targets, instance_summary_pairs, project=MOZILLA_PROJ, with_instances=True):
    #     self.session_prompt = f"I am a text {self.answer_role}. " \
    #                           "I can extract specific parts directly from a given bug report. " \
    #                           "All extracted parts are the substring of the bug report. " \
    #                           "If a specific part doesn't exist in the bug report, I will response with 'None'.\n"
    #     # self.get_targets(all_targets)
    #     # for target in self.targets:
    #     #     target_intro = f"{target.name}: {target.explanation}\n"
    #     #     self.session_prompt = self.session_prompt + target_intro
    #     target_intro = f"{Placeholder.SUGGESTED_SOLUTION}: the conjecture or proposed fix for the bug\n" \
    #                    f"{Placeholder.ACTUAL_BEHAVIOR}: the observed behavior of the system or software being reported as having a bug or issue\n" \
    #                    f"{Placeholder.TRIGGER_ACTION}: the brief description of the action or event that causes the bug to occur\n" \
    #                    f"{Placeholder.PLATFORM}: platform-level where the issue is occurring, platform is the specific operating system, hardware, or other environment in which the system or application is being used\n" \
    #                    f"{Placeholder.COMPONENT}: component-level where the issue is occurring, component is the specific part or subsystem of the system or application in which the issue is occurring\n\n"
    #     self.session_prompt = self.session_prompt + target_intro
    #     if with_instances:
    #         self.get_instances(instance_summary_pairs, project)
    #         if self.instances:
    #             instance_prompts = self.convert_instances_into_prompts()
    #             for instance_prompt in instance_prompts:
    #                 self.session_prompt = self.session_prompt + instance_prompt
    #     # print(self.session_prompt)

    def question_for_summary(self, summary):
        self.summary_question = f"Bug summary: {summary.text}\n" \
                                f"Please extract the {Placeholder.SUGGESTED_SOLUTION}, " \
                                f"{Placeholder.ACTUAL_BEHAVIOR}, {Placeholder.TRIGGER_ACTION}, " \
                                f"{Placeholder.PLATFORM}, {Placeholder.COMPONENT} from the bug summary " \
                                f"(if don't exist, respond with None):\n"
        # self.summary_question = f"Bug summary: {summary.text}\n" \
        #                         f"Please extract the following sections from the bug summary:\n" \
        #                         f"{Placeholder.SUGGESTED_SOLUTION}: \n" \
        #                         f"{Placeholder.ACTUAL_BEHAVIOR}: \n" \
        #                         f"{Placeholder.TRIGGER_ACTION}: \n" \
        #                         f"{Placeholder.PLATFORM}: \n" \
        #                         f"{Placeholder.COMPONENT}: \n" \
        #                         f"Bug description: <DESCRIPTION>{summary.bug.description.text}</DESCRIPTION>\n" \
        #                         f"Please extract the following sections from the bug description:\n" \
        #                         f"{Placeholder.SUGGESTED_SOLUTION}: \n" \
        #                         f"{Placeholder.ACTUAL_BEHAVIOR}: \n" \
        #                         f"{Placeholder.TRIGGER_ACTION}: \n" \
        #                         f"{Placeholder.PLATFORM}: \n" \
        #                         f"{Placeholder.COMPONENT}: \n"

    def question_for_description(self, description):
        # <DESCRIPTION>{description.text}</DESCRIPTION>
        # self.description_question = f"Bug description: <DESCRIPTION>{description.text}</DESCRIPTION>\n" \
        #                             f"Please extract the {Placeholder.SUGGESTED_SOLUTION}, " \
        #                             f"{Placeholder.ACTUAL_BEHAVIOR}, {Placeholder.TRIGGER_ACTION}, " \
        #                             f"{Placeholder.PLATFORM}, {Placeholder.COMPONENT} from the bug description:\n"
        self.desc_question = f"Bug description: {Placeholder.TAG_DESCRIPTION[0]}{description.text}{Placeholder.TAG_DESCRIPTION[1]}\n" \
                             f"Please extract the {Placeholder.SUGGESTED_SOLUTION}, " \
                             f"{Placeholder.ACTUAL_BEHAVIOR}, {Placeholder.TRIGGER_ACTION}, " \
                             f"{Placeholder.PLATFORM}, {Placeholder.COMPONENT} from the bug description " \
                             f"(if don't exist, respond with None):\n"

    def get_messages(self, instance_summary_pairs, project=MOZILLA_PROJ, with_instances=True):
        qa_pairs = None
        if with_instances:
            self.get_instances(instance_summary_pairs, project)
            qa_pairs = self.convert_instances_into_qa_pairs()
        messages = LLMUtil.get_messages_for_turbo(self.system_role, self.question_role, self.answer_role,
                                                  self.session_prompt, qa_pairs)
        return messages

    def add_question_into_messages(self, question, messages):
        role_content_dict = {'role': f'{self.question_role}', 'content': f'{question}'}
        messages.append(role_content_dict)
        return messages

    def extract_info_from_summary_pair(self, summary_pair, instance_summary_pairs, project, with_instances=True):
        messages = self.get_messages(instance_summary_pairs, project, with_instances)
        # extract summary
        self.question_for_summary(summary_pair.rm_summary)
        # print(self.summary_question)
        # input()
        if llm is None:
            summary_question, summary_answer = LLMUtil.question_answer(self.summary_question)
        else:
            summary_question = LLMUtil.SESSION_PROMPT + '\n' + self.summary_question
            summary_answer = llm.ask_davinci(summary_question)
            if LLMUtil.reach_chatgpt_limited_request(summary_answer, summary_pair):
                return None, None
        # summary_answer = Answer.extract_answers(summary_answer)
        time.sleep(5)
        # extract description
        self.question_for_description(summary_pair.bug.description)
        if llm is None:
            desc_question, desc_answer = LLMUtil.question_answer(self.desc_question)
        else:
            desc_answer = llm.ask_davinci(self.desc_question)
            desc_question = self.desc_question
            if LLMUtil.reach_chatgpt_limited_request(desc_answer, summary_pair):
                return None, None
        # desc_question, desc_answer = LLMUtil.question_answer(self.desc_question)
        # print(summary_question)
        # print(summary_answer)
        # print(desc_question)
        # print(desc_answer)
        answer = Answer.from_answer(summary_pair, summary_answer, desc_answer)
        raw_answer = RawAnswer(summary_pair, QA(summary_question, summary_answer), QA(desc_question, desc_answer))

        # answer = Answer.from_answer(summary_pair, summary_answer)
        # raw_answer = RawAnswer(summary_pair, QA(summary_question, summary_answer))

        return answer, raw_answer
        # return answer

    def extract_info_from_desc(self, description, llm=None):
        """

        Args:
            description ():
            llm ():

        Returns: desc_answer [, , , ,], raw_answer: string

        """
        # extract description
        self.question_for_description(description)
        # desc_question = LLMUtil.SESSION_PROMPT + '\n' + self.desc_question
        if llm is None:
            desc_question, desc_answer = LLMUtil.question_answer(self.desc_question)
        else:
            desc_question = LLMUtil.SESSION_PROMPT + '\n' + self.desc_question
            desc_answer = llm.ask_davinci(desc_question)
            # desc_question = self.desc_question
        # if desc_answer:
        raw_answer = desc_answer
        desc_answer = Answer.extract_answer_from_text_for_extractor(desc_answer)

        return desc_answer, raw_answer

    # def extract_info_from_summary_pair(self, summary_pair, llm=None):
    #     # extract summary
    #     self.question_for_summary(summary_pair.rm_summary)
    #     # print(self.summary_question)
    #     # input()
    #     if llm is None:
    #         summary_question, summary_answer = LLMUtil.question_answer(self.summary_question)
    #     else:
    #         summary_question = LLMUtil.SESSION_PROMPT + '\n' + self.summary_question
    #         summary_answer = llm.ask_davinci(summary_question)
    #         if LLMUtil.reach_chatgpt_limited_request(summary_answer, summary_pair):
    #             return None, None
    #     # summary_answer = Answer.extract_answers(summary_answer)
    #     time.sleep(5)
    #     # extract description
    #     self.question_for_description(summary_pair.bug.description)
    #     if llm is None:
    #         desc_question, desc_answer = LLMUtil.question_answer(self.desc_question)
    #     else:
    #         desc_answer = llm.ask_davinci(self.desc_question)
    #         desc_question = self.desc_question
    #         if LLMUtil.reach_chatgpt_limited_request(desc_answer, summary_pair):
    #             return None, None
    #     # desc_question, desc_answer = LLMUtil.question_answer(self.desc_question)
    #     # print(summary_question)
    #     # print(summary_answer)
    #     # print(desc_question)
    #     # print(desc_answer)
    #     answer = Answer.from_answer(summary_pair, summary_answer, desc_answer)
    #     raw_answer = RawAnswer(summary_pair, QA(summary_question, summary_answer), QA(desc_question, desc_answer))
    #
    #     # answer = Answer.from_answer(summary_pair, summary_answer)
    #     # raw_answer = RawAnswer(summary_pair, QA(summary_question, summary_answer))
    #
    #     return answer, raw_answer
    #     # return answer
    #
    # def extract_info_from_desc(self, description, llm=None):
    #     """
    #
    #     Args:
    #         description ():
    #         llm ():
    #
    #     Returns: desc_answer [, , , ,], raw_answer: string
    #
    #     """
    #     # extract description
    #     self.question_for_description(description)
    #     # desc_question = LLMUtil.SESSION_PROMPT + '\n' + self.desc_question
    #     if llm is None:
    #         desc_question, desc_answer = LLMUtil.question_answer(self.desc_question)
    #     else:
    #         desc_question = LLMUtil.SESSION_PROMPT + '\n' + self.desc_question
    #         desc_answer = llm.ask_davinci(desc_question)
    #         # desc_question = self.desc_question
    #     # if desc_answer:
    #     raw_answer = desc_answer
    #     desc_answer = Answer.extract_answer_from_text_for_extractor(desc_answer)
    #
    #     return desc_answer, raw_answer


class Discriminator:
    def __init__(self):
        self.session_prompt = None
        self.instances = None
        self.actual_behavior_question = None
        self.trigger_action_question = None

        self.vague_understandable_concise_question = None

        # easy to understand
        self.spelling_question = f"Does the bug summary have the {Placeholder.SPELLING_ERROR}?"
        self.syntax_question = f"Does the bug summary have the {Placeholder.SYNTAX_ERROR}?"
        self.declarative_statement_question = f"Is the bug summary a question?"
        self.present_tense_question = f"Does the bug summary use the {Placeholder.PRESENT_TENSE}?"

        # concise
        # self.concise_question = None
        self.personal_pronoun_question = f"Does the bug summary use the {Placeholder.PERSONAL_PRONOUN}?"
        self.emotional_reaction_question = None
        self.offence_question = f"Does the bug summary use the {Placeholder.OFFENCE}?"
        self.wishy_washy_words_question = f"Does the bug summary use the {Placeholder.WISHY_WASHY_WORD}?"

    def get_instances(self, summary_pairs, project=MOZILLA_PROJ):
        """
        Mozilla: 9 instances
                 is_actual_behavior_vague(6); is_trigger_action_vague(2);
                 spelling error(); syntax error();
                 declarative statement(1); present tense(0); personal pronoun(1); emotional reaction(1);
                 offensive words(1); wishy-washy words(1);
            https://bugzilla.mozilla.org/show_bug.cgi?id=581023
            (581023, 0, 1): is_actual_behavior_vague(add constraints); is_trigger_action_vague(specific)
                # https://bugzilla.mozilla.org/show_bug.cgi?id=1218099
                # (1218099, 0, 1): is_actual_behavior_vague(add details); personal pronoun(I)
            https://bugzilla.mozilla.org/show_bug.cgi?id=1121800
            (1121800, 0, 1): is_actual_behavior_vague(specific add details); wishy-washy words(can't seem to)
            https://bugzilla.mozilla.org/show_bug.cgi?id=1217216
            (1217216, 0, 1): is_actual_behavior_vague(add details); is_trigger_action_vague(add details)
                # https://bugzilla.mozilla.org/show_bug.cgi?id=902486
                # (902486, 0, 1): is_actual_behavior_vague(specific); is_trigger_action_vague(add details)
            https://bugzilla.mozilla.org/show_bug.cgi?id=1606300
            (1606300, 0, 1): is_actual_behavior_vague(specific); personal pronoun(I try to save)
                # https://bugzilla.mozilla.org/show_bug.cgi?id=1583398
                # (1583398, 0, 1): is_actual_behavior_vague(specific); present tense(did)
                # https://bugzilla.mozilla.org/show_bug.cgi?id=1122695
                # (1122695, 0, 1): is_actual_behavior_vague(specific); is_trigger_action_vague(specific)
                # https://bugzilla.mozilla.org/show_bug.cgi?id=1294426
                # (1294426, 0, 1): is_actual_behavior_vague(specific); declarative statement(Why fonts in hints are bigger than in the address field?)
                # https://bugzilla.mozilla.org/show_bug.cgi?id=1297839
                # (1297839, 0, 1): offensive words(Firefox Developers Remove Everything Good)
                # https://bugzilla.mozilla.org/show_bug.cgi?id=1629639
                # (1629639, 0, 1): emotional reaction(Urlbar Search Tips is annoying)
                # https://bugzilla.mozilla.org/show_bug.cgi?id=831452
                # (831452, 1, 2): personal pronoun(When you)
        Args:
            summary_pairs ():
            project ():

        Returns:

        """
        self.instances = []
        if project == MOZILLA_PROJ:
            bug_id_summary_ids_list = [(581023, 0, 1), (1121800, 0, 1), (1217216, 0, 1),
                                       (1606300, 0, 1),
                                       # (1583398, 0, 1),
                                       # (1294426, 0, 1),
                                       # (1297839, 0, 1),
                                       # (1629639, 0, 1),
                                       # (831452, 1, 2)
                                       ]
        else:
            bug_id_summary_ids_list = []
        for bug_id_summary_ids in bug_id_summary_ids_list:
            instance = summary_pairs.get_summary_pair_by_bug_id_summary_ids(bug_id_summary_ids[0],
                                                                            bug_id_summary_ids[1],
                                                                            bug_id_summary_ids[2])
            self.instances.append(instance)

    def get_session_prompt(self, instance_summary_pairs, project=MOZILLA_PROJ, with_instances=True):
        self.session_prompt = f"I am a text discriminator. " \
                              "I can assess the quality of text by providing 'Yes' or 'No' answers to specific questions while also explaining my reasoning.\n"
        # "Especially, I can determine whether an actual behavior or trigger action needs refinement based on the reference by the following aspects:\n" \
        # "\t1. whether it can be modified from being vague or unclear to specific, to-the-point and providing clear and detailed information\n" \
        # "\t2. whether more details such as necessary conditions or constraints need to be added to define the scope of impact\n" \
        # "\t3. whether it can be more precise to prevent confusion and misleading\n" \
        # "\t4. whether more standard language and terminology can be used to ensure consistency across bug reports\n"
        # self.session_prompt = self.session_prompt + target_intro
        if with_instances:
            self.get_instances(instance_summary_pairs, project)
            if self.instances:
                # self.session_prompt = self.session_prompt + '\n' + f'The followings are {len(self.instances)} instances for questions and answers:' + '\n\n'
                instance_prompts = self.convert_instances_into_prompts()
                for index, instance_prompt in enumerate(instance_prompts):
                    # if index == 0:
                    #     self.session_prompt = instance_prompt
                    # else:
                    # self.session_prompt = self.session_prompt + f'\n\nInstance {index + 1}: ' + instance_prompt
                    self.session_prompt = self.session_prompt + instance_prompt

    def convert_instances_into_prompts(self):
        instance_prompts = None
        if self.instances:
            instance_prompts = []
            for instance in self.instances:
                self.question_for_vague_understandable_concise(instance.rm_summary, instance.rm_summary)
                question = self.vague_understandable_concise_question
                count = 1
                answer = ''
                if instance.rm_summary.is_actual_behavior_vague:
                    answer = answer + f"{count}. Yes, {instance.rm_summary.is_actual_behavior_vague}\n"
                    count = count + 1
                elif instance.rm_summary.actual_behavior and instance.rm_summary.desc_actual_behavior:
                    answer = answer + f"{count}. No, {Placeholder.ACTUAL_BEHAVIOR} from bug summary don't need to be refined by {Placeholder.ACTUAL_BEHAVIOR} from bug description\n"
                    count = count + 1
                if instance.rm_summary.is_trigger_action_vague:
                    answer = answer + f"{count}. Yes, {instance.rm_summary.is_trigger_action_vague}\n"
                    count = count + 1
                elif instance.rm_summary.trigger_action and instance.rm_summary.desc_trigger_action:
                    answer = answer + f"{count}. No, {Placeholder.TRIGGER_ACTION} from bug summary don't need to be refined by {Placeholder.TRIGGER_ACTION} from bug description\n"
                    count = count + 1
                if instance.rm_summary.spelling_error:
                    answer = answer + f"{count}. Yes, this bug summary has the {Placeholder.SPELLING_ERROR}: {instance.rm_summary.spelling_error}. Should be '{instance.add_summary.spelling_error}'\n"
                    count = count + 1
                else:
                    answer = answer + f"{count}. No, no {Placeholder.SPELLING_ERROR}\n"
                    count = count + 1
                if instance.rm_summary.syntax_error:
                    answer = answer + f"{count}. Yes, this bug summary has the {Placeholder.SYNTAX_ERROR}: '{instance.rm_summary.syntax_error}'. Should be '{instance.add_summary.syntax_error}'\n"
                    count = count + 1
                else:
                    answer = answer + f"{count}. No, no {Placeholder.SYNTAX_ERROR}\n"
                    count = count + 1
                if instance.rm_summary.declarative_statement:
                    answer = answer + f"{count}. Yes, this bug summary is a question: '{instance.rm_summary.declarative_statement}'. Can be rewritten into a {Placeholder.DECLARATIVE_STATEMENT} '{instance.add_summary.declarative_statement}'\n"
                    count = count + 1
                else:
                    answer = answer + f"{count}. No, this bug summary is not a question\n"
                    count = count + 1
                if instance.rm_summary.present_tense:
                    answer = answer + f"{count}. No, this bug summary doesn't use the {Placeholder.PRESENT_TENSE}: '{instance.rm_summary.present_tense}'. Can be rewritten into '{instance.add_summary.present_tense}'\n"
                    count = count + 1
                else:
                    answer = answer + f"{count}. Yes, this bug summary uses the {Placeholder.PRESENT_TENSE}\n"
                    count = count + 1
                if instance.rm_summary.personal_pronoun:
                    answer = answer + f"{count}. Yes, this bug summary use the {Placeholder.PERSONAL_PRONOUN}: '{instance.rm_summary.personal_pronoun}'\n"
                    count = count + 1
                else:
                    answer = answer + f"{count}. No, this bug summary doesn't use the {Placeholder.PERSONAL_PRONOUN}\n"
                    count = count + 1
                if instance.rm_summary.emotional_reaction:
                    answer = answer + f"{count}. No, this bug summary has the {Placeholder.EMOTIONAL_REACTION}: '{instance.rm_summary.emotional_reaction}'\n"
                    count = count + 1
                else:
                    answer = answer + f"{count}. Yes, this bug summary doesn't have the {Placeholder.EMOTIONAL_REACTION}\n"
                    count = count + 1
                if instance.rm_summary.offensive_words:
                    answer = answer + f"{count}. Yes, this bug summary has the {Placeholder.OFFENCE}: '{instance.rm_summary.offensive_words}'. Be impolite\n"
                    count = count + 1
                else:
                    answer = answer + f"{count}. No, this bug summary doesn't have the {Placeholder.OFFENCE}\n"
                    count = count + 1
                if instance.rm_summary.wishy_washy_words:
                    answer = answer + f"{count}. Yes, this bug summary has the {Placeholder.WISHY_WASHY_WORD}: '{instance.rm_summary.wishy_washy_words}'\n"
                    # count = count + 1
                else:
                    answer = answer + f"{count}. No, this bug summary doesn't have the {Placeholder.WISHY_WASHY_WORD}\n\n"
                    # count = count + 1

                # instance = LLMUtil.QUESTION_SEQUENCE + question + LLMUtil.ANSWER_SEQUENCE + answer
                instance = question + '\n' + answer
                instance_prompts.append(instance)
        return instance_prompts

    def question_for_actual_behavior(self, summary_actual_behavior, description_actual_behavior):
        # self.actual_behavior_question = f"{Placeholder.ACTUAL_BEHAVIOR} in summary: {summary_actual_behavior}\n" \
        #                                 f"{Placeholder.ACTUAL_BEHAVIOR} in description: {description_actual_behavior}\n" \
        #                                 f"Answer the question by Yes or No and explain the reason. " \
        #                                 f"Can the {Placeholder.ACTUAL_BEHAVIOR} in summary can be refined based on " \
        #                                 f"the {Placeholder.ACTUAL_BEHAVIOR} in description?"
        if summary_actual_behavior is not None and description_actual_behavior is not None:
            self.actual_behavior_question = f"Can the actual behavior {Placeholder.TAG_ACTUAL_BEHAVIOR[0]}{summary_actual_behavior}{Placeholder.TAG_ACTUAL_BEHAVIOR[1]} be refined based on " \
                                            f"{Placeholder.TAG_ACTUAL_BEHAVIOR[0]}{description_actual_behavior}{Placeholder.TAG_ACTUAL_BEHAVIOR[1]}?"
            # self.actual_behavior_question = f"Can the actual behavior {Placeholder.TAG_ACTUAL_BEHAVIOR[0]}{summary_actual_behavior}{Placeholder.TAG_ACTUAL_BEHAVIOR[1]} be more specific by adding more details from " \
            #                                 f"{Placeholder.TAG_ACTUAL_BEHAVIOR[0]}{description_actual_behavior}{Placeholder.TAG_ACTUAL_BEHAVIOR[1]}?"
            # f" by these aspects: " \
            # f"a. from being vague to specific and providing clear and detailed information; " \
            # f"b. add more details such as necessary constraints to increase or decrease the impact; " \
            # f"c. more precise to prevent confusion and misleading; " \
            # f"d. more standard language and terminology can be used to ensure consistency across bug reports?"

    def question_for_trigger_action(self, summary_trigger_action, description_trigger_action):
        # self.trigger_action_question = f"{Placeholder.TRIGGER_ACTION} in summary: {summary_trigger_action}\n" \
        #                                f"{Placeholder.TRIGGER_ACTION} in description: {description_trigger_action}\n" \
        #                                f"Answer the question by Yes or No and explain the reason. " \
        #                                f"Does the {Placeholder.TRIGGER_ACTION} in summary can be refined based on " \
        #                                f"the {Placeholder.TRIGGER_ACTION} in description?"
        if summary_trigger_action is not None and description_trigger_action is not None:
            self.trigger_action_question = f"Can the trigger action {Placeholder.TAG_TRIGGER_ACTION[0]}{summary_trigger_action}{Placeholder.TAG_TRIGGER_ACTION[1]} be refined based on " \
                                           f"{Placeholder.TAG_TRIGGER_ACTION[0]}{description_trigger_action}{Placeholder.TAG_TRIGGER_ACTION[1]}?" \
                # self.trigger_action_question = f"Can the trigger action {Placeholder.TAG_TRIGGER_ACTION[0]}{summary_trigger_action}{Placeholder.TAG_TRIGGER_ACTION[1]} be more specific by adding more details from " \
            #                                f"{Placeholder.TAG_TRIGGER_ACTION[0]}{description_trigger_action}{Placeholder.TAG_TRIGGER_ACTION[1]}?"
            # f"by these aspects: " \
            #  f"a. from being vague to specific and providing clear and detailed information; " \
            #  f"b. add more details such as necessary constraints to increase or decrease the impact; " \
            #  f"c. more precise to prevent confusion and misleading; " \
            #  f"d. more standard language and terminology can be used to ensure consistency across bug reports?"

    def question_for_vague_understandable_concise(self, summary, answer):

        # self.vague_understandable_concise_question = f"{self.session_prompt}" \
        self.vague_understandable_concise_question = f"Bug summary: {summary.text}\n" \
                                                     f"Answer the following questions individually by Yes or No and explain " \
                                                     f"the reason:\n "
        # vague
        self.question_for_actual_behavior(answer.actual_behavior, answer.desc_actual_behavior)
        self.question_for_trigger_action(answer.trigger_action, answer.desc_trigger_action)
        # understandable
        self.question_for_spelling(summary)
        self.question_for_syntax(summary)
        self.question_for_declarative_statement(summary)
        self.question_for_present_tense(summary)
        # concise
        self.question_for_personal_pronoun(summary)
        self.question_for_emotional_reaction(summary)
        self.question_for_offence(summary)
        self.question_for_wishy_washy_words(summary)

        count = 1
        if answer.actual_behavior is not None and answer.desc_actual_behavior is not None:
            self.vague_understandable_concise_question = self.vague_understandable_concise_question + f"\t{count}. " \
                                                                                                      f"{self.actual_behavior_question}\n"
            count = count + 1
        if answer.trigger_action is not None and answer.desc_trigger_action is not None:
            self.vague_understandable_concise_question = self.vague_understandable_concise_question + f"\t{count}. " \
                                                                                                      f"{self.trigger_action_question}\n"
            count = count + 1
        self.vague_understandable_concise_question = self.vague_understandable_concise_question + f"\t{count}. " \
                                                                                                  f"{self.spelling_question}\n"
        count = count + 1
        self.vague_understandable_concise_question = self.vague_understandable_concise_question + f"\t{count}. " \
                                                                                                  f"{self.syntax_question}\n"
        count = count + 1
        self.vague_understandable_concise_question = self.vague_understandable_concise_question + f"\t{count}. " \
                                                                                                  f"{self.declarative_statement_question}\n"
        count = count + 1
        self.vague_understandable_concise_question = self.vague_understandable_concise_question + f"\t{count}. " \
                                                                                                  f"{self.present_tense_question}\n"
        count = count + 1
        self.vague_understandable_concise_question = self.vague_understandable_concise_question + f"\t{count}. " \
                                                                                                  f"{self.personal_pronoun_question}\n"
        count = count + 1
        self.vague_understandable_concise_question = self.vague_understandable_concise_question + f"\t{count}. " \
                                                                                                  f"{self.emotional_reaction_question}\n"
        count = count + 1
        self.vague_understandable_concise_question = self.vague_understandable_concise_question + f"\t{count}. " \
                                                                                                  f"{self.offence_question}\n"
        count = count + 1
        self.vague_understandable_concise_question = self.vague_understandable_concise_question + f"\t{count}. " \
                                                                                                  f"{self.wishy_washy_words_question}\n"

    # def question_for_understandable_concise(self, summary):
    #     self.understandable_concise_question = f"Bug summary: {summary.text}\n" \
    #                                            f"Answer the following questions individually by Yes or No and explain " \
    #                                            f"the reason:\n "
    #     # f"Bug summary: {summary.text}\n" \
    #     self.question_for_spelling(summary)
    #     self.question_for_syntax(summary)
    #     self.question_for_declarative_statement(summary)
    #     self.question_for_present_tense(summary)
    #
    #     self.question_for_personal_pronoun(summary)
    #     self.question_for_offence(summary)
    #     self.question_for_wishy_washy_words(summary)
    #
    #     count = 1
    #     self.understandable_concise_question = self.understandable_concise_question + f"\t{count}. " \
    #                                                                                   f"{self.spelling_question}\n"
    #     count = count + 1
    #     self.understandable_concise_question = self.understandable_concise_question + f"\t{count}. " \
    #                                                                                   f"{self.syntax_question}\n"
    #     count = count + 1
    #     self.understandable_concise_question = self.understandable_concise_question + f"\t{count}. " \
    #                                                                                   f"{self.declarative_statement_question}\n"
    #     count = count + 1
    #     self.understandable_concise_question = self.understandable_concise_question + f"\t{count}. " \
    #                                                                                   f"{self.present_tense_question}\n"
    #     count = count + 1
    #     self.understandable_concise_question = self.understandable_concise_question + f"\t{count}. " \
    #                                                                                   f"{self.personal_pronoun_question}\n"
    #     count = count + 1
    #     self.understandable_concise_question = self.understandable_concise_question + f"\t{count}. " \
    #                                                                                   f"{self.offence_question}\n"
    #     count = count + 1
    #     self.understandable_concise_question = self.understandable_concise_question + f"\t{count}. " \
    #                                                                                   f"{self.wishy_washy_words_question}\n"

    def question_for_spelling(self, summary):
        # self.spelling_question = f"Answer the question by Yes or No and explain the reason. " \
        #                          f"Does <summary> {summary.text} </summary> have the {Placeholder.SPELLING_ERRORS}?"
        self.spelling_question = f"Does {Placeholder.TAG_SUMMARY[0]}{summary.text}{Placeholder.TAG_SUMMARY[1]} have the {Placeholder.SPELLING_ERROR}?"
        # return spelling_question

    def question_for_syntax(self, summary):
        # self.syntax_question = f"Does <summary> {summary.text} </summary> use the standard English?"
        # self.syntax_question = f"Answer the question by Yes or No and explain the reason. " \
        #                        f"Does <summary> {summary.text} </summary> have the {Placeholder.SYNTAX_ERRORS}?"
        self.syntax_question = f"Does {Placeholder.TAG_SUMMARY[0]}{summary.text}{Placeholder.TAG_SUMMARY[1]} have the {Placeholder.SYNTAX_ERROR}?"

    def question_for_declarative_statement(self, summary):
        # self.syntax_question = f"Does <summary> {summary.text} </summary> use the standard English?"
        # self.declarative_statement_question = f"Answer the question by Yes or No and explain the reason. " \
        #                        f"Is <summary> {summary.text} </summary> a question?"
        self.declarative_statement_question = f"Is {Placeholder.TAG_SUMMARY[0]}{summary.text}{Placeholder.TAG_SUMMARY[1]} a question?"

    def question_for_present_tense(self, summary):
        # self.syntax_question = f"Does <summary> {summary.text} </summary> use the standard English?"
        # self.present_tense_question = f"Answer the question by Yes or No and explain the reason. " \
        #                        f"Does <summary> {summary.text} </summary> use the {Placeholder.PRESENT_TENSE}?"
        self.present_tense_question = f"Does {Placeholder.TAG_SUMMARY[0]}{summary.text}{Placeholder.TAG_SUMMARY[1]} use the {Placeholder.PRESENT_TENSE}?"

    def question_for_personal_pronoun(self, summary):
        # self.personal_pronoun_question = f"Answer the question by Yes or No and explain the reason. " \
        #                                  f"Does <summary> {summary.text} </summary> use the {Placeholder.PERSONAL_PRONOUN}?"
        self.personal_pronoun_question = f"Does {Placeholder.TAG_SUMMARY[0]}{summary.text}{Placeholder.TAG_SUMMARY[1]} use the {Placeholder.PERSONAL_PRONOUN}?"

    def question_for_emotional_reaction(self, summary):
        # self.emotional_reaction_question = f"Answer the question only by Positive, Neutral, or Negative. " \
        #                                    f"Decide whether the sentiment of <summary> {summary.text} </summary> is " \
        #                                    f"positive, neutral, or negative."
        self.emotional_reaction_question = f"Does {Placeholder.TAG_SUMMARY[0]}{summary.text}{Placeholder.TAG_SUMMARY[1]} use the neutral sentiment?"

    def question_for_offence(self, summary):
        # self.offence_question = f"Answer the question by Yes or No and explain the reason. " \
        #                         f"Does <summary> {summary.text} </summary> use the {Placeholder.OFFENCE}?"

        self.offence_question = f"Does {Placeholder.TAG_SUMMARY[0]}{summary.text}{Placeholder.TAG_SUMMARY[1]} use the {Placeholder.OFFENCE}?"

    def question_for_wishy_washy_words(self, summary):
        # self.wishy_washy_words_question = f"Answer the question by Yes or No and explain the reason. " \
        #                                   f"Does <summary> {summary.text} </summary> use the " \
        #                                   f"{Placeholder.WISHY_WASHY_WORD}?"
        self.wishy_washy_words_question = f"Does {Placeholder.TAG_SUMMARY[0]}{summary.text}{Placeholder.TAG_SUMMARY[1]} use the " \
                                          f"{Placeholder.WISHY_WASHY_WORD}?"

    @staticmethod
    def question_for_text_length(text):
        question = f"Text: {text}\n" \
                   f"How many words are in the text?"
        answer = LLMUtil.question_answer(question)

    def discriminate_info_from_ans(self, summary_pair, answer, raw_answer, llm=None):
        # if answer.actual_behavior and answer.desc_actual_behavior:
        #     self.question_for_actual_behavior(answer.actual_behavior, answer.desc_actual_behavior)
        #     actual_behavior_ans = LLMUtil.question_answer(self.actual_behavior_question)
        #     actual_behavior_ans = Answer.extract_answer_from_text(actual_behavior_ans, ',')
        #     answer.is_actual_behavior_vague = actual_behavior_ans
        # if answer.trigger_action and answer.desc_trigger_action:
        #     self.question_for_trigger_action(answer.trigger_action, answer.desc_trigger_action)
        #     trigger_action_ans = LLMUtil.question_answer(self.trigger_action_question)
        #     trigger_action_ans = Answer.extract_answer_from_text(trigger_action_ans, ',')
        #     answer.is_trigger_action_vague = trigger_action_ans
        if answer is not None and raw_answer is not None:
            self.question_for_vague_understandable_concise(summary_pair.rm_summary, answer)
            if llm is None:
                vague_understandable_concise_question, ans = LLMUtil.question_answer(
                    self.vague_understandable_concise_question)
            else:
                discriminator_question = self.session_prompt + '\n' + self.vague_understandable_concise_question
                # discriminator_question = self.session_prompt + LLMUtil.QUESTION_SEQUENCE + self.vague_understandable_concise_question
                # print(discriminator_question)
                ans = llm.ask_davinci(discriminator_question)
                if LLMUtil.reach_chatgpt_limited_request(ans, summary_pair):
                    return None, None
                vague_understandable_concise_question = discriminator_question
            raw_answer.discriminator = QA(vague_understandable_concise_question, ans)
            ans = Answer.extract_answer_from_text_for_discriminator(ans)
            count = 0
            if answer.actual_behavior is not None and answer.desc_actual_behavior is not None:
                answer.is_actual_behavior_vague = ans[count]
                count = count + 1
            if answer.trigger_action is not None and answer.desc_trigger_action is not None:
                answer.is_trigger_action_vague = ans[count]
                count = count + 1
            answer.spelling_error = ans[count]
            count = count + 1
            answer.syntax_error = ans[count]
            count = count + 1
            answer.declarative_statement = ans[count]
            count = count + 1
            answer.present_tense = ans[count]
            count = count + 1
            answer.personal_pronoun = ans[count]
            count = count + 1
            answer.emotional_reaction = ans[count]
            count = count + 1
            answer.offensive_words = ans[count]
            count = count + 1
            answer.wishy_washy_words = ans[count]

            # self.question_for_spelling(summary)
            # ans = LLMUtil.question_answer(self.spelling_question)
            # ans = Answer.extract_answers(ans, ',')
            # answer.spelling_error = ans
            # self.question_for_syntax(summary)
            # ans = LLMUtil.question_answer(self.syntax_question)
            # ans = Answer.extract_answers(ans, ',')
            # answer.syntax_error = ans
            # self.question_for_declarative_statement(summary)
            # ans = LLMUtil.question_answer(self.declarative_statement_question)
            # ans = Answer.extract_answers(ans, ',')
            # answer.declarative_statement = ans
            # self.question_for_present_tense(summary)
            # ans = LLMUtil.question_answer(self.present_tense_question)
            # ans = Answer.extract_answers(ans, ',')
            # answer.present_tense = ans
            # self.question_for_personal_pronoun(summary)
            # ans = LLMUtil.question_answer(self.personal_pronoun_question)
            # ans = Answer.extract_answers(ans, ',')
            # answer.personal_pronoun = ans
            # self.question_for_emotional_reaction(summary)
            # ans = LLMUtil.question_answer(self.emotional_reaction_question)
            # ans = Answer.extract_answer_from_text(ans, '.')
            # answer.emotional_reaction = ans
            # self.question_for_offence(summary)
            # ans = LLMUtil.question_answer(self.offence_question)
            # ans = Answer.extract_answers(ans, ',')
            # answer.offensive_words = ans
            # self.question_for_wishy_washy_words(summary)
            # ans = LLMUtil.question_answer(self.wishy_washy_words_question)
            # ans = Answer.extract_answers(ans, ',')
            # answer.wishy_washy_words = ans

            # self.question_for_text_length(summary.text)

        return answer, raw_answer

    # def discriminate_info_from_ans(self, summary, answer):
    #     if answer.actual_behavior and answer.desc_actual_behavior:
    #         self.question_for_actual_behavior(answer.actual_behavior, answer.desc_actual_behavior)
    #         actual_behavior_ans = LLMUtil.question_answer(self.actual_behavior_question)
    #         actual_behavior_ans = Answer.extract_answer_from_text(actual_behavior_ans, ',')
    #         answer.is_actual_behavior_vague = actual_behavior_ans
    #     if answer.trigger_action and answer.desc_trigger_action:
    #         self.question_for_trigger_action(answer.trigger_action, answer.desc_trigger_action)
    #         trigger_action_ans = LLMUtil.question_answer(self.trigger_action_question)
    #         trigger_action_ans = Answer.extract_answer_from_text(trigger_action_ans, ',')
    #         answer.is_trigger_action_vague = trigger_action_ans
    #
    #     self.question_for_understandable_concise(summary)
    #     ans = LLMUtil.question_answer(self.understandable_concise_question)
    #     ans = Answer.extract_answer_from_text(ans, ',')
    #     answer.spelling_error = ans[0]
    #     answer.syntax_error = ans[1]
    #     answer.declarative_statement = ans[2]
    #     answer.present_tense = ans[3]
    #     answer.personal_pronoun = ans[4]
    #     answer.offensive_words = ans[5]
    #     answer.wishy_washy_words = ans[6]
    #     # self.question_for_spelling(summary)
    #     # ans = LLMUtil.question_answer(self.spelling_question)
    #     # ans = Answer.extract_answers(ans, ',')
    #     # answer.spelling_error = ans
    #     # self.question_for_syntax(summary)
    #     # ans = LLMUtil.question_answer(self.syntax_question)
    #     # ans = Answer.extract_answers(ans, ',')
    #     # answer.syntax_error = ans
    #     # self.question_for_declarative_statement(summary)
    #     # ans = LLMUtil.question_answer(self.declarative_statement_question)
    #     # ans = Answer.extract_answers(ans, ',')
    #     # answer.declarative_statement = ans
    #     # self.question_for_present_tense(summary)
    #     # ans = LLMUtil.question_answer(self.present_tense_question)
    #     # ans = Answer.extract_answers(ans, ',')
    #     # answer.present_tense = ans
    #     # self.question_for_personal_pronoun(summary)
    #     # ans = LLMUtil.question_answer(self.personal_pronoun_question)
    #     # ans = Answer.extract_answers(ans, ',')
    #     # answer.personal_pronoun = ans
    #     self.question_for_emotional_reaction(summary)
    #     ans = LLMUtil.question_answer(self.emotional_reaction_question)
    #     ans = Answer.extract_answer_from_text(ans, '.')
    #     answer.emotional_reaction = ans
    #     # self.question_for_offence(summary)
    #     # ans = LLMUtil.question_answer(self.offence_question)
    #     # ans = Answer.extract_answers(ans, ',')
    #     # answer.offensive_words = ans
    #     # self.question_for_wishy_washy_words(summary)
    #     # ans = LLMUtil.question_answer(self.wishy_washy_words_question)
    #     # ans = Answer.extract_answers(ans, ',')
    #     # answer.wishy_washy_words = ans
    #
    #     # self.question_for_text_length(summary.text)
    #
    #     return answer

# class Optimizer:
#     def __init__(self):
#         # easy to understand
#         self.spelling_question = None
#         self.grammar_question = None
#         # concise
#         self.personal_pronoun_question = None
#         self.emotional_reaction_question = None
#         self.offence_question = None
#         self.wishy_washy_words_question = None
#
#     def question_for_spelling(self, summary):
#         pass
#
#     def question_for_grammar(self, summary_trigger_action, description_trigger_action):
#         pass
