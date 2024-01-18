from bpy.types import Context, Mesh, Object, Operator


class MPBakeTexture(Operator):
    bl_idname = "object.magicaply_bake_texture"
    bl_label = "Bake texture"
    bl_description = "Bake the texture. **UV must be unwrapped in before**"
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

        # Check UV Layer
        mesh: Mesh = obj.data
        layers = mesh.uv_layers
        if len(layers) == 0:
            self.report({"ERROR"}, "Active object has no UV Layer.")
            return {"CANCELLED"}

        return {"FINISHED"}
