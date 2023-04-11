import copy
from datetime import datetime

from bug_changing.types.comment import Comment
from bug_changing.types.description import Description
from bug_changing.types.history import History
from bug_changing.types.product_component_pair import ProductComponentPair
from bug_changing.types.summary import Summary, SummaryPair
from bug_changing.types.tossing_path import TossingPath
from bug_changing.utils.nlp_util import NLPUtil
from config import DATETIME_FORMAT


class Bug:

    def __init__(self, id=None, summary=None, description=None, product_component_pair=None, tossing_path=None,
                 creation_time=None, closed_time=None, last_change_time=None, status=None, resolution=None,
                 summary_path=None, bug_reporter=None, type=None, cc_list=None, assignee=None, severity=None,
                 priority=None, assignee_path=None, history_list=None, comments=None
                 # qa_contact=None, regressions=None, blocks=None, duplicates=None,
                 ):

        self.id = id
        self.summary = summary
        self.description = description
        self.product_component_pair = product_component_pair
        self.tossing_path = tossing_path
        self.creation_time = creation_time
        self.closed_time = closed_time
        self.last_change_time = last_change_time
        self.status = status
        self.resolution = resolution
        self.type = type
        self.severity = severity
        self.priority = priority

        self.summary_path = summary_path

        self.reporter = bug_reporter
        self.cc_list = cc_list
        self.assignee = assignee
        self.assignee_path = assignee_path

        self.history_list = history_list
        self.comments = comments
        # self.qa_contact = qa_contact
        # self.regressions = regressions
        # self.blocks = blocks
        # self.duplicates = duplicates

    def __repr__(self):
        return f'{self.id} - {self.summary} - ' \
               f'{self.product_component_pair} - {self.tossing_path} - {self.creation_time} - ' \
               f'{self.closed_time} - {self.last_change_time}'

    def __str__(self):
        return f'{self.id} - {self.summary} - ' \
               f'{self.product_component_pair} - {self.tossing_path} - {self.creation_time} - ' \
               f'{self.closed_time} - {self.last_change_time}'

    @staticmethod
    def dict_to_object(bug_dict):
        bug = Bug()
        bug.id = bug_dict['id']
        bug.summary = bug_dict['summary']
        if bug_dict['comments']:
            bug.description = Description(bug, bug_dict['comments'][0]['text'])
        bug.product_component_pair = ProductComponentPair(bug_dict['product'], bug_dict['component'])
        bug.tossing_path = TossingPath(bug.get_tossing_path(bug_dict['history']))

        bug.creation_time = datetime.strptime(bug_dict['creation_time'], DATETIME_FORMAT)
        # bug.creation_time = datetime.strptime(bug_dict['creation_time'], "%Y-%m-%d %H:%M:%S")
        if 'cf_last_resolved' in bug_dict.keys() and bug_dict['cf_last_resolved'] is not None:
            bug.closed_time = datetime.strptime(bug_dict['cf_last_resolved'], DATETIME_FORMAT)
            # bug.closed_time = datetime.strptime(bug_dict['cf_last_resolved'], "%Y-%m-%d %H:%M:%S")
        bug.last_change_time = datetime.strptime(bug_dict['last_change_time'], DATETIME_FORMAT)
        # bug.last_change_time = datetime.strptime(bug_dict['last_change_time'], "%Y-%m-%d %H:%M:%S")
        bug.status = bug_dict['status']
        bug.resolution = bug_dict['resolution']
        if 'type' in bug_dict.keys():
            bug.type = bug_dict['type']

        bug.summary_path = bug.get_summary_path(bug_dict['history'])

        # bug.reporter = Attendee.from_dict(bug_dict['creator_detail'])
        bug.reporter = bug_dict['creator']
        # cc_list = []
        # for cc in bug_dict['cc_detail']:
        #     cc_list.append(Attendee.from_dict(cc))
        # bug.cc_list = cc_list
        bug.cc_list = bug_dict['cc']
        # bug.assigner = Attendee.from_dict(bug_dict['assigned_to_detail'])
        bug.assignee = bug_dict['assigned_to']
        bug.assignee_path = bug.get_changed_field_path(bug_dict['history'], 'assigned_to')

        bug.severity = bug_dict['severity']
        bug.priority = bug_dict['priority']

        bug.history_list = History.get_history_list(bug_dict['history'])
        bug.comments = Comment.get_comments(bug_dict['comments'])

        # bug.regressions = bug_dict['regressions']
        # bug.blocks = bug_dict['blocks']
        # bug.duplicates = bug_dict['duplicates']

        # bug.summary_token = NLPUtil.preprocess(bug.summary)
        # bug.description_token = NLPUtil.preprocess(bug.description)
        return bug

    def get_tossing_path(self, history):
        tossing_path = []
        is_tossing = 0
        for one in history:
            product_component_pair = ProductComponentPair()
            for change in one['changes']:
                if change['field_name'] == 'product':
                    product_component_pair.product = change['removed']
                    is_tossing = 1
                if change['field_name'] == 'component':
                    product_component_pair.component = change['removed']
                    is_tossing = 1
            if is_tossing == 1 and \
                    (product_component_pair.product is not None or product_component_pair.component is not None):
                tossing_path.append(product_component_pair)
        tossing_path.append(self.product_component_pair)
        tossing_path = Bug.complete_tossing_path(tossing_path)

        return tossing_path

    @staticmethod
    def complete_tossing_path(tossing_path):
        n = len(tossing_path)
        i = 0
        for pair in reversed(tossing_path):
            if pair.product is None:
                tossing_path[n - i - 1].product = tossing_path[n - i].product
            if pair.component is None:
                tossing_path[n - i - 1].component = tossing_path[n - i].component
            i = i + 1
        return tossing_path

    def get_summary_path(self, history, field_name='summary'):
        """
        get summary_path, summary in the path are Summary
        Args:
            history ():
            field_name ():

        Returns: [Summary, Summary, ...]
        """
        change_list = self.get_changed_field_path(history, field_name)
        summary_path = list()
        for index, change in enumerate(change_list):
            summary_path.append(Summary(index, self, change))
        return summary_path

    def get_specific_summary_pair(self, rm_summary_id=None, added_summary_id=None):
        """

        Args:
            rm_summary_id ():
            added_summary_id ():

        Returns: rm_summary, added_summary

        """
        if rm_summary_id is None and added_summary_id is None:
            rm_summary_id = 0
            added_summary_id = 1
        rm_summary = copy.deepcopy(self.summary_path[rm_summary_id])
        added_summary = copy.deepcopy(self.summary_path[added_summary_id])
        return SummaryPair(rm_summary, added_summary)

    def get_goal_oriented_summary_pairs(self):
        """
        summary_path: A->B->C
        Returns: [(A, C), (B, C)]
        """
        # print(self.summary_path)
        summary_pairs = []
        for index, summary in enumerate(self.summary_path):
            if index != len(self.summary_path) - 1:
                summary_pairs.append(self.get_specific_summary_pair(index, -1))
        # print(summary_pairs)
        return summary_pairs

    def get_changed_field_path(self, history, field_name):
        """
        Args:
            history ():
            field_name ():
        Returns:
        """
        change_list = []
        # is_tossing = 0
        for one in history:
            for change in one['changes']:
                if change['field_name'] == field_name:
                    change_list.append(change['removed'])
        if field_name == 'summary':
            change_list.append(self.summary)  # the final one
        elif field_name == 'assigned_to':
            change_list.append(self.assignee)  # the final one
        return change_list

    def get_texts_from_comments(self):
        texts = []
        for comment in self.comments:
            texts.append(comment.text)
        return texts

    def does_summary_summarize_desc(self, percentage=0.7):
        if self.description:
            proportion = NLPUtil.calculate_common_word_proportion(self.summary, self.description.text)
            if proportion >= percentage:
                # print(common_tokens)
                # print(proportion)
                return True
            else:
                # print(common_tokens)
                # print(proportion)
                return False
        return False

    def is_summary_part_of_desc(self, percentage=0.6):
        if self.description:
            longest_substring = NLPUtil.get_longest_common_substring(self.summary, self.description.text)
            summary_length = len(self.summary)
            if longest_substring:
                proportion = len(longest_substring) / summary_length
            else:
                return False
            if proportion > percentage:
                return True
            else:
                # print(longest_substring)
                # print(proportion)
                return False
        return False

    def is_summary_rewriting_for_structure(self):
        """
        is the changes between the first and last summary for stucture
        Returns:
        """
        f_summary = self.summary_path[0].text
        l_summary = self.summary_path[-1].text
        f_extract = NLPUtil.extract_tag_by_regex(f_summary)
        l_extract = NLPUtil.extract_tag_by_regex(l_summary)
        if f_extract:
            # print(f_summary)
            # print(f_extract)
            f_summary = f_summary.replace(f_extract, '').strip()
            # print(f_summary)
        if l_extract:
            # print(l_summary)
            # print(l_extract)
            l_summary = l_summary.replace(l_extract, '').strip()
            # print(l_summary)

        if f_summary == l_summary:
            # print(f'remove: {l_summary}')
            return True
        return False


