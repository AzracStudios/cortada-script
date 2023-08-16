from typing import Self
from position import Position
from symboltable import SymbolTable

class Context:
    def __init__(
        self,
        display_name: str,
        parent: Self | None = None,
        parent_entry_pos: Position | None = None,
    ) -> None:
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table: SymbolTable
