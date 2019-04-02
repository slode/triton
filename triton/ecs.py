
class Component(object):
    pass

class System(object):
    def __init__(self):
        self.registry = None

    def update(self, *args, **kwargs):
        raise NotImplementedError()

class Registry:
    def __init__(self):
        self._entities = {}
        self._components = {}
        self._entity_id = 0
        self._systems = []

    def add_system(self, system):
        system.registry = self
        self._systems.append(system)

    def add_entity(self, *components):
        self._entity_id += 1
        for c in components:
            self.add_component(self._entity_id, c)
        return self._entity_id

    def add_component(self, entity, comp):
        comp_type = type(comp)
        if entity not in self._entities:
            self._entities[entity] = {}
        self._entities[entity][comp_type] = comp

        if comp_type not in self._components:
            self._components[comp_type] = set()
        self._components[comp_type].add(entity)

    def remove_component(self, entity, component):
        comp_type = type(comp)
        if comp_type in self._entities[entity]:
            del self._entities[entity][comp_type]
        self._components[comp_type].remove(entity)

    def get_components(self, *types):
        comps = self._components
        ents = self._entities
        try:
            for ent in set.intersection(*[comps[t] for t in types]):
                yield ent, [ents[ent][t] for t in types]
        except KeyError:
            pass

    def get_entity(self, entity, *types):
        ents = self._entities
        return [ents[entity][t] for t in types]

    def update(self, *args, **kwargs):
        for system in self._systems:
            system.update(*args, **kwargs)

