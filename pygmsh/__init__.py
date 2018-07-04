# -*- coding: utf-8 -*-
#
from __future__ import print_function

from .__about__ import __version__, __author__, __author_email__, __website__

from . import built_in
from . import opencascade
from . import meshing
from .helpers import generate_mesh, get_gmsh_major_version, rotation_matrix
from .meshing.sets import boundary_of, points_of

__all__ = [
    "built_in",
    "opencascade",
    "meshing",
    "boundary_of",
    "points_of",
    "generate_mesh",
    "get_gmsh_major_version",
    "rotation_matrix",
    "__version__",
    "__author__",
    "__author_email__",
    "__website__",
]

try:
    import pipdate
except ImportError:
    pass
else:
    if pipdate.needs_checking(__name__):
        print(pipdate.check(__name__, __version__), end="")
