import bpy
import tempfile
import platform
import subprocess

def PoissonDef(self, context):

    tmpdir = tempfile.mkdtemp()

    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].levels = 1
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subdivision")
    #bpy.ops.object.convert(target='MESH')


    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.delete(type='EDGE_FACE')
    bpy.ops.object.editmode_toggle()

    bpy.ops.wm.collada_export(filepath=tmpdir+"/Pontos.dae", selected=True)

    if platform.system() == "Linux":
        subprocess.call('meshlabserver -i '+tmpdir+'/Pontos.dae -o '+tmpdir+'/Poisson.ply -s ~/Programs/OrtogOnBlender/Meshlab/Poisson.mlx -om vc fq wn', shell=True)
        
    bpy.ops.object.delete(use_global=False)

        
    bpy.ops.import_mesh.ply(filepath=tmpdir+"/Poisson.ply", files=[], directory="", filter_glob="*.ply")

class Poisson(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.poisson"
    bl_label = "Ortog Poisson"
    
    def execute(self, context):
       PoissonDef(self, context)
       return {'FINISHED'}

bpy.utils.register_class(Poisson)
