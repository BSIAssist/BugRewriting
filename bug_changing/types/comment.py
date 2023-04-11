from datetime import datetime

from config import DATETIME_FORMAT


class Comment:
    def __init__(self, id=None, count=None, text=None, author=None, creation_time=None):
        self.id = id
        self.count = count
        self.text = text
        self.author = author
        self.creation_time = creation_time

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f'{self.count} - {self.author} - {self.creation_time} - {self.text}'

    def __str__(self):
        return f'{self.count} - {self.author} - {self.creation_time} - {self.text}'

    def __hash__(self):
        # print(hash(str(self)))
        return hash(str(self))

    @classmethod
    def from_dict(cls, comment_dict):
        if 'author' in comment_dict.keys():
            return Comment(comment_dict['id'], comment_dict['count'], comment_dict['text'], comment_dict['author'],
                           datetime.strptime(comment_dict['creation_time'], DATETIME_FORMAT))
        elif 'creator' in comment_dict.keys():
            return Comment(comment_dict['id'], comment_dict['count'], comment_dict['text'], comment_dict['creator'],
                           datetime.strptime(comment_dict['creation_time'], DATETIME_FORMAT))

    @staticmethod
    def get_comments(comment_dict_list):
        comments = []
        for comment_dict in comment_dict_list:
            comments.append(Comment.from_dict(comment_dict))
        return comments
