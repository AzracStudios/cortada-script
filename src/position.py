class Position:
    def __init__(self, idx, col, ln, file_name, file_src):
        self.idx = idx
        self.col = col
        self.ln = ln
        self.file_name = file_name
        self.file_src = file_src

    def copy(self):
        return Position(self.idx, self.col, self.ln, self.file_name, self.file_src)

    def advance(self, char=None):
        self.idx += 1
        self.col += 1

        if char == "\n":
            self.col = 0
            self.ln += 1

        return self
    
    def __repr__(self):
        return f"Ln: {self.ln + 1}, Col: {self.col}"
