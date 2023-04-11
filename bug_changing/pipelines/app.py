from pathlib import Path

from tqdm import tqdm

from bug_changing.pipelines.evaluator import Evaluator
from bug_changing.pipelines.rewriter import Rewriter
from bug_changing.types.answer import Answers
from bug_changing.types.placeholder import Placeholder
from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.llm_util import LLMUtil
import time

from bug_changing.utils.metrics_util import MetricsUtil
from config import MOZILLA_PROJ, OUTPUT_DIR, MOZILLA_SUMMARY_LEN, ECLIPSE_PROJ, ECLIPSE_SUMMARY_LEN
import os


class App:
    def __init__(self):
        self.evaluator = Evaluator()
        self.rewriter = Rewriter()

    @staticmethod
    def process_by_rewriting(summary_pairs, project=MOZILLA_PROJ, llm=None):
        """
        rewrite bug summary
        Args:
            summary_pairs ():

        Returns:

        """
        # session_prompt = "I'm a bug summary rewriter. " \
        #                  "I can rewrite the bug summary based on the bug description. " \
        #                  "The rewritten bug summary is one-sentence.\n"
        # session_prompt = "I'm a bug summary rewriter. " \
        #                  "I can rewrite the bug summary based on the bug description. " \
        #                  "The rewritten bug summary is around 13 words.\n"
        # session_prompt = "I'm a bug summary rewriter. " \
        #                  "I can rewrite the bug summary based on the bug description. " \
        #                  "The rewritten bug summary is specific, concise, easy-to-understand and around 13 words.\n"
        session_prompt = "I'm a bug summary rewriter. " \
                         "I can rewrite the bug summary based on the bug description. " \
                         "The rewritten bug summary is around 13 words and satisfies the following conditions:\n" \
                         "\t1. don't contain suggested solution\n" \
                         "\t2. contain actual behavior\n" \
                         "\t3. contain trigger action\n" \
                         "\t4. contain where the bug happens in the platform-level\n" \
                         "\t5. contain where the bug happens in the component-level\n" \
                         f"\t6. don't have {Placeholder.SPELLING_ERROR}\n" \
                         f"\t7. don't have {Placeholder.SYNTAX_ERROR}\n" \
                         f"\t8. don't use the question sentence\n" \
                         f"\t9. use the {Placeholder.PRESENT_TENSE}\n" \
                         f"\t10. don't use {Placeholder.PERSONAL_PRONOUN}\n" \
                         f"\t11. use the neutral sentiment\n" \
                         f"\t12. don't use {Placeholder.OFFENCE}\n" \
                         f"\t13. don't use {Placeholder.WISHY_WASHY_WORD}\n"
        foldername = 'rewrite'
        prompt_type = 'rewrite'
        # prompt_type = 'rewrite_with_length'
        # prompt_type = 'rewrite_with_length_softgoal'
        # prompt_type = 'rewrite_with_length_hardgoal'
        folder_path = Path(OUTPUT_DIR, project, foldername, prompt_type)
        # checking if the directory demo_folder2
        # exist or not.
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
        sources_path = Path(folder_path, "sources.txt")
        references_path = Path(folder_path, "references.txt")
        answers_path = Path(folder_path, "answers.txt")
        sources = []
        references = []
        answers = []
        for index, summary_pair in tqdm(enumerate(summary_pairs), ascii=True):
            bug = summary_pair.bug
            LLMUtil.CHAT_LOG = None
            question = f"Bug summary: {summary_pair.rm_summary.text}\n" \
                       f"Bug description: {Placeholder.TAG_DESCRIPTION[0]}{bug.description.text}{Placeholder.TAG_DESCRIPTION[1]}\n" \
                       f"Please rewrite the bug summary based on the bug description." \
                       f"The rewritten bug summary: "
            question = session_prompt + question
            # print(question)
            # input()
            if llm is None:
                question, answer = LLMUtil.question_answer(question)
            else:
                answer = llm.ask_davinci(question)
                if answer == "Unusable response produced, maybe login session expired. " \
                             "Try 'pkill firefox' and 'chatgpt install'":
                    print(f"{answer}\n"
                          f"has already processed {index} summary pairs\n"
                          f"Can continue with {bug.id}: {summary_pair.rm_summary.id} {summary_pair.add_summary.id}")
                    break
            print(f"{LLMUtil.QUESTION_SEQUENCE}{question}")
            print(f"{LLMUtil.ANSWER_SEQUENCE}{answer}")
            sources.append(summary_pair.rm_summary.text)
            references.append(summary_pair.add_summary.text)
            answers.append(answer.replace('\n', ' '))
            FileUtil.dump_txt(sources_path, sources)
            FileUtil.dump_txt(references_path, references)
            FileUtil.dump_txt(answers_path, answers)
            gleus, avg_gleu = MetricsUtil.gleu(sources_path, references_path, answers_path)
            rouges, avg_rouge = MetricsUtil.rouge(answers, references)
            MetricsUtil.show_metrics([answers[-1]], [references[-1]], [rouges[-1]], avg_rouge, [summary_pair],
                                     [gleus[-1]], avg_gleu)
            print("##############################################################################")
            # if index == 49:
            #     break
            time.sleep(1.5)  # Sleep for 3 seconds
        rouges, avg_rouge = MetricsUtil.rouge(answers, references)
        gleus, avg_gleu = MetricsUtil.gleu(sources_path, references_path, answers_path)
        MetricsUtil.show_metrics(answers, references, rouges, avg_rouge, summary_pairs, gleus, avg_gleu)

        return answers

    @staticmethod
    def process_by_groundtruth_rewriting(summary_pairs, project=MOZILLA_PROJ, llm=None):
        """
        rewrite bug summary
        Args:
            summary_pairs ():

        Returns:

        """
        # session_prompt = "I'm a bug summary rewriter. " \
        #                  "I can rewrite the bug summary based on the bug description. " \
        #                  "The rewritten bug summary is around 13 words.\n"
        # session_prompt = "I'm a bug summary rewriter. " \
        #                  "I can rewrite the bug summary based on the bug description. " \
        #                  "The rewritten bug summary is specific, concise, easy-to-understand and around 13 words.\n"
        session_prompt = "I'm a bug summary rewriter. " \
                         "I can rewrite the bug summary based on the bug description. " \
                         "The rewritten bug summary is around 13 words."
        foldername = 'rewrite'
        # prompt_type = 'rewrite_with_length'
        # prompt_type = 'rewrite_with_length_softgoal'
        prompt_type = 'rewrite_with_length_groundtruth'
        folder_path = Path(OUTPUT_DIR, project, foldername, prompt_type)
        # checking if the directory demo_folder2
        # exist or not.
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
        sources_path = Path(folder_path, "sources.txt")
        references_path = Path(folder_path, "references.txt")
        answers_path = Path(folder_path, "answers.txt")
        sources = []
        references = []
        answers = []
        for index, summary_pair in tqdm(enumerate(summary_pairs), ascii=True):
            bug = summary_pair.bug
            LLMUtil.CHAT_LOG = None
            question = f"Bug summary: {summary_pair.rm_summary.text}\n" \
                       f"Bug description: {Placeholder.TAG_DESCRIPTION[0]}{bug.description}{Placeholder.TAG_DESCRIPTION[1]}\n" \
                       f"Please rewrite the bug summary based on the bug description." \
                       f"The rewritten bug summary: "
            question = session_prompt + question
            # print(question)
            # input()
            if llm is None:
                question, answer = LLMUtil.question_answer(question)
            else:
                answer = llm.ask_davinci(question)
                if answer == "Unusable response produced, maybe login session expired. " \
                             "Try 'pkill firefox' and 'chatgpt install'":
                    print(f"{answer}\n"
                          f"has already processed {index} summary pairs\n"
                          f"Can continue with {bug.id}: {summary_pair.rm_summary.id} {summary_pair.add_summary.id}")
                    break
            print(f"{LLMUtil.QUESTION_SEQUENCE}{question}")
            print(f"{LLMUtil.ANSWER_SEQUENCE}{answer}")
            sources.append(summary_pair.rm_summary.text)
            references.append(summary_pair.add_summary.text)
            answers.append(answer.replace('\n', ' '))
            FileUtil.dump_txt(sources_path, sources)
            FileUtil.dump_txt(references_path, references)
            FileUtil.dump_txt(answers_path, answers)
            gleus, avg_gleu = MetricsUtil.gleu(sources_path, references_path, answers_path)
            rouges, avg_rouge = MetricsUtil.rouge(answers, references)
            MetricsUtil.show_metrics([answers[-1]], [references[-1]], [rouges[-1]], avg_rouge, [summary_pair],
                                     [gleus[-1]], avg_gleu)
            print("##############################################################################")
            if index == 49:
                break
            time.sleep(1.5)  # Sleep for 3 seconds
        rouges, avg_rouge = MetricsUtil.rouge(answers, references)
        gleus, avg_gleu = MetricsUtil.gleu(sources_path, references_path, answers_path)
        MetricsUtil.show_metrics(answers, references, rouges, avg_rouge, summary_pairs, gleus, avg_gleu)

        return answers

    @staticmethod
    def process_by_turbo_generation(summary_pairs, prompt_type, project=MOZILLA_PROJ):
        """
        generate bug summary
        Args:
            project ():
            summary_len ():
            prompt_type ():
            summary_pairs ():

        Returns:

        """
        summary_len = None
        if project == MOZILLA_PROJ:
            summary_len = MOZILLA_SUMMARY_LEN
        elif project == ECLIPSE_PROJ:
            summary_len = ECLIPSE_SUMMARY_LEN
        session_prompt = ''

        # session_prompt = "I'm a bug summary generator. " \
        #                  "I can generate a bug summary based on the bug description.\n"
        # session_prompt = "I'm a bug summary generator. " \
        #                  "I can generate the one-sentence bug summary based on the bug description.\n"
        if prompt_type == 'generation_with_length':
            session_prompt = f"I'm a bug summary generator. " \
                             f"I can generate a bug summary (around {summary_len} words) based on the bug description.\n"
        # session_prompt = "I'm a bug summary generator. " \
        #                  "I can generate a specific, concise and easy-to-understand bug summary (around 13 words) based on the bug description.\n"
        elif prompt_type == 'generation_with_length_hardgoal':
            session_prompt = f"I'm a bug summary generator. " \
                             f"I can generate a specific, concise and easy-to-understand bug summary (around {summary_len} words) based on the bug description.\n" \
                             "The generated bug summary satisfies the following conditions:" \
                             "\t1. don't contain suggested solution\n" \
                             "\t2. contain actual behavior\n" \
                             "\t3. contain trigger action\n" \
                             "\t4. contain where the bug happens in the platform-level\n" \
                             "\t5. contain where the bug happens in the component-level\n" \
                             f"\t6. don't have {Placeholder.SPELLING_ERROR}\n" \
                             f"\t7. don't have {Placeholder.SYNTAX_ERROR}\n" \
                             f"\t8. don't use the question sentence\n" \
                             f"\t9. use the {Placeholder.PRESENT_TENSE}\n" \
                             f"\t10. don't use {Placeholder.PERSONAL_PRONOUN}\n" \
                             f"\t11. use the neutral sentiment\n" \
                             f"\t12. don't use {Placeholder.OFFENCE}\n" \
                             f"\t13. don't use {Placeholder.WISHY_WASHY_WORD}\n"
        references = []
        answers = []
        for index, summary_pair in tqdm(enumerate(summary_pairs), ascii=True):
            bug = summary_pair.bug
            messages = LLMUtil.get_messages_for_turbo(session_prompt)
            question = f"Bug description: {Placeholder.TAG_DESCRIPTION[0]}{bug.description}{Placeholder.TAG_DESCRIPTION[1]}\n" \
                       f"Please generate the bug summary based on the bug description." \
                       f"The generated bug summary: "
            messages = LLMUtil.add_role_content_dict_into_messages(LLMUtil.ROLE_USER, question, messages)
            answer = LLMUtil.ask_turbo(messages)
            messages = LLMUtil.add_role_content_dict_into_messages(LLMUtil.ROLE_ASSISTANT, answer, messages)
            print(messages)
            references.append(summary_pair.add_summary.text)
            answers.append(answer.replace('\n', ' '))

        return answers

    @staticmethod
    def process_by_turbo_rewriting(summary_pairs, prompt_type, project):
        """
            prompt_type = 'rewrite_with_length'
            prompt_type = 'rewrite_with_length_softgoal'
            prompt_type = 'rewrite_with_length_hardgoal'
        generate bug summary
        Args:
            project ():
            prompt_type ():
            summary_pairs ():

        Returns:

        """
        summary_len = None
        if project == MOZILLA_PROJ:
            summary_len = MOZILLA_SUMMARY_LEN
        elif project == ECLIPSE_PROJ:
            summary_len = ECLIPSE_SUMMARY_LEN
        session_prompt = ''
        # session_prompt = "I'm a bug summary rewriter. " \
        #                  "I can rewrite the bug summary based on the bug description. " \
        #                  "The rewritten bug summary is one-sentence.\n"
        if prompt_type == 'rewrite_with_length':
            session_prompt = f"I'm a bug summary rewriter. " \
                             f"I can rewrite the bug summary based on the bug description. " \
                             f"The rewritten bug summary is around {summary_len} words.\n"

        # session_prompt = "I'm a bug summary rewriter. " \
        #                  "I can rewrite the bug summary based on the bug description. " \
        #                  "The rewritten bug summary is specific, concise, easy-to-understand and around 13 words.\n"
        elif prompt_type == 'rewrite_with_length_hardgoal':
            session_prompt = f"I'm a bug summary rewriter. " \
                             f"I can rewrite the bug summary based on the bug description. " \
                             f"The rewritten bug summary is around {summary_len} words and " \
                             f"satisfies the following conditions:\n" \
                             "\t1. don't contain suggested solution\n" \
                             "\t2. contain actual behavior\n" \
                             "\t3. contain trigger action\n" \
                             "\t4. contain where the bug happens in the platform-level\n" \
                             "\t5. contain where the bug happens in the component-level\n" \
                             f"\t6. don't have {Placeholder.SPELLING_ERROR}\n" \
                             f"\t7. don't have {Placeholder.SYNTAX_ERROR}\n" \
                             f"\t8. don't use the question sentence\n" \
                             f"\t9. use the {Placeholder.PRESENT_TENSE}\n" \
                             f"\t10. don't use {Placeholder.PERSONAL_PRONOUN}\n" \
                             f"\t11. use the neutral sentiment\n" \
                             f"\t12. don't use {Placeholder.OFFENCE}\n" \
                             f"\t13. don't use {Placeholder.WISHY_WASHY_WORD}\n"
        folder_path = Path(OUTPUT_DIR, project, 'rewrite', prompt_type)
        # checking if the directory demo_folder2
        # exist or not.
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
        sources_path = Path(folder_path, "sources.txt")
        references_path = Path(folder_path, "references.txt")
        answers_path = Path(folder_path, "answers.txt")

        sources = []
        references = []
        answers = []
        for index, summary_pair in tqdm(enumerate(summary_pairs), ascii=True):
            bug = summary_pair.bug
            messages = LLMUtil.get_messages_for_turbo(session_prompt)
            question = f"Bug summary: {summary_pair.rm_summary.text}\n" \
                       f"Bug description: {Placeholder.TAG_DESCRIPTION[0]}{bug.description.text}{Placeholder.TAG_DESCRIPTION[1]}\n" \
                       f"Please rewrite the bug summary based on the bug description." \
                       f"The rewritten bug summary: "
            messages = LLMUtil.add_role_content_dict_into_messages(LLMUtil.ROLE_USER, question, messages)
            answer = LLMUtil.ask_turbo(messages)
            messages = LLMUtil.add_role_content_dict_into_messages(LLMUtil.ROLE_ASSISTANT, answer, messages)
            print(messages)
            sources.append(summary_pair.rm_summary.text)
            references.append(summary_pair.add_summary.text)
            answers.append(answer.replace('\n', ' '))
            FileUtil.dump_txt(sources_path, sources)
            FileUtil.dump_txt(references_path, references)
            FileUtil.dump_txt(answers_path, answers)
        return answers

    @staticmethod
    def process_by_generation(summary_pairs, llm=None):
        """
        generate bug summary
        Args:
            llm ():
            summary_pairs ():

        Returns:

        """
        # session_prompt = "I'm a bug summary generator. " \
        #                  "I can generate a bug summary based on the bug description.\n"
        # session_prompt = "I'm a bug summary generator. " \
        #                  "I can generate the one-sentence bug summary based on the bug description.\n"
        session_prompt = "I'm a bug summary generator. " \
                         "I can generate a bug summary (around 13 words) based on the bug description.\n"
        # session_prompt = "I'm a bug summary generator. " \
        #                  "I can generate a specific, concise and easy-to-understand bug summary (around 13 words) based on the bug description.\n"
        # session_prompt = "I'm a bug summary generator. " \
        #                  "I can generate a specific, concise and easy-to-understand bug summary (around 13 words) based on the bug description.\n" \
        #                  "The generated bug summary satisfies the following conditions:" \
        #                  "\t1. don't contain suggested solution\n" \
        #                  "\t2. contain actual behavior\n" \
        #                  "\t3. contain trigger action\n" \
        #                  "\t4. contain where the bug happens in the platform-level\n" \
        #                  "\t5. contain where the bug happens in the component-level\n" \
        #                  "\t6. "
        references = []
        answers = []
        for index, summary_pair in tqdm(enumerate(summary_pairs), ascii=True):
            bug = summary_pair.bug
            LLMUtil.CHAT_LOG = None
            # question = f"Bug description: {Placeholder.TAG_DESCRIPTION[0]}{bug.description}{Placeholder.TAG_DESCRIPTION[1]}\n" \
            #            f"Please generate the bug summary based on the bug description." \
            #            f"The generated bug summary: "
            question = f"Bug description: {Placeholder.TAG_DESCRIPTION[0]}{bug.description}{Placeholder.TAG_DESCRIPTION[1]}\n" \
                       f"Please generate the bug summary based on the bug description." \
                       f"The generated bug summary: "
            question = session_prompt + question
            # print(question)
            # input()
            if llm is None:
                question, answer = LLMUtil.question_answer(question)
            else:
                answer = llm.ask_davinci(question)
                if answer == "Unusable response produced, maybe login session expired. " \
                             "Try 'pkill firefox' and 'chatgpt install'":
                    print(f"{answer}\n"
                          f"has already processed {index} summary pairs\n"
                          f"Can continue with {bug.id}: {summary_pair.rm_summary.id} {summary_pair.add_summary.id}")
                    break
            print(f"{LLMUtil.QUESTION_SEQUENCE}{question}")
            print(f"{LLMUtil.ANSWER_SEQUENCE}{answer}")
            references.append(summary_pair.add_summary.text)
            answers.append(answer.replace('\n', ' '))
            rouges, avg_rouges = MetricsUtil.rouge(answers, references)
            MetricsUtil.show_metrics([answers[-1]], [references[-1]], [rouges[-1]], avg_rouges, [summary_pair])
            print("##############################################################################")
            # if index == 49:
            #     break
            time.sleep(1.5)  # Sleep for 3 seconds
        rouges, avg_rouges = MetricsUtil.rouge(answers, references)
        MetricsUtil.show_metrics(answers, references, rouges, avg_rouges, summary_pairs)

        return answers

    def process(self, test_summary_pairs, instance_summary_pairs, all_targets, goal_model, project=MOZILLA_PROJ,
                extractor_with_instances=True, discriminator_with_instances=True, rewriter_with_instances=True,
                hard_goal_repeat_num=2, rewrite_question_with_extractor_result=True):
        answers = []
        raw_answers = []
        # get the session prompt of extractor
        # self.evaluator.extractor.get_session_prompt(all_targets)
        # LLMUtil.SESSION_PROMPT = self.evaluator.extractor.session_prompt
        # self.evaluator.discriminator.get_session_prompt()

        # print(LLMUtil.SESSION_PROMPT)
        # count = 0
        for index, summary_pair in tqdm(enumerate(test_summary_pairs), ascii=True):
            # LLMUtil.SESSION_PROMPT = self.evaluator.extractor.session_prompt
            # self.evaluator = Evaluator()
            # self.rewriter = Rewriter()
            # if count == 0:
            #     count = count + 1
            #     continue
            # LLMUtil.CHAT_LOG = None
            answer, raw_answer = self.evaluator.evaluate(summary_pair, instance_summary_pairs, all_targets, project,
                                                         extractor_with_instances, discriminator_with_instances)

            # time.sleep(5)
            answer, raw_answer = self.rewriter.rewrite(summary_pair, answer, raw_answer, goal_model, project,
                                                       rewriter_with_instances, hard_goal_repeat_num,
                                                       rewrite_question_with_extractor_result)
            # if answer is None and raw_answer is None:
            #     print(f"has already processed {index} summary pairs\n"
            #           f"Can continue with {summary_pair.bug.id}: {summary_pair.rm_summary.id} {summary_pair.add_summary.id}")
            #     break
            # time.sleep(5)
            print('answer******************************************************')
            print(answer)
            # print('raw_answer******************************************************')
            # print(raw_answer)
            print('################################################################')
            answers.append(answer)
            raw_answers.append(raw_answer)
            # input()
            # time.sleep(5)
        return Answers(answers), raw_answers
    # def process(self, bugs):
    #     # get the session prompt of extractor
    #     instances = self.evaluator.extractor.get_instances(summary_pairs=None)
    #     self.evaluator.extractor.get_session_prompt(instances)
    #     LLMUtil.SESSION_PROMPT = self.evaluator.extractor.session_prompt
    #     print(LLMUtil.SESSION_PROMPT)
    #
    #     continue_flag = True
    #     while continue_flag:
    #         LLMUtil.CHAT_LOG = None
    #         bug, summary_id = bugs.get_bug_by_input()
    #         summary = bug.summary_path[summary_id]
    #         answer = self.evaluator.evaluate(summary)
    #         answer = self.rewriter.rewrite(answer)
    #
    #         print(answer)
    #         print("Continue? Y or N")
    #         continue_flag = input()
    #         if continue_flag == "Y":
    #             continue_flag = True
    #         else:
    #             continue_flag = False
