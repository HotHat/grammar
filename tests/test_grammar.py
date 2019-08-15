import unittest
from cfg import *


class TestGrammar(unittest.TestCase):
    def setUp(self) -> None:
        self.t_plus = Terminal('+')
        self.t_left_bracket = Terminal('(')
        self.t_right_bracket = Terminal(')')
        self.t_mul = Terminal('*')
        self.t_id = Terminal('id')

        self.n_e = NonTerminal('E', True)
        self.n_t = NonTerminal('T')
        self.n_e2 = NonTerminal("E'")
        self.n_f = NonTerminal("F")
        self.n_t2 = NonTerminal("T'")

        self.P1 = Product(self.n_e, CgfRule(self.n_t, self.n_e2))
        self.P2 = Product(self.n_e2, CgfRule(self.t_plus, self.n_t, self.n_e2), Epsilon())
        self.P3 = Product(self.n_t, CgfRule(self.n_f, self.n_t2), CgfRule(self.t_mul, self.n_f, self.n_t2), Epsilon())
        self.P4 = Product(self.n_f, CgfRule(self.t_id), CgfRule(self.t_left_bracket, self.n_e, self.t_right_bracket))

    def test_node(self):
        print(self.t_plus)

    def test_rule(self):
        rule = CgfRule(self.n_t, self.n_e2)
        print(rule)

    def test_product(self):
        print(self.P1)
        print(self.P2)
        print(self.P3)
        print(self.P4)
