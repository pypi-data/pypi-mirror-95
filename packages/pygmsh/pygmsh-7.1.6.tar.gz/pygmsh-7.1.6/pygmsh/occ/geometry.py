import math

import gmsh

from .. import common
from .ball import Ball
from .box import Box
from .cone import Cone
from .cylinder import Cylinder
from .disk import Disk
from .dummy import Dummy
from .rectangle import Rectangle
from .torus import Torus
from .wedge import Wedge


class Geometry(common.CommonGeometry):
    def __init__(self):
        super().__init__(gmsh.model.occ)

    def __exit__(self, *a):
        # TODO remove once gmsh 4.7.0 is out
        # <https://gitlab.onelab.info/gmsh/gmsh/-/issues/1001>
        gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 0.0)
        gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 1.0e22)
        gmsh.finalize()

    @property
    def characteristic_length_min(self):
        return gmsh.option.getNumber("Mesh.CharacteristicLengthMin")

    @property
    def characteristic_length_max(self):
        return gmsh.option.getNumber("Mesh.CharacteristicLengthMax")

    @characteristic_length_min.setter
    def characteristic_length_min(self, val):
        gmsh.option.setNumber("Mesh.CharacteristicLengthMin", val)

    @characteristic_length_max.setter
    def characteristic_length_max(self, val):
        gmsh.option.setNumber("Mesh.CharacteristicLengthMax", val)

    def force_outward_normals(self, tag):
        self._OUTWARD_NORMALS.append(tag)

    def revolve(self, *args, **kwargs):
        if len(args) >= 4:
            angle = args[3]
        else:
            assert "angle" in kwargs
            angle = kwargs["angle"]

        assert angle < 2 * math.pi
        return super()._revolve(*args, **kwargs)

    def add_rectangle(self, *args, mesh_size=None, **kwargs):
        entity = Rectangle(*args, **kwargs)
        if mesh_size is not None:
            self._SIZE_QUEUE.append((entity, mesh_size))
        return entity

    def add_disk(self, *args, mesh_size=None, **kwargs):
        entity = Disk(*args, **kwargs)
        if mesh_size is not None:
            self._SIZE_QUEUE.append((entity, mesh_size))
        return entity

    def add_ball(self, *args, mesh_size=None, **kwargs):
        obj = Ball(*args, **kwargs)
        if mesh_size is not None:
            self._SIZE_QUEUE.append((obj, mesh_size))
        return obj

    def add_box(self, *args, mesh_size=None, **kwargs):
        box = Box(*args, **kwargs)
        if mesh_size is not None:
            self._SIZE_QUEUE.append((box, mesh_size))
        return box

    def add_cone(self, *args, mesh_size=None, **kwargs):
        cone = Cone(*args, **kwargs)
        if mesh_size is not None:
            self._SIZE_QUEUE.append((cone, mesh_size))
        return cone

    def add_cylinder(self, *args, mesh_size=None, **kwargs):
        cyl = Cylinder(*args, **kwargs)
        if mesh_size is not None:
            self._SIZE_QUEUE.append((cyl, mesh_size))
        return cyl

    def add_ellipsoid(self, center, radii, mesh_size=None):
        obj = Ball(center, 1.0)
        self.dilate(obj, center, radii)
        if mesh_size is not None:
            self._SIZE_QUEUE.append((obj, mesh_size))
        return obj

    def add_torus(self, *args, mesh_size=None, **kwargs):
        obj = Torus(*args, **kwargs)
        if mesh_size is not None:
            self._SIZE_QUEUE.append((obj, mesh_size))
        return obj

    def add_wedge(self, *args, mesh_size=None, **kwargs):
        obj = Wedge(*args, **kwargs)
        if mesh_size is not None:
            self._SIZE_QUEUE.append((obj, mesh_size))
        return obj

    def boolean_intersection(self, entities):
        """Boolean intersection, see
        https://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
        and tool_entity are called object and tool in gmsh documentation.
        """
        entities = [e if isinstance(e, list) else [e] for e in entities]

        ent = [e.dim_tag for e in entities[0]]
        # form subsequent intersections
        # https://gitlab.onelab.info/gmsh/gmsh/-/issues/999
        for e in entities[1:]:
            out, _ = gmsh.model.occ.intersect(
                ent,
                [ee.dim_tag for ee in e],
                removeObject=True,
                removeTool=True,
            )
            if len(out) == 0:
                raise RuntimeError("Empty intersection.")
            assert all(out[0] == item for item in out)
            ent = [out[0]]

        return [Dummy(*ent[0])]

    def boolean_union(self, entities):
        """Boolean union, see
        https://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
        and tool_entity are called object and tool in gmsh documentation.
        """
        entities = [e if isinstance(e, list) else [e] for e in entities]

        dim_tags, _ = gmsh.model.occ.fuse(
            [e.dim_tag for e in entities[0]],
            [ee.dim_tag for e in entities[1:] for ee in e],
            removeObject=True,
            removeTool=True,
        )
        return [Dummy(*dim_tag) for dim_tag in dim_tags]

    def boolean_difference(self, d0, d1, delete_first=True, delete_other=True):
        """Boolean difference, see
        https://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
        and tool_entity are called object and tool in gmsh documentation.
        """
        d0 = d0 if isinstance(d0, list) else [d0]
        d1 = d1 if isinstance(d1, list) else [d1]
        dim_tags, _ = gmsh.model.occ.cut(
            [d.dim_tag for d in d0],
            [d.dim_tag for d in d1],
            removeObject=delete_first,
            removeTool=delete_other,
        )
        return [Dummy(*dim_tag) for dim_tag in dim_tags]

    def boolean_fragments(self, d0, d1):
        """Boolean fragments, see
        https://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
        and tool_entity are called object and tool in gmsh documentation.
        """
        d0 = d0 if isinstance(d0, list) else [d0]
        d1 = d1 if isinstance(d1, list) else [d1]
        dim_tags, _ = gmsh.model.occ.fragment(
            [d.dim_tag for d in d0],
            [d.dim_tag for d in d1],
        )
        return [Dummy(*dim_tag) for dim_tag in dim_tags]
