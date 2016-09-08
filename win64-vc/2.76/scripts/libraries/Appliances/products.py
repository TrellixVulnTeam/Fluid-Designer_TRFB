"""
Microvellum 
Appliances 
Stores all of the Logic, Product, and Insert Class definitions for appliances
"""

import os
from mv import fd_types, unit

ASSEMBLY_PATH = os.path.join(os.path.dirname(__file__),"Parametric Appliances")
MATERIAL_FILE = os.path.join(os.path.dirname(__file__),"materials","materials.blend")

class Parametric_Wall_Appliance(fd_types.Assembly):
    
    library_name = "Appliances"
    type_assembly = "PRODUCT"
    
    # Name of the appliance in the assembly library
    appliance_name = ""
    
    def draw(self):
        self.create_assembly()
        dim_x = self.get_var("dim_x")
        dim_z = self.get_var("dim_z")
        dim_y = self.get_var("dim_y")
        assembly = self.add_assembly(file_path = os.path.join(ASSEMBLY_PATH,self.appliance_name))
        assembly.set_name(os.path.splitext(self.appliance_name)[0])
        assembly.x_dim('dim_x',[dim_x])
        assembly.y_dim('dim_y',[dim_y])
        assembly.z_dim('dim_z',[dim_z])
        assembly.assign_material("Chrome",MATERIAL_FILE,"Chrome")
        assembly.assign_material("Stainless Steel",MATERIAL_FILE,"Stainless Steel")
        assembly.assign_material("Black Anodized Metal",MATERIAL_FILE,"Black Anodized Metal")
        
#---------PRODUCT: PARAMETRIC APPLIANCES
        
class PRODUCT_Refrigerator(Parametric_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.assembly_name = "Refrigerator"
        self.width = unit.inch(36)
        self.height = unit.inch(84)
        self.depth = unit.inch(27)
        self.appliance_name = "Professional Refrigerator Generic.blend"
        
class PRODUCT_Range(Parametric_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.assembly_name = "Range"
        self.width = unit.inch(30)
        self.height = unit.inch(42)
        self.depth = unit.inch(28)
        self.appliance_name = "Professional Gas Range Generic.blend"
        
class PRODUCT_Dishwasher(Parametric_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.assembly_name = "Dishwasher"
        self.width = unit.inch(24)
        self.height = unit.inch(33.75)
        self.depth = unit.inch(27)
        self.appliance_name = "Professional Dishwasher Generic.blend"
        
class PRODUCT_Range_Hood(Parametric_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.assembly_name = "Range Hood"
        self.width = unit.inch(30)
        self.height = unit.inch(14)
        self.depth = unit.inch(12.5)
        self.appliance_name = "Wall Mounted Range Hood 01.blend"
        self.height_above_floor = unit.inch(60)
        
def register():
    pass

    