# SPDX-License-Identifier: LGPL-2.1-or-later
"""Rigid movement in the immediate parent's coordinates; no document writes."""
import math
import FreeCAD as App


def direction(vector):
    vector = App.Vector(vector)
    if not all(math.isfinite(v) for v in vector) or vector.Length < 1e-9:
        raise ValueError('Choose a nonzero finite direction')
    return vector.normalize()


def translation(vector, distance):
    if not math.isfinite(distance):
        raise ValueError('Enter a finite distance')
    return App.Placement(direction(vector) * distance, App.Rotation())


def rotation(point, vector, angle):
    if not math.isfinite(angle):
        raise ValueError('Enter a finite angle')
    rotate = App.Rotation(direction(vector), angle)
    return App.Placement(point - rotate.multVec(point), rotate)


def align_axes(source, target, parallel=False, reverse=False):
    origin, axis = source
    destination, target_axis = target
    rotate = App.Rotation(direction(axis), direction(target_axis) * (-1 if reverse else 1))
    # Coincidence has one unconstrained axial translation. Use the closest point
    # to avoid an arbitrary slide along the target axis.
    target_direction = direction(target_axis)
    closest = destination + target_direction * (origin - destination).dot(target_direction)
    return App.Placement((origin if parallel else closest) - rotate.multVec(origin), rotate)


def frame(origin, z_axis, x_axis):
    z = direction(z_axis)
    x = direction(x_axis)
    x -= z * x.dot(z)
    if x.Length < 1e-8:
        raise ValueError('Frame X and Z axes must not be parallel')
    x.normalize()
    return App.Placement(origin, App.Rotation(x, z.cross(x), z, 'ZXY'))


def align_frames(source, target):
    return target.multiply(source.inverse())
