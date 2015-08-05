import bpy

from .exceptions import *

def skull_import(context, filepath, decimate_factor, apply_modifier):
    try:
        bpy.ops.import_mesh.stl.poll()
    except AttributeError:
        raise ImportSTLException()

    # import STL mesh
    res = bpy.ops.import_mesh.stl(filepath=filepath)

    if res != {'FINISHED'}:
        raise ImportSkullException()

    if decimate_factor < 1.0:
        skull = context.object
        decimate = skull.modifiers.new('Decimate', type='DECIMATE')
        decimate.ratio = decimate_factor

        if apply_modifier:
            # apply the modifier
            res = {'CANCELLED'}
            if bpy.ops.object.modifier_apply.poll():
                res = bpy.ops.object.modifier_apply(apply_as='DATA', modifier='Decimate')

            if res != {'FINISHED'}:
                raise ImportSkullDecimateException(skull.name)

    # expand the view to the new object
    res = {'CANCELLED'}
    if bpy.ops.view3d.view_all.poll():
        res = bpy.ops.view3d.view_all()

    if res != {'FINISHED'}:
        raise ImportSkullViewAllException()


