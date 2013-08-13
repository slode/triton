#-------------------------------------------------------------------------------
# Name:        Entity
# Purpose:
#
# Author:      Stian Lode
#
# Created:     29.08.2012
# Copyright:   (c) Stian Lode 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
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