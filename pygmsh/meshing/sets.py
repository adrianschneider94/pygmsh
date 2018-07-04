from ..built_in.point import Point
from ..built_in.line_base import LineBase
from ..built_in.surface_base import SurfaceBase
from ..built_in.volume_base import VolumeBase


class Set(object):
    def __init__(self, elements):
        super(Set, self).__init__()
        self.elements = elements

    def empty(self):
        return len(self.elements) == 0


class PointSet(Set):
    def __init__(self, elements):
        assert False not in [isinstance(x, (Point, PointSet, str)) for x in elements]
        super(PointSet, self).__init__(elements)

    @property
    def code(self):
        points = list(filter(lambda element: isinstance(element, Point), self.elements))
        point_sets = list(filter(lambda element: isinstance(element, PointSet), self.elements))
        code = list(filter(lambda element: isinstance(element, str), self.elements))

        return ", ".join(
            [point.id for point in points] + [point_set.code for point_set in point_sets] + code
        )


class LineSet(Set):
    def __init__(self, elements):
        assert False not in [isinstance(x, (LineBase, LineSet, str)) for x in elements]
        super(LineSet, self).__init__(elements)

    @property
    def code(self):
        lines = list(filter(lambda element: isinstance(element, LineBase), self.elements))
        line_sets = list(filter(lambda element: isinstance(element, LineSet), self.elements))
        code = list(filter(lambda element: isinstance(element, str), self.elements))

        return ", ".join(
            [line.id for line in lines] + [line_set.code for line_set in line_sets] + code
        )

    @property
    def as_boolean_list(self):
        return "Line{{{id_list}}};".format(id_list=self.code)


class SurfaceSet(Set):
    def __init__(self, elements):
        assert False not in [isinstance(x, (SurfaceBase, SurfaceSet, str)) for x in elements]
        super(SurfaceSet, self).__init__(elements)

    @property
    def code(self):
        surfaces = list(filter(lambda element: isinstance(element, SurfaceBase), self.elements))
        surface_sets = list(filter(lambda element: isinstance(element, SurfaceSet), self.elements))
        code = list(filter(lambda element: isinstance(element, str), self.elements))

        return ", ".join(
            [surface.id for surface in surfaces] + [surface_set.code for surface_set in surface_sets] + code
        )

    @property
    def as_boolean_list(self):
        return "Surface{{{id_list}}};".format(id_list=self.code)


class VolumeSet(Set):
    def __init__(self, elements):
        assert False not in [isinstance(x, (VolumeBase, VolumeSet, str)) for x in elements]
        super(VolumeSet, self).__init__(elements)

    @property
    def code(self):
        volumes = list(filter(lambda element: isinstance(element, VolumeBase), self.elements))
        volume_sets = list(filter(lambda element: isinstance(element, VolumeSet), self.elements))
        code = list(filter(lambda element: isinstance(element, str), self.elements))

        return ", ".join(
            [volume.id for volume in volumes] + [volume_set.code for volume_set in volume_sets] + code
        )

    @property
    def as_boolean_list(self):
        return "Volume{{{id_list}}};".format(id_list=self.code)


def points_of(geometric_entity):
    return PointSet(
        ["PointsOf{{{boolean_list}}}".format(boolean_list=geometric_entity.as_boolean_list)]
    )


def boundary_of(geometric_entity):
    if not isinstance(geometric_entity, list):
        geometric_entity = [geometric_entity]

    try:
        line_set = LineSet(geometric_entity)
        return PointSet(
            ["Boundary{{{boolean_list}}}".format(boolean_list=line_set.as_boolean_list)]
        )
    except AssertionError:
        pass

    try:
        surface_set = SurfaceSet(geometric_entity)
        return LineSet(
            ["Boundary{{{boolean_list}}}".format(boolean_list=surface_set.as_boolean_list)]
        )
    except AssertionError:
        pass

    try:
        volume_set = VolumeSet(geometric_entity)
        return SurfaceSet(
            ["Boundary{{{boolean_list}}}".format(boolean_list=volume_set.as_boolean_list)]
        )
    except AssertionError:
        pass

    if isinstance(geometric_entity, (Point, PointSet)):
        raise TypeError("Can't compute boundary of a point.")

    elif isinstance(geometric_entity, LineBase):
        return PointSet(
            ["Boundary{{{prefix}{{{id}}};}}".format(prefix=geometric_entity._NAME, id=geometric_entity.id)]
        )
    elif isinstance(geometric_entity, LineSet):
        return PointSet(
            ["Boundary{{{prefix}{{{id}}};}}".format(prefix=geometric_entity._NAME, id=geometric_entity.id)]
        )
    elif isinstance(geometric_entity, SurfaceBase):
        return LineSet(
            ["Boundary{{{prefix}{{{id}}};}}".format(prefix=geometric_entity._NAME, id=geometric_entity.id)]
        )

    elif isinstance(geometric_entity, VolumeBase):
        return SurfaceSet(
            ["Boundary{{{prefix}{{{id}}};}}".format(prefix=geometric_entity._NAME, id=geometric_entity.id)]
        )

