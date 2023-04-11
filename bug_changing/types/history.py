from datetime import datetime

from config import DATETIME_FORMAT


class Change:
    def __init__(self, field_name=None, removed=None, added=None, comment_count=None, comment_id=None):
        self.field_name = field_name
        self.removed = removed
        self.added = added
        self.comment_count = comment_count
        self.comment_id = comment_id

    def __eq__(self, other):
        return self.field_name == other.field_name and self.added == other.added and self.removed == other.removed

    def __repr__(self):
        return f'{self.field_name} - {self.removed} - {self.added} - {self.comment_count} - {self.comment_id}'

    def __str__(self):
        return f'{self.field_name} - {self.removed} - {self.added} - {self.comment_count} - {self.comment_id}'

    def __hash__(self):
        # print(hash(str(self)))
        return hash(str(self))

    @classmethod
    def from_dict(cls, change_dict):
        change = Change(change_dict['field_name'], change_dict['removed'], change_dict['added'])
        comment_count = 'comment_count'
        comment_id = 'comment_id'
        if comment_count in change_dict.keys():
            change.comment_count = change_dict[comment_count]
        if comment_id in change_dict.keys():
            change.comment_id = change_dict[comment_id]
        return change

    @staticmethod
    def get_changes(change_dict_list):
        changes = []
        for change_dict in change_dict_list:
            changes.append(Change.from_dict(change_dict))
        return changes


class History:
    def __init__(self, who=None, when=None, changes=None):
        self.who = who
        self.when = when
        self.changes = changes

    def __eq__(self, other):
        return self.changes == other.changes

    def __repr__(self):
        return f'{self.who} - {self.when} - {self.changes}'

    def __str__(self):
        return f'{self.who} - {self.when} - {self.changes}'

    def __hash__(self):
        # print(hash(str(self)))
        return hash(str(self))

    @classmethod
    def from_dict(cls, history_dict):
        history = History(history_dict['who'], datetime.strptime(history_dict['when'], DATETIME_FORMAT))
        history.changes = Change.get_changes(history_dict['changes'])
        return history

    @staticmethod
    def get_history_list(history_dict_list):
        history_list = []
        for history_dict in history_dict_list:
            history_list.append(History.from_dict(history_dict))
        return history_list



