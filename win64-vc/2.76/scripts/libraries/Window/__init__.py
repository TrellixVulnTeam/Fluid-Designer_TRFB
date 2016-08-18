"""
Microvellum 
Windows
Stores all of the Logic, Product, and Insert Class definitions for Windows
"""

import bpy
import os
from . import LM_windows

def register():
    lib = bpy.context.window_manager.cabinetlib.lib_products.add()
    lib.module_name = __name__
    lib.lib_path = os.path.join(os.path.dirname(__file__),"products","Windows")
    lib.name = "Windows"
    
def unregister():
    pass
