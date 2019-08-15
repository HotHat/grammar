
class CgfNode:
    def __init__(self, name):
        self.name = name


class Terminal(CgfNode):
    def __str__(self):
        return '%s' % self.name
        # return 'Terminal(%s)' % self.name


class NonTerminal(CgfNode):
    def __init__(self, name, start_node=False):
        super().__init__(name)
        self.start_node = start_node

    def __str__(self):
        return '%s' % self.name
        # if self.start_node:
        # return '<S>NonTerminal(%s)' % self.name
        # else:
        #     return 'NonTerminal(%s)' % self.name


class CgfRule:
    def __init__(self, *node: CgfNode):
        self.node = node

    def __str__(self):
        st = ''
        for i in self.node:
            st = "%s %s" % (st, i)
        return st


class Epsilon(CgfRule):
    def __init__(self):
        super().__init__([])

    def __str__(self):
        return 'Epsilon'


class Product:
    def __init__(self, left: NonTerminal, right: CgfRule, *other: CgfRule):
        self.left = left
        self.right = [right]
        for i in other:
            self.right.append(i)

    def __str__(self):
        st = ''
        for i in self.right:
            st = "%s %s |" % (st, i)
        s = "%s -> %s" % (self.left, st)
        return s[:-2]


if __name__ == '__main__':

    # E --> TE'
    # E' --> +TE' | e
    # T --> FT'
    # T' --> *FT' | e
    # F --> id | (E)

    a = Terminal('+')
    b = Terminal('(')
    c = Terminal(')')
    d = Terminal('*')
    f = Terminal('id')
    g = Terminal('e')

    A = NonTerminal('E', True)
    B = NonTerminal('T')
    C = NonTerminal("E'")
    D = NonTerminal("F")
    F = NonTerminal("T'")

    P1 = Product(A, CgfRule(B, C))
    P2 = Product(C, CgfRule(a, B, C), Epsilon())
    P3 = Product(B, CgfRule(D, F), CgfRule(d, D, F), Epsilon())
    # P4 = Product(B, )
    P5 = Product(D, CgfRule(f), CgfRule(b, A, c))

    print(P1)
    print(P2)
    print(P3)
    # print(P4)
    print(P5)

