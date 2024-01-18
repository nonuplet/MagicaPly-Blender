import bpy
from bpy.types import Context, Mesh, Object, Operator


class MPSetOrigin(Operator):
    bl_idname = "object.magicaply_set_origin"
    bl_label = "Set Origin Bottom"
    bl_description = "Set the bottom of the model as the origin."
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

        set_origin(obj)

        return {"FINISHED"}


def set_origin(obj: Object):
    mesh: Mesh = obj.data
    min_z = min(v.co.z for v in mesh.vertices)
    bpy.context.scene.cursor.location = (0.0, 0.0, min_z)
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)

    obj.location = [0, 0, 0]
