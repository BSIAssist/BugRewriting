from bug_changing.types.placeholder import Placeholder
from bug_changing.utils.file_util import FileUtil
from bug_changing.utils.path_util import PathUtil
from config import MOZILLA_PROJ, ECLIPSE_PROJ


class GoalModel:
    def __init__(self, soft_goals=None, hard_goals=None):
        self.soft_goals = soft_goals
        self.hard_goals = hard_goals
        # self.actions = actions
        # self.targets = targets

    def __repr__(self):
        return f'SoftGoals: {self.soft_goals}' \
               f'\nHardGoals: {self.hard_goals}'

    def __str__(self):
        return f'SoftGoals: {self.soft_goals}' \
               f'\nHardGoals: {self.hard_goals}'

    @classmethod
    def initiate(cls, mozilla_summary_pairs, eclipse_summary_pairs=None):
        """
        build goal model
        1. get softgoals from Placeholder.SOFTGOAL_LIST
        2. get targets from Placeholder.TARGET_LIST
        3. get actions from Placeholder.ACTION_LIST
        4. add actions into targets
        5. get hard_goals from Placeholder.HARDGOAL_LIST
        6. add hardgoals into softgoals
        7. get instance from mozilla and eclipse:
           a. get hardgoals into summary_pairs
           b. instances into hardgoals
           c. get goal model
        Args:
            mozilla_summary_pairs ():
            eclipse_summary_pairs ():

        Returns: GoalModel

        """
        # get softgoals from Placeholder.SOFTGOAL_LIST
        soft_goals = []
        for softgoal in Placeholder.SOFTGOAL_LIST:
            softgoal = SoftGoal.from_dict(softgoal)
            soft_goals.append(softgoal)
        soft_goals = SoftGoals(soft_goals)

        # get targets from Placeholder.TARGET_LIST
        targets = []
        for target in Placeholder.TARGET_LIST:
            target = Target.from_dict(target)
            targets.append(target)
        targets = Targets(targets)

        # get actions from Placeholder.ACTION_LIST
        actions = []
        for action_targets_dict in Placeholder.ACTION_TARGETS_LIST:
            action = Action.from_dict(action_targets_dict, targets)
            actions.append(action)
        actions = Actions(actions)

        # add actions into targets
        actions.add_actions_into_targets()

        # get hard_goals from Placeholder.HARDGOAL_LIST
        hard_goals = []
        for hardgoal_dict in Placeholder.HARDGOAL_LIST:
            hardgoal = HardGoal.from_dict(hardgoal_dict, actions, targets, soft_goals)
            hard_goals.append(hardgoal)
        hard_goals = HardGoals(hard_goals)

        # add hardgoals into softgoals
        hard_goals.add_hardgoals_into_softgoals()

        # get instance summary pairs
        mozilla_summary_pairs.get_hard_goals(hard_goals, MOZILLA_PROJ)
        if eclipse_summary_pairs:
            eclipse_summary_pairs.get_hard_goals(hard_goals, ECLIPSE_PROJ)
        return cls(soft_goals, hard_goals), targets, actions


class SoftGoal:
    def __init__(self, name=None, explanation=None, benefits=None):
        self.name = name
        self.explanation = explanation
        self.benefits = benefits
        self.hard_goals = HardGoals([])

    def __repr__(self):
        output = f'{self.name}: ' \
                 f'\n\t\tExplanation: {self.explanation}' \
                 f'\n\t\tBenefits: {self.benefits}' \
                 f'\n\t\tHardGoals:'
        for hard_goal in self.hard_goals:
            output = output + f' <{hard_goal.action.name} - {hard_goal.target.name}>'
        return output

    def __str__(self):
        output = f'{self.name}: ' \
                 f'\n\t\tExplanation: {self.explanation}' \
                 f'\n\t\tBenefits: {self.benefits}' \
                 f'\n\t\tHardGoals:'
        for hard_goal in self.hard_goals:
            output = output + f' <{hard_goal.action.name} - {hard_goal.target.name}>'
        return output

    def __eq__(self, other):
        return self.name == other.name \
            # and self.id == other.id

    def __hash__(self):
        # print(hash(str(self)))
        return hash(str(self))

    @classmethod
    def from_dict(cls, softgoal_dict):
        return cls(softgoal_dict['name'], softgoal_dict['explanation'], softgoal_dict['benefits'])


