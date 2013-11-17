
class SpringDamperLink(object):
    """A link between two rigid bodies.

    The link applies the classical spring-damper second degree differential
    equation to the link.
    """
    def __init__(self, rb1, rb2, damping=0.3, spring=3.0, length=50):
        self._rb1 = rb1
        self._rb2 = rb2
        self._damping = damping
        self._spring = spring
        self._length = length

    def resolve(self):
        x = self._rb1.pos - self._rb2.pos
        dx = self._rb1.vel - self._rb2.vel
        if x.length() == 0.0:
            return
        n = x.unit_vector()
        f = self._spring * (self._length - x.length()) - self._damping * dx.dot(n)
        self._rb1.apply_force_to_com(n * f)
        self._rb2.apply_force_to_com(n * -f)


