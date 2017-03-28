'''
Created on Mar 27, 2017

@author: montes
'''

import bpy
import bgl
import blf

fractions_unicode = {"0.25": "\u00b9\u2044\u2084",
                     "0.5": "\u00b9\u2044\u2082",
                     "0.75": "\u00b3\u2044\u2084",
                     "0.125": "\u00b9\u2044\u2088",
                     "0.375": "\u00b3\u2044\u2088",
                     "0.625": "\u2075\u2044\u2088",
                     "0.875": "\u2077\u2044\u2088",
                     "0.0625": "\u00b9\u2044\u2081\u2086"}

def get_fraction_unicode(value):
    pass

def draw_opengl(self,context):
    context = bpy.context
    if context.window_manager.mv.use_opengl_dimensions:
        region = context.region
        
        if not context.space_data.region_quadviews:
            rv3d = context.space_data.region_3d
        else:
            if context.area.type != 'VIEW_3D' or context.space_data.type != 'VIEW_3D':
                return
            i = -1
            for region in context.area.regions:
                if region.type == 'WINDOW':
                    i += 1
                    if context.region.id == region.id:
                        break
            else:
                return
    
            rv3d = context.space_data.region_quadviews[i]
        
        layers = []
        for x in range(0, 20):
            if bpy.context.scene.layers[x] is True:
                layers.extend([x])
    
        bgl.glEnable(bgl.GL_BLEND)
    
        for obj in context.scene.objects:
            if obj.mv.type == 'VISDIM_A':
                
                for x in range(0, 20):
                    if obj.layers[x] is True:
                        if x in layers:
                            
                            opengl_dim = obj.mv.opengl_dim
                            if not opengl_dim.hide:
                                draw_dimensions(context, obj, opengl_dim, region, rv3d)
                        break
    
        #---------- restore opengl defaults
        bgl.glLineWidth(1)
        bgl.glDisable(bgl.GL_BLEND)
        bgl.glColor4f(0.0, 0.0, 0.0, 1.0)    
    
    else:
        return
    
def draw_dimensions(context, obj, opengl_dim, region, rv3d):
    scene_ogl_dim_props = bpy.context.scene.mv.opengl_dim
    
    pr = scene_ogl_dim_props.gl_precision
    fmt = "%1." + str(pr) + "f"
    
    units = scene_ogl_dim_props.gl_dim_units
    fsize = scene_ogl_dim_props.gl_font_size    
    a_size = scene_ogl_dim_props.gl_arrow_size
    a_type = scene_ogl_dim_props.gl_arrow_type
    b_type = scene_ogl_dim_props.gl_arrow_type
    
