# Copyright (c) 2013 Stian Lode
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

import fixtures
from triton.rete import Rete, Fact, Cond, Var


class CalledProd:
    def __init__(self):
        self._times_called = 0

    def __call__(self, net, token):
        self._times_called += 1

    def count(self):
        return self._times_called


def test_single_cond():
    callback = CalledProd()
    net = Rete()
    net.production(Cond("x", "length", ">", 1), production=callback)
    net.add_wme(Fact("a", "length", 2)).fire()
    assert callback.count() == 1
    net.add_wme(Fact("a", "length", 4)).fire()
    assert callback.count() == 2
    net.add_wme(Fact("a", "length", 1)).fire()
    assert callback.count() == 2


def test_double_cond():
    callback = CalledProd()
    net = Rete()
    net.production(Cond("x", "length", ">", 1), Cond("x", "weight", ">", 10), production=callback)

    net.add_wme(Fact("a", "length", 2)).fire()
    assert callback.count() == 0
    net.add_wme(Fact("a", "weight", 11)).fire()
    assert callback.count() == 1
    net.add_wme(Fact("a", "length", 1)).fire()
    assert callback.count() == 1
    net.add_wme(Fact("a", "length", 2)).fire()
    assert callback.count() == 2


def test_joined_cond():
    callback = CalledProd()
    net = Rete()
    net.production(
        Cond("x", "on-top-of", Var("y")), Cond("y", "weight", ">", 10), production=callback
    )

    net.add_wme(Fact("a", "on-top-of", "b")).fire()
    assert callback.count() == 0

    net.add_wme(Fact("a", "weight", 11)).fire()
    assert callback.count() == 0

    net.add_wme(Fact("b", "weight", 11)).fire()
    assert callback.count() == 1

    net.add_wme(Fact("b", "on-top-of", "a")).fire()
    assert callback.count() == 2


def test_secondary_joined_cond():
    callback = CalledProd()
    net = Rete()
    net.production(
        Cond("x", "on-top-of", Var("y")),
        Cond("y", "left-of", Var("z")),
        Cond("z", "length", 3),
        production=callback,
    )

    net.add_wme(Fact("a", "on-top-of", "b")).fire()
    assert callback.count() == 0

    net.add_wme(Fact("b", "left-of", "c")).fire()
    assert callback.count() == 0

    net.add_wme(Fact("c", "length", 3)).fire()
    assert callback.count() == 1


def test_duplicated_rule_join():
    callback = CalledProd()
    net = Rete()
    net.production(
        Cond("x", "on-top-of", Var("y")),
        Cond("y", "on-top-of", Var("z")),
        Cond("z", "count", ">", 2),
        production=callback,
    )

    net.add_wme(Fact("a", "on-top-of", "b")).fire()
    net.add_wme(Fact("b", "on-top-of", "c")).fire()
    net.add_wme(Fact("c", "count", 1)).fire()
    assert callback.count() == 0

    net.add_wme(Fact("c", "count", 3)).fire()
    assert callback.count() == 1


def test_duplicate_production():
    callback = CalledProd()
    net = Rete()
    net.production(Cond("z", "count", ">", 0), production=callback)
    net.production(Cond("z", "count", ">", 0), production=callback)

    net.add_wme(Fact("c", "count", 3)).fire()
    assert callback.count() == 2


def test_self_referential_production():
    def set_count_to_4(net, token):
        net.add_wme(Fact("c", "count", 4))

    callback = CalledProd()
    net = Rete()
    net.production(Cond("z", "count", ">", 0), production=callback)
    net.production(Cond("z", "count", ">", 0), production=set_count_to_4)

    net.add_wme(Fact("c", "count", 3)).fire()
    assert callback.count() == 1

    # no check for duplicate values.
    net.fire()
    assert callback.count() == 2


def test2():
    callback1 = CalledProd()
    callback2 = CalledProd()
    callback3 = CalledProd()
    net = Rete()
    net.production(
        Cond("x", "color", "==", "WHITE"), Cond("x", "count", "<", 5), production=callback1
    )
    net.production(Cond("x", "count", "<", 3), production=callback2)
    net.production(
        Cond("x", "color", "==", "GREEN"),
        Cond("x", "size", "==", "LARGE"),
        Cond("x", "count", ">=", 2),
        production=callback3,
    )

    net.add_wme(Fact("a", "color", "WHITE")).fire()
    net.add_wme(Fact("a", "size", "SMALL")).fire()
    net.add_wme(Fact("b", "size", "LARGE")).fire()
    net.add_wme(Fact("b", "color", "GREEN")).fire()
    net.add_wme(Fact("b", "size", "SMALL")).fire()
    assert callback1.count() == 0
    assert callback2.count() == 0
    assert callback3.count() == 0
    net.add_wme(Fact("a", "count", 2)).fire()
    assert callback1.count() == 1
    assert callback2.count() == 1
    net.add_wme(Fact("c", "color", "GREEN")).fire()
    assert callback1.count() == 1
    assert callback2.count() == 1
    net.add_wme(Fact("c", "size", "LARGE")).fire()
    assert callback1.count() == 1
    net.add_wme(Fact("b", "size", "LARGE")).fire()
    net.add_wme(Fact("a", "color", "WHITE")).fire()
    assert callback1.count() == 2
    net.add_wme(Fact("a", "count", 4)).fire()
    assert callback1.count() == 3
    net.add_wme(Fact("a", "count", 3)).fire()
    assert callback1.count() == 4
    net.add_wme(Fact("b", "count", 2)).fire()
    assert callback2.count() == 2
    assert callback3.count() == 1
