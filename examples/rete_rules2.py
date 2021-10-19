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
 
from triton.rete import Rete, Cond, Fact, Var, debug_production

net = Rete()
p1 = net.production(
        Cond("x", "left-of", Var("y")),
        Cond("y", "color",  "red"),
        Cond("x", "color",  "blue"),
        production=debug_production)

p2 = net.production(
        Cond("x", "left-of", Var("y")),
        Cond("y", "color",  "blue"),
        production=debug_production)

p3 = net.production(
        Cond("x", "left-of", Var("y")),
        Cond("x", "color",  "orange"),
        Cond("y", "color",  "in", ("red", "blue")),
        production=debug_production)

net.add_wme(Fact("a", "left-of", "b"))
net.add_wme(Fact("b", "color", "red"))
net.add_wme(Fact("b", "color", "blue"))
net.fire()
print("...")
net.add_wme(Fact("a", "color", "orange"))
net.fire()
print("...")
net.add_wme(Fact("b", "color", "red"))
net.fire()
print("...")
