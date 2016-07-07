"""
Microvellum 
Entry Doors 
Stores all of the Logic, Product, and Insert Class definitions for Entry Doors
"""

import bpy
import os

def register():
    lib = bpy.context.window_manager.cabinetlib.lib_products.add()
    lib.module_name = __name__
    lib.lib_path = os.path.join(os.path.dirname(__file__),"products","Entry Doors")
    lib.name = "Entry Doors"
    
def unregister():
    pass

