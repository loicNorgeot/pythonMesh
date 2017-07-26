import bpy
from bpy_extras.io_utils import ExportHelper, axis_conversion
from bpy.props import StringProperty, EnumProperty
import mathutils
import colorsys
from . import msh


#Define the operator names, properties and function
operatorID   = "import_mesh.mesh"
operatorText = "Import .mesh"
class operator(bpy.types.Operator, ExportHelper):
    """Import a Mesh file"""
    bl_idname = operatorID
    bl_label = operatorText
    filter_glob = StringProperty(
        default="*.mesh",
        options={'HIDDEN'},
    )
    check_extension = True
    filename_ext = ".mesh"
    def execute(self, context):
        keywords = self.as_keywords(ignore=('filter_glob','check_existing'))
        err = operatorFunction(self, context, **keywords)
        if err:
            return {'CANCELLED'}
        else:
            return {'FINISHED'}
def operatorFunction(operator, context, filepath):

    MESH = msh.Mesh(filepath)
    MESH.readSol()
    MESH.tets = msh.np.array([])
    MESH.discardUnused()

    meshes = []
    rTris = MESH.tris[:,-1].tolist() if len(MESH.tris)>0 else []
    rQuads = MESH.quads[:,-1].tolist() if len(MESH.quads)>0 else []
    tris = [t.tolist() for t in MESH.tris]
    quads = [q.tolist() for q in MESH.quads]
    verts = [v.tolist()[:-1] for v in MESH.verts]
    REFS = set(rTris + rQuads)

    for i,r in enumerate(REFS):
        refFaces = [t[:-1] for t in tris + quads if t[-1]==r]
        #refFaces = refFaces + [[q[:-1] for q in quads if q[-1] == r]]
        mesh_name = bpy.path.display_name_from_filepath(filepath)
        mesh = bpy.data.meshes.new(name=mesh_name)
        meshes.append(mesh)
        mesh.from_pydata(verts, [], refFaces)
        mesh.validate()
        mesh.update()


    if not meshes:
        return 1

    scene = context.scene

    objects = []
    for i,m in enumerate(meshes):
        obj = bpy.data.objects.new(m.name, m)
        bpy.ops.object.select_all(action='DESELECT')
        scene.objects.link(obj)
        scene.objects.active = obj
        mat = bpy.data.materials.new(m.name+"_material_"+str(i))
        if i==0:
            mat.diffuse_color = colorsys.hsv_to_rgb(0,0,1)
        else:
            mat.diffuse_color = colorsys.hsv_to_rgb(float(i/len(meshes)),1,1)
        obj.data.materials.append(mat)
        objects.append(obj)
    del meshes

    scene.update()
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:
        o.select=True
    bpy.ops.object.join()
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.editmode_toggle()

    #Solutions according to the weight paint mode (0 to 1 by default)
    if len(MESH.scalars) > 0:
        bpy.ops.object.vertex_group_add()
        vgrp = bpy.context.active_object.vertex_groups[0]
        for X in tris+quads:
            for x in X:
                vgrp.add([x],MESH.scalars[x],"REPLACE")
    del MESH
    del verts, tris, quads

    return 0

#register and unregister
def register():
    bpy.utils.register_class(operator)
def unregister():
    bpy.utils.unregister_class(operator)

#So that the addon can be loaded from the script editor
if __name__ == "__main__":
    register()
