import bpy

from .exceptions import *

from .lib import (
        get_cork_filepath,
        validate_executable,
        )

from .core import (
        slice_out,
        )


class CorkMeshSlicerPanel(bpy.types.Panel):
    bl_label = "Cork Mesh Slice"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Osteotomia'

    @staticmethod
    def draw(self, context):
        layout = self.layout
        layout.label(text="1,2,3")
        layout.operator('view3d.cork_mesh_slicer')


class CorkMeshSlicerOperator(bpy.types.Operator):
    """"""
    bl_idname = "view3d.cork_mesh_slicer"
    bl_label = "Mesh Slicer"
    bl_description = ""

    def exec(self, context):
        self.report({'INFO'}, "So far so good")
        slice_out()
        return {'FINISHED'}

    def invoke(self, context, event):
        cork = get_cork_filepath(context)

        try:
            validate_executable(cork)

        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

        return self.exec(context)


def register():
    bpy.utils.register_class(CorkMeshSlicerPanel)
    bpy.utils.register_class(CorkMeshSlicerOperator)


def unregister():
    bpy.utils.unregister_class(CorkMeshSlicerPanel)
    bpy.utils.unregister_class(CorkMeshSlicerOperator)
