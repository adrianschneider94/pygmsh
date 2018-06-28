from ..built_in.point import Point
from ..built_in.line_base import LineBase
from ..built_in.surface_base import SurfaceBase
from ..built_in.volume_base import VolumeBase


def get_prefix(geometric_entity):
    if isinstance(geometric_entity, Point):
        return "Point"
    if isinstance(geometric_entity, LineBase):
        return "Line"
    elif isinstance(geometric_entity, SurfaceBase):
        return "Surface"
    elif isinstance(geometric_entity, VolumeBase):
        return "Volume"
    else:
        raise TypeError


class Set(object):
    def __init__(self, elements):
        super(Set, self).__init__()
        self.elements = elements

    def empty(self):
        if len(self.elements) == 0:
            return True
        else:
            return False


class PointSet(Set):
    def __init__(self, elements):
        super(PointSet, self).__init__(elements)
        self.elements = elements

    @property
    def code(self):
        points = list(filter(lambda element: isinstance(element, Point), self.elements))
        point_sets = list(filter(lambda element: isinstance(element, PointSet), self.elements))
        code = list(filter(lambda element: isinstance(element, str), self.elements))

        return ", ".join([point.id for point in points] + [point_set.code for point_set in point_sets] + code)


class LineSet(Set):
    def __init__(self, elements):
        super(LineSet, self).__init__(elements)
        self.elements = elements

    @property
    def code(self):
        lines = list(filter(lambda element: isinstance(element, LineBase), self.elements))
        line_sets = list(filter(lambda element: isinstance(element, LineSet), self.elements))
        code = list(filter(lambda element: isinstance(element, str), self.elements))

        return ", ".join([line.id for line in lines] + [line_set.code for line_set in line_sets] + code)


class SurfaceSet(Set):
    def __init__(self, elements):
        super(SurfaceSet, self).__init__(elements)
        self.elements = elements

    @property
    def code(self):
        surfaces = list(filter(lambda element: isinstance(element, SurfaceBase), self.elements))
        surface_sets = list(filter(lambda element: isinstance(element, SurfaceSet), self.elements))
        code = list(filter(lambda element: isinstance(element, str), self.elements))

        return ", ".join([surface.id for surface in surfaces] + [surface_set.code for surface_set in surface_sets] + code)


def points_of(geometric_entity):
    return PointSet(["PointsOf{{{prefix}{{{id}}};}}".format(prefix=get_prefix(geometric_entity), id=geometric_entity.id)])


def boundary_of(geometric_entity):
    if isinstance(geometric_entity, Point):
        raise TypeError("Can't compute boundary of a point.")
    elif isinstance(geometric_entity, LineBase):
        return PointSet(["Boundary{{{prefix}{{{id}}};}}".format(prefix=get_prefix(geometric_entity), id=geometric_entity.id)])
    elif isinstance(geometric_entity, SurfaceBase):
        return LineSet(["Boundary{{{prefix}{{{id}}};}}".format(prefix=get_prefix(geometric_entity), id=geometric_entity.id)])
    elif isinstance(geometric_entity, VolumeBase):
        return SurfaceSet(["Boundary{{{prefix}{{{id}}};}}".format(prefix=get_prefix(geometric_entity), id=geometric_entity.id)])
    else:
        raise TypeError
