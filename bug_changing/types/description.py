class Description:
    def __init__(self, bug, text,
                 suggested_solution=None, actual_behavior=None, trigger_action=None,
                 platform=None, component=None,
                 length=None):
        self.bug = bug
        self.text = text
        self.suggested_solution = suggested_solution
        self.actual_behavior = actual_behavior
        self.trigger_action = trigger_action
        self.platform = platform
        self.component = component
        self.length = length
        # self.content = content
        # self.structure = structure

    def __eq__(self, other):
        return self.bug.id == other.bug.id and self.text == other.text

    def __repr__(self):
        return f'{self.bug.id} - {self.text}'

    def __str__(self):
        return f'{self.bug.id} - {self.text}'

    def __hash__(self):
        # print(hash(str(self)))
        return hash(str(self))

    @classmethod
    def from_description(cls, bug, text):
        return cls(bug, text)
