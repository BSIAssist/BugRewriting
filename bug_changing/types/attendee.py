

class Attendee:

    def __init__(self, email=None, id=None, name=None, real_name=None, nick=None):
        self.email = email
        self.id = id
        self.name = name
        self.real_name = real_name
        self.nick = nick

    def __eq__(self, other):
        return self.email == other.email

    def __repr__(self):
        return f'{self.email}'

    def __str__(self):
        return f'{self.email}'

    def __hash__(self):
        # print(hash(str(self)))
        return hash(str(self))

    @classmethod
    def from_dict(cls, attendee_dict):
        return Attendee(attendee_dict['email'], attendee_dict['id'], attendee_dict['name'],
                        attendee_dict['real_name'], attendee_dict['nick'])