class SoftGoals:
    def __init__(self, soft_goals=None):
        self.soft_goals = soft_goals
        # self.categories = categories  # action can be acted on

    def __iter__(self):
        for soft_goal in self.soft_goals:
            yield soft_goal

    def __getitem__(self, index):
        return self.soft_goals[index]

    def __repr__(self):
        return f'{self.soft_goals}' \
            # f' - {self.obscure}'

    def __str__(self):
        return f'{self.soft_goals}' \
            # f' - {self.obscure}'

    def __eq__(self, other):
        return self.soft_goals == other.soft_goals

    def __hash__(self):
        # print(hash(str(self)))
        return hash(str(self))

    def get_softgoal_by_name(self, name):
        for soft_goal in self.soft_goals:
            if soft_goal.name == name:
                return soft_goal
        return None

    def append(self, soft_goal):
        self.soft_goals.append(soft_goal)


class HardGoal:
    def __init__(self, action=None, target=None, explanation=None, soft_goal=None):
        self.action = action
        self.target = target
        self.explanation = explanation
        self.soft_goal = soft_goal
        self.instances = Instances()  # instance: eclipse/mozilla, SummaryPair (ini_summary, final_summary)

    def __repr__(self):
        return f'{self.action.name} - {self.target.name}' \
               f'\n\tExplanation: {self.explanation}' \
               f'\n\tSoftGoal: {self.soft_goal}' \
               f'\n\tInstances: {self.instances}'

    def __str__(self):
        return f'{self.action.name} - {self.target.name}' \
               f'\n\tExplanation: {self.explanation}' \
               f'\n\tSoftGoal: {self.soft_goal}' \
               f'\n\tInstances: {self.instances}'

    def __eq__(self, other):
        return self.action == other.action and self.target == other.target

    def __hash__(self):
        # print(hash(str(self)))
        return hash(str(self))

    @classmethod
    def from_dict(cls, hardgoal_dict, actions, targets, soft_goals):
        action = actions.get_action_by_name(hardgoal_dict['action'])
        target = targets.get_target_by_name(hardgoal_dict['target'])
        soft_goal = soft_goals.get_softgoal_by_name(hardgoal_dict['softgoal'])
        return cls(action, target, hardgoal_dict['explanation'], soft_goal)


