from typing import Self

class Position:
    def __init__(self, idx: int, col: int, ln: int, file_name: str):
        self.idx: int = idx
        self.col: int = col
        self.ln: int = ln
        self.file_name: str = file_name

    def copy(self) -> Self:
        return Position(self.idx, self.col, self.ln, self.file_name)

    def advance(self, char=None) -> Self:
        self.idx += 1
        self.col += 1

        if char == "\n":
            self.col = 0
            self.ln += 1

        return self
    
    def __repr__(self) -> str:
        return f"Ln: {self.ln + 1}, Col: {self.col}"
