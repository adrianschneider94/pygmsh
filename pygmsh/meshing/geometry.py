from ..built_in.geometry import Geometry as BaseBuiltInGeometry
from ..opencascade.geometry import Geometry as BaseOpenCascadeGeometry

from . import fields as Fields


class MeshingMixIn(object):
    def add_field(self, field):
        field.id = self._FIELD_ID
        self._FIELD_ID += 1
        self._GMSH_CODE.append(field.code)
        return field

    def set_background_field(self, field):
        self._GMSH_CODE.append("Background Field = {};".format(field.id))
        return True

    def achieve_coherence(self):
        self._GMSH_CODE.append("Coherence;")
        return True

    def add_distance_field(self, *, objects, n_nodes_by_edge=20):
        field = Fields.Distance(objects=objects, n_nodes_by_edge=n_nodes_by_edge)
        self.add_field(field)
        return field

    def add_math_eval_field(self, *, expression, fields=None):
        field = Fields.MathEval(expression=expression, fields=fields)
        self.add_field(field)
        return field

    def add_min_field(self, *, fields):
        field = Fields.Min(fields=fields)
        self.add_field(field)
        return field

    def add_max_field(self, *, fields):
        field = Fields.Max(fields=fields)
        self.add_field(field)
        return field


class BuiltInGeometry(BaseBuiltInGeometry, MeshingMixIn):
    pass


class OpenCascadeGeometry(BaseOpenCascadeGeometry, MeshingMixIn):
    pass
