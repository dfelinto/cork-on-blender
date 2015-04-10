#====================== BEGIN GPL LICENSE BLOCK ======================
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#======================= END GPL LICENSE BLOCK ========================

# <pep8 compliant>
bl_info = {
    "name": "Cork Mesh Slicer",
    "author": "Dalai Felinto",
    "version": (0, 9),
    "blender": (2, 7, 5),
    "location": "Tool Shelf",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"}


import bpy
from bpy.props import StringProperty

from . import init


# Preferences
class CorkMeshSlicerPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    use_libraries = StringProperty(
        name="Cork Executable",
        description="Location of cork binary file",
        default="",
        )

def register():
    bpy.utils.register_class(CorkMeshSlicerPreferences)
    init.register()


def unregister():
    bpy.utils.unregister_class(CorkMeshSlicerPreferences)
    init.unregister()


if __name__ == '__main__':
    register()
