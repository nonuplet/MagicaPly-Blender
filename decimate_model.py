import bpy
from bpy.types import Context, Object, Operator


class MPDecimate(Operator):
    bl_idname = "object.magicaply_decimate"
    bl_label = "Decimate model"
    bl_description = (
        "Decimate Model."
        "**There is a possibility of the texture getting corrupted"
        'if you haven\'t the "Unwrap Voxel UV."**'
    )
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

        decimate()

        return {"FINISHED"}


def decimate():
    bpy.ops.object.modifier_add(type="DECIMATE")
    deci = bpy.context.object.modifiers["Decimate"]
    deci.decimate_type = "DISSOLVE"
    deci.angle_limit = 0.0872655  # angle 5d
    bpy.ops.object.modifier_apply(modifier="Decimate", report=True)
