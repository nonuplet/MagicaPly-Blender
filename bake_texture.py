import bpy
from bpy.props import IntProperty
from bpy.types import Context, Material, Mesh, Object, Operator


class MPBakeTexture(Operator):
    bl_idname = "object.magicaply_bake_texture"
    bl_label = "Bake texture"
    bl_description = "Bake the texture. **UV must be unwrapped in before**"
    bl_options = {"REGISTER", "UNDO"}

    resolution: IntProperty(
        name="Texture Resolution",
        description="Resolution of Texture",
        default=512,
    )

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
        if not mesh.uv_layers:
            self.report({"ERROR"}, "Active object has no UV Layer.")
            return {"CANCELLED"}

        # Check Material
        if not mesh.materials:
            self.report({"ERROR"}, "Active object has no Material.")
            return {"CANCELLED"}

        auto_bake(obj, self.resolution)

        return {"FINISHED"}


def auto_bake(obj: Object, resolution: int):
    mesh: Mesh = obj.data
    material: Material = mesh.materials[0]
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    # Create Texture & Setup Material
    texture = bpy.data.images.new(obj.name, resolution, resolution)
    img_node = nodes.new(type="ShaderNodeTexImage")
    img_node.image = texture
    img_node.interpolation = "Closest"
    nodes.active = img_node

    # Bake
    cycles_bake()
    texture.pack()

    # Set baked texture
    bsdf = nodes.get("Principled BSDF")
    links.new(img_node.outputs["Color"], bsdf.inputs["Base Color"])


def cycles_bake():
    bpy.ops.object.mode_set(mode="OBJECT")
    render = bpy.context.scene.render
    render.engine = "CYCLES"
    bpy.context.scene.cycles.bake_type = "DIFFUSE"
    render.bake.use_pass_direct = False
    render.bake.use_pass_indirect = False
    render.bake.use_pass_color = True
    render.bake.use_selected_to_active = False
    render.bake.target = "IMAGE_TEXTURES"
    render.bake.use_clear = True
    render.bake.margin_type = "ADJACENT_FACES"
    render.bake.margin = 2
    bpy.ops.object.bake(type="DIFFUSE")
