"""
Microvellum 
Appliances 
Stores all of the Logic, Product, and Insert Class definitions for appliances
"""

import bpy
import os
from . import LM_appliances

def register():
    lib = bpy.context.window_manager.cabinetlib.lib_products.add()
    lib.module_name = __name__
    lib.lib_path = os.path.join(os.path.dirname(__file__),"products","Appliances")
    lib.name = "Appliances"
    
def unregister():
    pass

    