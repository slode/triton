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

from triton.rete import Rete, Cond, Fact, debug_production


net = Rete()
net.production(
    Cond("x", "color", "==", "WHITE"), Cond("x", "count", "<", 5), production=debug_production
)
net.production(Cond("x", "count", "<", 3), production=debug_production)
net.production(
    Cond("x", "color", "==", "GREEN"),
    Cond("x", "size", "==", "LARGE"),
    Cond("x", "count", ">=", 2),
    production=debug_production,
)

net.add_wme(Fact("x", "color", "WHITE")).fire()
net.add_wme(Fact("x", "size", "SMALL")).fire()
net.add_wme(Fact("y", "size", "LARGE")).fire()
net.add_wme(Fact("y", "color", "GREEN")).fire()
net.add_wme(Fact("y", "size", "SMALL")).fire()
net.add_wme(Fact("x", "count", 2)).fire()
net.add_wme(Fact("z", "color", "GREEN")).fire()
net.add_wme(Fact("z", "size", "LARGE")).fire()
net.add_wme(Fact("y", "size", "LARGE")).fire()
net.add_wme(Fact("x", "color", "WHITE")).fire()
net.add_wme(Fact("x", "count", 4)).fire()
net.add_wme(Fact("x", "count", 3)).fire()
net.add_wme(Fact("y", "count", 2)).fire()
