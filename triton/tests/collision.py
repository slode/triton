import unittest, math
from triton.vector import Vector
from triton.vector2d import Vector2d
from triton.shape import Sphere, Rectangle

class Test2dShapeCollision(unittest.TestCase):

    def test_sphere_direct_hit(self):
        sphere1 = Sphere(
            mass = 1,
            radius = 10,
            pos = Vector2d(10,10),
            vel = Vector2d(0,10),
            damping = 0.,
            elasticity = 1.0
            )
        sphere2 = Sphere(
            mass = 1,
            radius = 10,
            pos = Vector2d(10,30),
            vel = Vector2d(0,-10),
            damping = 0.,
            elasticity = 1.0
            )
        collides = sphere1.collides_with(sphere2)
        self.assertEqual(sphere1.pos, (10,10), "First check")
        self.assertTrue(collides)
        self.assertEqual(sphere1.dtheta, 0, "First dtheta")
        sphere1.resolve_collision(sphere2)
        self.assertEqual(sphere1.dtheta, 0)
        self.assertEqual(sphere1.pos, (10,10))
        self.assertEqual(sphere1.vel, (0,-10))

    def test_sphere_gracing_hit(self):
        sphere1 = Sphere(
            mass = 1,
            radius = 10,
            pos = Vector2d(10,10),
            vel = Vector2d(10,0),
            damping = 0.,
            elasticity = 1.0
            )
        sphere2 = Sphere(
            mass = 1,
            radius = 10,
            pos = Vector2d(10,30),
            vel = Vector2d(0, 0),
            damping = 0.,
            elasticity = 1.0
            )
        collides = sphere1.collides_with(sphere2)
        self.assertEqual(sphere1.pos, (10,10), "First check")
        self.assertTrue(collides)
        sphere1.resolve_collision(sphere2)
        self.assertEqual(sphere1.dtheta, 0)
        self.assertEqual(sphere2.dtheta, 0)
        self.assertEqual(sphere1.pos, (10,10))
        self.assertEqual(sphere1.vel, (10, 0))

    def test_sphere_slight_hit(self):
        sphere1 = Sphere(
            mass = 1,
            radius = 10,
            pos = Vector2d(10,10),
            vel = Vector2d(10,10),
            damping = 0.,
            elasticity = 1.0
            )
        sphere2 = Sphere(
            mass = 1,
            radius = 10,
            pos = Vector2d(10,30),
            vel = Vector2d(0, 0),
            damping = 0.,
            elasticity = 1.0
            )
        collides = sphere1.collides_with(sphere2)
        self.assertEqual(sphere1.pos, (10,10), "First check")
        self.assertTrue(collides)
        sphere1.resolve_collision(sphere2)
        self.assertEqual(sphere1.dtheta, 0)
        self.assertEqual(sphere2.dtheta, 0)
        self.assertEqual(sphere1.pos, (10,10))
        self.assertEqual(sphere1.vel, (10, 0))
        self.assertEqual(sphere2.vel, (0, 10))

    def test_rect_slight_hit(self):
        rect1 = Rectangle(
            mass = 1,
            dimensions = Vector2d(100, 20),
            pos = Vector2d(50,10),
            vel = Vector2d(0,0),
            theta = 0
            )

        sphere1 = Sphere(
            mass = 1,
            radius = 10,
            pos = Vector2d(10,30),
            vel = Vector2d(0,0),
            )

        collides = rect1.collides_with(sphere1)
        self.assertTrue(collides)
        rect1.resolve_collision(sphere1)

if __name__ == '__main__':
    unittest.main()
