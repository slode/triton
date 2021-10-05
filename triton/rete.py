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
    def __init__(self, match=None, target=None, **kwargs):
        super().__init__(type="alpha-node", **kwargs)
        self.match = match
        self.target = target

    def __json__(self):
        doc = super().__json__()
        doc.update({"match": self.match, "target": self.target})
        return doc

    def add_wme(self, wme):
        if self.match is not None:
            if getattr(wme, self.match) != self.target:
                return

        for child in self.children:
            child.add_wme(wme)

class AlphaMemoryNode(Node):
    def __init__(self, **kwargs):
        super().__init__(type="alpha-memory-node", **kwargs)
        self.wmes = set()
        self.name = gensym("AM")

    def __json__(self):
        doc = super().__json__()
        doc.update({"name": self.name, "wmes": [wme for wme in self.wmes]})
        return doc

    def add_wme(self, wme):
        self.wmes.add(wme)
        # calls beta nodes
        for child in self.children:
            assert isinstance(child, BetaNode)
            child.right_activation(wme)


class BetaNode(Node):
    def __init__(self, **kwargs):
        super().__init__(type="beta-node", **kwargs)
        self.beta_memory = None
        self.alpha_memory = None
        self.name = gensym("B")
        self.tests = []

    def __json__(self):
        doc = super().__json__()
        doc.update({"beta_memory": self.beta_memory.name, "alpha_memory": self.alpha_memory.name, "tests": self.tests})
        return doc

    def join_test(self, token, wme):
        for token_wme in token:
            if token_wme.id != wme.id:
                return False
        return True

    def right_activation(self, wme):
        for token in self.beta_memory.tokens:
            if self.join_test(token, wme):
                for child in self.children:
                    child.left_activation(token, wme)

        # Dummy memory
        if not self.beta_memory.tokens:
            for child in self.children:
                child.left_activation([], wme)

    def left_activation(self, token):
        for wme in self.alpha_memory.wmes:
            if self.join_test(token, wme):
                for child in self.children:
                    assert isinstance(child, (BetaMemoryNode, ProductionNode))
                    child.left_activation(token, wme)

    def add_beta_parent(self, beta_memory):
        self.beta_memory = beta_memory
        beta_memory.add_child(self)
        return beta_memory

    def add_alpha_parent(self, alpha_memory):
        self.alpha_memory = alpha_memory
        alpha_memory.add_child(self)
        return alpha_memory

class BetaMemoryNode(Node):
    def __init__(self, **kwargs):
        super().__init__(type="beta-memory-node", **kwargs)
        self.name = gensym("BM")
        self.tokens = []

    def __json__(self):
        doc = super().__json__()
        doc.update({"tokens": self.tokens})
        return doc

    def left_activation(self, token, wme):
        # token = token.copy()
        token.append(wme)
        self.tokens.append(token)
        for child in self.children:
            assert isinstance(child, BetaNode)
            child.left_activation(token)

class ProductionNode(Node):
    def __init__(self, callback=lambda x:x, **kwargs):
        super().__init__(type="production-node", **kwargs)
        self.callback = callback

    def __json__(self):
        doc = super().__json__()
        doc.update({"callback": str(self.callback.__code__.__str__())})
        return doc

    def left_activation(self, token, wme):
        token.append(wme)
        self.callback(token)

class Rete:
    def __init__(self):
        self._alpha_net = AlphaNode(net=self)
        self._alpha_memory = {}
        self._beta_net = {}
        self._beta_memory = {}
        self._terminal_nodes = {}

    def __json__(self):
        return {
                "_type": "rete",
                # "alpha_net": self._alpha_net,
                "alpha_memory": self._alpha_memory,
                # "beta_net": self._beta_net,
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

    def beta_node(self, beta_parent=None, alpha_parent=None, child=None):
        beta_node = BetaNode()
        beta_node.net = self
        if beta_parent is None:
            beta_parent = self.beta_memory()
        beta_node.add_beta_parent(beta_parent)
        beta_node.add_alpha_parent(alpha_parent)
        beta_node.add_child(child)
        self._beta_net[beta_node.name] = beta_node
        return child

    def beta_memory(self):
        beta_memory_node = BetaMemoryNode()
        beta_memory_node.net = self
        self._beta_memory[beta_memory_node.name] = beta_memory_node
        return beta_memory_node

    def production(self, *conds, production):
        bnode = None
        for test in conds:
            anode = net._alpha_net.add_child(AlphaNode(match="attr", target=test.attr)).add_child(AlphaNode(match="value", target=test.target)).add_child(net.alpha_memory())
            bnode = net.beta_node(
                beta_parent=bnode,
                alpha_parent=anode,
                child=ProductionNode(callback=production) if test == conds[-1] else net.beta_memory())

wme = namedtuple("WME", ["id", "attr", "value"])
test = namedtuple("TEST", ["attr", "operand", "target"])

net = Rete()
net.production(
        test("color", "==", "WHITE"),
        test("size", "==", "LARGE"),
        production=lambda x: print("PROD:", x))
net.production(
        test("color", "==", "GREEN"),
        production=lambda x: print("PROD2:", x))
net.production(
        test("color", "==", "GREEN"),
        test("size", "==", "LARGE"),
        production=lambda x: print("PROD3:", x))

# net.add_wme(wme("x", "color", "WHITE"))
# net.add_wme(wme("x", "size", "LARGE"))
net.add_wme(wme("y", "size", "LARGE"))
net.add_wme(wme("y", "color", "GREEN"))
net.add_wme(wme("y", "color", "WHITE"))
# net.add_wme(wme("z", "color", "GREEN"))
# net.add_wme(wme("z", "size", "LARGE"))
net.add_wme(wme("y", "color", "GREEN"))
# print(json.dumps(net.alpha_net(), default=lambda o: o.__json__(), indent=2, sort_keys=True))
