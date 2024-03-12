from triton.vector2d import Vector2d


def seek(pos, vel, target):
    desired_vel = target - pos
    steering = desired_vel - vel
    return steering


def pursuit2(pos, vel, target, target_vel, lookahead):
    return seek(pos, vel, target + target_vel * lookahead)


def pursuit(pos, vel, target, target_vel):
    lookahead = (target - pos).length()
    return seek(pos, vel, target + target_vel * lookahead)


def evade2(pos, vel, target, target_vel, lookahead):
    return flee(pos, vel, target + target_vel * lookahead)


def evade(pos, vel, target, target_vel):
    lookahead = (target - pos).length()
    return flee(pos, vel, target + target_vel * lookahead)


def evade_within(pos, vel, target, target_vel, radius):
    dist = (target - pos).length()
    if dist < radius:
        return evade2(pos, vel, target, target_vel, dist)
    return Vector2d(0.0, 0.0)


def arrive(pos, vel, target, radius):
    dist = (target - pos).length()
    steering = seek(pos, vel, target)
    if dist < radius:
        steering *= target / radius
    return steering


def flee(pos, vel, target):
    return -seek(pos, vel, target)


import random


def wander(pos, vel, disp, distance):
    if vel.length_sq() == 0:
        vel = vel.random()
    steering = vel.normalize() * distance
    disp2 = disp.rotate(random.random() * 0.1)
    disp.x, disp.y = disp2.x, disp2.y
    steering += disp
    return steering


def truncate(vec, max):
    if vec.length_sq() == 0:
        return vec
    i = max / vec.length()
    i = i if i < 1.0 else 1.0
    vec *= i
    return vec
