from ..built_in.point import Point
from ..built_in.line_base import LineBase
from ..built_in.surface_base import SurfaceBase

from . import sets


class Base(object):

    """
    Base class for the creation of size fields.
    """

    _ID = 0

    def __init__(self, field_type=""):
        self.id = Base._ID
        Base._ID += 1

        self.field_type = field_type
        self._code = ["Field[{}] = {};".format(self.id, self.field_type)]

    @property
    def code(self):
        return "\n".join(self._code)


class Distance(Base):
    def __init__(self, *, objects=None, n_nodes_by_edge=20):
        super(Distance, self).__init__(field_type="Distance")

        points = list(filter(lambda element: isinstance(element, Point), objects))
        point_sets = list(filter(lambda element: isinstance(element, sets.PointSet), objects))
        lines = list(filter(lambda element: isinstance(element, LineBase), objects))
        line_sets = list(filter(lambda element: isinstance(element, sets.LineSet), objects))
        surfaces = list(filter(lambda element: isinstance(element, SurfaceBase), objects))
        surfaces_sets = list(filter(lambda element: isinstance(element, sets.SurfaceSet), objects))

        nodes = sets.PointSet([*points, *point_sets])
        edges = sets.LineSet([*lines, *line_sets])
        faces = sets.SurfaceSet([*surfaces, *surfaces_sets])

        if not nodes.empty():
            self._code.append("Field[{id}].NodesList = {{{nodes}}};".format(id=self.id, nodes=nodes.code))
        if not edges.empty():
            self._code.append("Field[{id}].EdgesList = {{{edges}}};".format(id=self.id, edges=edges.code))
        if not faces.empty():
            self._code.append("Field[{id}].FacesList = {{{faces}}};".format(id=self.id, faces=faces.code))
        self._code.append("Field[{id}].NNodesByEdge = {nnodes};".format(id=self.id, nnodes=n_nodes_by_edge))


class MathEval(Base):
    def __init__(self, *, expression, fields=[]):
        super(MathEval, self).__init__(field_type="MathEval")
        self.expression = expression.format(*["F" + str(field.id) for field in fields])
        print(expression)
        self._code.append("Field[{}].F = \"{}\";".format(self.id, self.expression))


class Min(Base):
    def __init__(self, *, fields):
        super(Min, self).__init__(field_type="Min")
        assert False not in [isinstance(field, Base) for field in fields]

        self._code.append("Field[{}].FieldsList = {{{}}};".format(self.id, ", ".join([str(field.id) for field in fields])))


class Max(Base):
    def __init__(self, *, fields):
        super(Max, self).__init__(field_type="Max")
        assert False not in [isinstance(field, Base) for field in fields]

        self._code.append("Field[{}].FieldsList = {{{}}};".format(self.id, ", ".join([str(field.id) for field in fields])))