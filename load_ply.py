import os

import bpy
from bpy.props import CollectionProperty, StringProperty
from bpy.types import Context, Operator, OperatorFileListElement
from bpy_extras.io_utils import ImportHelper


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

    def execute(self, context: Context):
        paths = [os.path.join(self.directory, name.name) for name in self.files]

        for path in paths:
            import_ply(path)

        return {"FINISHED"}


def import_ply(path: str):
    try:
        name = os.path.splitext(os.path.basename(path))[0]
        print("path: " + path)
        bpy.ops.import_mesh.ply(filepath=path)
        obj = bpy.context.active_object
        obj.name = name

    except Exception as e:
        print(e)
