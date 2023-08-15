from type import *
from position import Position


class Token:
    def __init__(
        self,
        token_type: TokenType,
        start_pos: Position,
        value: TokenValue = None,
        end_pos: Position | None = None,
    ):
        self.type: TokenType = token_type
        self.value: TokenValue = value
        self.start_pos: Position = start_pos.copy()
        self.end_pos: Position = end_pos.copy() if end_pos else start_pos.copy().advance()

    def matches(self, token_type: TokenType, value: TokenValue) -> bool:
        return self.type == token_type and self.value == value

    def __repr__(self) -> str:
        return f"{self.type}{f':{self.value}' if self.value else ''}"
