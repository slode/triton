
class Event(object):
    pass

class Component(object):
    pass

class System(object):
    def __init__(self):
        self.registry = None
        self.listeners = {}
        self.events = []

    def initialize(self):
        raise NotImplementedError(self.__class__)

    def on(self, event, callback):
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(callback)

    def _receive(self, etype, einstance):
        if etype not in self.listeners:
            return
        self.events.append((etype, einstance))

    def emit(self, einstance):
        self.registry._propagate_event(einstance)
        
    def _update(self):
        event_queue = self.events
        self.events = []
        for etype, einst in event_queue:
            for listener in self.listeners[etype]:
                listener(einst)

class Registry:
    def __init__(self):
        self._entities = {}
        self._components = {}
        self._entity_id = 0
        self._systems = []

    def _propagate_event(self, einstance):
        etype = type(einstance)
        for system in self._systems:
            system._receive(etype, einstance)

    def add_system(self, system):
        system.registry = self
        self._systems.append(system)
        system.initialize()

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

    def remove_entities(self, entities):
        for entity in entities:
            self.remove_entity(entity)

    def remove_entity(self, entity):
        comps = list(self._entities[entity].values())
        [self.remove_component(entity, comp) for comp in comps]
        self._entities.pop(entity)

    def remove_component(self, entity, component):
        comp_type = type(component)
        self._entities[entity].pop(comp_type)
        self._components[comp_type].remove(entity)

    def get_components(self, *types):
        comps = self._components
        ents = self._entities
        for ent in self.get_entities(*types):
            yield ent, self.get_entity(ent, *types)

    def get_entities(self, *types):
        comps = self._components
        ents = self._entities
        try:
            return set.intersection(*[comps[t] for t in types])
        except KeyError:
            return set()

    def get_entity(self, entity, *types):
        ents = self._entities
        return [ents[entity][t] for t in types]

    def update(self):
        for system in self._systems:
            system._update()

