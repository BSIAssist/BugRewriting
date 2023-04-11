import openai
import time
import backoff


class LLMUtil:
    # OPENAI_API_KEY = "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"  # mine
    # OPENAI_API_KEY = "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"
    OPENAI_API_KEY = "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"
    DAVINCI_MODEL_NAME = "text-davinci-003"
    TURBO_MODEL_NAME = "gpt-3.5-turbo"
    TURBO_0301_MODEL_NAME = "gpt-3.5-turbo-0301"
    ROLE_SYSTEM = 'system'
    ROLE_USER = 'user'
    ROLE_ASSISTANT = 'assistant'
    ANSWER_SEQUENCE = "\nAI: "
    QUESTION_SEQUENCE = "\n\nKG: "
    # ANSWER_SEQUENCE = "\nA: "
    # QUESTION_SEQUENCE = "\n\nQ: "
    SESSION_PROMPT = ""
    CHAT_LOG = None

    GPT3 = 'GPT-3'
    CHATGPT = 'chatGPT'

    # # content: all summary: easy_to_understand
    # has_spelling_error = 'has_spelling_error'
    # has_syntax_error = 'has_syntax_error'
    # not_declarative_statement = 'not_declarative_statement'
    # not_present_tense = 'not_present_tense'
    # has_personal_pronoun = 'has_personal_pronoun'
    # has_emotional_reaction = 'has_emotional_reaction'
    # has_offence = 'has_offence'
    # has_wishy_washy_words = 'has_wishy_washy_words'

    # content: what when where
    # what = 'what'
    # when = 'when'
    # where = 'where'
    # # what
    # has_suggested_solution = 'has_suggested_solution'
    # has_actual_behavior = 'has_actual_behavior'
    # is_actual_behavior_obscure = 'is_actual_behavior_obscure'
    # # when
    # has_trigger_action = 'has_trigger_action'
    # is_trigger_action_obscure = 'is_trigger_action_obscure'
    # # where
    # has_platform = 'has_platform'
    # has_component = 'has_component'

    # target
    # target -> be easy-to-understand
    # typos = "spelling errors"
    # syntax_error = "syntax errors"
    # declarative_statement = "declarative statement"
    # present_tense = 'present tense'
    # personal_pronoun = 'personal pronoun'
    # emotional_reaction = 'emotional reaction'
    # offence = 'offence'
    # wishy_washy_words = 'wishy-washy words'

    # # target -> content
    # suggested_solution = "suggested solution"
    # actual_behavior = "actual behavior"
    # trigger_action = "trigger action"
    # platform = 'platform'
    # component = 'component'

    # action
    # add = 'add'
    # delete = 'delete'
    # modify = 'modify'

    # action_dict = {
    #     'add': "add",
    #     'delete': "delete",
    #     'modify': "modify"
    # }
    #
    # target_dict = {
    #     'suggested_solution': "suggested solution",
    #     'actual_behavior': "actual behavior",
    #     'trigger_action': "trigger action",
    #     'platform': 'platform',
    #     'component': 'component'
    # }

    # @staticmethod
    # def generate_prompt(bug):
    #     # template = f"Input: Bug summary: {bug.summary_path[0]}\n" \
    #     #            f"Output: Fixed bug summary: {bug.summary_path[-1]}\n" \
    #     #            "The instruction is: "
    #     # template = "Analyze the following bug summary:\n" \
    #     #            "DMD reports heap-unclassifed memory in mozilla::dom::FontFace::GetUnicodeRangeAsCharacterMap for Google sites\n" \
    #     #            "Does the bug summary have the typos and spelling errors? " \
    #     #            "Only answer Yes or No:\n" \
    #     #            "Yes\n\n" \
    #     #            "Analyze the following bug summary:\n" \
    #     #            f"{bug.summary_path[0]}\n" \
    #     #            "Does the bug summary have the typos and spelling errors? " \
    #     #            "Only answer Yes or No:"
    #     # template = "Analyze the following bug summary:\n" \
    #     #            f"{bug.summary_path[0]}\n" \
    #     #            "Rewrite the bug summary by the requirements below:\n" \
    #     #            "\t1. Fix spelling errors\n" \
    #     #            "\t2. Fix syntax errors\n" \
    #     #            "\t3. Use the present tense\n" \
    #     #            "The fixed bug summary:"
    #
    #     # template = "Analyze the following bug summary:\n" \
    #     #            f"{bug.summary_path[0]}\n" \
    #     #            "Its bug description:\n" \
    #     #            f"{bug.description}\n" \
    #     #            "Rewrite the bug summary by the requirements below:\n" \
    #     #            "\tDon't change words appearing in its bug description\n" \
    #     #            "\tFix spelling errors\n" \
    #     #            "The fixed bug summary:"
    #
    #     # template = "Analyze the following bug summary:\n" \
    #     #            f"{bug.summary_path[0]}\n" \
    #     #            "Rewrite the bug summary by the requirements below:\n" \
    #     #            "\t1. Please state objectively\n" \
    #     #            "The fixed bug summary:"
    #     # template = "Analyze the bug:\n" \
    #     #            f"Bug summary: ${bug.summary_path[0]}$\n" \
    #     #            f"Its bug description: ${bug.description}$\n" \
    #     #            "Does the bug summary contain a suggested solution? Yes or No"
    #     template = "Analyze the bug:\n" \
    #                f"Bug summary: {bug.summary_path[0]}\n" \
    #                "Does the bug summary contain a suggested solution? Yes or No"
    #     return template

    @staticmethod
    def ask_davinci(question, chat_log=None):
        """
        ask LLM question
        Args:
            question (question):
            chat_log (QA history):

        Returns: answer

        """
        if chat_log is None and LLMUtil.SESSION_PROMPT is not None:
            chat_log = LLMUtil.SESSION_PROMPT
        prompt_text = f'{chat_log}{LLMUtil.QUESTION_SEQUENCE}{question}{LLMUtil.ANSWER_SEQUENCE}'
        # print(prompt_text)
        response = openai.Completion.create(
            model=LLMUtil.DAVINCI_MODEL_NAME,
            prompt=prompt_text,
            temperature=0.7,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            # stop=[" KG:", " AI:"]
        )
        answer = response['choices'][0]['text'].strip()
        chat_log = LLMUtil.append_interaction_to_chat_log(question, answer, chat_log)
        return prompt_text, answer, chat_log

    @staticmethod
    def append_interaction_to_chat_log(question, answer, chat_log=None):
        """
        append the QA pair to chat_log
        Args:
            question ():
            answer ():
            chat_log ():

        Returns: updated chat_log

        """
        if chat_log is None:
            chat_log = LLMUtil.SESSION_PROMPT
        return f'{chat_log}{LLMUtil.QUESTION_SEQUENCE}{question}{LLMUtil.ANSWER_SEQUENCE}{answer}'

    @staticmethod
    def question_answer(question):
        """
        ask AI question and get answer
        Args:
            question ():

        Returns: answer
        Note: dict 引用传递
        """
        # question = question_dict[dict_key]
        # print(f"{LLMUtil.QUESTION_SEQUENCE}{question}")
        prompt_text, answer, LLMUtil.CHAT_LOG = LLMUtil.ask_davinci(question, LLMUtil.CHAT_LOG)
        # answer = answer.strip()
        # print(f"{LLMUtil.ANSWER_SEQUENCE}{answer}")
        return prompt_text, answer
        # answer_dict[dict_key] = answer
        # return answer_dict

    @staticmethod
    def reach_chatgpt_limited_request(answer, summary_pair):
        if answer == "Unusable response produced, maybe login session expired. " \
                     "Try 'pkill firefox' and 'chatgpt install'":
            print(f"{answer}\n"
                  f"Can continue with {summary_pair.bug.id}: {summary_pair.rm_summary.id} {summary_pair.add_summary.id}")
            return True
        return False

    @staticmethod
    @backoff.on_exception(backoff.expo, openai.error.RateLimitError)
    def ask_turbo(messages, model=TURBO_MODEL_NAME, temperature=1):
        """
        ask LLM question
        Args:
            temperature (): number Optional Defaults to 1
                            What sampling temperature to use, between 0 and 2.
                            Higher values like 0.8 will make the output more random,
                            while lower values like 0.2 will make it more focused and deterministic.
                            We generally recommend altering this or top_p but not both.
            model ():
            messages ():

        Returns: answer

        """
        # time.sleep(25)

        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        answer = response['choices'][0]['message']['content'].strip()
        return answer

    @staticmethod
    def get_messages_for_turbo(session_prompt, qa_pairs=None):
        """
        model="gpt-3.5-turbo",
        Args:
            system_role: for session_prompt,
            question_role: for question,
            answer_role: for answer,
            session_prompt: for system_role introduction
            qa_pairs (examples): (Q, A) pairs

        Returns:
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"},
                {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                {"role": "user", "content": "Where was it played?"}
            ]
        """
        messages = [{'role': LLMUtil.ROLE_SYSTEM, 'content': session_prompt}]
        if qa_pairs:
            for qa in qa_pairs:
                role_content_dict = {'role': LLMUtil.ROLE_USER, 'content': qa[0]}
                messages.append(role_content_dict)
                role_content_dict = {'role': LLMUtil.ROLE_ASSISTANT, 'content': qa[1]}
                messages.append(role_content_dict)
        return messages

    @staticmethod
    def add_role_content_dict_into_messages(role, content, messages):
        role_content_dict = {'role': role, 'content': content}
        messages.append(role_content_dict)
        return messages

    @staticmethod
    def show_messages(messages):
        for message in messages:
            print(f"{message['role']}: {message['content']}")

    # @staticmethod
    # def get_judgor_question(target):

    # # content to be easy_to_understand
    # @staticmethod
    # def analyze_bug_summary_spelling_grammar(bug, summary_id):
    #     bug_summary = bug.summary_path[int(summary_id)]
    #     question_dict = {
    #
    #     }

    # # content to be specific
    # @staticmethod
    # def analyze_bug_summary_what(bug, summary_id):
    #
    #     bug_summary = bug.summary_path[int(summary_id)]
    #
    #     what_question_dict = {
    #         LLMUtil.suggested_solution:
    #         # f"Analyze the bug summary: Storage Inspector's variables view should be selectable\n"
    #         # "The suggested solution tells the conjecture of how to fix it or what should happen.\n"
    #         # "Does the bug summary contain the suggested solution? "
    #         # "Yes or No"
    #         # f"{LLMUtil.answer_sequence}Yes\n"
    #         # the conjecture or proposed fix for the bug
    #             f"Analyze the bug summary: {bug_summary}\n"
    #             "The suggested solution states the conjecture or proposed fix for the bug.\n"
    #             "Does the bug summary contain the suggested solution? "
    #             "Yes or No",
    #         LLMUtil.actual_behavior:
    #             f"Analyze the bug summary: {bug_summary}\n"
    #             "The actual behavior tells developers what does happen.\n"
    #             "Does this bug summary have the actual behavior? "
    #             "Yes or No",
    #         LLMUtil.is_actual_behavior_obscure: f"Bug summary: {bug_summary}\n"
    #                                             f"Bug description: {bug.description}\n"
    #                                             f"Can the actual behavior in the bug summary be more specific? "
    #                                             f"Yes or No",
    #     }
    #     # Q&A: has_suggested_solution
    #     # Q&A: has_actual_behavior
    #     what_answer_dict = {
    #         LLMUtil.has_suggested_solution: LLMUtil.question_answer(what_question_dict[LLMUtil.has_suggested_solution]),
    #         LLMUtil.has_actual_behavior: LLMUtil.question_answer(what_question_dict[LLMUtil.has_actual_behavior]),
    #         LLMUtil.is_actual_behavior_obscure: None}
    #
    #     if what_answer_dict[LLMUtil.has_actual_behavior] == 'Yes':
    #         # Q&A: is_actual_behavior_obscure
    #         what_answer_dict[LLMUtil.is_actual_behavior_obscure] = LLMUtil.question_answer(
    #             what_question_dict[LLMUtil.is_actual_behavior_obscure])
    #
    #     return what_answer_dict
    #
    # @staticmethod
    # def analyze_bug_summary_when(bug, summary_id):
    #
    #     bug_summary = bug.summary_path[int(summary_id)]
    #
    #     when_question_dict = {
    #         LLMUtil.has_trigger_action:
    #             f"Analyze the bug summary: {bug_summary}\n"
    #             "The trigger action is the outline of the set of steps or actions "
    #             "that cause the actual behavior to occur.\n"
    #             "Does the bug summary contain the trigger action? "
    #             "Yes or No",
    #         LLMUtil.is_trigger_action_obscure: f"Bug summary: {bug_summary}\n"
    #                                            f"Bug description: {bug.description}\n"
    #                                            f"Can the trigger action in the bug summary be more specific? "
    #                                            f"Yes or No",
    #
    #     }
    #     # Q&A: has_trigger_action
    #     when_answer_dict = {
    #         LLMUtil.has_trigger_action: LLMUtil.question_answer(when_question_dict[LLMUtil.has_trigger_action]),
    #         LLMUtil.is_trigger_action_obscure: None}
    #
    #     if when_answer_dict[LLMUtil.has_trigger_action] == 'Yes':
    #         # Q&A: is_trigger_action_obscure
    #         when_answer_dict[LLMUtil.is_trigger_action_obscure] = LLMUtil.question_answer(
    #             when_question_dict[LLMUtil.is_trigger_action_obscure])
    #
    #     return when_answer_dict
    #
    # @staticmethod
    # def analyze_bug_summary_where(bug, summary_id):
    #
    #     # is_trigger_action_obscure = 'is_trigger_action_obscure'
    #
    #     bug_summary = bug.summary_path[int(summary_id)]
    #
    #     when_question_dict = {
    #         LLMUtil.has_platform:
    #             f"Analyze the bug summary: {bug_summary}\n"
    #             "The platform refers to the specific operating system, hardware, or other environment "
    #             "in which the system or application is being used"
    #             "Does the bug summary contain the platform? "
    #             "Yes or No",
    #         LLMUtil.has_component:
    #             f"Analyze the bug summary: {bug_summary}\n"
    #             "The component refers to a specific part or subsystem of the system or application "
    #             "that is experiencing the issue."
    #             "Does the bug summary contain the component? "
    #             "Yes or No",
    #
    #     }
    #     # Q&A: has_platform
    #     # Q&A: has_component
    #     when_answer_dict = {LLMUtil.has_platform: LLMUtil.question_answer(when_question_dict[LLMUtil.has_platform]),
    #                         LLMUtil.has_component: LLMUtil.question_answer(when_question_dict[LLMUtil.has_component])}
    #
    #     return when_answer_dict
    #
    # @staticmethod
    # def fix_template(context, action, target):
    #     """
    #     针对 a specific aim, generate a specific question
    #     Args:
    #         context ():
    #         action ():
    #         target ():
    #
    #     Returns:
    #
    #     """
    #
    #     if action == LLMUtil.delete:
    #         if target == 'suggested solution':
    #             delete_template = f"Please rewrite the bug summary by deleting the {target}. \n" \
    #                               f"The fixed bug summary: "
    #             return delete_template
    #     if action == LLMUtil.add:
    #         add_template = f"Bug description: {context}\n" \
    #                        f"If the bug description has the {target}, " \
    #                        f"please rewrite the bug summary by {action}ing the {target}. \n" \
    #                        f"The fixed bug summary: "
    #         return add_template
    #     if action == LLMUtil.modify:
    #         modify_template = f"Bug description: {context}\n" \
    #                           f"Please rewrite the bug summary by {action}ing the {target} with more details.\n" \
    #                           f"The fixed bug summary: "
    #         return modify_template
    #
    # @staticmethod
    # def fix_template_for_merging(action, target):
    #     """
    #     根据 answer_dict (what when where), 得到一个总的reformulation quesiton
    #     Args:
    #         action ():
    #         target ():
    #
    #     Returns:
    #
    #     """
    #     if action == LLMUtil.delete:
    #         if target == 'suggested solution':
    #             delete_template = f"{action} the {target} \n"
    #             return delete_template
    #     if action == LLMUtil.add:
    #         add_template = f"{action} the {target}, if the bug description has the {target} \n"
    #         return add_template
    #     if action == LLMUtil.modify:
    #         modify_template = f"{action} the {target} with more details.\n"
    #         return modify_template
    #
    # @staticmethod
    # def add_modify_for_more_details(context, has_answer, is_obscure_answer, target):
    #     """
    #     if has target:
    #         if is_obscure:
    #             modify
    #     else:
    #         add target, if context contains it
    #     Args:
    #         context ():
    #         has_answer ():
    #         is_obscure_answer ():
    #         target ():
    #
    #     Returns:
    #
    #     """
    #     if has_answer == 'Yes':
    #         if is_obscure_answer == 'Yes':
    #             question = LLMUtil.fix_template(context, LLMUtil.modify, target)
    #             LLMUtil.question_answer(question)
    #     else:
    #         question = LLMUtil.fix_template(context, LLMUtil.add, target)
    #         LLMUtil.question_answer(question)
    #
    # @staticmethod
    # def add_modify_for_more_details_for_merging(has_answer, is_obscure_answer, target):
    #     question = None
    #     if has_answer == 'Yes':
    #         if is_obscure_answer == 'Yes':
    #             question = LLMUtil.fix_template_for_merging(LLMUtil.modify, target)
    #             # LLMUtil.question_answer(question)
    #     else:
    #         question = LLMUtil.fix_template_for_merging(LLMUtil.add, target)
    #         # LLMUtil.question_answer(question)
    #     return question
    #
    # @staticmethod
    # def fix_bug_summary_what(context, what_answer_dict):
    #     if what_answer_dict[LLMUtil.has_suggested_solution] == 'Yes':
    #         question = LLMUtil.fix_template(context, LLMUtil.delete, LLMUtil.suggested_solution)
    #         LLMUtil.question_answer(question)
    #     LLMUtil.add_modify_for_more_details(context,
    #                                         what_answer_dict[LLMUtil.has_actual_behavior],
    #                                         what_answer_dict[LLMUtil.is_actual_behavior_obscure],
    #                                         LLMUtil.actual_behavior)
    #
    # @staticmethod
    # def fix_bug_summary_when(context, when_answer_dict):
    #     LLMUtil.add_modify_for_more_details(context,
    #                                         when_answer_dict[LLMUtil.has_trigger_action],
    #                                         when_answer_dict[LLMUtil.is_trigger_action_obscure],
    #                                         LLMUtil.trigger_action)
    #
    # @staticmethod
    # def fix_bug_summary_where(context, where_answer_dict):
    #     if where_answer_dict[LLMUtil.has_platform] == "No":
    #         question = LLMUtil.fix_template(context, LLMUtil.add, LLMUtil.platform)
    #         LLMUtil.question_answer(question)
    #
    #     if where_answer_dict[LLMUtil.has_component] == "No":
    #         question = LLMUtil.fix_template(context, LLMUtil.add, LLMUtil.component)
    #         LLMUtil.question_answer(question)
    #
    # @staticmethod
    # def fix_bug_summary(context, answer_dict):
    #     what_answer_dict = answer_dict[LLMUtil.what]
    #     when_answer_dict = answer_dict[LLMUtil.when]
    #     where_answer_dict = answer_dict[LLMUtil.where]
    #     conditions = []
    #     question = f"Bug description: {context}\n" \
    #                f"Based on the bug description, please reformulate the bug summary as follows:\n"
    #
    #     # what
    #     if what_answer_dict[LLMUtil.has_suggested_solution] == 'Yes':
    #         condition = LLMUtil.fix_template_for_merging(LLMUtil.delete, LLMUtil.suggested_solution)
    #         conditions.append(condition)
    #     condition = LLMUtil.add_modify_for_more_details_for_merging(what_answer_dict[LLMUtil.has_actual_behavior],
    #                                                                 what_answer_dict[
    #                                                                     LLMUtil.is_actual_behavior_obscure],
    #                                                                 LLMUtil.actual_behavior)
    #     if condition:
    #         conditions.append(condition)
    #
    #     # when
    #     condition = LLMUtil.add_modify_for_more_details_for_merging(when_answer_dict[LLMUtil.has_trigger_action],
    #                                                                 when_answer_dict[LLMUtil.is_trigger_action_obscure],
    #                                                                 LLMUtil.trigger_action)
    #     if condition:
    #         conditions.append(condition)
    #
    #     # where
    #     if where_answer_dict[LLMUtil.has_platform] == "No":
    #         condition = LLMUtil.fix_template_for_merging(LLMUtil.add, LLMUtil.platform)
    #         conditions.append(condition)
    #     if where_answer_dict[LLMUtil.has_component] == "No":
    #         condition = LLMUtil.fix_template_for_merging(LLMUtil.add, LLMUtil.component)
    #         conditions.append(condition)
    #
    #     # add conditions to question
    #     for index, condition in enumerate(conditions):
    #         question = question + f"\t{index + 1}. {condition}"
    #     question = question + f"The reformulated bug summary: "
    #     LLMUtil.question_answer(question)
    #     # return answer