class HardGoals:
    def __init__(self, hard_goals=[]):
        self.hard_goals = hard_goals
        # self.categories = categories  # action can be acted on

    def __iter__(self):
        for hard_goal in self.hard_goals:
            yield hard_goal

    def __getitem__(self, index):
        return self.hard_goals[index]

    def __repr__(self):
        return f'{self.hard_goals}' \
            # f' - {self.obscure}'

    def __str__(self):
        return f'{self.hard_goals}' \
            # f' - {self.obscure}'

    def __eq__(self, other):
        return self.hard_goals == other.hard_goals

    def __len__(self):
        return len(self.hard_goals)

    def __hash__(self):
        # print(hash(str(self)))
        return hash(str(self))

    def append(self, hard_goal):
        if self.hard_goals is None:
            self.hard_goals = []
        self.hard_goals.append(hard_goal)

    def add_hardgoals_into_softgoals(self):
        for hard_goal in self.hard_goals:
            hard_goal.soft_goal.hard_goals.append(hard_goal)

    def get_hardgoal_by_action_and_target(self, action, target):
        for hard_goal in self.hard_goals:
            if hard_goal.action.name == action and hard_goal.target.name == target:
                return hard_goal
        return None

    def generate_prompt(self):
        prompt = ''
        # print(len(self.hard_goals))
        for index, hard_goal in enumerate(self.hard_goals):
            if hard_goal.action.name == Placeholder.MODIFY:
                if hard_goal.target.name == Placeholder.ACTUAL_BEHAVIOR \
                        or hard_goal.target.name == Placeholder.TRIGGER_ACTION:
                    requirement = f"\t{index + 1}. refine the {hard_goal.target.name}\n"
                    prompt = prompt + requirement
                    continue
                elif hard_goal.target.name == Placeholder.DECLARATIVE_STATEMENT \
                        or hard_goal.target.name == Placeholder.PRESENT_TENSE:
                    requirement = f"\t{index + 1}. use the {hard_goal.target.name}\n"
                    prompt = prompt + requirement
                    continue
            elif hard_goal.action.name == Placeholder.DELETE:
                if hard_goal.target.name == Placeholder.PERSONAL_PRONOUN \
                        or hard_goal.target.name == Placeholder.OFFENCE \
                        or hard_goal.target.name == Placeholder.WISHY_WASHY_WORD:
                    requirement = f"\t{index + 1}. don't use the {hard_goal.target.name}\n"
                    prompt = prompt + requirement
                    continue
                elif hard_goal.target.name == Placeholder.EMOTIONAL_REACTION:
                    requirement = f"\t{index + 1}. don't have the {hard_goal.target.name}\n"
                    prompt = prompt + requirement
                    continue
            requirement = f"\t{index + 1}. {hard_goal.action.name} the {hard_goal.target.name}\n"
            prompt = prompt + requirement
            # print(prompt)
        return prompt

    def generate_prompt_with_extrator_result(self, answer_or_instance_rm_summary):
        """
        Args:
            answer_or_instance_rm_summary ():

        Returns:

        """
        prompt = ''
        # print(len(self.hard_goals))
        for index, hard_goal in enumerate(self.hard_goals):
            if hard_goal.action.name == Placeholder.MODIFY:
                if hard_goal.target.name == Placeholder.ACTUAL_BEHAVIOR \
                        or hard_goal.target.name == Placeholder.TRIGGER_ACTION:
                    if hard_goal.target.name == Placeholder.ACTUAL_BEHAVIOR:
                        requirement = f"\t{index + 1}. refine the actual behavior from bug summary {Placeholder.TAG_ACTUAL_BEHAVIOR[0]}{answer_or_instance_rm_summary.actual_behavior}{Placeholder.TAG_ACTUAL_BEHAVIOR[1]} " \
                                      f"based on the actual behavior from bug description {Placeholder.TAG_ACTUAL_BEHAVIOR[0]}{answer_or_instance_rm_summary.desc_actual_behavior}{Placeholder.TAG_ACTUAL_BEHAVIOR[1]}\n"
                    else:
                        requirement = f"\t{index + 1}. refine the trigger action from bug summary {Placeholder.TAG_TRIGGER_ACTION[0]}{answer_or_instance_rm_summary.trigger_action}{Placeholder.TAG_TRIGGER_ACTION[1]} " \
                                      f"based on the trigger action from bug description {Placeholder.TAG_TRIGGER_ACTION[0]}{answer_or_instance_rm_summary.desc_trigger_action}{Placeholder.TAG_TRIGGER_ACTION[1]}\n"
                    prompt = prompt + requirement
                    continue
                elif hard_goal.target.name == Placeholder.DECLARATIVE_STATEMENT \
                        or hard_goal.target.name == Placeholder.PRESENT_TENSE:
                    requirement = f"\t{index + 1}. use the {hard_goal.target.name}\n"
                    prompt = prompt + requirement
                    continue
            elif hard_goal.action.name == Placeholder.DELETE:
                if hard_goal.target.name == Placeholder.PERSONAL_PRONOUN \
                        or hard_goal.target.name == Placeholder.OFFENCE \
                        or hard_goal.target.name == Placeholder.WISHY_WASHY_WORD:
                    requirement = f"\t{index + 1}. don't use the {hard_goal.target.name}\n"
                    prompt = prompt + requirement
                    continue
                elif hard_goal.target.name == Placeholder.EMOTIONAL_REACTION:
                    requirement = f"\t{index + 1}. don't have the {hard_goal.target.name}\n"
                    prompt = prompt + requirement
                    continue
            if hard_goal.target.name == Placeholder.SUGGESTED_SOLUTION:
                requirement = f"\t{index + 1}. {hard_goal.action.name} the " \
                              f"{Placeholder.TAG_SUGGESTED_SOLUTION[0]}{answer_or_instance_rm_summary.suggested_solution}{Placeholder.TAG_SUGGESTED_SOLUTION[1]}\n"
            elif hard_goal.target.name == Placeholder.ACTUAL_BEHAVIOR:
                requirement = f"\t{index + 1}. summarize the actual behavior {Placeholder.TAG_ACTUAL_BEHAVIOR[0]}{answer_or_instance_rm_summary.desc_actual_behavior}{Placeholder.TAG_ACTUAL_BEHAVIOR[1]} " \
                              f"and {hard_goal.action.name} the summarized actual behavior\n"
                # requirement = f"\t{index + 1}. {hard_goal.action.name} the summarized " \
                #               f"{Placeholder.TAG_ACTUAL_BEHAVIOR[0]}{answer_or_instance_rm_summary.desc_actual_behavior}{Placeholder.TAG_ACTUAL_BEHAVIOR[1]}\n"
                #               # f"and {hard_goal.action.name} the summarized {Placeholder.ACTUAL_BEHAVIOR}\n"
            elif hard_goal.target.name == Placeholder.TRIGGER_ACTION:
                requirement = f"\t{index + 1}. summarize the trigger action {Placeholder.TAG_TRIGGER_ACTION[0]}{answer_or_instance_rm_summary.desc_trigger_action}{Placeholder.TAG_TRIGGER_ACTION[1]} " \
                              f"and {hard_goal.action.name} the summarized trigger action\n"
                # requirement = f"\t{index + 1}. {hard_goal.action.name} the summarized " \
                #               f"{Placeholder.TAG_TRIGGER_ACTION[0]}{answer_or_instance_rm_summary.desc_trigger_action}{Placeholder.TAG_TRIGGER_ACTION[1]}\n"
                #               # f"and {hard_goal.action.name} the summarized {Placeholder.TRIGGER_ACTION}\n"
            elif hard_goal.target.name == Placeholder.PLATFORM:
                requirement = f"\t{index + 1}. simplify the platform {Placeholder.TAG_PLATFORM[0]}{answer_or_instance_rm_summary.desc_platform}{Placeholder.TAG_PLATFORM[1]} and " \
                              f"{hard_goal.action.name} the simplified platform\n"
                # requirement = f"\t{index + 1}. {hard_goal.action.name} the simplified " \
                #               f"{Placeholder.TAG_PLATFORM[0]}{answer_or_instance_rm_summary.desc_platform}{Placeholder.TAG_PLATFORM[1]}\n"
                #               # f"and {hard_goal.action.name} the simplified {Placeholder.PLATFORM}\n"
            elif hard_goal.target.name == Placeholder.COMPONENT:
                requirement = f"\t{index + 1}. simplify the component {Placeholder.TAG_COMPONENT[0]}{answer_or_instance_rm_summary.desc_component}{Placeholder.TAG_COMPONENT[1]} and " \
                              f"{hard_goal.action.name} the simplified component\n"
                #
                # requirement = f"\t{index + 1}. {hard_goal.action.name} the simplified " \
                #               f"{Placeholder.TAG_COMPONENT[0]}{answer_or_instance_rm_summary.desc_component}{Placeholder.TAG_COMPONENT[1]}\n"
                #               # f"and {hard_goal.action.name} the simplified {Placeholder.COMPONENT}\n"
            else:
                requirement = f"\t{index + 1}. {hard_goal.action.name} the {hard_goal.target.name}\n"
            prompt = prompt + requirement
            # print(prompt)
        return prompt


