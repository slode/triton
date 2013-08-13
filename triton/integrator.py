#-------------------------------------------------------------------------------
# Name:        Integrator
# Purpose:
#
# Author:      Stian Lode
#
# Created:     02.09.2012
# Copyright:   (c) Stian Lode 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class Integrator:

    @classmethod
    def rk4(self, t, dt, x, f):
        k1 = dt * f(t, x)
        k2 = dt * f(t + 0.5*dt, x + 0.5*k1)
        k3 = dt * f(t + 0.5*dt, x + 0.5*k2)
        k4 = dt * f(t + dt, x + k3)
        return t + dt, x + (k1 + 2*(k2 + k3) + k4)/6.0



def main():
    from vector2d import Vector2d

    def f(t, x):
        return Vector2d( -1.9 * x[0] - 1.7* x[1], x[0])

    t = 0
    dt = 0.05
    x = Vector2d(20,10)
    data1 = []
    data2 = []
    for i in range(300):
        t, x = Integrator.rk4(t, dt, x, f)
        # vel
        data1.append((t, x[0]))
        #pos
        data2.append((t, x[1]))

    from pylab import plot, show, legend
    p1, = plot([i for i,j in data1], [j for i,j in data1], 'k--')
    p2, = plot([i for i,j in data2], [j for i,j in data2], 'k-')
    legend([p1, p2], ["Velocity", "Position"])
    show()

if __name__ == '__main__':
    main()