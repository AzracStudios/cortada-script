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


class StringNode(Node):
    def __init__(self, tok: Token):
        self.tok: Token = tok
        Node.__init__(self, self.tok.start_pos, self.tok.end_pos)

    def __repr__(self):
        return f"{self.tok}"


class FmtStringNode(Node):
    def __init__(self, nodes: list[Node]):
        self.nodes = nodes
        Node.__init__(
            self, self.nodes[0].start_pos, self.nodes[len(self.nodes) - 1].end_pos
        )

    def __repr__(self):
        return f"({[node for node in self.nodes]})"


class BooleanNode(Node):
    def __init__(self, tok: Token):
        self.tok: Token = tok
        Node.__init__(self, self.tok.start_pos, self.tok.end_pos)

    def __repr__(self):
        return f"{self.tok}"


class NilNode(Node):
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


class IfNode(Node):
    def __init__(self, cases: list[tuple[Node, Node]], else_case: Node | None):
        self.cases = cases
        self.else_case = else_case
        Node.__init__(
            self,
            self.cases[0][0].start_pos,
            (self.else_case or self.cases[len(self.cases) - 1][0]).end_pos,
        )


class WhileNode(Node):
    def __init__(self, condition: Node, do: Node):
        self.condition = condition
        self.do = do
        Node.__init__(self, self.condition.start_pos, do.end_pos)


class FnDefNode(Node):
    def __init__(
        self, var_name: Token | None, arg_names: list[Token] | None, body: Node
    ):
        self.var_name = var_name
        self.arg_names = arg_names
        self.body = body

        Node.__init__(
            self,
            (
                self.var_name or self.arg_names[0] if self.arg_names else self.body
            ).start_pos,
            self.body.end_pos,
        )


class CallNode(Node):
    def __init__(self, to_call: Node, args: list[Node] | None):
        self.to_call = to_call
        self.args = args

        Node.__init__(
            self,
            self.to_call.start_pos,
            (self.args[len(self.args) - 1] if self.args else self.to_call).end_pos,
        )
