
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
        super().__init__()

    def __str__(self):
        return 'Epsilon'


class Product:
    def __init__(self, left: NonTerminal, right: CgfRule, *rules: CgfRule):
        self.left = left
        self.right = [right]
        for i in rules:
            self.right.append(i)

    def add(self, *rules: CgfRule) -> None:
        for i in rules:
            self.right.append(i)

    def __str__(self) -> str:
        st = ''
        for i in self.right:
            st = "%s %s |" % (st, i)
        s = "%s -> %s" % (self.left, st)
        return s[:-2]


class Grammar:
    def __init__(self, *products: Product):
        self.products = []
        for i in products:
            self.products.append(i)

    def add(self, *products: Product) -> None:
        for i in products:
            self.products.append(i)

    def get_non_terminal(self):
        pass

    def get_terminal(self):
        pass

    def first(self):
        pass

    def follow(self):
        pass

    def __str__(self) -> str:
        st = ''
        for i in self.products:
            st = "%s %s \n" % (st, i)
        return st
