

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
    instance = None

    def __init__(self):
        super().__init__(Terminal('Є'))

    def __str__(self):
        return 'Epsilon'

    def __hash__(self):
        return hash('__EPSILON__')

    def __eq__(self, other):
        if type(other) is Epsilon:
            return True
        return False


class Product:
    def __init__(self, left: NonTerminal, right: CgfRule, *rules: CgfRule):
        self.left = left
        self.right = [right]
        for i in rules:
            self.right.append(i)

    def add(self, *rules: CgfRule) -> None:
        for i in rules:
            self.right.append(i)

    def have_epsilon(self):
        for i in self.right:
            # print(type(i))
            if type(i) is Epsilon:
                return True
        return False

    def __str__(self) -> str:
        st = ''
        for i in self.right:
            st = "%s %s |" % (st, i)
        s = "%s -> %s" % (self.left, st)
        return s[:-2]


class Grammar:
    EPSILON = Epsilon()

    def __init__(self, *products: Product):
        self.products = {}
        for i in products:
            self.products[i.left] = i

        self.first_set = {}
        self.follow_set = {}

    def add(self, *products: Product) -> None:
        for i in products:
            self.products[i.left] = i

    def get_non_terminal(self):
        # sm = set()
        # for rhs in self.products.values():
        #     for n in rhs:
        #         for i in n.nodes:
        #             if type(i) == NonTerminal:
        #                 sm.add(i)
        s = self.products.keys()

        # if sm != s:
        #     raise Exception('non terminal not match')

        return s

    def get_terminal(self):
        s = set()
        for rhs in self.products.values():
            for n in rhs.right:
                for i in n.nodes:
                    if type(i) == Terminal:
                        s.add(i)
        return s

    def first_non_terminal(self, t: CgfNode):
        """
        1. If x is a terminal, then FIRST(x) = { ‘x’ }
        2. If x-> Є, is a production rule, then add Є to FIRST(x).
        3. If X->Y1 Y2 Y3….Yn is a production,
           1. FIRST(X) = FIRST(Y1)
           2. If FIRST(Y1) contains Є then FIRST(X) = { FIRST(Y1) – Є } U { FIRST(Y2) }
           3. If FIRST (Yi) contains Є for all i = 1 to n, then add Є to FIRST(X).
        """
        if type(t) is Terminal:
            return {t}

        s = set()
        product = self.products[t]
        for rule in product.right:
            if type(rule) is Epsilon:
                s.add(rule)
            else:
                if type(rule.nodes[0]) is Terminal:
                    s.add(rule.nodes[0])
                else:
                    through = True
                    for it in rule.nodes:
                        # is non terminal have cal first
                        if it in self.first_set:
                            r = self.first_set[it]
                        else:
                            r = self.first_non_terminal(it)

                        # print(id(Grammar.EPSILON))
                        if Grammar.EPSILON in r:
                            r = r.difference({Grammar.EPSILON})
                            s = s.union(r)
                        else:
                            s = s.union(r)
                            through = False
                            break
                    if through:
                        s.add(Grammar.EPSILON)
        # set the first set
        if type(t) is NonTerminal and t not in self.first_set:
            self.first_set[t] = s

        return s

    def first(self):
        non_terminal = self.get_non_terminal()

        for i in non_terminal:
            self.first_non_terminal(i)

        return self.first_set

    def follow(self, t: NonTerminal):
        """
        1) FOLLOW(S) = { $ }   // where S is the starting Non-Terminal
        2) If A -> pBq is a production, where p, B and q are any grammar symbols,
           then everything in FIRST(q)  except ? is in FOLLOW(B.
        3) If A->pB is a production, then everything in FOLLOW(A) is in FOLLOW(B).
        4) If A->pBq is a production and FIRST(q) contains ?,
           then FOLLOW(B) contains { FIRST(q) – ? } U FOLLOW(A)
        """
        s = set()
        if t.start_node:
            s.add((1, Terminal('$')))

        for k, v in self.products.items():
            for n, rules in enumerate(v.right):
                # find the node
                for idx, item in enumerate(rules.nodes):
                    if t is item:
                        if idx < len(rules.nodes) - 1:
                            first = self.first_non_terminal(rules.nodes[idx + 1])
                            if Grammar.EPSILON in first:
                                s.add((3, k))

                            s.add((2, rules.nodes[idx+1]))
                        else:
                            if k is not t:
                                s.add((3, k))
        return s

    def __str__(self) -> str:
        st = ''
        for (k, v) in self.products.items():
            sm = ''
            for i in v.right:
                sm = "%s %s |" % (sm, i)
            st = st + "%s  -> %s \n" % (k, sm[:-1])
        return st
