# Copyright (c) 2021 Stian Lode
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from collections import namedtuple


class Node:
    __symbol_counter = {}
    def gensym(self, prefix):
        Node.__symbol_counter.setdefault(prefix, 0)
        Node.__symbol_counter[prefix] += 1
        return prefix + "_" + str(Node.__symbol_counter[prefix])

    def __init__(self, type=None, parent=None, net=None):
        self.name = self.gensym(type)
        self.net = net
        self.parent = parent
        if self.parent is not None:
            self.parent.add_child(self)
        self.children = set()

    def __json__(self):
        return {
            "name": self.name,
            "parent": self.parent #if self.parent is not None else None
            # "children": [c.name for c in self.children]
        }

    def add_child(self, node):
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
        "~=": operator.ne,
        "is": operator.is_,
        "nis": operator.is_not,
        "is not": operator.is_not,
    }

    def __init__(self, test=None, **kwargs):
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

            if isinstance(self.test.target, Var) and not isinstance(wme.value, Var):
                wme.value = Var(self.test.target.identity, bound=wme.value)
            elif not self.TEST_OPERATOR[self.test.operand](wme.value, self.test.target):
                return

        for child in self.children:
            child.add_wme(wme)

    def add_test(self, test):
        for child in self.children:
            if child.test == test:
                return child
        return self.add_child(AlphaNode(net=self.net, parent=self, test=test))

    def add_memory(self):
        for child in self.children:
            if isinstance(child, AlphaMemoryNode):
                return child
        return self.add_child(AlphaMemoryNode(net=self.net, parent=self))

class AlphaMemoryNode(Node):
    def __init__(self, **kwargs):
        super().__init__(type="alpha-memory-node", **kwargs)
        self.wmes = {}

    def __json__(self):
        doc = super().__json__()
        doc.update({"wmes": self.wmes})
        return doc

    def retract_wme(self, wme):
        if wme.id in self.wmes:
            self.wmes.pop(wme.id)

    def add_wme(self, wme):
        self.wmes[wme.id] = wme
        self.net._add_retraction(wme, self)
        for child in self.children:
            assert isinstance(child, BetaNode)
            child.right_activation(wme)


class BetaNode(Node):
    def __init__(self, alpha_memory=None, test=None, **kwargs):
        super().__init__(type="beta-node", **kwargs)
        assert alpha_memory is not None

        self.test = test
        self.alpha_memory = alpha_memory
        alpha_memory.add_child(self)

    def join_test(self, token, wme):
        for twme in token:
            if twme.id == wme.id:
                return True

            if isinstance(twme.value, Var) and twme.value.bound == wme.id:
                return True

            if isinstance(wme.value, Var) and wme.value.bound == twme.id:
                return True
        return False

    def __json__(self):
        doc = super().__json__()
        doc.update({"alpha_memory": self.alpha_memory if self.alpha_memory is not None else None})
        return doc

    def right_activation(self, wme):
        if self.parent is None:
            for child in self.children:
                child.left_activation([], wme)
        else:
            for token in self.parent.tokens.values():
                if self.join_test(token, wme):
                    for child in self.children:
                        assert isinstance(child, (BetaMemoryNode, ProductionNode))
                        child.left_activation(token, wme)

    def left_activation(self, token):
        for wme in list(self.alpha_memory.wmes.values()):
            if self.join_test(token, wme):
                for child in self.children:
                    assert isinstance(child, (BetaMemoryNode, ProductionNode))
                    child.left_activation(token, wme)

    def add_memory(self):
        for child in self.children:
            if isinstance(child, BetaMemoryNode):
                return child
        return self.add_child(BetaMemoryNode(net=self.net, parent=self))

class BetaMemoryNode(Node):
    def __init__(self, **kwargs):
        super().__init__(type="beta-memory-node", **kwargs)
        self.tokens = {}

    def __json__(self):
        doc = super().__json__()
        doc.update({"tokens": self.tokens})
        return doc

    def retract_wme(self, wme):
        if wme.id in self.tokens:
            self.tokens.pop(wme.id)
        
    def left_activation(self, token, wme):
        token = token.copy()
        token.append(wme)
        self.tokens[wme.id] = token
        self.net._add_retraction(wme, self)
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
        doc.update({
            "callback": str(self.callback.__code__.__str__()),
            "tokens": self.tokens
        })
        return doc

    def retract_wme(self, wme):
        if wme.id in self.tokens:
            self.tokens.pop(wme.id)

    def left_activation(self, token, wme):
        token = token.copy()
        token.append(wme)
        self.net._add_retraction(wme, self)
        self.tokens[wme.id] = lambda: self.callback(self.net, token)

