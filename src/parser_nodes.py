from tok import Token
from position import Position


class Node:
    def __init__(self, start_pos: Position, end_pos: Position):
        self.start_pos: Position = start_pos
        self.end_pos: Position = end_pos


class NumberNode(Node):
    def __init__(self, tok: Token):
        self.tok: Token = tok
        Node.__init__(self, self.tok.start_pos, self.tok.end_pos)

    def __repr__(self):
        return f"{self.tok}"


class BooleanNode(Node):
    def __init__(self, tok: Token):
        self.tok: Token = tok
        Node.__init__(self, self.tok.start_pos, self.tok.end_pos)

    def __repr__(self):
        return f"{self.tok}"


class BinaryOperatorNode(Node):
    def __init__(self, left_node: Node, op_tok: Token, right_node: Node):
        self.left_node: Node = left_node
        self.op_tok: Token = op_tok
        self.right_node: Node = right_node
        Node.__init__(self, self.left_node.start_pos, self.right_node.end_pos)

    def __repr__(self):
        return f"({self.left_node} {self.op_tok} {self.right_node})"


class UnaryOperatorNode(Node):
    def __init__(self, op_tok: Token, right_node: Node):
        self.op_tok: Token = op_tok
        self.right_node: Node = right_node
        Node.__init__(self, self.op_tok.start_pos, self.right_node.end_pos)

    def __repr__(self):
        return f"({self.op_tok} {self.right_node})"


class VariableInitNode(Node):
    def __init__(self, var_name: Token, value: Node):
        self.var_name = var_name
        self.value = value
        Node.__init__(self, self.var_name.start_pos, self.value.end_pos)

    def __repr__(self):
        return f"(INIT {self.var_name} = {self.value})"


class VariableAssignNode(Node):
    def __init__(self, var_name: Token, value: Node):
        self.var_name = var_name
        self.value = value
        Node.__init__(self, self.var_name.start_pos, self.value.end_pos)

    def __repr__(self):
        return f"(ASGN {self.var_name} = {self.value})"


class VariableAccessNode(Node):
    def __init__(self, var_name: Token):
        self.var_name = var_name
        Node.__init__(self, self.var_name.start_pos, self.var_name.end_pos)

    def __repr__(self):
        return f"(ACCESS {self.var_name})"
