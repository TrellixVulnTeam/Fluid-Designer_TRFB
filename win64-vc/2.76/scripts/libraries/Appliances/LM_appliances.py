"""
Microvellum 
Appliances 
Stores all of the Logic, Product, and Insert Class definitions for appliances
"""

import fd
import os

ROOT_PATH = os.path.join(os.path.dirname(__file__),"assemblies")
APPLIANCES = os.path.join(ROOT_PATH,"Appliance Assemblies")

HIDDEN_FOLDER_NAME = "_HIDDEN"
APPLIANCE_LIBRARY_NAME = "Appliance Assemblies"

class Parametric_Wall_Appliance(fd.Library_Assembly):
    
    library_name = "Appliances"
    placement_type = "Standard"
    type_assembly = "PRODUCT"
    
    # Name of the category to retrieve the appliance from
    appliance_category = ""
    
    # Name of the appliance in the assembly library
    appliance_name = ""
    
    def draw(self):
        self.create_assembly()
        
        dim_x = self.get_var("dim_x")
        dim_z = self.get_var("dim_z")
        dim_y = self.get_var("dim_y")
        assembly = self.add_assembly(filepath = os.path.join(APPLIANCES,self.appliance_category,self.appliance_name))
        assembly.x_dim('dim_x',[dim_x])
        assembly.y_dim('dim_y',[dim_y])
        assembly.z_dim('dim_z',[dim_z])
        
        self.update()

#---------PRODUCT: PARAMETRIC APPLIANCES
        
class PRODUCT_Refrigerator(Parametric_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.assembly_name = "Refrigerator"
        self.width = fd.inches(36)
        self.height = fd.inches(84)
        self.depth = fd.inches(27)
        self.appliance_category = "Parametric Appliances"
        self.appliance_name = "Professional Refrigerator Generic.blend"
        
class PRODUCT_Range(Parametric_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.assembly_name = "Range"
        self.width = fd.inches(30)
        self.height = fd.inches(42)
        self.depth = fd.inches(28)
        self.appliance_category = "Parametric Appliances"
        self.appliance_name = "Professional Gas Range Generic.blend"
        
class PRODUCT_Dishwasher(Parametric_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.assembly_name = "Dishwasher"
        self.width = fd.inches(24)
        self.height = fd.inches(33.75)
        self.depth = fd.inches(27)
        self.appliance_category = "Parametric Appliances"
        self.appliance_name = "Professional Dishwasher Generic.blend"
        
class PRODUCT_Range_Hood(Parametric_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.assembly_name = "Range Hood"
        self.width = fd.inches(30)
        self.height = fd.inches(14)
        self.depth = fd.inches(12.5)
        self.appliance_category = "Parametric Appliances"
        self.appliance_name = "Wall Mounted Range Hood 01.blend"
        self.height_above_floor = fd.inches(60)
        
def register():
    pass
    
def unregister():
    pass

    