class Rete:
    def __init__(self):
        self._alpha_root = AlphaNode(None, net=self)
        self._prod_memory = {}
        self._wmes = {}

    def __json__(self):
        return {
            "_type": "rete-network",
            "prod_memory": self._prod_memory,
            "wmes": list(self._wmes)
        }

    def dump(self):
        import json
        print(json.dumps(net, default=lambda x: x.__json__(), indent=4))

    def _add_retraction(self, wme, node):
        self._wmes.setdefault(((wme.id, wme.attr)), set()).add(node)

    def _create_beta_node(self, parent=None, alpha_memory=None, production=None):
        for c in alpha_memory.children:
            if isinstance(c, BetaNode) and c.parent==parent:
                bnode = c
                break
        else:
            bnode = BetaNode(parent=parent, alpha_memory=alpha_memory, net=self)

        if production is not None:
            return self._create_production(parent=bnode, callback=production)

        return bnode.add_memory()

    def _create_production(self, **kwargs):
        production_node = ProductionNode(net=self, **kwargs)
        self._prod_memory[production_node.name] = production_node
        return production_node

    def add_wme(self, wme):
        """Adds a WME to the system

        WMEs with identical "id" and "attr" attributes will be retracted from
        the network prior to adding a WME.

        Args:
            wme: a WME instance on the form: wme("id", "attr", "value")
        
        Returns:
            a reference to the rete network
        """
        self.retract_wme(wme)
        self._alpha_root.add_wme(wme)
        return self

    def retract_wme(self, wme):
        """Retract a WME from the network

        Retracting a WME from the system will remove the WME from all memory nodes
        
        Returns:
            a reference to the rete network
        """
        for node in self._wmes.pop((wme.id, wme.attr), ()):
            node.retract_wme(wme)
        return self

    def production(self, *conds, production):
        """Adds a production consisting of a set of tests with a corresponding action

        Args:
            conds: n number of RETE_TEST instances describing the tests run
            production: a callback taking two arguments, net and token.
                - net is the Rete instance
                - token: is a list of matched wmes
        Returns:
            a reference to the rete network
        """
        bmemory = None
        for test in conds:
            amemory = self._alpha_root.add_test(test).add_memory()
            bmemory = self._create_beta_node(
                parent=bmemory,
                alpha_memory=amemory,
                production=production if test == conds[-1] else None)
        return self
    
    def fire(self):
        """Runs all actions associated with triggered productions
        
        Returns:
            a reference to the rete network
        """
        fire_prod = []
        for node in self._prod_memory.values():
            fire_prod.extend(node.tokens.values())
            node.tokens.clear()

        for prod in fire_prod:
            prod()
        return self


class Fact:
    def __init__(self, id, attr, value):
        self.id = id
        self.attr = attr
        self.value = value

    def __repr__(self):
        return self.__str__()

    def __json__(self):
        return self.__str__()

    def __str__(self):
        return "{}({}, {}, {})".format(self.__class__.__name__, self.id, self.attr, self.value)

class Test:
    def __init__(self, *args):
        if len(args) == 3:
            self.id, self.attr, self.target = args
            self.operand = "=="
        elif len(args) == 4:
            self.id, self.attr, self.operand, self.target = args

    def __eq__(self, other):
        return (self.id == other.id
                and self.attr == other.attr
                and self.operand == other.operand
                and self.target == other.target)

    def __json__(self):
        return self.__str__()

    def __repr__(self):
        return "{}({}, {}, {}, {})".format(self.__class__.__name__, self.id, self.attr, self.operand, self.target)

    def __str__(self):
        return "{}({}, {}, {}, {})".format(self.__class__.__name__, self.id, self.attr, self.operand, self.target)

class Var:
    def __init__(self, identity, bound=None):
        self.identity = identity
        self.bound = bound

    def __repr__(self):
        return "{}({}, {})".format(self.__class__.__name__, self.identity, self.bound)

    def __str__(self):
        return "Var(id={}, bound={})".format(self.identity, self.bound)
    
    def __eq__(self, other):
        return self.bound == other.bound


def debug_production(net: Rete, token: [Fact]):
    print(", ".join(["{0.id} {0.attr} {0.value}".format(fact) for fact in token]))

if __name__ == "__main__":

    net = Rete()
    net.production(
            Test("author", "wrote", Var("book")),
            Test("book", "is-written-by", Var("author")),
            Test("author", "is-gender", "male"),
            Test("book", "is-genre", "fantasy"),
            production=debug_production)

    net.production(
            Test("author", "is", Var("author")),
            Test("book", "is-written-by", Var("author")),
            production=debug_production)

    net.production(
            Test("book", "is-written-by", Var("auth")),
            Test("auth", "is-gender", "male"),
            production=debug_production)

    net.production(
            Test("book", "is-written-by", Var("auth")),
            Test("auth", "is-gender", "female"),
            production=debug_production)


    net.add_wme(Fact("Tolkien", "is-gender", "male"))
    net.add_wme(Fact("The hobbit", "is-written-by", "Tolkien"))
    net.add_wme(Fact("Harry Potter", "is-written-by", "Rowling"))
    net.add_wme(Fact("Rowling", "is-gender", "female"))
    net.add_wme(Fact("Rowling", "is", "Rowling"))
    net.add_wme(Fact("The hobbit", "is-genre", "fantasy"))
    net.add_wme(Fact("Harry Potter", "is-genre", "fantasy"))
    net.add_wme(Fact("Rowling", "wrote", "Harry Potter"))
    net.add_wme(Fact("Tolkien", "wrote", "The hobbit"))
    net.fire()

