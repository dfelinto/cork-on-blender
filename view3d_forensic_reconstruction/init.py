import bpy
from bpy.props import (
        BoolProperty,
        EnumProperty,
        FloatProperty,
        IntProperty,
        StringProperty,
        )

from bpy.types import (
        Operator,
        Panel,
        )

from bpy_extras.io_utils import (
        ImportHelper,
        )

import bmesh

from .exceptions import *

from .lib import (
        get_cork_filepath,
        validate_executable,
        )

from .skull import (
        skull_import,
        )

from .alignment import (
        natural_orientation,
        )

from .cork import (
        slice_out,
        )


# ############################################################
# User Interface
# ############################################################

class AcquireDataPanel(Panel):
    bl_label = "Acquire Data"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Forensic Reconstruction'

    @staticmethod
    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.operator("view3d.skull_import", icon="FILE_FOLDER")


class NaturalOrientationPanel(Panel):
    bl_label = "Natural Orientation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Forensic Reconstruction'

    @staticmethod
    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.operator("view3d.natural_orientation")


class CorkMeshSlicerPanel(Panel):
    bl_label = "Cork Mesh Slice"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Forensic Reconstruction'

    @staticmethod
    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.operator("view3d.cork_mesh_slicer", text="Union").method="UNION"
        col.operator("view3d.cork_mesh_slicer", text="Difference").method="DIFF"
        col.operator("view3d.cork_mesh_slicer", text="Intersect").method="INTERSECT"
        col.operator("view3d.cork_mesh_slicer", text="XOR").method="XOR"
        col.operator("view3d.cork_mesh_slicer", text="Resolve").method="RESOLVE"
        col.separator()
        col.operator("view3d.cork_mesh_slicer", text="", icon='QUESTION', emboss=False).show_help = True


# ############################################################
# Operators
# ############################################################

class SkullImportOperator(Operator, ImportHelper):
    """"""
    bl_idname = "view3d.skull_import"
    bl_label = "Skull Importer"
    bl_description = ""

    filename_ext = ".stl"

    filter_glob = StringProperty(
        default="*.stl",
        options={'HIDDEN'},
        )

    decimate_factor = FloatProperty(
            name="Decimator Factor",
            default=0.35,
            min=0.0,
            max=1.0,
            description="Simplify the mesh by this factor (1.0 = original mesh)",
            options={'SKIP_SAVE'},
            )

    apply_modifier = BoolProperty(
            name="Apply Decimate Modifier",
            default=True,
            description="",
            options={'SKIP_SAVE'},
            )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        try:
            skull_import(
                    context,
                    self.properties.filepath,
                    self.decimate_factor,
                    self.apply_modifier,
                    )

        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

        return {'FINISHED'}


class NaturalOrientationOperator(Operator):
    """"""
    bl_idname = "view3d.natural_orientation"
    bl_label = "Natural Orientation"
    bl_description = ""

    width = FloatProperty(
            name="Width",
            subtype='DISTANCE',
            description="",
            default=0.30,
            min=0.0,
            max=1.0,
            )

    height = FloatProperty(
            name="Height",
            subtype='DISTANCE',
            description="",
            default=0.50,
            min=0.0,
            max=1.0,
            )

    @classmethod
    def poll(cls, context):
        if (context.mode == 'EDIT_MESH'):
            ob = context.active_object
            return ob and \
                   ob.select and \
                   ob.type == 'MESH'
        else:
            return False

    def exec(self, context):
        try:
            error_scale,  \
            error_angle = \
                    natural_orientation(
                    context.active_object,
                    self._selected_verts,
                    self.width,
                    self.height,
                    )

        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

        self.report({'INFO'}, "Precision difference: {0:.2f} (distance), {1:.2f} (angle)".format(error_scale, error_angle))
        return {'FINISHED'}

    def invoke(self, context, event):
        mesh = context.active_object.data
        bm = bmesh.from_edit_mesh(mesh)
        selected_verts = [v for v in bm.verts if v.select]

        _len = len(selected_verts)

        if _len != 3:
            self.report({'ERROR'}, "Natural Orientation requires 3 selected vertices ({0} selected)".format(_len))
            return {'CANCELLED'}

        self._selected_verts = selected_verts
        return self.exec(context) # TODO

        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=150)

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        col.prop(self, "width")
        col.prop(self, "height")


