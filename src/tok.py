from position import Position


class Token:
    def __init__(
        self,
        token_type,
        start_pos,
        value=None,
        end_pos=None,
    ):
        self.type = token_type
        self.value = value
        self.start_pos = start_pos.copy()
        self.end_pos = end_pos.copy() if end_pos else start_pos.copy().advance()

    def matches(self, token_type, value):
        return self.type == token_type and self.value == value

    def __repr__(self):
        return f"{self.type}{f':{self.value}' if self.value else ''}"
