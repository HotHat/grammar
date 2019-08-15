import unittest
from cfg import *


class TestGrammar2(unittest.TestCase):
    def setUp(self) -> None:

        self.t_a = Terminal('a')
        self.t_b = Terminal('b')
        self.t_d = Terminal('d')
        self.t_g = Terminal('g')
        self.t_h = Terminal('h')

        self.n_s = NonTerminal('S', True)
        self.n_a = NonTerminal('A')
        self.n_b = NonTerminal("B")
        self.n_c = NonTerminal("C")

        self.p1 = Product(self.n_s,
                          CgfRule(self.n_a, self.n_c, self.n_b),
                          CgfRule(self.n_c, self.t_b, self.t_b),
                          CgfRule(self.n_b, self.t_a))

        self.p2 = Product(self.n_a,
                          CgfRule(self.t_d, self.t_a),
                          CgfRule(self.n_b, self.n_c))

        self.p3 = Product(self.n_b, CgfRule(self.t_g), Grammar.EPSILON)
        self.p4 = Product(self.n_c, CgfRule(self.t_h), Grammar.EPSILON)

        self.grammar = Grammar(self.p1, self.p2, self.p3, self.p4)

    def test_grammar(self):
        print(self.grammar)

    def test_get_non_terminal(self):
        s = self.grammar.get_non_terminal()
        for i in s:
            print(i)

    def test_get_terminal(self):
        s = self.grammar.get_terminal()
        for i in s:
            print(i)

    def test_first(self):
        s = self.grammar.first2(self.n_s)
        print('FIRST(%s) = %s' % (self.n_s, list(map(lambda x: str(x), s))))
        s = self.grammar.first2(self.n_a)
        print('FIRST(%s) = %s' % (self.n_a, list(map(lambda x: str(x), s))))
        s = self.grammar.first2(self.n_b)
        print('FIRST(%s) = %s' % (self.n_b, list(map(lambda x: str(x), s))))
        s = self.grammar.first2(self.n_c)
        print('FIRST(%s) = %s' % (self.n_c, list(map(lambda x: str(x), s))))

    def test_epsilon(self):
        e = Grammar.EPSILON
        print(id(e))
        e = Grammar.EPSILON
        print(id(e))

    def test_nn(self):
        a = {'a', 'b', 'c'}
        a = a.difference({'a'})

        print(a)
