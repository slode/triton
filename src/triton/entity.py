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
 
 
import uuid

class EntityRegister(object):
    def __init__(self):
        self._register = {}

    def add_entity(self, entity):
        while True:
            entity_uuid = str(uuid.uuid1())
            if entity_uuid not in self._register:
                entity.uuid = entity_uuid
                print("registering entity " + entity_uuid)
                self._register[entity.uuid] = entity
                return entity_uuid

    def get_entity(self, entity_uuid):
        if entity_uuid in self._register:
            return self._register[entity_uuid]
        raise IndexError("Unable to find entity " + entity_uuid)


class Entity(object):
    def __init__(self):
        self._entity_uuid = None

    @property
    def uuid(self):
        return self._entity_uuid

    @uuid.setter
    def uuid(self, uuid):
        self._entity_uuid = uuid

def main():
    my_ent_reg = EntityRegister()
    my_uuid = my_ent_reg.add_entity(Entity())
    my_ent = my_ent_reg.get_entity(my_uuid)

    if my_uuid == my_ent.uuid:
        print('Same entity')
    else:
        print('Not same entity')

if __name__ == '__main__':
    main()
