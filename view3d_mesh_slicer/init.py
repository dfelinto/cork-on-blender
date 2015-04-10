import bpy


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
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.exec(context)


def register():
    bpy.utils.register_class(CorkMeshSlicerPanel)
    bpy.utils.register_class(CorkMeshSlicerOperator)


def unregister():
    bpy.utils.unregister_class(CorkMeshSlicerPanel)
    bpy.utils.unregister_class(CorkMeshSlicerOperator)
