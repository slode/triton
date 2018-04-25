from action import *

if __name__ == "__main__":

# Pipe-handler
    class PHPickPipeFromPipeDeck(Action):
        preconditions = {"ph-has-pipe": False, "pd-has-pipe": True }
        effects = {"ph-has-pipe": True, "pd-has-pipe": False}

    class PHPickPipeFromPipeMagazine(Action):
        preconditions = {"ph-has-pipe": False, "pm-has-pipe": True }
        effects = {"ph-has-pipe": True, "pm-has-pipe": False}

    class PHStabPipeInStickupWithSpinIn(Action):
        preconditions = {"ph-has-pipe": True, "wc-has-stickup": True}
        effects = {"wc-has-pipe": True}

    class PHStabPipeInEmptyWC(Action):
        preconditions = {"ph-has-pipe": True, "wc-has-stickup": False, "wc-has-pipe": False}
        effects = {"wc-has-pipe": True, "wc-has-stickup": False}

    class PHPickPipeInStickupWithSpinOut(Action):
        preconditions = {"wc-has-pipe": True, "wc-has-stickup": False}
        effects = {"ph-has-pipe": True, "wc-has-pipe": False}

    class PHPipeToPipeMagazine(Action):
        preconditions = {"ph-has-pipe": True, "pm-has-pipe": False, "el-connected": False}
        effects = {"ph-has-pipe": False, "pm-has-pipe": True}

    class PHDisconnectToEl(Action):
        preconditions = {"ph-has-pipe": True, "el-connected": True}
        effects = {"ph-has-pipe": False}

    class PHDisconnectToSlips(Action):
        preconditions = {"ph-has-pipe": True, "slips-connected": True}
        effects = {"ph-has-pipe": False}

#Slips
    class SlipsConnect(Action):
        preconditions = {"slips-connected": False}
        effects = {"slips-connected": True}

    class SlipsDisconnect(Action):
        preconditions = {"el-connected": True, "slips-connected": True}
        effects = {"slips-connected": False}

# Elevator
    class ELConnectPipe(Action):
        preconditions = {"wc-has-pipe": True, "el-connected": False}
        effects = {"el-connected": True}

    class ELConnectStickup(Action):
        preconditions = {"wc-has-stickup": True, "el-connected": False}
        effects = {"el-connected": True}

    class ELDisconnectToPH(Action):
        preconditions = {"el-connected": True, "ph-connected": True}
        effects = {"el-connected": False}

    class ELDisconnectToSlips(Action):
        preconditions = {"el-connected": True, "slips-connected": True}
        effects = {"el-connected": False}

    class ELLower(Action):
        preconditions = {"wc-has-pipe": True, "el-connected": True, "ph-has-pipe": False, "slips-connected": False}
        effects = {"wc-has-stickup": True, "wc-has-pipe": False, "tripped-in": True}

    class ELLift(Action):
        preconditions = {"tripped-in": True, "tripped-out": False, "wc-has-pipe": False, "el-connected": True, "ph-has-pipe": False, "slips-connected": False}
        effects = {"wc-has-stickup": False, "wc-has-pipe": True, "tripped-out": True}

# Misc
    class PDLoadPipe(Action):
        preconditions = {"pd-has-pipe": False}
        effects = {"pd-has-pipe": True}

    class RigDirector(Agent):
        def init(self):
            self.state = {
                    "ph-connected": False,
                    "el-connected": False,
                    "slips-connected": False,
                    "ph-has-pipe": False,
                    "pd-has-pipe": False,
                    "pm-has-pipe": False,
                    "wc-has-stickup": False,
                    "wc-has-pipe": False,
                    }
            self.actions.append(PHPickPipeFromPipeDeck)
            self.actions.append(PHPickPipeFromPipeMagazine)
            self.actions.append(PHStabPipeInStickupWithSpinIn)
            self.actions.append(PHStabPipeInEmptyWC)
            self.actions.append(PHPipeToPipeMagazine)
            self.actions.append(PHPickPipeInStickupWithSpinOut)
            self.actions.append(PHDisconnectToEl)
            self.actions.append(PHDisconnectToSlips)
            self.actions.append(SlipsConnect)
            self.actions.append(SlipsDisconnect)
            self.actions.append(ELConnectPipe)
            self.actions.append(ELConnectStickup)
            self.actions.append(ELDisconnectToPH)
            self.actions.append(ELDisconnectToSlips)
            self.actions.append(ELLower)
            self.actions.append(ELLift)
            self.actions.append(PDLoadPipe)

    import cmd
    class RigShell(cmd.Cmd):
        intro = "Rig action planner"
        prompt = "rap>"
        completekey = None

        def do_run_in_hole(self, arg):
            self.agent.state["tripped-in"] = False
            self.agent.set_goal(Goal({
                "tripped-in": True,
                "el-connected": False}))
            self._eval()

        def do_pull_out_of_hole(self, arg):
            self.agent.state["tripped-out"] = False
            self.agent.set_goal(Goal({
                "tripped-out": True,
                "el-connected": False}))
            self._eval()

        def do_clear_well_center(self, arg):
            self.agent.set_goal(Goal({
                "el-connected": False,
                }))
            self._eval()

        def do_load_pipe_deck(self, arg):
            self.agent.set_goal(Goal({
                "pd-has-pipe": True,
                }))
            self._eval()
        
        def do_load_pipe_magazine(self, arg):
            self.agent.set_goal(Goal({
                "pm-has-pipe": True,
                }))
            self._eval()

        def do_state(self, arg):
            print(self.agent.state)

        def do_goals(self, arg):
            print(self.agent.goals)

        def _eval(self):
            while self.agent.verify_goals() == False:
                action = goal_planner(self.agent)
                if action is None:
                    print("No plan found")
                    self.agent.goals = []

                self.agent.do_action(action)

    shell = RigShell()
    shell.agent = RigDirector()
    shell.cmdloop()