class Instances:
    def __init__(self):
        self.mozilla_instances = []
        self.eclipse_instances = []

    def __repr__(self):
        return f'{MOZILLA_PROJ} Instances: {self.mozilla_instances}' \
               f'\n{ECLIPSE_PROJ} Instances: {self.eclipse_instances}'

    def __str__(self):
        return f'{MOZILLA_PROJ} Instances: {self.mozilla_instances}' \
               f'\n{ECLIPSE_PROJ} Instances: {self.eclipse_instances}'

    def __eq__(self, other):
        return self.mozilla_instances == other.mozilla_instances and self.eclipse_instances == other.eclipse_instances

    def __hash__(self):
        # print(hash(str(self)))
        return hash(str(self))

    def append(self, instance, project=MOZILLA_PROJ):
        if project == MOZILLA_PROJ:
            self.mozilla_instances.append(instance)
            self.mozilla_instances = list(set(self.mozilla_instances))
        elif project == ECLIPSE_PROJ:
            self.eclipse_instances.append(instance)
            self.eclipse_instances = list(set(self.eclipse_instances))

    def get_mozilla_instances(self):
        pass


class Action:
    def __init__(self, name=None, targets=None):
        self.name = name
        self.targets = targets  # obj action can be acted on

    def __repr__(self):
        output = f'{self.name} -'
        for target in self.targets:
            output = output + ' [' + target.name + ']'
        return output

    def __str__(self):
        output = f'{self.name} -'
        for target in self.targets:
            output = output + ' [' + target.name + ']'
        return output

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        # print(hash(str(self)))
        return hash(str(self))

    @classmethod
    def from_dict(cls, action_targets_dict, target_objs):
        action = action_targets_dict["action"]
        targets = action_targets_dict["targets"]
        target_obj_list = []
        for target in targets:
            target = target_objs.get_target_by_name(target)
            target_obj_list.append(target)
        return cls(action, Targets(target_obj_list))


