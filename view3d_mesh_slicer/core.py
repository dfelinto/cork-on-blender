import bpy

from .exceptions import *

def slice_out(context, cork, method, base, plane):
    scene = context.scene
    active = scene.objects.active

    # 1. export base
    scene.objects.active = base
    filepath = '/tmp/base.off'
    if bpy.ops.export_mesh.off.poll():
        bpy.ops.export_mesh.off(filepath=filepath)
    else:
        scene.objects.active = active
        raise ExportMeshException(base, filepath)

    # 2. export plane to OFF
    scene.objects.active = plane
    filepath = '/tmp/plane.off'
    if bpy.ops.export_mesh.off.poll():
        bpy.ops.export_mesh.off(filepath=filepath)
    else:
        scene.objects.active = active
        raise ExportMeshException(plane, filepath)

    # 3. call cork with arguments
    # 4. import resulting OFF mesh
    pass
