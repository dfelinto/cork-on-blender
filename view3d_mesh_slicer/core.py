import bpy

from .exceptions import *

def slice_out(context, cork, method, base, plane):
    import subprocess

    scene = context.scene
    active = scene.objects.active

    filepath_base = '/tmp/base.off'
    filepath_plane = '/tmp/plane.off'
    filepath_result = '/tmp/result.off'

    # export base
    print("Exporting file \"{0}\"".format(filepath_base))
    scene.objects.active = base
    if bpy.ops.export_mesh.off.poll():
        bpy.ops.export_mesh.off(filepath=filepath_base)
    else:
        scene.objects.active = active
        raise ExportMeshException(base, filepath_base)

    # export plane to OFF
    print("Exporting file \"{0}\"".format(filepath_plane))
    scene.objects.active = plane
    if bpy.ops.export_mesh.off.poll():
        bpy.ops.export_mesh.off(filepath=filepath_plane)
    else:
        scene.objects.active = active
        raise ExportMeshException(plane, filepath_plane)

    # call cork with arguments
    print("{0} {1} {2} {3} {4}".format(cork, method, filepath_base, filepath_plane, filepath_result))
    try:
        subprocess.call((cork, method, filepath_base, filepath_plane, filepath_result))
    except Exception as error:
        raise error

    # import resulting OFF mesh
    print("Importing file \"{0}\"".format(filepath_result))
    if bpy.ops.import_mesh.off.poll():
        bpy.ops.import_mesh.off(filepath=filepath_result)
    else:
        scene.objects.active = active
        raise ImportMeshException(filepath_result)

    # move object to a new layer
    result = [obj for obj in context.selected_objects if obj not in (base, plane)][0]
    result.layers[1] = True
    result.select = False

    print("Object \"{0}\" created successfully".format(result.name))

    # restore previous status
    scene.objects.active = active
