import re

from bug_changing.types.placeholder import Placeholder


class QA:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def __repr__(self):
        return f'Q: {self.question}\n' \
               f'A: {self.answer}'

    def __str__(self):
        return f'Q: {self.question}\n' \
               f'A: {self.answer}'


class RawAnswer:
    def __init__(self, summary_pair, extractor_summary=None, extractor_desc=None, discriminator=None, rewriter=None):
        self.summary_pair = summary_pair  # SummaryPair
        self.extractor_summary = extractor_summary  # QA
        self.extractor_desc = extractor_desc  # QA
        self.discriminator = discriminator  # QA
        self.rewriter = rewriter  # QA

    def __repr__(self):
        return f'{self.summary_pair.rm_summary.text}:\n' \
               f'{self.extractor_summary}\n' \
               f'{self.extractor_desc}\n' \
               f'{self.discriminator}\n' \
               f'{self.rewriter}'

    def __str__(self):
        return f'{self.summary_pair.rm_summary.text}:\n' \
               f'{self.extractor_summary}\n' \
               f'{self.extractor_desc}\n' \
               f'{self.discriminator}\n' \
               f'{self.rewriter}'


class Answer:
    def __init__(self, summary_pair, suggested_solution=None, actual_behavior=None,
                 trigger_action=None, platform=None, component=None,
                 desc_suggested_solution=None, desc_actual_behavior=None,
                 desc_trigger_action=None, desc_platform=None, desc_component=None,
                 is_actual_behavior_vague=None, is_trigger_action_vague=None,
                 spelling_error=None, syntax_error=None, declarative_statement=None,
                 present_tense=None, personal_pronoun=None, emotional_reaction=None,
                 offensive_words=None, wishy_washy_words=None, rewritten_summary=None,
                 length=None):
        self.summary_pair = summary_pair
        self.suggested_solution = suggested_solution
        self.actual_behavior = actual_behavior
        self.trigger_action = trigger_action
        self.platform = platform
        self.component = component
        self.desc_suggested_solution = desc_suggested_solution
        self.desc_actual_behavior = desc_actual_behavior
        self.desc_trigger_action = desc_trigger_action
        self.desc_platform = desc_platform
        self.desc_component = desc_component
        self.is_actual_behavior_vague = is_actual_behavior_vague
        self.is_trigger_action_vague = is_trigger_action_vague

        self.spelling_error = spelling_error

        self.syntax_error = syntax_error
        self.declarative_statement = declarative_statement
        self.present_tense = present_tense

        self.personal_pronoun = personal_pronoun
        self.emotional_reaction = emotional_reaction
        self.offensive_words = offensive_words
        self.wishy_washy_words = wishy_washy_words
        self.rewritten_summary = rewritten_summary
        self.length = length

    def __repr__(self):
        return f'{self.summary_pair.rm_summary.text}:\n' \
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
               f'\t{Placeholder.WISHY_WASHY_WORD}: {self.wishy_washy_words}\n' \
               f'Rewritten summary: {self.rewritten_summary}'

    def __str__(self):
        return f'{self.summary_pair.rm_summary.text}:\n' \
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
               f'\t{Placeholder.WISHY_WASHY_WORD}: {self.wishy_washy_words}\n' \
               f'Rewritten summary: {self.rewritten_summary}'

    @classmethod
    def extract_answer_from_text_for_extractor(cls, text):
    # def extract_answer_from_text_for_extractor(cls, text, split_char=':'):
        suggested_solution = None
        actual_behavior = None
        trigger_action = None
        platform = None
        component = None
        # keywords = '[^a-zA-Z0-9]*|'.join(
        #     {Placeholder.SUGGESTED_SOLUTION, Placeholder.ACTUAL_BEHAVIOR, Placeholder.TRIGGER_ACTION,
        #      Placeholder.PLATFORM, Placeholder.COMPONENT}) + '[^a-zA-Z0-9]*'
        # print(keywords)
        # print(type(keywords))
        # extract_pattern = re.compile(r"(?P<TITLE>%s)(?P<SECTION>.*?)(?=%s|$)" % (keywords, keywords), re.DOTALL)
        extract_patterns = [re.compile(r"(?P<TITLE>%s)(?P<SECTION>.*?)(?=%s|$)" % (
                                f"{Placeholder.SUGGESTED_SOLUTION}:", f"{Placeholder.ACTUAL_BEHAVIOR}:"), re.DOTALL),
                            re.compile(r"(?P<TITLE>%s)(?P<SECTION>.*?)(?=%s|$)" % (
                                f"{Placeholder.ACTUAL_BEHAVIOR}:", f"{Placeholder.TRIGGER_ACTION}:"), re.DOTALL),
                            re.compile(r"(?P<TITLE>%s)(?P<SECTION>.*?)(?=%s|$)" % (
                                f"{Placeholder.TRIGGER_ACTION}:", f"{Placeholder.PLATFORM}:"), re.DOTALL),
                            re.compile(r"(?P<TITLE>%s)(?P<SECTION>.*?)(?=%s|$)" % (
                                f"{Placeholder.PLATFORM}:", f"{Placeholder.COMPONENT}:"), re.DOTALL),
                            re.compile(r"(?P<TITLE>%s)(?P<SECTION>.*?)(?=%s|$)" % (f"{Placeholder.COMPONENT}:", '$'),
                                       re.DOTALL),
                            ]
        for extract_pattern in extract_patterns:
            matching_rs = extract_pattern.finditer(text)  # matching result
            for rs in matching_rs:
                section_title = rs.groupdict()["TITLE"]
                section_title = re.sub('[^A-Za-z0-9]+', ' ',
                                       section_title).strip()  # remove non-alpha-number and 首尾空格回车等
                # print(section_title)
                section_text = rs.groupdict()["SECTION"]
                # print(section_text)
                if section_title == Placeholder.SUGGESTED_SOLUTION:
                    suggested_solution = section_text
                elif section_title == Placeholder.ACTUAL_BEHAVIOR:
                    actual_behavior = section_text
                elif section_title == Placeholder.TRIGGER_ACTION:
                    trigger_action = section_text
                elif section_title == Placeholder.PLATFORM:
                    platform = section_text
                elif section_title == Placeholder.COMPONENT:
                    component = section_text
        extracted_answers = [suggested_solution.replace('\n', ' ').strip(), actual_behavior.replace('\n', ' ').strip(),
                             trigger_action.replace('\n', ' ').strip(), platform.replace('\n', ' ').strip(),
                             component.replace('\n', ' ').strip()]
        # lines = text.splitlines()
        # # print(lines)
        # extracted_answers = []
        # for line in lines:
        #     if line.strip():
        #         ans = line.split(split_char, 1)
        #         # print(ans)
        #         if len(ans) > 1:
        #             if split_char == ':':
        #                 extracted_answers.append(ans[1].strip())
        #             else:
        #                 num_char = '.'
        #                 if num_char in ans[0]:
        #                     ans[0] = ans[0].split(num_char, 1)[1]
        #                 extracted_answers.append([ans[0].strip(), ans[1].strip()])
        #         else:
        #             extracted_answers.append([ans[0].strip()])
        extracted_answers = cls.preprocess_answer(extracted_answers)
        return extracted_answers

    @classmethod
    def extract_answer_from_text_for_discriminator(cls, text, split_char='.'):
        lines = text.splitlines()
        # print(lines)
        extracted_answers = []
        for line in lines:
            if line.strip():
                ans = line.split(split_char, 1)
                # print(ans)
                if len(ans) > 1:
                    ans[1] = ans[1].strip()
                    if ans[1].startswith('Yes'):
                        extracted_answers.append(['Yes', ans[1]])
                    elif ans[1].startswith('No') or ans[1].startswith('N/A'):
                        extracted_answers.append(['No', ans[1]])
                    else:
                        extracted_answers.append(['No', ans[1]])
                else:
                    """
                    @todo: delete this else?
                    """
                    extracted_answers.append([ans[0].strip()])
        extracted_answers = cls.preprocess_answer(extracted_answers)
        return extracted_answers

    @staticmethod
    def preprocess_answer(answers):
        preprocessed_answers = []
        for answer in answers:
            if type(answer) == list:
                if answer[0] == 'Yes':
                    answer[0] = True
                elif answer[0] == 'No':
                    answer[0] = False
            else:
                if answer in ['None', 'None mentioned', 'None mentioned explicitly',
                              'None (not mentioned in the bug description)', 'None specified', 'None provided']:
                    answer = None
            preprocessed_answers.append(answer)
        if len(preprocessed_answers) == 1:
            return preprocessed_answers[0]
        return preprocessed_answers

    @classmethod
    def from_answer(cls, summary_pair, summary_ans, desc_ans=None):
        # print(summary_ans)
        summary_ans = cls.extract_answer_from_text_for_extractor(summary_ans)
        if desc_ans:
            desc_ans = cls.extract_answer_from_text_for_extractor(desc_ans)
            return cls(summary_pair,
                       summary_ans[0], summary_ans[1], summary_ans[2], summary_ans[3], summary_ans[4],
                       desc_ans[0], desc_ans[1], desc_ans[2], desc_ans[3], desc_ans[4])
        return cls(summary_pair,
                   summary_ans[0], summary_ans[1], summary_ans[2], summary_ans[3], summary_ans[4])

    @classmethod
    def from_summary_pair(cls, summary_pair):
        rm_summary = summary_pair.rm_summary
        # add_summary = summary_pair.add_summary
        answer = cls(summary_pair, rm_summary.suggested_solution, rm_summary.actual_behavior,
                     rm_summary.trigger_action, rm_summary.platform, rm_summary.component,
                     None, None, None, None, None)
        if rm_summary.is_actual_behavior_vague:
            answer.is_actual_behavior_vague = [True]
        else:
            answer.is_actual_behavior_vague = [False]
        if rm_summary.is_trigger_action_vague:
            answer.is_trigger_action_vague = [True]
        else:
            answer.is_trigger_action_vague = [False]
        if rm_summary.spelling_error:
            answer.spelling_error = [True, rm_summary.spelling_error]
        else:
            answer.spelling_error = [False, rm_summary.spelling_error]
        if rm_summary.syntax_error:
            answer.syntax_error = [True, rm_summary.syntax_error]
        else:
            answer.syntax_error = [False, rm_summary.syntax_error]
        if rm_summary.declarative_statement:
            answer.declarative_statement = [True, rm_summary.declarative_statement]
        else:
            answer.declarative_statement = [False, rm_summary.declarative_statement]
        if rm_summary.present_tense:
            answer.present_tense = [False, rm_summary.present_tense]
        else:
            answer.present_tense = [True, rm_summary.present_tense]
        if rm_summary.personal_pronoun:
            answer.personal_pronoun = [True, rm_summary.personal_pronoun]
        else:
            answer.personal_pronoun = [False, rm_summary.personal_pronoun]
        if rm_summary.emotional_reaction:
            answer.emotional_reaction = [False, rm_summary.emotional_reaction]
        else:
            answer.emotional_reaction = [True, rm_summary.emotional_reaction]
        if rm_summary.offensive_words:
            answer.offensive_words = [True, rm_summary.offensive_words]
        else:
            answer.offensive_words = [False, rm_summary.offensive_words]
        if rm_summary.wishy_washy_words:
            answer.wishy_washy_words = [True, rm_summary.wishy_washy_words]
        else:
            answer.wishy_washy_words = [False, rm_summary.wishy_washy_words]
        return answer


class Answers:
    def __init__(self, answers=None):
        self.answers = answers

    def __iter__(self):
        for answer in self.answers:
            yield answer

    def __getitem__(self, index):
        return self.answers[index]

    def __len__(self):
        return len(self.answers)

    def get_answer_from_summary_pair(self):
        pass

    def get_groundtruth_answers_from_summary_pairs(self):
        answers = []
        for answer in self.answers:
            answers.append(Answer.from_summary_pair(answer.summary_pair))
        return Answers(answers)
