import os

import bpy
from bpy.props import BoolProperty, CollectionProperty, IntProperty, StringProperty
from bpy.types import Context, Operator, OperatorFileListElement
from bpy_extras.io_utils import ImportHelper

from . import bake_texture, setup_model, unwrap_uv, decimate_model, set_origin


class MPLoadPly(Operator, ImportHelper):
    bl_idname = "import.magicaply_load_models"
    bl_label = "Import Magicavoxel .ply"
    bl_description = "Import Magicavoxel .ply model(s)"
    bl_options = {"REGISTER", "UNDO"}

    files: CollectionProperty(
        name="File Path",
        description="Path to .ply file exported by Magicavoxel",
        type=OperatorFileListElement,
    )

    directory: StringProperty()

    filter_glob: StringProperty(default="*.ply", options={"HIDDEN"})

    auto_setup: BoolProperty(
        name="Setup Model",
        description="Automatically setup material of model and unwrap UV",
        default=True,
    )

    merge_vertices: BoolProperty(
        name="Merge Vertices", description="Merge overlapping vertices", default=True
    )

    bake: BoolProperty(name="Bake Texture", description="Bake textures", default=True)

    resolution: IntProperty(
        name="Texture Resolution", description="texture resolution for baking", default=512
    )

    decimate: BoolProperty(
        name="Apply Decimate", description="Apply Decimate Modifier", default=False
    )

    origin_bottom: BoolProperty(
        name="Set Bottom as Origin", description="Set the bottom of model as origin", default=False
    )

    def execute(self, context: Context):
        paths = [os.path.join(self.directory, name.name) for name in self.files]

        for path in paths:
            import_ply(
                path,
                self.auto_setup,
                self.merge_vertices,
                self.bake,
                self.resolution,
                self.decimate,
                self.origin_bottom,
            )

        return {"FINISHED"}


def import_ply(
    path: str,
    setup: bool,
    merge_vertices: bool,
    bake: bool,
    resolution: int,
    decimate: bool,
    origin_bottom: bool,
):
    try:
        name = os.path.splitext(os.path.basename(path))[0]
        print("path: " + path)
        bpy.ops.import_mesh.ply(filepath=path)
        obj = bpy.context.active_object
        obj.name = name

        if not setup:
            return

        setup_model.setup_model(obj, merge_vertices)
        unwrap_uv.unwrap_uv(obj.data)

        if bake:
            bake_texture.auto_bake(obj, resolution)

        if decimate:
            decimate_model.decimate()

        if origin_bottom:
            set_origin.set_origin(obj)

    except Exception as e:
        print(e)
