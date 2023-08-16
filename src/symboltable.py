class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None

    def get(self, name):
        val = self.symbols.get(name, None)
        if not val and self.parent:
            return self.parent.get(name, None)
        return val

    def set(self, name, val):
        self.symbols[name] = val

    def remove(self, name):
        del self.symbols[name]
