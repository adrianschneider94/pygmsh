from ..built_in.point import Point
from ..built_in.line_base import LineBase
from ..built_in.surface_base import SurfaceBase

from . import sets


class Base(object):
    """
    Base class for the creation of Gmsh size fields.

    Parameters
    ----------
    field_type : str
        The Gmsh identifier of the field, e.g. "Min", "Max", "Attractor", "Distance", "Threshold".
    """

    _ID = 0

    def __init__(self, *, field_type):
        assert isinstance(field_type, str)

        self.field_type = field_type
        self.id = Base._ID
        Base._ID += 1

        self._code = [
            "Field[{id}] = {field_type};".format(
                id=self.id,
                field_type=self.field_type
            )
        ]

    @property
    def code(self):
        return "\n".join(self._code)


class Distance(Base):
    """
    A Gmsh distance field. The field has the value of the shortest distance to the given objects.

    Parameters
    ----------
    objects : list
        A list which contains the objects the distance is calculated from. It may contain Points, PointSets, Lines,
        LineSets, Surfaces and SurfaceSets.
    n_nodes_by_edge : int
        The nuber of nodes, by which a curve is approximated for the distance calculation.

    Notes
    -----
    The class sorts the given objects into points (nodes), lines (edges) and surfaces (faces) and adds the corresponding
    Gmsh code.

    """

    def __init__(self, *, objects, n_nodes_by_edge=20):
        super(Distance, self).__init__(field_type="Distance")

        assert False not in [
            isinstance(x, (Point, sets.PointSet, LineBase, sets.LineSet, SurfaceBase, sets.SurfaceSet))
            for x in objects
        ]

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
            self._code.append("Field[{id}].NodesList = {{{nodes}}};".format(
                id=self.id,
                nodes=nodes.code
            ))

        if not edges.empty():
            self._code.append("Field[{id}].EdgesList = {{{edges}}};".format(
                id=self.id,
                edges=edges.code
            ))

        if not faces.empty():
            self._code.append("Field[{id}].FacesList = {{{faces}}};".format(
                id=self.id,
                faces=faces.code
            ))

        if False in (nodes.empty(), edges.empty(), faces.empty()):
            self._code.append("Field[{id}].NNodesByEdge = {nnodes};".format(
                id=self.id,
                nnodes=n_nodes_by_edge
            ))


class MathEval(Base):
    """
    A Gmsh MathEval Field.

    Parameters
    ----------
    expression : str
        The gmsh expression that is evaluated. x, y, z are the spatial variables, field can be supplied by the python
        .format syntax.
    fields
        A list, tuple or dict of fields for evaluating the expression.

    Examples
    --------
    The fields are be supplied in the .format syntax:

    >>> field1 = MathEval(expression="1.0")
    >>> field2 = MathEval(expression="Sin({})", fields=[field1])

    >>> field1 = MathEval(expression="1.0")
    >>> field2 = MathEval(expression="Sin({input_field})", fields=dict(input_field=field1))


    """
    def __init__(self, *, expression, fields=None):
        super(MathEval, self).__init__(field_type="MathEval")

        if fields is not None:
            assert isinstance(fields, list) or isinstance(fields, tuple) or isinstance(fields, dict)

            if isinstance(fields, dict):
                assert False not in [isinstance(value, Base) for key, value in fields.items()]
                fields = {key: "F" + str(value.id) for key, value in fields.items()}
                self.expression = expression.format(**fields)

            else:
                assert False not in [isinstance(field, Base) for field in fields]
                self.expression = expression.format(*["F" + str(field.id) for field in fields])

        else:
            self.expression = expression

        self._code.append(
            "Field[{id}].F = \"{expression}\";".format(
                id=self.id,
                expression=self.expression
            )
        )


class Min(Base):
    """
    A Gmsh Min Field. Returns the minimum of all the given input fields.

    Parameters
    ----------
    fields : list
        The fields of which the minimum is calculated.
    """

    def __init__(self, *, fields):
        super(Min, self).__init__(field_type="Min")
        assert False not in [isinstance(field, Base) for field in fields]

        self._code.append(
            "Field[{id}].FieldsList = {{{fields}}};".format(
                id=self.id,
                fields=", ".join([str(field.id) for field in fields])
            )
        )


class Max(Base):
    """
    A Gmsh Min Field. Returns the maximum of all the given input fields.

    Parameters
    ----------
    fields : list
        The fields of which the maximum is calculated.
    """

    def __init__(self, *, fields):
        super(Max, self).__init__(field_type="Max")
        assert False not in [isinstance(field, Base) for field in fields]

        self._code.append(
            "Field[{id}].FieldsList = {{{fields}}};".format(
                id=self.id,
                fields=", ".join([str(field.id) for field in fields])
            )
        )
