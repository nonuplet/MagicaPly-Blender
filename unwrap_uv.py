import bpy
from bpy.types import Context, Object, Operator


class MPUnwrapUv(Operator):
    bl_idname = "uv.magicaply_setup_model"
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

        unwrap_uv(obj)

        return {"FINISHED"}


def unwrap_uv(obj: Object):
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
