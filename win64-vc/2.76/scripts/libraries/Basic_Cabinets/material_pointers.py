'''
Created on Jul 26, 2016

@author: Andrew
'''
from mv import fd_types

CABINET_MATERIAL = ("Plastics","Melamine","White Melamine")
CHROME = ("Metals","Metals","Chrome")

class Material_Pointers():
    
    Basic_Cabinet_Material = fd_types.Material_Pointer(CABINET_MATERIAL)
    Basic_Cabinet_Pull_Material = fd_types.Material_Pointer(CHROME)