class Actions:
    def __init__(self, actions=None):
        self.actions = actions
        # self.categories = categories  # action can be acted on

    def __iter__(self):
        for action in self.actions:
            yield action

    def __getitem__(self, index):
        return self.actions[index]

    def __repr__(self):
        return f'{self.actions}' \
            # f' - {self.obscure}'

    def __str__(self):
        return f'{self.actions}' \
            # f' - {self.obscure}'

    def __eq__(self, other):
        return self.actions == other.actions

    def __hash__(self):
        # print(hash(str(self)))
        return hash(str(self))

    def append(self, action):
        if self.actions is None:
            self.actions = []
        self.actions.append(action)

    def add_actions_into_targets(self):
        for action in self.actions:
            for target in action.targets:
                target.actions.append(action)

    def get_action_by_name(self, name):
        for action in self.actions:
            if action.name == name:
                return action
        return None


class Target:
    def __init__(self, name=None, explanation=None, optional=None, obscure=None):
        self.name = name
        self.explanation = explanation
        self.optional = optional
        self.obscure = obscure
        # self.extract = extract
        self.actions = Actions()

        # self.has_or_not()  # question if the bug summary having the target
        # self.be_obscure_or_not()  # if obscure not None, question if the target can be more specific

    def __repr__(self):
        output = f'{self.name}: {self.explanation}' \
                 f'\n\tOptional: {self.optional}' \
                 f'\n\tObscure: {self.obscure}' \
                 f'\n\tActions:'
        for action in self.actions:
            output = output + " " + action.name
        return output

    def __str__(self):
        output = f'{self.name}: {self.explanation}' \
                 f'\n\tOptional: {self.optional}' \
                 f'\n\tObscure: {self.obscure}' \
                 f'\n\tActions:'
        for action in self.actions:
            output = output + " " + action.name
        return output

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        # print(hash(str(self)))
        return hash(str(self))

    @classmethod
    def from_dict(cls, target_dict):
        return cls(target_dict['name'], target_dict['explanation'],
                   target_dict['optional'], target_dict['obscure'])


class Targets:
    """
    the category of target
    """

    def __init__(self, targets):
        self.targets = targets
        # self.num = len(categories)

    def __iter__(self):
        for target in self.targets:
            yield target

    def __getitem__(self, index):
        return self.targets[index]

    def __repr__(self):
        return f'{self.targets}'

    def __str__(self):
        return f'{self.targets}'

    def append(self, target):
        self.targets.append(target)

    def get_target_by_name(self, name):
        for target in self.targets:
            if target.name == name:
                return target
        return None

    # def check_what(self):
    #     """
    #     what: suggested_solution, actual_behavior
    #     Returns:
    #
    #     """
    #     qa_list = []
    #     category_1 = self.get_category_by_name(Placeholder.SUGGESTED_SOLUTION)
    #     qa_list.extend(category_1.check())
    #     category_2 = self.get_category_by_name(Placeholder.ACTUAL_BEHAVIOR)
    #     qa_list.extend(category_2.check())
    #     return qa_list
    #
    # def check_when(self):
    #     """
    #     what: trigger_action
    #     Returns:
    #
    #     """
    #     qa_list = []
    #     category_1 = self.get_category_by_name(Placeholder.TRIGGER_ACTION)
    #     qa_list.extend(category_1.check())
    #     return qa_list
    #
    # def check_where(self):
    #     """
    #     where: platform, component
    #     Returns:
    #     """
    #     qa_list = []
    #     category_1 = self.get_category_by_name(Placeholder.PLATFORM)
    #     qa_list.extend(category_1.check())
    #
    #     category_2 = self.get_category_by_name(Placeholder.COMPONENT)
    #     qa_list.extend(category_2.check())
    #
    #     return qa_list
    #
    # def check(self):
    #     qa_list = []
    #     qa_list.extend(self.check_what())
    #     qa_list.extend(self.check_when())
    #     qa_list.extend(self.check_where())
    #     return qa_list