class CorkMeshSlicerOperator(Operator):
    """"""
    bl_idname = "view3d.cork_mesh_slicer"
    bl_label = "Mesh Slicer"
    bl_description = ""

    method = EnumProperty(
        description="",
        items=(("UNION", "Union", "A + B"),
               ("DIFF", "Difference", "A - B"),
               ("INTERSECT", "Intersection", "A n B"),
               ("XOR", "XOR", "A xor B"),
               ("RESOLVE", "Resolve", "Intersect and connect"),
               ),
        default="DIFF",
        options={'SKIP_SAVE'},
        )

    show_help = bpy.props.BoolProperty(
            name="Help",
            description="",
            default=False,
            options={'HIDDEN', 'SKIP_SAVE'},
            )

    _commands = {
            'UNION':'-union',
            'DIFF':'-diff',
            'INTERSECT':'-isct',
            'XOR':'-xor',
            'RESOLVE':'-resolve',
            }

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.select

    def exec(self, context):
        try:
            slice_out(context, self._cork, self._method, self._base, self._plane)
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

        return {'FINISHED'}

    def invoke(self, context, event):
        if self.show_help:
            context.window_manager.popup_menu(self.help_draw, title='Help', icon='QUESTION')
            return {'CANCELLED'}

        cork = get_cork_filepath(context)

        try:
            validate_executable(cork)
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

        try:
            self.check_errors(context.selected_objects, self.method)
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

        self._cork = cork
        self._plane = context.active_object
        self._base = context.selected_objects[0] if context.selected_objects[0] != self._plane else context.selected_objects[1]
        self._method = self._commands.get(self.method)

        return self.exec(context)

    def check_errors(self, objects, method):
        """"""
        if len(objects) != 2:
            raise NumberSelectionException

        for obj in objects:
            if obj.type != 'MESH':
                raise NonMeshSelectedException(obj)

    def help_draw(self, _self, context):
        layout = _self.layout
        col = layout.column()

        col.label(text="This operator works from the selected to the active objects")
        col.label(text="The active must be a single plane")

        col.separator()
        col.label(text="Union")
        col.label(text="Compute the Boolean union of in0 and in1, and output the result")

        col.separator()
        col.label(text="Difference")
        col.label(text="Compute the Boolean difference of in0 and in1, and output the result")

        col.separator()
        col.label(text="Intersect")
        col.label(text="Compute the Boolean intersection of in0 and in1, and output the result")

        col.separator()
        col.label(text="XOR")
        col.label(text="Compute the Boolean XOR of in0 and in1, and output the result")

        col.separator()
        col.label(text="Resolve")
        col.label(text="Intersect the two meshes in0 and in1, and output the connected mesh with those")
        col.label(text="intersections made explicit and connected")


# ############################################################
# Registration
# ############################################################

def register():
    # the order here determines the UI order
    bpy.utils.register_class(AcquireDataPanel)
    bpy.utils.register_class(NaturalOrientationPanel)
    bpy.utils.register_class(CorkMeshSlicerPanel)

    bpy.utils.register_class(SkullImportOperator)
    bpy.utils.register_class(NaturalOrientationOperator)
    bpy.utils.register_class(CorkMeshSlicerOperator)


def unregister():
    bpy.utils.unregister_class(AcquireDataPanel)
    bpy.utils.unregister_class(NaturalOrientationPanel)
    bpy.utils.unregister_class(CorkMeshSlicerPanel)

    bpy.utils.unregister_class(SkulImportOperator)
    bpy.utils.unregister_class(NaturalOrientationOperator)
    bpy.utils.unregister_class(CorkMeshSlicerOperator)


