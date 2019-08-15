
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
    def __init__(self, first: CgfNode, *nodes: CgfNode):
        self.nodes = [first]
        for i in nodes:
            self.nodes.append(i)

    def __str__(self):
        st = ''
        for i in self.nodes:
            st = "%s %s" % (st, i)
        return st


class Epsilon(CgfRule):
    def __init__(self):
        super().__init__(Terminal('Є'))

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
        self.products = {}
        for i in products:
            self.products[i.left] = i.right

    def add(self, *products: Product) -> None:
        for i in products:
            self.products[i.left] = i.right

    def get_non_terminal(self):
        sm = set()
        for rhs in self.products.values():
            for n in rhs:
                for i in n.nodes:
                    if type(i) == NonTerminal:
                        sm.add(i)
        s = self.products.keys()

        if sm != s:
            raise Exception('non terminal not match')

        return s

    def get_terminal(self):
        s = set()
        for rhs in self.products.values():
            for n in rhs:
                for i in n.nodes:
                    if type(i) == Terminal:
                        s.add(i)
        return s

    def first(self):
        pass

    def first2(self, t: NonTerminal):
        s = set()
        rules = self.products[t]
        for rule in rules:
            if type(rule) is Epsilon:
                s.add(str(rule.nodes[0]))
            else:
                if type(rule.nodes[0]) is Terminal:
                    s.add(str(rule.nodes[0]))
                else:
                    # TODO: first is non terminal
                    pass
        return s

    def follow(self):
        pass

    def __str__(self) -> str:
        st = ''
        for (k, v) in self.products.items():
            sm = ''
            for i in v:
                sm = "%s %s |" % (sm, i)
            st = st + "%s  -> %s \n" % (k, sm[:-1])
        return st
