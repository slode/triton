#-------------------------------------------------------------------------------
# Name:        StateMachine
# Purpose:
#
# Author:      Stian Lode
#
# Created:     30.08.2012
# Copyright:   (c) Stian Lode 2012
# Licence:     GPL
#-------------------------------------------------------------------------------

class StateMachine:
    def __init__(self, entity):
        self._entity = entity
        self._previous_state = None
        self._active_state = None
        self._default_state = None

    def get_entity(self):
        return self._entity

    def set_entity(self, entity):
        self._entity = entity

    def set_default_state(self, state):
        self._default_state = state

    def set_state(self, state):
        if self._active_state:
            self._active_state.exit()

        self._previous_state = self._active_state
        if not state:
            state = self._default_state

        self._active_state = None
        if state:
            self._active_state = state()
            self._active_state.entity = self._entity
            self._active_state.set_state_machine(self)
            self._active_state.enter()

    def goto_previous_state(self):
        self.set_state(self._previous_state)

    def update(self):
        if self._active_state:
            self._active_state.update()

class State:
    def set_state_machine(self, state_machine):
        self._state_machine = state_machine

    @property
    def entity(self, entity):
        self._state_machine.get_entity()

    def goto(self, state):
        self._state_machine.set_state(state)

    def enter(self):
        print("entering " + self.__class__.__name__)

    def exit(self):
        print("exitting " + self.__class__.__name__)

    def update(self):
        print("updating " + self.__class__.__name__)

def main():
    class CharState(State):
        def update(self):
            if len(self.entity.string) == 0:
                return self.goto(None)

            elif self.entity.string[0:1].isdigit():
                return self.goto(NumberState)

            else:
                print(self.entity.string[0:1] + " is a character.")
                self.entity.string = self.entity.string[1:]

    class NumberState(State):
        def update(self):
            if len(self.entity.string) == 0:
                return self.goto(None)

            elif not self.entity.string[0:1].isdigit():
                return self.goto(CharState)

            else:
                print(self.entity.string[0:1] + " is a numeric.")
                self.entity.string = self.entity.string[1:]

    class entity:
        def __init__(self, str = "asdfasdfa124123asd"):
            self.string = str

    e = entity()
    my_machine = StateMachine(e)
    my_machine.set_state(CharState)

    for i in range(100):
        my_machine.update()

if __name__ == '__main__':
    main()