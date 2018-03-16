
class Action:
    preconditions = {}
    effects = {}
    cost = 1.0

    def is_done(self):
        return True

    def check_precondition(self):
        return True

    def perform_action(self, agent):
        print("Performing " + __class__ + ".")

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.__class__.__name__

class Goal:
    def __init__(self, conditions):
        self.conditions = conditions

    def get_conditions(self):
        return self.conditions


class Agent:
    def __init__(self):
        self.goals = []
        self.actions = []
        self.state = {}
        self.init()

    def get_actions(self):
        raise NotImplementedError()

    def set_goal(self, goal):
        self.goal.prepend(goal)

    def get_goal(self):
        return self.goal[0] if len(self.goal) else None

def goal_planner(agent, goal):
    actions = set(action() for action in agent.actions)
    goal_conditions = dict(goal.get_conditions())
    state = dict(agent.state)

    def validate_actions(state, actions, goal_conditions, cost=0):
        valid_actions = {}
        if set(goal_conditions.items()) <= set(state.items()):
            return cost

        for action in actions:
            # can I perform this action now
            newstate = state.copy()
            newstate.update(action.effects)
            if set(action.preconditions.items()) <= set(state.items()):
                valid_actions[action] = validate_actions(
                        newstate,
                        actions - set([action]),
                        goal_conditions,
                        cost + action.cost)

        return valid_actions

    v = validate_actions(state, actions, goal_conditions)
    import pprint
    pprint.pprint(v, width=10, depth=10)


if __name__ == "__main__":
    class StealOre(Action):
        preconditions = {}
        effects = {"hasOre": True}
        cost = 20.0

    class MineOre(Action):
        preconditions = {"hasTool": True, "hasOre": False}
        effects = {"hasOre": True}

    class SellOre(Action):
        preconditions = {"hasOre": True}
        effects = {"hasOre": False, "hasMoney": True}

    class Drink(Action):
        preconditions = {"hasMoney": True}
        effects = {"hasFun": True, "hasMoney": False}

    class Brawl(Action):
        preconditions = {"hasFun": False, "hasMoney": False}
        effects = {}
        cost = 20.0

    class BuyTool(Action):
        preconditions = {"hasTool": False, "hasMoney": True}
        effects = {"hasTool": True}

    class Dwarf(Agent):
        def init(self):
            self.state = {"hasTool": False, "hasOre": False, "hasMoney": False, "hasFun": False}
            self.actions.append(MineOre)
            self.actions.append(StealOre)
            self.actions.append(SellOre)
            self.actions.append(Drink)
            self.actions.append(BuyTool)
            self.actions.append(Brawl)

    gimli = Dwarf()
    tool_goal = Goal({"hasFun": True})
    goal_planner(gimli, tool_goal)

