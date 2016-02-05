import bpy

from math import pi

from mathutils import Matrix

from .exceptions import *


def get_angle_distance(origin, a, b):
    """
    calculates the angle and distance
    between the vertices and the origin
    """
    v1 = a - origin
    v2 = b - origin

    angle = v1.angle(v2)
    dist_a = v1.length
    dist_b = v2.length

    return angle, dist_a, dist_b


def sort_vertices(a, b, c, width, height):
    """
    sort the vertices in origin, horizontal, vertical
    """
    data = []
    data.append((a, get_angle_distance(a, b, c)))
    data.append((b, get_angle_distance(b, a, c)))
    data.append((c, get_angle_distance(c, a, b)))

    angle = -1
    origin = None
    d1 = None
    d2 = None

    for key, (value, foo, bar) in data:
        if value > angle:
            angle = value
            origin = key
            d1 = foo
            d2 = bar

    v1, v2 = [v for v in (a, b, c) if v != origin]

    if height > width:
        if d1 > d2:
            vertical = v1
            horizontal = v2
        else:
            vertical = v2
            horizontal = v1
    else:
        if d1 > d2:
            vertical = v2
            horizontal = v1
        else:
            vertical = v1
            horizontal = v2

    return origin, horizontal, vertical


def natural_orientation(ob, verts, width, height):
    """
    rotate the object based on the selected vertices
    so that they are aligned vertically and horizontally
    """
    assert(len(verts) == 3)

    matrix_world = ob.matrix_world
    v = []
    for vert in verts:
        v.append((matrix_world * vert))

    origin, horizontal, vertical = sort_vertices(v[0], v[1], v[2], width, height)

    scale_vertical = (vertical - origin).length / height
    scale_horizontal = (horizontal - origin).length / width

    scale = (scale_vertical + scale_horizontal) * 0.5

    # rotate the object
    x = (horizontal - origin).normalized()
    y = (vertical - origin).normalized()

    matrix = Matrix().to_3x3()
    matrix[2] = y
    matrix[1] = y.cross(x)
    matrix[0] = matrix[1].cross(y)

    ob.matrix_world = matrix.to_4x4() * matrix_world

    # scale the object
    ob.scale /= scale

    # calculate the errors
    error_scale = scale_vertical - scale_horizontal
    error_angle = x.angle(y) - (pi * 0.5)

    return error_scale, error_angle
