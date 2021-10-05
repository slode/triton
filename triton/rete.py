from collections import namedtuple
import json

SYMNR = 0
def gensym(prefix):
    global SYMNR
    SYMNR += 1
    return prefix + str(SYMNR)

class Node:
    def __init__(self, type=None, parent=None, net=None):
        self.type = type
        self.parent = parent
        self.children = set()
        self.net = net

    def __json__(self):
        return {"_type": self.type, "children": [c for c in self.children]}

    def add_child(self, node):
        node.net = self.net
        if node not in self.children:
            self.children.add(node)
        return node


class AlphaNode(Node):
    import operator
    TEST_OPERATOR = {
        "=": operator.eq,
        "==": operator.eq,
        "<=": operator.le,
        ">=": operator.ge,
        "<": operator.lt,
        ">": operator.gt,
        "!=": operator.ne,
        "<>": operator.ne,
        "~=": operator.ne
    }
    def __init__(self, test, **kwargs):
        super().__init__(type="alpha-node", **kwargs)
        self.test = test

    def __json__(self):
        doc = super().__json__()
        doc.update({"test": self.test})
        return doc

    def add_wme(self, wme):
        if self.test is not None:
            if not wme.attr == self.test.attr:
                return
            if not self.TEST_OPERATOR[self.test.operand](wme.value, self.test.target):
                return

        for child in self.children:
            child.add_wme(wme)

    def add_test(self, test):
        for child in self.children:
            if child.test == test:
                return child
        return self.add_child(AlphaNode(test))

    def add_memory(self):
        for child in self.children:
            if isinstance(child, AlphaMemoryNode):
                return child
        return self.add_child(net.alpha_memory())

class AlphaMemoryNode(Node):
    def __init__(self, **kwargs):
        super().__init__(type="alpha-memory-node", **kwargs)
        self.wmes = {}
        self.name = gensym("AM")

    def __json__(self):
        doc = super().__json__()
        doc.update({"name": self.name, "wmes": self.wmes})
        return doc

    def add_wme(self, wme):
        self.wmes[wme.id] = wme
        # calls beta nodes
        for child in self.children:
            assert isinstance(child, BetaNode)
            child.right_activation(wme)


class BetaNode(Node):
    def __init__(self, parent=None, alpha_memory=None, **kwargs):
        super().__init__(type="beta-node", **kwargs)
        self.parent = parent
        if self.parent is not None:
            parent.add_child(self)

        self.alpha_memory = alpha_memory
        assert self.alpha_memory is not None
        alpha_memory.add_child(self)

    def join_test(self, token, wme):
        for token_wme in token:
            if token_wme.id != wme.id:
                return False
        return True

    def __json__(self):
        doc = super().__json__()
        doc.update({"parent": self.parent.name, "alpha_memory": self.alpha_memory.name, "tests": self.tests})
        return doc

    def right_activation(self, wme):
        if self.parent is None:
            for child in self.children:
                child.left_activation([], wme)
        else:
            if wme.id in self.parent.tokens:
                token = self.parent.tokens[wme.id]
                for child in self.children:
                    child.left_activation(token, wme)

    def left_activation(self, token):
        for wme in self.alpha_memory.wmes.values():
            if self.join_test(token, wme):
                for child in self.children:
                    assert isinstance(child, (BetaMemoryNode, ProductionNode))
                    child.left_activation(token, wme)

class BetaMemoryNode(Node):
    def __init__(self, **kwargs):
        super().__init__(type="beta-memory-node", **kwargs)
        self.name = gensym("BM")
        self.tokens = {}#[]

    def __json__(self):
        doc = super().__json__()
        doc.update({"name": self.name, "tokens": self.tokens})
        return doc

    def left_activation(self, token, wme):
        token = token.copy()
        token.append(wme)
        self.tokens.setdefault(wme.id, []).append(token)
        for child in self.children:
            assert isinstance(child, BetaNode)
            child.left_activation(token)

class ProductionNode(Node):
    def __init__(self, callback=lambda x:x, **kwargs):
        super().__init__(type="production-node", **kwargs)
        self.callback = callback
        self.tokens = {}

    def __json__(self):
        doc = super().__json__()
        doc.update({"callback": str(self.callback.__code__.__str__()), "token": self.tokens})
        return doc

    def left_activation(self, token, wme):
        token.append(wme)
        self.tokens[wme.id] = token
        self.callback(token)

class Rete:
    def __init__(self):
        self._alpha_net = AlphaNode(None, net=self)
        self._alpha_memory = {}
        self._beta_memory = {}
        self._terminal_nodes = {}

    def __json__(self):
        return {
                "_type": "rete",
                # "alpha_net": self._alpha_net,
                "alpha_memory": self._alpha_memory,
                "beta_memory": self._beta_memory
                }

    def add_wme(self, wme):
        self._alpha_net.add_wme(wme)

    def alpha_net(self):
        return self._alpha_net

    def alpha_memory(self):
        alpha_memory = AlphaMemoryNode()
        alpha_memory.net = self
        self._alpha_memory[alpha_memory.name] = alpha_memory
        return alpha_memory

    def beta_node(self, parent=None, alpha_memory=None, child=None):
        beta_node = BetaNode(parent=parent, alpha_memory=alpha_memory, net=self)
        if child is None:
            child = self.beta_memory()
        beta_node.add_child(child)
        return child

    def beta_memory(self):
        beta_memory_node = BetaMemoryNode()
        beta_memory_node.net = self
        self._beta_memory[beta_memory_node.name] = beta_memory_node
        return beta_memory_node

    def production(self, *conds, production):
        bnode = None
        for test in conds:
            amemory = self._alpha_net.add_test(test).add_memory()
            bnode = self.beta_node(
                parent=bnode,
                alpha_memory=amemory,
                child=ProductionNode(callback=production) if test == conds[-1] else None)

wme = namedtuple("WME", ["id", "attr", "value"])
test = namedtuple("ALPHA_TEST", ["attr", "operand", "target"])

net = Rete()
net.production(
        test("color", "==", "WHITE"),
        test("size", "==", "SMALL"),
        production=lambda x: print("PROD:", x))
net.production(
        test("count", "<", 3),
        production=lambda x: print("count is less than 3:", x))
net.production(
        test("color", "!=", "GREEN"),
        test("size", "==", "LARGE"),
        production=lambda x: print("PROD3:", x))

net.add_wme(wme("x", "color", "WHITE"))
net.add_wme(wme("x", "size", "SMALL"))
net.add_wme(wme("x", "size", "LARGE"))
net.add_wme(wme("y", "size", "LARGE"))
net.add_wme(wme("y", "color", "GREEN"))
net.add_wme(wme("y", "size", "SMALL"))
net.add_wme(wme("z", "color", "GREEN"))
net.add_wme(wme("z", "size", "LARGE"))
net.add_wme(wme("y", "color", "WHITE"))
net.add_wme(wme("y", "count", 4))
net.add_wme(wme("y", "count", 2))
# print(json.dumps(net.alpha_net(), default=lambda o: o.__json__(), indent=2, sort_keys=True))
