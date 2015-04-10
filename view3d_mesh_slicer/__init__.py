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
class CorkMeshSlicerPanel(bpy.types.Panel):
    bl_label = "Cork Mesh Slice"
    bl_region_type = 'TOOLS'

    @staticmethod
    def draw(self, context):
        layout = self.layout
        layout.label(text="1,2,3")
        layout.operator('view3d.cork_mesh_slicer')

class CorkMeshSlicerOperator(bpy.types.Operator):
    """"""
    bl_idname = "view3d.cork_mesh_slicer"
    bl_label = "Cork Mesh Slicer"
    bl_description = ""

    def exec(self, context):
        return {'FINISHED'}



def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == '__main__':
    register()
