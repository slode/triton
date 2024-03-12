from triton.behavior.behavior_tree import *

from random import random


class MoveToDestination(Node):
    def start(self, bb):
        bb.setdefault("distance", 5)

    def update(self, bb):
        if bb["distance"] > 0:
            bb["distance"] -= 1
            print("Moving to destination")
            return Status.Running
        else:
            print("Reached destination")
            return Status.Success


class SearchForTarget(Node):
    def update(self, bb):
        if random() > 0.8:
            print("Target found")
            return Status.Success
        else:
            print("Target not found")
            return Status.Failed


class AttackTarget(Node):
    def update(self, bb):
        if random() > 0.9:
            print("Target died")
            return Status.Success
        else:
            print("Attacking target")
            return Status.Running


class TestHealth(Node):
    def update(self, bb):
        if random() > 0.5:
            print("Low health")
            return Status.Failed
        else:
            return Status.Running


class HasItem(Node):
    def update(self, bb):
        if random() > 0.5:
            print("No healing potion")
            return Status.Success

        print("Has healing")
        return Status.Failed


class DrinkHealing(Node):
    def update(self, bb):
        print("Healed")
        return Status.Success


if __name__ == "__main__":
    p = Parallel()
    p.add(
        Selector(children=[TestHealth(), HasItem(), DrinkHealing()]),
        Sequence(children=[SearchForTarget(), MoveToDestination(), AttackTarget()]),
    )

    bb = {}
    print("TICK")
    from time import sleep

    while p.tick(bb) != Status.Success:
        continue
        sleep(0.5)
