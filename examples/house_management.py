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
 
from triton.rete import Rete, test, wme, debug_production

def print_status(wme):
    print("The {0.attr} in the {0.id} is {0.value}".format(wme))

def enable_heater(house, token):
    fact = next(filter(lambda x: x.attr=="temperature", token))
    house.add_wme(wme(fact.id, "heater", True))

def disable_heater(house, token):
    fact = next(filter(lambda x: x.attr=="temperature", token))
    house.add_wme(wme(fact.id, "heater", False))

def adjust_temperature(house, token):
    """Simulates natural temperature fluctuations with and without heater"""
    debug_production(house, token)
    heater = next(filter(lambda x: x.attr=="heater", token))
    temp = next(filter(lambda x: x.attr=="temperature", token))
    new_temp = temp.value + 1 if heater.value else temp.value - 1
    house.add_wme(wme(heater.id, "temperature", new_temp))

house_rules = Rete()
house_rules.production(
        test("temperature", "!=", None),
        test("heater", "!=", None),
        production=adjust_temperature)

house_rules.production(
        test("temperature", "<", 20),
        test("heater", "!=", True),
        production=enable_heater)

house_rules.production(
        test("temperature", ">", 25),
        test("heater", "==", True),
        production=disable_heater)



house_rules.add_wme(wme("kitchen", "heater", False))
house_rules.add_wme(wme("kitchen", "temperature", 14))

house_rules.add_wme(wme("bedroom", "heater", False))
house_rules.add_wme(wme("bedroom", "temperature", 25))

house_rules.add_wme(wme("tv-room", "heater", False))
house_rules.add_wme(wme("tv-room", "temperature", 22))

# example of network self-change
for i in range(8):
    house_rules.fire()
    print("...")

