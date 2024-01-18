from typing import List

import bmesh
import bpy
import numpy as np
from bmesh.types import BMFace, BMLayerItem, BMLoopUV
from bpy.types import Context, Mesh, Object, Operator
from bpy_extras import bmesh_utils
from mathutils import Vector


class MPUnwrapUv(Operator):
    bl_idname = "object.magicaply_unwrap_uv"
    bl_label = "Unwrap Voxel UV"
    bl_description = "Perform UV unwrapping and optimization for the voxel model."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: Context):
        obj = context.active_object

        # Check type of object
        if type(obj) is not Object:
            self.report({"ERROR"}, "Object is not active.")
            return {"CANCELLED"}
        if obj.type != "MESH":
            self.report({"ERROR"}, "Active object is not Mesh.")
            return {"CANCELLED"}

        unwrap_uv(obj.data)

        return {"FINISHED"}


def unwrap_uv(mesh: Mesh):
    # Initial Unwrap
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(
        angle_limit=1.55334,
        margin_method="SCALED",
        island_margin=0.005,
        area_weight=0,
        correct_aspect=True,
        scale_to_bounds=True,
    )
    bpy.ops.uv.align_rotation()
    bpy.ops.uv.pack_islands(
        udim_source="CLOSEST_UDIM",
        rotate=True,
        rotate_method="CARDINAL",
        scale=True,
        margin_method="SCALED",
        margin=0.005,
        shape_method="CONCAVE",
    )

    # Optimize UV for Voxel
    voxel_unwrap(mesh, 512)


def snap_to_pixel(x: float, y: float, resolution: int):
    res = np.array([x, y])
    res *= resolution
    res = np.round(res)
    return res


def voxel_unwrap(mesh: Mesh, resolution: int):
    bm = bmesh.from_edit_mesh(mesh)
    bm.faces.ensure_lookup_table()

    islands: List[List[BMFace]] = bmesh_utils.bmesh_linked_uv_islands(bm, bm.loops.layers.uv[0])
    uv_layer: BMLayerItem = bm.loops.layers.uv.get("UVMap")

    for island in islands:
        vertices = []
        edge_length = (island[0].loops[0][uv_layer].uv - island[0].loops[1][uv_layer].uv).length
        origin: Vector = island[0].loops[0][uv_layer].uv.copy()

        for face in island:
            for loop in face.loops:
                uv: BMLoopUV = loop[uv_layer]
                v = uv.uv - origin
                vertices.append([v.x / edge_length, v.y / edge_length])

        np_vertices = np.round(np.array(vertices))
        unit = 2
        np_vertices *= unit

        offset = snap_to_pixel(origin.x, origin.y, resolution)
        np_vertices += offset

        np_vertices /= resolution

        idx = 0
        for face in island:
            for loop in face.loops:
                uv: BMLoopUV = loop[uv_layer]
                uv.uv.x = np_vertices[idx][0]
                uv.uv.y = np_vertices[idx][1]
                idx += 1

    bmesh.update_edit_mesh(mesh)