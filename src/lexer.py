from position import Position
from tok import Token
from error import Error

class Lexer:
    def __init__(self, file_name: str, src: str):
        self.file_name: str = file_name
        self.src: str = src
        self.char: str|None = ""
        self.position: Position = Position(-1, -1, 0, self.file_name)
        self.should_advance_next_ittr: bool = True
        self.tokens: list[Token] = []

    def advance(self) -> None:
        self.position.advance(self.char)
        
        if self.position.idx < len(self.src):
            self.char = self.src[self.position.idx]
            return
        
        self.char = None

    def next(self) -> tuple[Token|None, Error|None]:
        # TODO: Implement lexing
        return (None, None)

    def tokenize(self) -> list[Token] | Error:
        while self.char:
            next_token, error = self.next()
            
            if error: return error
            
            if self.should_advance_next_ittr:
                self.advance()

            if next_token: self.tokens.append(next_token)

        return self.tokens
