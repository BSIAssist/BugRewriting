class Placeholder:
    # softgoal
    CONCISE = 'concise'
    SPECIFIC = 'specific'
    UNDERSTANDABLE = 'easy-to-understand'

    SEARCHABLE = 'searchable'
    IDENTIFIABLE = 'identifiable'
    # answer: Yes or No
    YES = "Yes"
    NO = 'No'

    TAG_SUMMARY = ['<SUMMARY>', '</SUMMARY>']
    TAG_DESCRIPTION = ['<DESCRIPTION>', '</DESCRIPTION>']
    TAG_SUGGESTED_SOLUTION = ['<SUGGESTED_SOLUTION>', '</SUGGESTED_SOLUTION>']
    TAG_ACTUAL_BEHAVIOR = ['<ACTUAL_BEHAVIOR>', '</ACTUAL_BEHAVIOR>']
    TAG_TRIGGER_ACTION = ['<TRIGGER_ACTION>', '</TRIGGER_ACTION>']
    TAG_PLATFORM = ['<PLATFORM>', '</PLATFORM>']
    TAG_COMPONENT = ['<COMPONENT>', '</COMPONENT>']
    # categories
    # all summary
    SPELLING_ERROR = "spelling error"
    SYNTAX_ERROR = "syntax error"
    DECLARATIVE_STATEMENT = "declarative statement"
    PRESENT_TENSE = "present tense"
    PERSONAL_PRONOUN = "personal pronoun (I, she, he, me, my, her, him, they, them)"
    EMOTIONAL_REACTION = "emotional reaction"
    OFFENCE = "offensive words"
    WISHY_WASHY_WORD = "wishy-washy words (seem, appear)"
    # what
    SUGGESTED_SOLUTION = "suggested solution"
    ACTUAL_BEHAVIOR = "actual behavior"
    IS_ACTUAL_BEHAVIOR_VAGUE = "is actual behavior vague"
    # when
    TRIGGER_ACTION = "trigger action"
    IS_TRIGGER_ACTION_VAGUE = "is trigger action vague"
    # where
    PLATFORM = 'platform'
    COMPONENT = 'component'

    # action
    ADD = 'add'
    DELETE = 'delete'
    MODIFY = 'modify'

    # # action_list
    # ACTION_LIST = [ADD, DELETE, MODIFY]

    # target
    TARGET_LIST = [
        # easy to understand all summary
        {'name': SPELLING_ERROR,
         'explanation': 'typos and misused words',
         'optional': None,
         'obscure': None,
         # 'actions': SPELLING_ERROR
         },
        {'name': SYNTAX_ERROR,
         'explanation': 'syntax error',
         'optional': None,
         'obscure': None,
         # 'extract': None
         },
        {'name': DECLARATIVE_STATEMENT,
         'explanation': 'declarative sentences',
         'optional': None,
         'obscure': None,
         # 'extract': None
         },
        {'name': PRESENT_TENSE,
         'explanation': 'the present tense',
         'optional': None,
         'obscure': None,
         # 'extract': None
         },
        # concise
        {'name': PERSONAL_PRONOUN,
         'explanation': "I, she, he, me, her, him",
         'optional': None,
         'obscure': None,
         # 'extract': PERSONAL_PRONOUN
         },
        {'name': EMOTIONAL_REACTION,
         'explanation': "sentiment analysis: positive or negative",
         'optional': None,
         'obscure': None,
         # 'extract': EMOTIONAL_REACTION
         },
        {'name': OFFENCE,
         'explanation': 'offensive words',
         'optional': None,
         'obscure': None,
         # 'extract': OFFENCE
         },
        {'name': WISHY_WASHY_WORD,
         'explanation': 'wishy-washy words (seem, appear)',
         'optional': None,
         'obscure': None,
         # 'extract': WISHY_WASHY_WORD
         },
        # specific
        {'name': SUGGESTED_SOLUTION,
         'explanation': "the conjecture or proposed fix for the bug",
         'optional': None,
         'obscure': None,
         # 'extract': SUGGESTED_SOLUTION
         },
        {'name': ACTUAL_BEHAVIOR,
         'explanation': "the observed behavior of the system or software being reported as having a bug or issue",
         'optional': None,
         'obscure': 'based on the bug description',
         # 'extract': ACTUAL_BEHAVIOR
         },
        {'name': TRIGGER_ACTION,
         'explanation': "the brief description of the action or event that causes the bug to occur",
         'optional': 'if it is a display issue',
         'obscure': 'based on the bug description',
         # 'extract': TRIGGER_ACTION
         },
        {'name': PLATFORM,
         'explanation': "the specific operating system, hardware, or other environment"
                        " in which the system or application is being used",
         'optional': "if happens on all or multiple platforms",
         'obscure': None,
         # 'extract': PLATFORM
         },
        {'name': COMPONENT,
         'explanation': "the specific part or subsystem of the system or application where the issue is occurring",
         'optional': "if there is only one place to find it or self-explaining",
         'obscure': None,
         # 'extract': COMPONENT
         },
    ]

    # action
    ACTION_TARGETS_LIST = [
        {'action': ADD,
         'targets': [ACTUAL_BEHAVIOR, TRIGGER_ACTION, PLATFORM, COMPONENT]},
        {'action': DELETE,
         'targets': [PERSONAL_PRONOUN, EMOTIONAL_REACTION, OFFENCE, WISHY_WASHY_WORD,
                     SUGGESTED_SOLUTION, PLATFORM, COMPONENT]},
        {'action': MODIFY,
         'targets': [SPELLING_ERROR, SYNTAX_ERROR, DECLARATIVE_STATEMENT, PRESENT_TENSE,
                     ACTUAL_BEHAVIOR, TRIGGER_ACTION, PLATFORM, COMPONENT]}
    ]

    SOFTGOAL_LIST = [
        {'name': CONCISE,
         'explanation': "be to-the-point and avoid redundant and irrelevant words for understanding bug reports",
         'benefits': None
         # [('objective', ''),
         #  ('polite', '')]
         },
        {'name': SPECIFIC,
         'explanation': "be crisp, precise and hold all important information within a sentence",
         'benefits': [('searchable', 'Most database search strings involve looking at summary first, '
                                     'descriptive enough so that somebody would find '
                                     'the bug report on the basis of the words this summary contains'),
                      ('identifiable', 'finding existing bugs and prevent filing of duplicates')]
         },
        {'name': UNDERSTANDABLE,
         'explanation': "be easily understood",
         'benefits': None
         }
    ]

    HARDGOAL_LIST = [
        # UNDERSTANDABLE
        {
            'action': MODIFY,
            'target': SPELLING_ERROR,
            'explanation': 'fix typos and misused words '
                           '(be professional to increase the credibility of bug report '
                           'and make it easy for developers to understand)',
            'softgoal': UNDERSTANDABLE,
            'instances': None
        },
        {
            'action': MODIFY,
            'target': SYNTAX_ERROR,
            'explanation': 'fix syntax error '
                           '(be professional to increase the credibility of bug report '
                           'and make it easy for developers to understand)',
            'softgoal': UNDERSTANDABLE,
            'instances': None
        },
        {
            'action': MODIFY,
            'target': DECLARATIVE_STATEMENT,
            'explanation': 'use the declarative statement '
                           '(be objective to state the facts of the issue, '
                           'rather than asking a question or expressing uncertainty)',
            'softgoal': UNDERSTANDABLE,
            'instances': None
        },
        {
            'action': MODIFY,
            'target': PRESENT_TENSE,
            'explanation': 'use the present tense '
                           '(to convey a sense of immediacy: '
                           'the issue still exists and needs to be addressed.)',
            'softgoal': UNDERSTANDABLE,
            'instances': None
        },
        # concise
        {
            'action': DELETE,
            'target': PERSONAL_PRONOUN,
            'explanation': 'delete personal pronoun '
                           '(to make the issue more impersonal and focus on the problem, '
                           'rather than on the person reporting it)',
            'softgoal': CONCISE,
            'instances': None
        },
        {
            'action': DELETE,
            'target': EMOTIONAL_REACTION,
            'explanation': 'avoid describing emotional reactions '
                           '(to keep the focus on the technical issue '
                           'and make the bug report more actionable, objective and professional)',
            'softgoal': CONCISE,
            'instances': None
        },
        {
            'action': DELETE,
            'target': OFFENCE,
            'explanation': 'avoid using offensive words '
                           '(be polite, respectful and professional '
                           'and focus on the technical issue not blame to the developer)',
            'softgoal': CONCISE,
            'instances': None
        },
        {
            'action': DELETE,
            'target': WISHY_WASHY_WORD,
            'explanation': 'avoid using wishy-washy or redundant words '
                           '(be certain and concise and tell the developer they will see the issue)',
            'softgoal': CONCISE,
            'instances': None
        },
        # specific
        # what
        {
            'action': DELETE,
            'target': SUGGESTED_SOLUTION,
            'explanation': 'delete suggested solution '
                           '(to describe the issue, not to provide a solution '
                           'and let development team investigate the issue independently, without bias)',
            'softgoal': SPECIFIC,
            'instances': None
        },
        {
            'action': ADD,
            'target': ACTUAL_BEHAVIOR,
            'explanation': 'add actual behavior '
                           '(to tell developers to observe what does happen)',
            'softgoal': SPECIFIC,
            'instances': None
        },
        {
            'action': MODIFY,
            'target': ACTUAL_BEHAVIOR,
            'explanation': 'modify actual behavior '
                           '(from obscure to specific: be to-the-point '
                           'to make it easy for developers understand what goes wrong at first glance '
                           'and decide the severity and priority of it; '
                           'for adding details: with necessary details (such as the conditions under which the problem occurs) '
                           'make developers determine the impact scope and root cause quickly; '
                           'correction: be precise to prevent confusion and misleading for developers; '
                           'for more standard expression: to make it easier to track and manage issues over time '
                           'by using standard language and terminology to ensure consistency across bug reports)',
            'softgoal': SPECIFIC,
            'instances': None
        },
        # when
        {
            'action': ADD,
            'target': TRIGGER_ACTION,
            'explanation': 'add trigger action '
                           '(to tell developers the specific scenario where the issue appears)',
            'softgoal': SPECIFIC,
            'instances': None
        },
        {
            'action': MODIFY,
            'target': TRIGGER_ACTION,
            'explanation': 'modify trigger action '
                           '(from obscure to specific: to provide clear and detailed information about '
                           'what actions caused the bug to occur; '
                           'for adding details: to help developers to be more aware of the conditions that cause the bug; '
                           'correction: be precise to reproduce the issue with greater ease)',
            'softgoal': SPECIFIC,
            'instances': None
        },
        # where
        {
            'action': ADD,
            'target': PLATFORM,
            'explanation': 'add platform '
                           '(to help developers to understand where the bug occurred '
                           'and if the issue is specific to certain platform)',
            'softgoal': SPECIFIC,
            'instances': None
        },
        {
            'action': DELETE,
            'target': PLATFORM,
            'explanation': 'delete platform '
                           '(be not platform-specific: if the issue occurs on multiple platforms; '
                           'be concise: if the summary is already detailed '
                           'and including the platform information would make it too long and difficult to read)',
            'softgoal': SPECIFIC,
            'instances': None
        },
        # {
        #     'action': MODIFY,
        #     'target': PLATFORM,
        #     'explanation': 'modify platform '
        #                    'for adding details: with necessary details (such as relevant information about the environment in which the bug occurred) '
        #                    'make developers determine the impact scope and root cause quickly; )',
        #     'softgoal': SPECIFIC,
        #     'instances': None
        # },
        {
            'action': ADD,
            'target': COMPONENT,
            'explanation': 'add component '
                           '(to help developers to understand where the bug occurred '
                           'and if the issue is specific to certain component)',
            'softgoal': SPECIFIC,
            'instances': None
        },
        {
            'action': DELETE,
            'target': COMPONENT,
            'explanation': 'delete component '
                           '(be not component-specific: if the issue occurs on multiple component; '
                           'be self-explaining: if there is only one place to find the issue object '
                           'and the mention of it is self-explaining'
                           'be concise: if the summary is already detailed '
                           'and including the component information would make it too long and difficult to read)',
            'softgoal': SPECIFIC,
            'instances': None
        },
        # {
        #     'action': MODIFY,
        #     'target': COMPONENT,
        #     'explanation': 'modify component '
        #                    'for adding details: with necessary details (such as relevant information about the component in which the bug occurred) '
        #                    'make developers determine the impact scope and root cause quickly; )',
        #     'softgoal': SPECIFIC,
        #     'instances': None
        # },

    ]
