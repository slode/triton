import math

from triton.vector2d import Vector2d

def bounding_box(polygon):
    p1 = polygon[0]
    x_min = p1.x
    x_max = p1.x
    y_min = p1.y
    y_max = p1.y

    for p in polygon[1:]:
        if p.x < x_min:
            x_min = p.x
        elif p.x > x_max:
            x_max = p.x
        if p.y < y_min:
            y_min = p.y
        elif p.y > y_max:
            y_max = p.y
    return (x_min, x_max, y_min, y_max)

def point_outside_box(point, box):
    if (box[0] > point.x or box[1] < point.x
        or box[2] > point.y or box[3] < point.y):
        return True
    return False

def point_in_polygon(point, polygon):
    bb = bounding_box(polygon)
    # fail-fast check
    if point_outside_box(point, bb):
        return False


    

def main():
    polygon = []
    polygon.append(Vector2d(0.0, 0.0))
    polygon.append(Vector2d(10.0, 0.0))
    polygon.append(Vector2d(20.0, 10.0))
    polygon.append(Vector2d(10.0, 10.0))
    polygon.append(Vector2d(0.0, 10.0))

    point_inside = Vector2d(10.0, 10.0)
    point_outside = Vector2d(30.0, 10.0)

    assert not point_outside_box(point_inside, bounding_box(polygon))
    assert point_outside_box(point_outside, bounding_box(polygon))



if __name__ == '__main__':
    main()