#
# class Target:
#     def __init__(self, target=None, category=None, more_details_from_description=None, optional=None, obscure=None):
#         self.target = target
#         self.category = category
#         self.more_details_from_description = more_details_from_description  # obscure for modifying
#         self.optional = optional
#         self.obscure = obscure
#
#     def __repr__(self):
#         return f'{self.target}: {self.category}\n' \
#                f'\t{self.more_details_from_description}' \
#             # f' - {self.obscure}'
#
#     def __str__(self):
#         return f'{self.target}: {self.category}\n' \
#                f'\t{self.more_details_from_description}' \
#             # f' - {self.obscure}'
#
#     def __eq__(self, other):
#         return self.target == other.target and self.category == self.category
#
#     def __hash__(self):
#         # print(hash(str(self)))
#         return hash(str(self))
#
#
# class QA:
#     def __init__(self, question=None, answer=None):
#         self.question = question
#         self.answer = answer
#
#     def __repr__(self):
#         return f'{self.question}: {self.question}'
#
#     def __str__(self):
#         return f'{self.question}: {self.question}'
#
#     def __eq__(self, other):
#         return self.question == other.question and self.answer == self.answer
#
#     def __hash__(self):
#         # print(hash(str(self)))
#         return hash(str(self))


# class Result:
#     def __init__(self, question=None, answer=None):
#         self.
#
#     def __repr__(self):
#         return f'{self.target}: {self.category}\n' \
#                f'\t{self.more_details_from_description}' \
#             # f' - {self.obscure}'
#
#     def __str__(self):
#         return f'{self.target}: {self.category}\n' \
#                f'\t{self.more_details_from_description}' \
#             # f' - {self.obscure}'
#
#     def __eq__(self, other):
#         return self.target == other.target and self.category == self.category
#
#     def __hash__(self):
#         # print(hash(str(self)))
#         return hash(str(self))

# class Targets:
#     def __init__(self, targets=None, questions=None, answers=None):
#         self.targets = targets
#         self.questions = questions
#         self.answers = answers
#
#     def __repr__(self):
#         return f'{self.name}: {self.explanation}' \
#             # f' - {self.obscure}'
#
#     def __str__(self):
#         return f'{self.name}: {self.explanation}' \
#             # f' - {self.obscure}'
#
#     def __eq__(self, other):
#         return self.name == other.name
#
#     def __hash__(self):
#         # print(hash(str(self)))
#         return hash(str(self))


# class Answer:
#     def __init__(self, specific=None, concise=None, easy_to_understand=None, length=None):
#         self.specific = specific
#         self.concise = concise
#         self.easy_to_understand = easy_to_understand
#
#     def __repr__(self):
#         return f'{self.name}: {self.explanation}' \
#             # f' - {self.obscure}'
#
#     def __str__(self):
#         return f'{self.name}: {self.explanation}' \
#             # f' - {self.obscure}'
#
#     def __eq__(self, other):
#         return self.name == other.name
#
#     def __hash__(self):
#         # print(hash(str(self)))
#         return hash(str(self))

# class Content:
#     def __init__(self, what_hardgoals=None, when_hardgoals=None, where_hardgoals=None, all_hardgoals=None):
#         self.what_hardgoals = what_hardgoals
#         self.when_hardgoals = when_hardgoals
#         self.where_hardgoals = where_hardgoals
#         self.all_hardgoals = all_hardgoals
#
#     def __repr__(self):
#         return f'{self.text} - \n{self.concepts}'
#
#     def __str__(self):
#         return f'{self.text} - \n{self.concepts}'
#
#     def __eq__(self, other):
#         return self.text == other.text \
#             # and self.id == other.id
#
#     def __hash__(self):
#         # print(hash(str(self)))
#         return hash(str(self))
#
#
# class Length:
#     def __init__(self, softgoals=None):
#         self.softgoals = softgoals
#
#
# class GoalModel:
#     def __init__(self, length=None, content=None, structure=None):
#         self.length = length
#         self.content = content
#         self.structure = structure
#
#     def __repr__(self):
#         return f'{self.text} - \n{self.concepts}'
#
#     def __str__(self):
#         return f'{self.text} - \n{self.concepts}'
#
#     def __eq__(self, other):
#         return self.text == other.text \
#             # and self.id == other.id
#
#     def __hash__(self):
#         # print(hash(str(self)))
#         return hash(str(self))
