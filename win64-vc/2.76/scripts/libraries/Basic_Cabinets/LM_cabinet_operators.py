'''
Created on Aug 5, 2016

@author: Andrew
'''
import bpy
from mv import fd_types, utils, unit

class OPERATOR_Draw_Plan(bpy.types.Operator):
    bl_idname = "cabinet.draw_plan"
    bl_label = "Draw Plan View"
    bl_description = "Creates the plan view for cabinets"
    
    object_name = bpy.props.StringProperty(name="Object Name",default="")
        
    def execute(self, context):
        obj_bp = bpy.data.objects[self.object_name]

        product = fd_types.Assembly(obj_bp)
        thickness = product.get_prompt("Panel Thickness")
        l_end = product.get_prompt("Left End Condition")
        r_end = product.get_prompt("Right End Condition")
        
        x_placement = product.obj_bp.location.x
        
        cabinet_mesh = utils.create_cube_mesh(product.obj_bp.mv.name_object,
                                              (product.obj_x.location.x,
                                               product.obj_y.location.y,
                                               product.obj_z.location.z))

        cabinet_mesh.parent = obj_bp.parent
        cabinet_mesh.location = product.obj_bp.location
        cabinet_mesh.location.x = x_placement
        cabinet_mesh.rotation_euler = product.obj_bp.rotation_euler
        cabinet_mesh.mv.type = 'CAGE'
        
        #TODO: Draw Fillers, Cabinet Shapes, Cabinet Text
                            
        return {'FINISHED'}
    
def register():
    bpy.utils.register_class(OPERATOR_Draw_Plan)