
class Action:
    preconditions = {}
    effects = {}
    cost = 1.0

    def __init__(self):
        self.visits = 0

    def visited(self):
        self.visits += 1
        return self.visits

    def is_done(self):
        return True

    def check_precondition(self):
        return True

    def _perform(self, agent):
        debug("Performing " + str(self) + ".")
        self.perform(agent)

    def perform(self, agent):
        pass

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.__class__.__name__

class Goal:
    def __init__(self, conditions):
        self.conditions = conditions

    def get_conditions(self):
        return self.conditions

    def __str__(self):
        return self.repr()

    def __repr__(self):
        return "Goal: "+ str(self.conditions)


class Agent:
    def __init__(self):
        self.goals = []
        self.actions = []
        self.state = {}
        self.init()

    def get_actions(self):
        raise NotImplementedError()

    def do_action(self, action):
        if action is None:
            return
        action._perform(self)
        self.state.update(action.effects)

    def set_goal(self, goal):
        self.goals.insert(0, goal)

    def get_goals(self):
        return self.goals

    def verify_goals(self):
        for g in self.goals:
            if (set(g.get_conditions().items()) <= set(self.state.items())):
                self.goals.remove(g)
        return len(self.goals) == 0

def debug(msg):
    print(msg)

def goal_planner(agent):

    def validate_actions(state, actions, goal_conditions, cost=0):

        if set(goal_conditions.items()) <= set(state.items()):
            return [cost]

        valid_actions = []

        for action in actions:
            if set(action.preconditions.items()) <= set(state.items()):
                new_state = state.copy()
                new_state.update(action.effects)

                total_cost = validate_actions(
                        new_state,
                        actions - set([action]),
                        goal_conditions,
                        cost + action.cost)

                if total_cost is not None:
                    total_cost.append(action)
                    valid_actions.append(total_cost)

        if len(valid_actions) == 0:
            return None

        valid_actions.sort(key=lambda plan: plan[0])
        return valid_actions[0]

    plans = []
    for goal in agent.goals:
        goal_conditions = dict(goal.get_conditions())
        actions = set(action() for action in agent.actions)
        state = agent.state.copy()
        v = validate_actions(state, actions, goal_conditions)

        try:
            if v is None:
                debug("No valid plan")
                continue
            if v == [0]:
                debug("Goal reached")
                continue
            plans.append(v)
        except:
            pass

    # Pick the plan that leads to goal fulfillment at least cost.
    plans.sort()
    try:
        return plans[0][-1]
    except:
        pass

if __name__ == "__main__":

    class StealOre(Action):
        preconditions = {"hasMoney": False }
        effects = {"hasOre": True, "hasFun": False}
        cost = 10.0

    class MineOre(Action):
        preconditions = {"hasTool": True, "hasOre": False}
        effects = {"hasOre": True}

        def perform(self, agent):
            if agent.state.setdefault("tool_age", 0) > 5:
                debug("Tool broken!")
                agent.state["hasTool"] = False
                agent.state["tool_age"] = 0
            agent.state["tool_age"] += 1

    class SellOre(Action):
        preconditions = {"hasOre": True}
        effects = {"hasOre": False, "hasMoney": True}

    class Drink(Action):
        preconditions = {"hasMoney": True}
        effects = {"hasFun": True, "hasMoney": False}
        cost = 2.0

    class Brawl(Action):
        preconditions = {"hasFun": False}
        effects = {"hasFun": True}
        cost = 20.0

    class BuyTool(Action):
        preconditions = {"hasTool": False, "hasMoney": True}
        effects = {"hasTool": True, "hasMoney": False}

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
    gimli.set_goal(Goal({"hasTool": True}))
    gimli.set_goal(Goal({"hasMoney": True}))
    gimli.set_goal(Goal({"hasFun": True}))
    gimli.set_goal(Goal({"hasOre": True}))

    while True:
        if gimli.verify_goals():
            print("Reached goal")
            break
        action = goal_planner(gimli)
        gimli.do_action(action)
