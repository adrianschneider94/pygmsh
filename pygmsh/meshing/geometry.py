from ..built_in.geometry import Geometry as BaseBuiltInGeometry
from ..opencascade.geometry import Geometry as BaseOpenCascadeGeometry

from .fields import Base


class MeshingMixIn(object):
    def add_field(self, field):
        field.id = self._FIELD_ID
        self._FIELD_ID += 1
        self._GMSH_CODE.append(field.code)
        return field

    def set_background_field(self, field):
        self._GMSH_CODE.append("Background Field = {};".format(field.id))

    def achieve_coherence(self):
        self._GMSH_CODE.append("Coherence;")


class BuiltInGeometry(BaseBuiltInGeometry, MeshingMixIn):
    pass


class OpenCascadeGeometry(BaseOpenCascadeGeometry, MeshingMixIn):
    pass
