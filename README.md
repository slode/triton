# Triton

Triton is a library for creating small two dimensional contraptions made from
rigid bodies, spring-damper links and duct tape.

The examples require pygame to be installed.

## Usage

```python
sphere = Sphere(
    mass = 10.0,
    radius = 10.0,
    pos = Vector2d(10.0, 10.0),
    vel = Vector2d(2.0, 2.0),
    damping = 0.99,
    elasticity = 0.97)

sphere.collides_with(other_sphere)
sphere.resolve_collision(other_sphere)

# Applies force to the center-of-mass
sphere.apply_force(sphere.pos, Vector2d(1.0, 1.0))
sphere.apply_force_to_com(Vector2d(1.0, 1.0))

# Updates the state of the object based on external forces and state
sphere.update(t, dt)

```

