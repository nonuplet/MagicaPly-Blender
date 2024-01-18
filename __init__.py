# Copyright (C) 2024 Kokonoe
import bpy.utils

# This file is part of MagicaPly-Blender.

# MagicaPly-Blender is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# MagicaPly-Blender is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

bl_info = {
    "name": "MagicaPly-Blender",
    "author": "Kokonoe",
    "version": (0, 1, 0),
    "blender": (3, 6, 0),
    "location": "",
    "description": "An add-on to optimize MagicaVoxel's .ply format models in Blender.",
    "warning": "This add-on currently under testing. There is a possibility that bugs may occur.",
    "support": "COMMUNITY",
    "doc_url": "https://github.com/nonuplet/MagicaPly-Blender",
    "tracker_url": "https://github.com/nonuplet/MagicaPly-Blender",
    "category": "Import-Export",
}

from bpy.types import Menu

from . import bake_texture, setup_model, unwrap_uv


class MagicaPlyMTObjectMenu(Menu):
    bl_idname = "MagicaPly_MT_Object"
    bl_label = "MagicaPly"
    bl_description = "MagicaPly Menu"

    def draw(self, context):
        layout = self.layout
        layout.operator(setup_model.MPSetupModel.bl_idname)
        layout.operator(unwrap_uv.MPUnwrapUv.bl_idname)
        layout.operator(bake_texture.MPBakeTexture.bl_idname)


def menu_setup_func(self, context):
    self.layout.separator()
    self.layout.menu(MagicaPlyMTObjectMenu.bl_idname)


classes = [
    setup_model.MPSetupModel,
    unwrap_uv.MPUnwrapUv,
    bake_texture.MPBakeTexture,
    MagicaPlyMTObjectMenu,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_object.append(menu_setup_func)
    print("Registering MagicaPly-Blender")


def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_setup_func)
    for cls in classes:
        bpy.utils.unregister_class(cls)
    print("Unregistering MagicaPly-Blender")


if __name__ == "__main__":
    register()
