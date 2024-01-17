import bpy
from bpy.types import Context, Mesh, Object, Operator


class MPSetupModel(Operator):
    bl_idname = "object.magicaply_setup_model"
    bl_label = "Setup Magicavoxel .ply"
    bl_description = "Setup Magicavoxel .ply model"
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

        setup_model(obj)

        return {"FINISHED"}


def setup_model(obj: Object, merge_vertices: bool = True):
    current_ui = bpy.context.area.ui_type

    try:
        name = obj.name
        obj_mesh: Mesh = obj.data

        # Setup new material
        material = bpy.data.materials.new(name)
        if obj_mesh.materials:
            obj_mesh.materials[0] = material
        else:
            obj_mesh.materials.append(material)

        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links
        nodes.clear()

        bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
        vert_color = nodes.new(type="ShaderNodeAttribute")
        vert_color.attribute_name = "Col"
        output = nodes.new(type="ShaderNodeOutputMaterial")
        links.new(vert_color.outputs["Color"], bsdf.inputs["Base Color"])
        links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])

        # Merge by distance
        if merge_vertices:
            bpy.ops.object.shade_smooth(use_auto_smooth=True, auto_smooth_angle=0.523599)
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_all(action="SELECT")
            bpy.ops.mesh.remove_doubles()
            bpy.ops.object.mode_set(mode="OBJECT")

    except Exception as e:
        print(e)

    finally:
        bpy.context.area.ui_type = current_ui
