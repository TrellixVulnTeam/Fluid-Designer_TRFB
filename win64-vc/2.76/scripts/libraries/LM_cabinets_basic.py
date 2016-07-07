"""
Microvellum 
Basic Cabinet Library
Stores all the products for the Basic Cabinet Library
"""

import math
import bpy
import fd

import LM_exteriors
import LM_splitters

LIBRARY_NAME = "Cabinets - Basic"
BASE_CATEGORY_NAME = "Base Cabinets"
TALL_CATEGORY_NAME = "Tall Cabinets"
UPPER_CATEGORY_NAME = "Upper Cabinets"
OUTSIDE_CORNER_CATEGORY_NAME = "Outside Corner Cabinets"
INSIDE_CORNER_CATEGORY_NAME = "Inside Corner Cabinets"
TRANSITION_CATEGORY_NAME = "Transition Cabinets"
STARTER_CATEGORY_NAME = "Starter Cabinets"
DRAWER_CATEGORY_NAME = "Drawer Cabinets"
BLIND_CORNER_CATEGORY_NAME = "Blind Corner Cabinets"

#----------CARCASS ASSEMBLIES
HIDDEN_FOLDER_NAME = "_HIDDEN"
BASE_CARCASS = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Carcasses","Base Carcass")
BASE_DIAGONAL_CARCASS = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Carcasses","Base Diagonal Carcass")
BASE_OUTSIDE_CORNER_RADIUS_CARCASS = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Carcasses","Base Outside Corner Radius Carcass")
BASE_OUTSIDE_CORNER_CHAMFERED_CARCASS = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Carcasses","Base Outside Corner Chamfered Carcass")
BASE_PIE_CUT_CARCASS = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Carcasses","Base Pie Cut Carcass")
BASE_TRANSITION_CARCASS = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Carcasses","Base Transition Carcass")
SINK_CARCASS = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Carcasses","Sink Carcass")
SUSPENDED_CARCASS = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Carcasses","Suspended Carcass")
TALL_CARCASS = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Carcasses","Tall Carcass")
TALL_OUTSIDE_CORNER_CHAMFERED_CARCASS = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Carcasses","Tall Outside Corner Chamfered Carcass")
TALL_OUTSIDE_CORNER_RADIUS_CARCASS = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Carcasses","Tall Outside Corner Radius Carcass")
TALL_TRANSITION_CARCASS = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Carcasses","Tall Transition Carcass")
UPPER_CARCASS = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Carcasses","Upper Carcass")
UPPER_DIAGONAL_CARCASS = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Carcasses","Upper Diagonal Carcass")
UPPER_OUTSIDE_CORNER_CHAMFERED_CARCASS = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Carcasses","Upper Outside Corner Chamfered Carcass")
UPPER_OUTSIDE_CORNER_RADIUS_CARCASS = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Carcasses","Upper Outside Corner Radius Carcass")
UPPER_PIE_CUT_CARCASS = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Carcasses","Upper Pie Cut Carcass")
UPPER_TRANSITION_CARCASS = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Carcasses","Upper Transition Carcass")

#----------SHELF ASSEMBLIES
SHELVES = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Shelves","Shelves")
SHELVES_CHAMFERED = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Shelves","Shelves Chamfered")
SHELVES_DIAGONAL = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Shelves","Shelves Diagonal")
SHELVES_PIE_CUT = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Shelves","Shelves Pie Cut")

BLIND_PANEL = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Cut Parts","Part with Edgebanding")
MICROWAVE = (HIDDEN_FOLDER_NAME,"Appliances Assemblies","Microwaves","Conventional Microwave")
VENT = (HIDDEN_FOLDER_NAME,"Appliances Assemblies","Range Hoods","Wall Mounted Range Hood 01")

#----------PRODUCT BASE CLASSES
class Basic_Standard(fd.Library_Assembly):
    """ Standard Basic Cabinet
    """
    
    property_id = "basic_cabinets.basic_cabinet_prompts"
    type_assembly = "PRODUCT"

    """ Type:fd.Library_Assembly - The main carcass used """
    carcass = None
    
    """ Type: tuple of strings - The assembly path of the main carcass used """
    carcass_path = ""
    
    """ Type: string - {Base, Tall, Upper, Sink, Suspended} """
    carcass_type = ""  
    
    """ Type:fd.Library_Assembly - Splitter insert to add to the cabinet """
    splitter = None
    
    """ Type:fd.Library_Assembly - Interior insert to add to the cabinet """
    interior = None
    
    """ Type:fd.Library_Assembly - Exterior insert to add to the cabinet """
    exterior = None
    
    """ Type:bool - This adds an empty opening to the carcass for starter products """
    add_empty_opening = False
    
    """ Type:bool - This adds a microwave below the cabinet. 
                        This is typically only used for upper cabinets """
    add_microwave = False
    
    """ Type:bool - This adds a vent below the cabinet. 
                        This is typically only used for upper cabinets """
    add_vent_hood = False
        
    def set_drivers_for_assembly(self,assembly):
        Width = self.carcass.get_var("dim_x",'Width')
        Height = self.carcass.get_var("dim_z",'Height')
        Depth = self.carcass.get_var("dim_y",'Depth')
        ToeKickHeight = self.carcass.get_var("Toe Kick Height",'ToeKickHeight')
        Material_Thickness = self.carcass.get_var("Material Thickness")
        
        assembly.x_loc('Material_Thickness',[Material_Thickness])
        assembly.y_loc('Depth',[Depth])
        
        if self.carcass_type in {"Base","Tall","Sink"}:
            assembly.z_loc('ToeKickHeight+Material_Thickness',[ToeKickHeight,Material_Thickness])
            assembly.z_dim('fabs(Height)-Material_Thickness*2-ToeKickHeight',[Height,Material_Thickness,ToeKickHeight])
            
        if self.carcass_type in {"Upper","Suspended"}:
            self.mirror_z = True
            assembly.z_loc('Height+Material_Thickness',[Height,Material_Thickness])        
            assembly.z_dim('fabs(Height)-Material_Thickness*2',[Height,Material_Thickness])
            
        assembly.x_rot(value = 0)
        assembly.y_rot(value = 0)
        assembly.z_rot(value = 0)            
        assembly.x_dim('Width-Material_Thickness*2',[Width,Material_Thickness])
        assembly.y_dim('fabs(Depth)-Material_Thickness',[Depth,Material_Thickness])   
        
    def draw(self):
        self.create_assembly()
        
        Product_Width = self.get_var('dim_x','Product_Width')
        Product_Height = self.get_var('dim_z','Product_Height')
        Product_Depth = self.get_var('dim_y','Product_Depth')
        
        self.carcass = self.add_assembly(self.carcass_path)
        self.carcass.obj_bp.parent = self.obj_bp
        self.carcass.x_loc(value = 0)
        self.carcass.y_loc(value = 0)
        self.carcass.z_loc(value = 0)
        self.carcass.x_rot(value = 0)
        self.carcass.y_rot(value = 0)
        self.carcass.z_rot(value = 0)
        self.carcass.x_dim('Product_Width',[Product_Width])
        self.carcass.y_dim('Product_Depth',[Product_Depth])
        self.carcass.z_dim('Product_Height',[Product_Height])

        vdim_x = fd.Dimension()
        vdim_x.parent(self.obj_bp)
        
        if self.mirror_z:
            vdim_x.start_z(value = fd.inches(5))
        else:
            vdim_x.start_z(value = -fd.inches(5))
            
        if self.carcass_type == 'Upper':
            vdim_x.start_y(value = fd.inches(8))
        else:
            vdim_x.start_y(value = fd.inches(3))
            
        vdim_x.end_x('Product_Width',[Product_Width])
        
        if self.splitter:
            self.splitter.draw()
            self.splitter.obj_bp.parent = self.obj_bp
            self.set_drivers_for_assembly(self.splitter)
             
        if self.interior:
            interior_assembly = self.add_assembly(self.interior)
            self.set_drivers_for_assembly(interior_assembly)
 
        if self.exterior:
            self.exterior.draw()
            self.exterior.obj_bp.parent = self.obj_bp
            self.set_drivers_for_assembly(self.exterior)
  
        if self.add_empty_opening:
            pass
              
        if self.add_vent_hood:
            self.add_prompt(name="Vent Height",prompt_type='DISTANCE',value= fd.inches(14),tab_index=0,export=False)
            Vent_Height = self.get_var('Vent Height')
            vent = self.add_assembly(VENT)
            vent.set_name("Vent")
            vent.x_loc(value = 0)
            vent.y_loc(value = 0)
            vent.z_loc('Product_Height-Vent_Height',[Product_Height,Vent_Height])
            vent.x_dim('Product_Width',[Product_Width])
            vent.y_dim('Product_Depth',[Product_Depth])
            vent.z_dim('Vent_Height',[Vent_Height])
              
        if self.add_microwave:
            vent = self.add_assembly(MICROWAVE)
            vent.set_name("Microwave")
            vent.x_loc(value = 0)
            vent.y_loc(value = 0)
            vent.z_loc('Product_Height',[Product_Height])
            vent.x_dim('Product_Width',[Product_Width])
            vent.y_dim('Product_Depth',[Product_Depth])
            
        self.update()        
        
class Inside_Corner(fd.Library_Assembly):
    
    property_id = "basic_cabinets.basic_cabinet_prompts"
    type_assembly = "PRODUCT"
    placement_type = "Corner"
    
    """ Type:fd.Library_Assembly - The main carcass used """
    carcass = None
    
    """ Type: tuple of strings - The assembly path of the main carcass used """
    carcass_path = ""
    
    """ Type: string - {Base, Upper} """
    carcass_type = ""     
    
    """ Type: string - {Notched, Diagonal} """
    carcass_shape = ""      
    
    """ Type:fd.Library_Assembly - Interior insert to add to the cabinet """
    interior = None
    
    """ Type:fd.Library_Assembly - Exterior insert to add to the cabinet """
    exterior = None    
    
    def set_drivers_for_assembly(self,assembly):
        Width = self.carcass.get_var("dim_x",'Width')
        Height = self.carcass.get_var("dim_z",'Height')
        Depth = self.carcass.get_var("dim_y",'Depth')
        
    def add_pie_cut_doors(self):
        Width = self.carcass.get_var("dim_x",'Width')
        Height = self.carcass.get_var("dim_z",'Height')
        Depth = self.carcass.get_var("dim_y",'Depth')
        ToeKickHeight = self.carcass.get_var("Toe Kick Height",'ToeKickHeight')
        Material_Thickness = self.carcass.get_var("Material Thickness")    
        Left_Side_Depth = self.carcass.get_var("Left Side Depth")
        Right_Side_Depth = self.carcass.get_var("Right Side Depth")            
        
        self.exterior.draw()
        self.exterior.obj_bp.parent = self.obj_bp
        
        self.exterior.x_loc('Left_Side_Depth',[Left_Side_Depth])
        self.exterior.y_loc('-Right_Side_Depth',[Right_Side_Depth])
        
        self.exterior.x_rot(value = 0)
        self.exterior.y_rot(value = 0)
        self.exterior.z_rot(value = 0)
        
        self.exterior.x_dim('Width-Left_Side_Depth-Material_Thickness',[Width,Left_Side_Depth,Material_Thickness])
        self.exterior.y_dim('Depth+Right_Side_Depth+Material_Thickness',[Depth,Right_Side_Depth,Material_Thickness])      
        
        if self.carcass_type == "Base":
            self.exterior.z_loc('ToeKickHeight+Material_Thickness',[ToeKickHeight, Material_Thickness])
            self.exterior.z_dim('fabs(Height)-ToeKickHeight-Material_Thickness',[Height,ToeKickHeight,Material_Thickness])  
            
        if self.carcass_type == "Upper":
            self.exterior.z_loc('Height+Material_Thickness',[Height,Material_Thickness])
            self.exterior.z_dim('fabs(Height)-Material_Thickness*2',[Height,Material_Thickness])         
        
    def add_diagonal_doors(self):
        Width = self.carcass.get_var("dim_x",'Width')
        Height = self.carcass.get_var("dim_z",'Height')
        Depth = self.carcass.get_var("dim_y",'Depth')
        ToeKickHeight = self.carcass.get_var("Toe Kick Height",'ToeKickHeight')
        Material_Thickness = self.carcass.get_var("Material Thickness")    
        Left_Side_Depth = self.carcass.get_var("Left Side Depth")
        Right_Side_Depth = self.carcass.get_var("Right Side Depth") 
        
        self.exterior.draw()
        self.exterior.obj_bp.parent = self.obj_bp
        self.exterior.x_loc('Left_Side_Depth',[Left_Side_Depth])
        self.exterior.y_loc('Depth+Material_Thickness',[Depth,Material_Thickness])
        
        self.exterior.x_rot(value = 0)
        self.exterior.y_rot(value = 0)        
        self.exterior.z_rot('atan((fabs(Depth)-Material_Thickness-Right_Side_Depth)/(fabs(Width)-Material_Thickness-Left_Side_Depth))',
                            [Depth,Material_Thickness,Right_Side_Depth,Width,Left_Side_Depth])
        
        self.exterior.x_dim('sqrt(((fabs(Depth)-Material_Thickness-Right_Side_Depth)**2)+((fabs(Width)-Material_Thickness-Left_Side_Depth)**2))',
                    [Depth,Material_Thickness,Right_Side_Depth,Width,Left_Side_Depth])
        self.exterior.y_dim('Depth+Right_Side_Depth+Material_Thickness',[Depth, Right_Side_Depth,Material_Thickness])     
        self.exterior.z_dim('fabs(Height)-ToeKickHeight-Material_Thickness*2',[Height,ToeKickHeight,Material_Thickness])  
        
        if self.carcass_type == "Base":
            self.exterior.z_loc('ToeKickHeight+Material_Thickness',[ToeKickHeight,Material_Thickness])
            
        if self.carcass_type == "Upper":
            self.exterior.z_loc('Height+Material_Thickness',[Height,Material_Thickness])
        
    def draw(self):
        self.create_assembly()

        Product_Width = self.get_var('dim_x','Product_Width')
        Product_Height = self.get_var('dim_z','Product_Height')
        Product_Depth = self.get_var('dim_y','Product_Depth')
        
        self.carcass = self.add_assembly(self.carcass_path)
        self.carcass.obj_bp.parent = self.obj_bp
        
        self.carcass.x_loc(value = 0)
        self.carcass.y_loc(value = 0)
        self.carcass.z_loc(value = 0)
        
        self.carcass.x_rot(value = 0)
        self.carcass.y_rot(value = 0)
        self.carcass.z_rot(value = 0)
        self.carcass.x_dim('Product_Width',[Product_Width])
        self.carcass.y_dim('Product_Depth',[Product_Depth])
        self.carcass.z_dim('Product_Height',[Product_Height])
        
        if self.carcass_shape == 'Notched':
            self.product_shape = 'INSIDE_NOTCH'
            if self.exterior:
                self.add_pie_cut_doors()
          
        if self.carcass_shape == 'Diagonal':
            self.product_shape = 'INSIDE_DIAGONAL'
            if self.exterior:
                self.add_diagonal_doors()

        self.update()            
        
class Outside_Corner(fd.Library_Assembly):
    
    property_id = "basic_cabinets.basic_cabinet_prompts"
    type_assembly = "PRODUCT"
    placement_type = "Corner"

    """ Type:fd.Library_Assembly - The main carcass used """
    carcass = None
    
    """ Type: tuple of strings - The assembly path of the main carcass used """
    carcass_path = ""    
    
    """ Type: string - {Base, Upper} """
    carcass_type = ""     
    
    """ Type: string - {Notched, Diagonal} """
    carcass_shape = ""      
    
    """ Type:fd.Library_Assembly - Interior insert to add to the cabinet """
    interior = None
    
    """ Type:fd.Library_Assembly - Exterior insert to add to the cabinet """
    exterior = None 
    
    def draw(self):
        self.create_assembly()

        Product_Height = self.get_var('dim_z','Product_Height')
        Product_Depth = self.get_var('dim_y','Product_Depth')
        
        self.carcass = self.add_assembly(self.carcass_path)
        self.carcass.obj_bp.parent = self.obj_bp
        self.carcass.x_loc(value = 0)
        self.carcass.y_loc(value = 0)
        self.carcass.z_loc(value = 0)
        self.carcass.x_rot(value = 0)
        self.carcass.y_rot(value = 0)
        self.carcass.z_rot(value = 0)
        self.carcass.x_dim('fabs(Product_Depth)',[Product_Depth])
        self.carcass.y_dim('Product_Depth',[Product_Depth])
        self.carcass.z_dim('Product_Height',[Product_Height])
        
        if self.carcass_shape == 'Notched':
            self.product_shape = 'OUTSIDE_NOTCH'
            if self.exterior:
                pass #TODO
        
        if self.carcass_shape == 'Diagonal':
            self.product_shape = 'OUTSIDE_DIAGONAL'
            if self.exterior:
                pass #TODO
            
        if self.carcass_shape == 'Radius':
            self.product_shape = 'OUTSIDE_RADIUS'
            if self.exterior:
                pass #TODO            
        
        self.update()        

class Blind_Corner(fd.Library_Assembly):
    
    property_id = "basic_cabinets.basic_cabinet_prompts"
    type_assembly = "PRODUCT"
    product_shape = "RECTANGLE"
    
    blind_side = "Left" # {Left, Right}
    
    """ Type:fd.Library_Assembly - The main carcass used """
    carcass = None
    
    """ Type: tuple of strings - The assembly path of the main carcass used """
    carcass_path = ""    
    
    """ Type: string - {Base, Tall, Upper} """
    carcass_type = ""     
    
    """ Type:fd.Library_Assembly - Splitter insert to add to the cabinet """
    splitter = None
    
    """ Type:fd.Library_Assembly - Interior insert to add to the cabinet """
    interior = None
    
    """ Type:fd.Library_Assembly - Exterior insert to add to the cabinet """
    exterior = None 
    
    def draw(self):
        g = bpy.context.scene.lm_frameless_cabinets
        self.create_assembly()
        
        self.carcass = self.add_assembly(self.carcass_path)
        self.carcass.obj_bp.parent = self.obj_bp

        self.add_tab(name='Blind Corner Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        if self.carcass_type == 'Base':
            self.add_prompt(name="Blind Panel Width",prompt_type='DISTANCE',value=g.Base_Cabinet_Depth,tab_index=0)
            
        if self.carcass_type == 'Tall':
            self.add_prompt(name="Blind Panel Width",prompt_type='DISTANCE',value=g.Tall_Cabinet_Depth,tab_index=0)
            
        if self.carcass_type == 'Upper':
            self.mirror_z = True
            self.add_prompt(name="Blind Panel Width",prompt_type='DISTANCE',value=g.Upper_Cabinet_Depth,tab_index=0)
            
        self.add_prompt(name="Blind Panel Reveal",prompt_type='DISTANCE',value=g.Blind_Panel_Reveal,tab_index=0)
        self.add_prompt(name="Inset Blind Panel",prompt_type='CHECKBOX',value=g.Inset_Blind_Panel,tab_index=0)
        self.add_prompt(name="Blind Panel Thickness",prompt_type='DISTANCE',value=fd.inches(.75),tab_index=1)
        
        Product_Width = self.get_var('dim_x','Product_Width')
        Product_Height = self.get_var('dim_z','Product_Height')
        Product_Depth = self.get_var('dim_y','Product_Depth')
        Blind_Panel_Width = self.get_var('Blind Panel Width')
        Blind_Panel_Reveal = self.get_var('Blind Panel Reveal')
        Inset_Blind_Panel = self.get_var('Inset Blind Panel')
        Carcass_Width = self.carcass.get_var("dim_x",'Carcass_Width')
        Carcass_Depth = self.carcass.get_var("dim_y",'Carcass_Depth')
        Carcass_Height = self.carcass.get_var("dim_z",'Carcass_Height')
        Toe_Kick_Height = self.carcass.get_var("Toe Kick Height")
        Material_Thickness = self.carcass.get_var("Material Thickness")
        
        self.carcass.x_loc(value = 0)
        self.carcass.y_loc(value = 0)
        self.carcass.z_loc(value = 0)
        self.carcass.x_rot(value = 0)
        self.carcass.y_rot(value = 0)
        self.carcass.z_rot(value = 0)
        self.carcass.x_dim('Product_Width',[Product_Width])
        self.carcass.y_dim('Product_Depth',[Product_Depth])
        self.carcass.z_dim('Product_Height',[Product_Height])
        
        blind_panel = self.add_assembly(BLIND_PANEL)
        blind_panel.obj_bp.mv.name_object = "Blind Panel"
        
        if self.blind_side == "Left":
            blind_panel.x_loc('IF(Inset_Blind_Panel,Material_Thickness,0)',[Inset_Blind_Panel,Material_Thickness])
            blind_panel.y_dim('(Blind_Panel_Width+Blind_Panel_Reveal-IF(Inset_Blind_Panel,Material_Thickness,0))*-1',
                              [Blind_Panel_Width,Blind_Panel_Reveal,Inset_Blind_Panel,Material_Thickness])
                        
        if self.blind_side == "Right":
            blind_panel.x_loc('Carcass_Width-IF(Inset_Blind_Panel,Material_Thickness,0)',
                              [Carcass_Width,Inset_Blind_Panel,Material_Thickness])
            blind_panel.y_dim('Blind_Panel_Width+Blind_Panel_Reveal-IF(Inset_Blind_Panel,Material_Thickness,0)',
                              [Blind_Panel_Width,Blind_Panel_Reveal,Material_Thickness,Inset_Blind_Panel])
            
        blind_panel.y_loc('Carcass_Depth+IF(Inset_Blind_Panel,Material_Thickness,0)',
                          [Carcass_Depth,Inset_Blind_Panel,Material_Thickness])
        
        if self.carcass_type in {"Base","Tall","Sink"}:
            blind_panel.z_loc('Toe_Kick_Height+IF(Inset_Blind_Panel,Material_Thickness,0)',
                              [Toe_Kick_Height,Inset_Blind_Panel,Material_Thickness])
            blind_panel.x_dim('Carcass_Height-Toe_Kick_Height-IF(Inset_Blind_Panel,Material_Thickness*2,0)',
                              [Carcass_Height,Toe_Kick_Height,Inset_Blind_Panel,Material_Thickness])
            
        if self.carcass_type in {"Upper","Suspended"}:
            blind_panel.z_loc('Carcass_Height+Material_Thickness-IF(Inset_Blind_Panel,0,Material_Thickness)',
                              [Carcass_Height,Inset_Blind_Panel,Material_Thickness])
            blind_panel.x_dim('fabs(Carcass_Height)-Material_Thickness*2+IF(Inset_Blind_Panel,0,Material_Thickness*2)',
                              [Carcass_Height,Material_Thickness,Inset_Blind_Panel])
            
        blind_panel.x_rot(value = 0)
        blind_panel.y_rot(value = -90)
        blind_panel.z_rot(value = 90)
        
        if self.splitter:
            self.splitter.draw()
            self.splitter.obj_bp.parent = self.obj_bp
               
            self.splitter.y_loc('Carcass_Depth',[Carcass_Depth])
            self.splitter.x_rot(value = 0)
            self.splitter.y_rot(value = 0)
            self.splitter.z_rot(value = 0)
            self.splitter.y_dim('fabs(Carcass_Depth)-Material_Thickness-IF(Inset_Blind_Panel,Material_Thickness,0)',
                                [Carcass_Depth,Inset_Blind_Panel,Material_Thickness])                    
            
            if self.carcass_type in {"Base","Tall","Sink"}:
                self.splitter.z_loc('Toe_Kick_Height+Material_Thickness',[Toe_Kick_Height,Material_Thickness])
                self.splitter.z_dim('fabs(Carcass_Height)-Toe_Kick_Height-Material_Thickness*2',
                                    [Carcass_Height,Material_Thickness,Toe_Kick_Height])
                
            if self.carcass_type in {"Upper","Suspended"}:
                self.splitter.z_loc('Carcass_Height+Material_Thickness',[Carcass_Height,Material_Thickness])    
                self.splitter.z_dim('fabs(Carcass_Height)-Material_Thickness*2',[Carcass_Height,Material_Thickness])        
            
            if self.blind_side == "Left":
                self.splitter.x_loc('Blind_Panel_Width+Blind_Panel_Reveal',[Blind_Panel_Width,Blind_Panel_Reveal])
                self.splitter.x_dim('Carcass_Width-(Blind_Panel_Width+Blind_Panel_Reveal+Material_Thickness)',
                                    [Carcass_Width,Blind_Panel_Width,Blind_Panel_Reveal,Material_Thickness])
            else:
                self.splitter.x_loc('Material_Thickness',[Material_Thickness])  
                self.splitter.x_dim('Carcass_Width-(Blind_Panel_Width+Blind_Panel_Reveal+Material_Thickness)',
                                    [Carcass_Width,Blind_Panel_Width,Blind_Panel_Reveal,Material_Thickness])

            
        if self.interior:
            interior = self.add_assembly(self.interior)
            
            interior.x_loc('Material_Thickness',[Material_Thickness])
            interior.y_loc('Carcass_Depth+Material_Thickness',[Carcass_Depth,Material_Thickness])
            interior.x_rot(value = 0)
            interior.y_rot(value = 0)
            interior.z_rot(value = 0)
            interior.x_dim('Carcass_Width-Material_Thickness*2',[Carcass_Width,Material_Thickness])
            interior.y_dim('-Carcass_Depth-Material_Thickness*2',[Carcass_Depth,Material_Thickness])
            
            if self.carcass_type in {"Base","Tall","Sink"}:
                interior.z_loc('Toe_Kick_Height+Material_Thickness',[Toe_Kick_Height,Material_Thickness])
                interior.z_dim('Carcass_Height-Toe_Kick_Height-Material_Thickness*2',
                               [Carcass_Height,Toe_Kick_Height,Material_Thickness])
            
            if self.carcass_type in {"Upper","Suspended"}:
                interior.z_loc('Carcass_Height+Material_Thickness',[Carcass_Height,Material_Thickness])
                interior.z_dim('fabs(Carcass_Height)-Material_Thickness*2',[Carcass_Height,Material_Thickness])
            
        if self.exterior:
            self.exterior.draw()
            self.exterior.obj_bp.parent = self.obj_bp
                
            self.exterior.y_loc('Carcass_Depth',[Carcass_Depth])
            self.exterior.x_rot(value = 0)
            self.exterior.y_rot(value = 0)
            self.exterior.z_rot(value = 0)
            self.exterior.y_dim('fabs(Carcass_Depth)-Material_Thickness-IF(Inset_Blind_Panel,Material_Thickness,0)',
                                [Carcass_Depth,Inset_Blind_Panel,Material_Thickness])

            if self.carcass_type in {"Base","Tall","Sink"}:
                self.exterior.z_loc('Toe_Kick_Height+Material_Thickness',[Toe_Kick_Height,Material_Thickness])
                self.exterior.z_dim('fabs(Carcass_Height)-Toe_Kick_Height-Material_Thickness*2',
                                    [Carcass_Height,Material_Thickness,Toe_Kick_Height])
                
            if self.carcass_type in {"Upper","Suspended"}:
                self.exterior.z_loc('Carcass_Height+Material_Thickness',[Carcass_Height,Material_Thickness])
                self.exterior.z_dim('fabs(Carcass_Height)-Material_Thickness*2',[Carcass_Height,Material_Thickness])
            
            if self.blind_side == "Left":
                self.exterior.x_loc('Blind_Panel_Width+Blind_Panel_Reveal',[Blind_Panel_Width,Blind_Panel_Reveal])
                self.exterior.x_dim('Carcass_Width-(Blind_Panel_Width+Blind_Panel_Reveal+Material_Thickness)',
                                    [Carcass_Width,Blind_Panel_Width,Blind_Panel_Reveal,Material_Thickness])
            else:
                self.exterior.x_loc('Material_Thickness',[Material_Thickness])
                self.exterior.x_dim('Carcass_Width-(Blind_Panel_Width+Blind_Panel_Reveal+Material_Thickness)',
                                    [Carcass_Width,Blind_Panel_Width,Blind_Panel_Reveal,Material_Thickness])
                
        self.update()

class Transition(fd.Library_Assembly):
    
    property_id = "basic_cabinets.basic_cabinet_prompts"
    type_assembly = "PRODUCT"
    
    """ Type:fd.Library_Assembly - The main carcass used """
    carcass = None
    
    """ Type: string - {Base, Tall, Upper} """
    carcass_type = ""  
    
    """ Type:fd.Library_Assembly - Interior insert to add to the cabinet """
    interior = None
    
    """ Type:fd.Library_Assembly - Exterior insert to add to the cabinet """
    exterior = None  
        
    def add_doors(self):
        Width = self.carcass.get_var("dim_x",'Width')
        Height = self.carcass.get_var("dim_z",'Height')
        Depth = self.carcass.get_var("dim_y",'Depth')
        ToeKickHeight = self.carcass.get_var("Toe Kick Height",'ToeKickHeight')
        Material_Thickness = self.carcass.get_var("Material Thickness")
        Left_Side_Depth = self.carcass.get_var("Left Side Depth")
        Right_Side_Depth = self.carcass.get_var("Right Side Depth")
        
        self.exterior.draw()
        self.exterior.obj_bp.parent = self.obj_bp
        self.exterior.x_loc('Material_Thickness',[Material_Thickness])
        self.exterior.y_loc('-Left_Side_Depth',[Left_Side_Depth])
        self.exterior.x_rot(value = 0)
        self.exterior.y_rot(value = 0)
        self.exterior.z_rot('atan((Left_Side_Depth-Right_Side_Depth)/(Width-Material_Thickness*2))',
                            [Width, Material_Thickness,Right_Side_Depth,Left_Side_Depth])
        self.exterior.x_dim('sqrt(((Left_Side_Depth-Right_Side_Depth)**2)+((Width-Material_Thickness*2)**2))',
                            [Width, Material_Thickness,Right_Side_Depth,Left_Side_Depth])
        self.exterior.y_dim('Depth+Right_Side_Depth+Material_Thickness',[Depth,Right_Side_Depth,Material_Thickness])
        self.exterior.z_dim('fabs(Height)-(ToeKickHeight+Material_Thickness*2)',[Height,Material_Thickness,ToeKickHeight])
        
        if self.carcass_type in {"Base","Tall"}:
            self.exterior.z_loc('ToeKickHeight+Material_Thickness',[Material_Thickness, ToeKickHeight])
        if self.carcass_type == "Upper":
            self.exterior.z_loc('Height+Material_Thickness',[Height,Material_Thickness])        
        
    def draw(self):
        self.create_assembly()

        Product_Width = self.get_var('dim_x','Product_Width')
        Product_Height = self.get_var('dim_z','Product_Height')
        Product_Depth = self.get_var('dim_y','Product_Depth')
        
        self.carcass = self.add_assembly(self.carcass_path)
        self.carcass.obj_bp.parent = self.obj_bp
        self.carcass.x_loc(value = 0)
        self.carcass.y_loc(value = 0)
        self.carcass.z_loc(value = 0)
        self.carcass.x_rot(value = 0)
        self.carcass.y_rot(value = 0)
        self.carcass.z_rot(value = 0)
        self.carcass.x_dim('Product_Width',[Product_Width])
        self.carcass.y_dim('Product_Depth',[Product_Depth])
        self.carcass.z_dim('Product_Height',[Product_Height])
        
        if self.exterior:
            self.add_doors()

        self.update()

#----------PRODUCTS: Base Cabinets

class PRODUCT_1_Door_Base(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.assembly_name = "1 Door Base"
        self.width = g.Width_1_Door
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Cabinet_Depth
        self.carcass_path = BASE_CARCASS
        self.carcass_type =  "Base"
        self.exterior = LM_exteriors.INSERT_Base_Single_Door()
        self.interior = SHELVES
        
class PRODUCT_2_Door_Base(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.assembly_name = "2 Door Base"
        self.width = g.Width_2_Door
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Cabinet_Depth
        self.carcass_path = BASE_CARCASS
        self.carcass_type =  "Base"
        self.exterior = LM_exteriors.INSERT_Base_Double_Door()  
        self.interior = SHELVES     
        
class PRODUCT_2_Door_Sink(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.assembly_name = "2 Door Sink"
        self.width = g.Width_2_Door
        self.height = g.Sink_Cabinet_Height
        self.depth = g.Sink_Cabinet_Depth
        self.carcass_path = SINK_CARCASS
        self.carcass_type =  "Base"
        self.exterior = LM_exteriors.INSERT_Base_Double_Door()
        self.interior = None        
        
class PRODUCT_2_Door_with_False_Front_Sink(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.assembly_name = "2 Door with False Front Sink"
        self.width = g.Width_2_Door
        self.height = g.Sink_Cabinet_Height
        self.depth = g.Sink_Cabinet_Depth
        self.carcass_path = SINK_CARCASS
        self.carcass_type =  "Base"
        self.exterior = LM_exteriors.INSERT_Base_Double_Door_With_False_Front()
        self.interior = None       
        
class PRODUCT_2_Door_2_False_Front_Sink(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.assembly_name = "2 Door 2 False Front Sink"
        self.width = g.Width_2_Door
        self.height = g.Sink_Cabinet_Height
        self.depth = g.Sink_Cabinet_Depth
        self.carcass_path = SINK_CARCASS
        self.carcass_type =  "Base"
        self.exterior = LM_exteriors.INSERT_Base_Double_Door_With_2_False_Front()
        self.interior = None         
        
class PRODUCT_1_Door_Sink(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.assembly_name = "1 Door Sink"
        self.width = g.Width_1_Door
        self.height = g.Sink_Cabinet_Height
        self.depth = g.Sink_Cabinet_Depth
        self.carcass_path = SINK_CARCASS
        self.carcass_type =  "Base"
        self.exterior = LM_exteriors.INSERT_Base_Single_Door()
        self.interior = None 
        
class PRODUCT_1_Door_1_Drawer_Base(Basic_Standard):
     
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.assembly_name = "1 Door 1 Drawer Base"
        self.width = g.Width_1_Door
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Cabinet_Depth
        self.carcass_path = BASE_CARCASS
        self.carcass_type =  "Base"
        self.splitter = LM_splitters.INSERT_2_Vertical_Openings()
        self.splitter.opening_1_height = g.Top_Drawer_Front_Height - fd.inches(1)
        self.splitter.exterior_1 = LM_exteriors.INSERT_1_Drawer()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.interior_2 = None
        self.splitter.exterior_2 = LM_exteriors.INSERT_Base_Single_Door()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}    
        
class PRODUCT_2_Door_2_Drawer_Base(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.assembly_name = "2 Door 2 Drawer Base"
        self.width = g.Width_2_Door
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Cabinet_Depth
        self.carcass_path = BASE_CARCASS
        self.carcass_type =  "Base"
        self.splitter = LM_splitters.INSERT_2_Vertical_Openings()
        self.splitter.opening_1_height = g.Top_Drawer_Front_Height - fd.inches(1)
        self.splitter.exterior_1 = LM_exteriors.INSERT_Horizontal_Drawers()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.interior_2 = None
        self.splitter.exterior_2 = LM_exteriors.INSERT_Base_Double_Door()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}    
        
class PRODUCT_Microwave_2_Door_Base(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.assembly_name = "Microwave 2 Door Base"
        self.width = g.Width_2_Door
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Cabinet_Depth
        self.carcass_path = BASE_CARCASS
        self.carcass_type =  "Base"
        self.splitter = LM_splitters.INSERT_2_Vertical_Openings()
        self.splitter.exterior_2 = LM_exteriors.INSERT_Base_Double_Door()            
        
class PRODUCT_Microwave_2_Drawer_Base(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.assembly_name = "Microwave 2 Drawer Base"
        self.width = g.Width_2_Door
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Cabinet_Depth
        self.carcass_path = BASE_CARCASS
        self.carcass_type =  "Base"
        self.splitter = LM_splitters.INSERT_2_Vertical_Openings()
        self.splitter.exterior_2 = LM_exteriors.INSERT_2_Drawer_Stack()                  
        
#---------PRODUCTS: Drawer Cabinets
        
class PRODUCT_1_Drawer(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = DRAWER_CATEGORY_NAME
        self.assembly_name = "1 Drawer"
        self.width = g.Width_Drawer
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Cabinet_Depth
        self.carcass_path = BASE_CARCASS
        self.carcass_type =  "Base"
        self.exterior = LM_exteriors.INSERT_1_Drawer()       
        
class PRODUCT_2_Drawer(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = DRAWER_CATEGORY_NAME
        self.assembly_name = "2 Drawer"
        self.width = g.Width_Drawer
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Cabinet_Depth
        self.carcass_path = BASE_CARCASS
        self.carcass_type =  "Base"
        self.exterior = LM_exteriors.INSERT_2_Drawer_Stack()
        if not g.Equal_Drawer_Stack_Heights:
            self.exterior.top_drawer_front_height = g.Top_Drawer_Front_Height         
            
class PRODUCT_3_Drawer(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = DRAWER_CATEGORY_NAME
        self.assembly_name = "3 Drawer"
        self.width = g.Width_Drawer
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Cabinet_Depth
        self.carcass_path = BASE_CARCASS
        self.carcass_type =  "Base"
        self.exterior = LM_exteriors.INSERT_3_Drawer_Stack()
        if not g.Equal_Drawer_Stack_Heights:
            self.exterior.top_drawer_front_height = g.Top_Drawer_Front_Height     
            
class PRODUCT_4_Drawer(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = DRAWER_CATEGORY_NAME
        self.assembly_name = "4 Drawer"
        self.width = g.Width_Drawer
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Cabinet_Depth
        self.carcass_path = BASE_CARCASS
        self.carcass_type =  "Base"
        self.exterior = LM_exteriors.INSERT_4_Drawer_Stack()
        if not g.Equal_Drawer_Stack_Heights:
            self.exterior.top_drawer_front_height = g.Top_Drawer_Front_Height                   
        
#---------PRODUCTS: Suspended Cabinets

class PRODUCT_1_Drawer_Suspended(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = DRAWER_CATEGORY_NAME
        self.assembly_name = "1 Drawer Suspended"
        self.width = g.Width_Drawer
        self.height = g.Suspended_Cabinet_Height
        self.depth = g.Suspended_Cabinet_Depth
        self.mirror_z = True
        self.carcass_path = SUSPENDED_CARCASS
        self.carcass_type =  "Suspended"
        self.height_above_floor = g.Base_Cabinet_Height
        self.exterior = LM_exteriors.INSERT_1_Drawer()
        
class PRODUCT_2_Drawer_Suspended(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = DRAWER_CATEGORY_NAME
        self.assembly_name = "2 Drawer Suspended"
        self.width = g.Width_Drawer * 2
        self.height = g.Suspended_Cabinet_Height
        self.depth = g.Suspended_Cabinet_Depth
        self.mirror_z = True
        self.carcass_path = SUSPENDED_CARCASS
        self.carcass_type =  "Suspended"
        self.height_above_floor = g.Base_Cabinet_Height
        self.exterior = LM_exteriors.INSERT_Horizontal_Drawers()        
        
#---------PRODUCTS: Tall Cabinets        

class PRODUCT_1_Door_Tall(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = TALL_CATEGORY_NAME
        self.assembly_name = "1 Door Tall"
        self.width = g.Width_1_Door
        self.height = g.Tall_Cabinet_Height
        self.depth = g.Tall_Cabinet_Depth
        self.carcass_path = TALL_CARCASS
        self.carcass_type = "Tall"
        self.exterior = LM_exteriors.INSERT_Tall_Single_Door()
        self.interior = None
        
class PRODUCT_2_Door_Tall(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = TALL_CATEGORY_NAME
        self.assembly_name = "2 Door Tall"
        self.width = g.Width_2_Door
        self.height = g.Tall_Cabinet_Height
        self.depth = g.Tall_Cabinet_Depth
        self.carcass_path = TALL_CARCASS
        self.carcass_type = "Tall"
        self.exterior = LM_exteriors.INSERT_Tall_Double_Door()
        self.interior = None    
        
class PRODUCT_1_Double_Door_Tall(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = TALL_CATEGORY_NAME
        self.assembly_name = "1 Double Door Tall"
        self.width = g.Width_1_Door
        self.height = g.Tall_Cabinet_Height
        self.depth = g.Tall_Cabinet_Depth
        self.carcass_path = TALL_CARCASS
        self.carcass_type = "Tall"
        self.splitter = LM_splitters.INSERT_2_Vertical_Openings()
        self.splitter.exterior_1 = LM_exteriors.INSERT_Upper_Single_Door()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.interior_2 = None
        self.splitter.exterior_2 = LM_exteriors.INSERT_Base_Single_Door()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}        
        
class PRODUCT_2_Double_Door_Tall(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = TALL_CATEGORY_NAME
        self.assembly_name = "2 Double Door Tall"
        self.width = g.Width_2_Door
        self.height = g.Tall_Cabinet_Height
        self.depth = g.Tall_Cabinet_Depth
        self.carcass_path = TALL_CARCASS
        self.carcass_type = "Tall"
        self.splitter = LM_splitters.INSERT_2_Vertical_Openings()
        self.splitter.exterior_1 = LM_exteriors.INSERT_Upper_Double_Door()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.interior_2 = None
        self.splitter.exterior_2 = LM_exteriors.INSERT_Base_Double_Door()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}   
        
class PRODUCT_2_Door_2_Drawer_Tall(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = TALL_CATEGORY_NAME
        self.assembly_name = "2 Door 2 Drawer Tall"
        self.width = g.Width_2_Door
        self.height = g.Tall_Cabinet_Height
        self.depth = g.Tall_Cabinet_Depth
        self.carcass_path = TALL_CARCASS
        self.carcass_type = "Tall"
        self.splitter = LM_splitters.INSERT_2_Vertical_Openings()
        self.splitter.opening_2_height = fd.inches(20)
        self.splitter.exterior_1 = LM_exteriors.INSERT_Tall_Double_Door()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.interior_1 = None
        self.splitter.exterior_2 = LM_exteriors.INSERT_2_Drawer_Stack()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}   
        
class PRODUCT_2_Door_3_Drawer_Tall(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = TALL_CATEGORY_NAME
        self.assembly_name = "2 Door 3 Drawer Tall"
        self.width = g.Width_2_Door
        self.height = g.Tall_Cabinet_Height
        self.depth = g.Tall_Cabinet_Depth
        self.carcass_path = TALL_CARCASS
        self.carcass_type = "Tall"
        self.splitter = LM_splitters.INSERT_2_Vertical_Openings()
        self.splitter.opening_2_height = fd.inches(20)
        self.splitter.exterior_1 = LM_exteriors.INSERT_Tall_Double_Door()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.interior_1 = None
        self.splitter.exterior_2 = LM_exteriors.INSERT_3_Drawer_Stack()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}                  

#---------PRODUCTS: Upper Cabinets

class PRODUCT_1_Door_Upper(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = UPPER_CATEGORY_NAME
        self.assembly_name = "1 Door Upper"
        self.width = g.Width_1_Door
        self.height = g.Upper_Cabinet_Height
        self.depth = g.Upper_Cabinet_Depth
        self.mirror_z = True
        self.height_above_floor = g.Height_Above_Floor
        self.carcass_path = UPPER_CARCASS
        self.carcass_type = "Upper"
        self.exterior = LM_exteriors.INSERT_Upper_Single_Door()
        self.interior = SHELVES        
        
class PRODUCT_2_Door_Upper(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = UPPER_CATEGORY_NAME
        self.assembly_name = "2 Door Upper"
        self.width = g.Width_2_Door
        self.height = g.Upper_Cabinet_Height
        self.depth = g.Upper_Cabinet_Depth
        self.mirror_z = True
        self.height_above_floor = g.Height_Above_Floor
        self.carcass_path = UPPER_CARCASS
        self.carcass_type = "Upper"
        self.exterior = LM_exteriors.INSERT_Upper_Double_Door()
        self.interior = SHELVES      

class PRODUCT_1_Double_Door_Upper(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = UPPER_CATEGORY_NAME
        self.assembly_name = "1 Double Door Upper"
        self.width = g.Width_1_Door
        self.height = g.Upper_Cabinet_Height
        self.depth = g.Upper_Cabinet_Depth
        self.mirror_z = True
        self.height_above_floor = g.Height_Above_Floor
        self.carcass_path = UPPER_CARCASS
        self.carcass_type = "Upper"
        self.splitter = LM_splitters.INSERT_2_Vertical_Openings()
        self.splitter.exterior_1 = LM_exteriors.INSERT_Upper_Single_Door()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.exterior_2 = LM_exteriors.INSERT_Upper_Single_Door()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}
        
class PRODUCT_2_Double_Door_Upper(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = UPPER_CATEGORY_NAME
        self.assembly_name = "2 Double Door Upper"
        self.width = g.Width_2_Door
        self.height = g.Upper_Cabinet_Height
        self.depth = g.Upper_Cabinet_Depth
        self.mirror_z = True
        self.height_above_floor = g.Height_Above_Floor
        self.carcass_path = UPPER_CARCASS
        self.carcass_type = "Upper"
        self.splitter = LM_splitters.INSERT_2_Vertical_Openings()
        self.splitter.exterior_1 = LM_exteriors.INSERT_Upper_Double_Door()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.exterior_2 = LM_exteriors.INSERT_Upper_Double_Door()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}        
        
class PRODUCT_2_Door_2_Drawer_Upper(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = UPPER_CATEGORY_NAME
        self.assembly_name = "2 Door 2 Drawer Upper"
        self.width = g.Width_2_Door
        self.height = g.Upper_Cabinet_Height
        self.depth = g.Upper_Cabinet_Depth
        self.mirror_z = True
        self.height_above_floor = g.Height_Above_Floor
        self.carcass_path = UPPER_CARCASS
        self.carcass_type = "Upper"
        self.splitter = LM_splitters.INSERT_2_Vertical_Openings()
        self.splitter.exterior_1 = LM_exteriors.INSERT_Upper_Double_Door()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.interior_1 = None
        self.splitter.exterior_2 = LM_exteriors.INSERT_2_Drawer_Stack()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}        
        
class PRODUCT_2_Door_Upper_with_Vent(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = UPPER_CATEGORY_NAME
        self.assembly_name = "2 Door Upper with Vent"
        self.width = g.Width_2_Door
        self.height = g.Upper_Cabinet_Height - fd.inches(20)
        self.depth = g.Upper_Cabinet_Depth
        self.mirror_z = True
        self.height_above_floor = g.Height_Above_Floor
        self.carcass_path = UPPER_CARCASS
        self.carcass_type = "Upper"
        self.exterior = LM_exteriors.INSERT_Upper_Double_Door()
        self.interior = None
        self.add_vent_hood = True        
        
class PRODUCT_2_Door_Upper_with_Microwave(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = UPPER_CATEGORY_NAME
        self.assembly_name = "2 Door Upper with Microwave"
        self.width = fd.inches(30)
        self.height = g.Upper_Cabinet_Height - fd.inches(20)
        self.depth = g.Upper_Cabinet_Depth
        self.mirror_z = True
        self.height_above_floor = g.Height_Above_Floor
        self.carcass_path = UPPER_CARCASS
        self.carcass_type = "Upper"
        self.exterior = LM_exteriors.INSERT_Upper_Double_Door()
        self.interior = SHELVES
        self.add_microwave = True        
        
class PRODUCT_Microwave_2_Door_Upper(Basic_Standard):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = UPPER_CATEGORY_NAME
        self.assembly_name = "Microwave 2 Door Upper"
        self.width = g.Width_2_Door
        self.height = g.Upper_Cabinet_Height
        self.depth = g.Upper_Cabinet_Depth
        self.mirror_z = True
        self.height_above_floor = g.Height_Above_Floor
        self.carcass_path = UPPER_CARCASS
        self.carcass_type = "Upper"
        self.splitter = LM_splitters.INSERT_2_Vertical_Openings()
        self.splitter.exterior_1 = LM_exteriors.INSERT_Upper_Double_Door()        

#---------PRODUCTS: Inside Corner Cabinets

class PRODUCT_Pie_Cut_Corner_Base(Inside_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = INSIDE_CORNER_CATEGORY_NAME
        self.assembly_name = "Pie Cut Corner Base"
        self.width = g.Base_Inside_Corner_Size
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Inside_Corner_Size
        self.carcass_path = BASE_PIE_CUT_CARCASS
        self.carcass_type = "Base"
        self.carcass_shape = "Notched"
        self.exterior = LM_exteriors.INSERT_Base_Pie_Cut_Door()
        self.interior = None
        
class PRODUCT_Pie_Cut_Corner_Upper(Inside_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = INSIDE_CORNER_CATEGORY_NAME
        self.assembly_name = "Pie Cut Corner Upper"
        self.width = g.Upper_Inside_Corner_Size
        self.height = g.Upper_Cabinet_Height
        self.depth = g.Upper_Inside_Corner_Size
        self.height_above_floor = g.Height_Above_Floor
        self.mirror_z = True
        self.carcass_path = UPPER_PIE_CUT_CARCASS
        self.carcass_type = "Upper"
        self.carcass_shape = "Notched"
        self.exterior = LM_exteriors.INSERT_Upper_Pie_Cut_Door()
        self.interior = None        
        
class PRODUCT_1_Door_Diagonal_Corner_Base(Inside_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = INSIDE_CORNER_CATEGORY_NAME
        self.assembly_name = "1 Door Diagonal Corner Base"
        self.width = g.Base_Inside_Corner_Size
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Inside_Corner_Size
        self.carcass_path = BASE_DIAGONAL_CARCASS
        self.carcass_type = "Base"
        self.carcass_shape = "Diagonal"
        self.exterior = LM_exteriors.INSERT_Base_Single_Door()
        self.interior = None        

class PRODUCT_2_Door_Diagonal_Corner_Base(Inside_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = INSIDE_CORNER_CATEGORY_NAME
        self.assembly_name = "2 Door Diagonal Corner Base"
        self.width = g.Base_Inside_Corner_Size
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Inside_Corner_Size
        self.carcass_path = BASE_DIAGONAL_CARCASS
        self.carcass_type = "Base"
        self.carcass_shape = "Diagonal"
        self.exterior = LM_exteriors.INSERT_Base_Double_Door()
        self.interior = None    
        
class PRODUCT_1_Door_Diagonal_Corner_Upper(Inside_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = INSIDE_CORNER_CATEGORY_NAME
        self.assembly_name = "1 Door Diagonal Corner Upper"
        self.width = g.Upper_Inside_Corner_Size
        self.height = g.Upper_Cabinet_Height
        self.depth = g.Upper_Inside_Corner_Size
        self.height_above_floor = g.Height_Above_Floor
        self.mirror_z = True        
        self.carcass_path = UPPER_DIAGONAL_CARCASS
        self.carcass_type = "Upper"
        self.carcass_shape = "Diagonal"
        self.exterior = LM_exteriors.INSERT_Upper_Single_Door()
        self.interior = None        

class PRODUCT_2_Door_Diagonal_Corner_Upper(Inside_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = INSIDE_CORNER_CATEGORY_NAME
        self.assembly_name = "2 Door Diagonal Corner Upper"
        self.width = g.Upper_Inside_Corner_Size
        self.height = g.Upper_Cabinet_Height
        self.depth = g.Upper_Inside_Corner_Size
        self.height_above_floor = g.Height_Above_Floor
        self.mirror_z = True        
        self.carcass_path = UPPER_DIAGONAL_CARCASS
        self.carcass_type = "Upper"
        self.carcass_shape = "Diagonal"
        self.exterior = LM_exteriors.INSERT_Upper_Double_Door()
        self.interior = None            

#---------PRODUCTS: Outside Corner Cabinets

class PRODUCT_Outside_Radius_Corner_Base(Outside_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = OUTSIDE_CORNER_CATEGORY_NAME
        self.assembly_name = "Outside Radius Corner Base"
        self.width = g.Width_1_Door
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Cabinet_Depth
        self.carcass_path = BASE_OUTSIDE_CORNER_RADIUS_CARCASS
        self.carcass_type = "Base"
        self.carcass_shape = "Radius"
        self.exterior = None
        self.interior = None

class PRODUCT_Outside_Radius_Corner_Tall(Outside_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = OUTSIDE_CORNER_CATEGORY_NAME
        self.assembly_name = "Outside Radius Corner Tall"
        self.width = g.Width_1_Door
        self.height = g.Tall_Cabinet_Height
        self.depth = g.Tall_Cabinet_Depth
        self.carcass_path = TALL_OUTSIDE_CORNER_RADIUS_CARCASS
        self.carcass_type = "Tall"
        self.carcass_shape = "Radius"
        self.exterior = None
        self.interior = None
        
class PRODUCT_Outside_Radius_Corner_Upper(Outside_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = OUTSIDE_CORNER_CATEGORY_NAME
        self.assembly_name = "Outside Radius Corner Upper"
        self.width = g.Width_1_Door
        self.height = g.Upper_Cabinet_Height
        self.depth = g.Upper_Cabinet_Depth
        self.mirror_z = True
        self.height_above_floor = g.Height_Above_Floor
        self.carcass_path = UPPER_OUTSIDE_CORNER_RADIUS_CARCASS
        self.carcass_type = "Upper"
        self.carcass_shape = "Radius"
        self.exterior = None
        self.interior = None
        
class PRODUCT_Outside_Chamfer_Corner_Base(Outside_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = OUTSIDE_CORNER_CATEGORY_NAME
        self.assembly_name = "Outside Chamfer Corner Base"
        self.width = g.Width_1_Door
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Cabinet_Depth
        self.carcass_path = BASE_OUTSIDE_CORNER_CHAMFERED_CARCASS
        self.carcass_type = "Base"
        self.carcass_shape = "Diagonal"
        self.exterior = None
        self.interior = None

class PRODUCT_Outside_Chamfer_Corner_Tall(Outside_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = OUTSIDE_CORNER_CATEGORY_NAME
        self.assembly_name = "Outside Chamfer Corner Tall"
        self.width = g.Width_1_Door
        self.height = g.Tall_Cabinet_Height
        self.depth = g.Tall_Cabinet_Depth
        self.carcass_path = TALL_OUTSIDE_CORNER_CHAMFERED_CARCASS
        self.carcass_type = "Tall"
        self.carcass_shape = "Diagonal"
        self.exterior = None
        self.interior = None
        
class PRODUCT_Outside_Chamfer_Corner_Upper(Outside_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = OUTSIDE_CORNER_CATEGORY_NAME
        self.assembly_name = "Outside Chamfer Corner Upper"
        self.width = g.Width_1_Door
        self.height = g.Upper_Cabinet_Height
        self.depth = g.Upper_Cabinet_Depth
        self.mirror_z = True
        self.height_above_floor = g.Height_Above_Floor
        self.carcass_path = UPPER_OUTSIDE_CORNER_CHAMFERED_CARCASS
        self.carcass_type = "Upper"
        self.carcass_shape = "Diagonal"
        self.exterior = None
        self.interior = None


#---------PRODUCTS: Blind Corner Cabinets

class PRODUCT_1_Door_Blind_Left_Corner_Base(Blind_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.assembly_name = "1 Door Blind Left Corner Base"
        self.blind_side = "Left"
        self.width = g.Base_Width_Blind
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Cabinet_Depth
        self.carcass_path = BASE_CARCASS
        self.carcass_type =  "Base"
        self.exterior = LM_exteriors.INSERT_Base_Single_Door()
        self.interior = SHELVES

class PRODUCT_1_Door_Blind_Right_Corner_Base(Blind_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.assembly_name = "1 Door Blind Right Corner Base"
        self.blind_side = "Right"
        self.width = g.Base_Width_Blind
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Cabinet_Depth
        self.carcass_path = BASE_CARCASS
        self.carcass_type =  "Base"
        self.exterior = LM_exteriors.INSERT_Base_Single_Door()
        self.interior = SHELVES
        
class PRODUCT_1_Door_Blind_Left_Corner_Tall(Blind_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.assembly_name = "1 Door Blind Left Corner Tall"
        self.blind_side = "Left"
        self.width = g.Tall_Width_Blind
        self.height = g.Tall_Cabinet_Height
        self.depth = g.Tall_Cabinet_Depth
        self.carcass_path = TALL_CARCASS
        self.carcass_type =  "Tall"
        self.exterior = LM_exteriors.INSERT_Tall_Single_Door()
        self.interior = SHELVES

class PRODUCT_1_Door_Blind_Right_Corner_Tall(Blind_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.assembly_name = "1 Door Blind Right Corner Tall"
        self.blind_side = "Right"
        self.width = g.Tall_Width_Blind
        self.height = g.Tall_Cabinet_Height
        self.depth = g.Tall_Cabinet_Depth
        self.carcass_path = TALL_CARCASS
        self.carcass_type =  "Tall"
        self.exterior = LM_exteriors.INSERT_Tall_Single_Door()
        self.interior = SHELVES   
        
class PRODUCT_1_Door_Blind_Left_Corner_Upper(Blind_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.assembly_name = "1 Door Blind Left Corner Upper"
        self.blind_side = "Left"
        self.height_above_floor = g.Height_Above_Floor
        self.mirror_z = True
        self.width = g.Upper_Width_Blind
        self.height = g.Upper_Cabinet_Height
        self.depth = g.Upper_Cabinet_Depth
        self.carcass_path = UPPER_CARCASS
        self.carcass_type =  "Upper"
        self.exterior = LM_exteriors.INSERT_Upper_Single_Door()
        self.interior = SHELVES

class PRODUCT_1_Door_Blind_Right_Corner_Upper(Blind_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.assembly_name = "1 Door Blind Right Corner Upper"
        self.blind_side = "Right"
        self.height_above_floor = g.Height_Above_Floor
        self.mirror_z = True
        self.width = g.Upper_Width_Blind
        self.height = g.Upper_Cabinet_Height
        self.depth = g.Upper_Cabinet_Depth
        self.carcass_path = UPPER_CARCASS
        self.carcass_type =  "Upper"
        self.exterior = LM_exteriors.INSERT_Upper_Single_Door()
        self.interior = SHELVES     

class PRODUCT_2_Door_Blind_Left_Corner_Base(Blind_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.assembly_name = "2 Door Blind Left Corner Base"
        self.blind_side = "Left"
        self.width = g.Base_Width_Blind
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Cabinet_Depth
        self.carcass_path = BASE_CARCASS
        self.carcass_type =  "Base"
        self.exterior = LM_exteriors.INSERT_Base_Double_Door()
        self.interior = SHELVES

class PRODUCT_2_Door_Blind_Right_Corner_Base(Blind_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.assembly_name = "2 Door Blind Right Corner Base"
        self.blind_side = "Right"
        self.width = g.Base_Width_Blind
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Cabinet_Depth
        self.carcass_path = BASE_CARCASS
        self.carcass_type =  "Base"
        self.exterior = LM_exteriors.INSERT_Base_Double_Door()
        self.interior = SHELVES
        
class PRODUCT_2_Door_Blind_Left_Corner_Tall(Blind_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.assembly_name = "2 Door Blind Left Corner Tall"
        self.blind_side = "Left"
        self.width = g.Tall_Width_Blind
        self.height = g.Tall_Cabinet_Height
        self.depth = g.Tall_Cabinet_Depth
        self.carcass_path = TALL_CARCASS
        self.carcass_type =  "Tall"
        self.exterior = LM_exteriors.INSERT_Tall_Double_Door()
        self.interior = SHELVES

class PRODUCT_2_Door_Blind_Right_Corner_Tall(Blind_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.assembly_name = "2 Door Blind Right Corner Tall"
        self.blind_side = "Right"
        self.width = g.Tall_Width_Blind
        self.height = g.Tall_Cabinet_Height
        self.depth = g.Tall_Cabinet_Depth
        self.carcass_path = TALL_CARCASS
        self.carcass_type =  "Tall"
        self.exterior = LM_exteriors.INSERT_Tall_Double_Door()
        self.interior = SHELVES   
        
class PRODUCT_2_Door_Blind_Left_Corner_Upper(Blind_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.assembly_name = "2 Door Blind Left Corner Upper"
        self.blind_side = "Left"
        self.height_above_floor = g.Height_Above_Floor
        self.mirror_z = True
        self.width = g.Upper_Width_Blind
        self.height = g.Upper_Cabinet_Height
        self.depth = g.Upper_Cabinet_Depth
        self.carcass_path = UPPER_CARCASS
        self.carcass_type =  "Upper"
        self.exterior = LM_exteriors.INSERT_Upper_Double_Door()
        self.interior = SHELVES

class PRODUCT_2_Door_Blind_Right_Corner_Upper(Blind_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.assembly_name = "2 Door Blind Right Corner Upper"
        self.blind_side = "Right"
        self.height_above_floor = g.Height_Above_Floor
        self.mirror_z = True
        self.width = g.Upper_Width_Blind
        self.height = g.Upper_Cabinet_Height
        self.depth = g.Upper_Cabinet_Depth
        self.carcass_path = UPPER_CARCASS
        self.carcass_type =  "Upper"
        self.exterior = LM_exteriors.INSERT_Upper_Double_Door()
        self.interior = SHELVES  

class PRODUCT_1_Door_1_Drawer_Blind_Right_Corner_Base(Blind_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.assembly_name = "1 Door 1 Drawer Blind Right Corner Base"
        self.blind_side = "Right"
        self.width = g.Base_Width_Blind
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Cabinet_Depth
        self.carcass_path = BASE_CARCASS
        self.carcass_type =  "Base"
        self.splitter = LM_splitters.INSERT_2_Vertical_Openings()
        self.splitter.opening_1_height = g.Top_Drawer_Front_Height - fd.inches(1)
        self.splitter.exterior_1 = LM_exteriors.INSERT_1_Drawer()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.exterior_2 = LM_exteriors.INSERT_Base_Single_Door()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}
        
class PRODUCT_1_Door_1_Drawer_Blind_Left_Corner_Base(Blind_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.assembly_name = "1 Door 1 Drawer Blind Left Corner Base"
        self.blind_side = "Left"
        self.width = g.Base_Width_Blind
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Cabinet_Depth
        self.carcass_path = BASE_CARCASS
        self.carcass_type =  "Base"
        self.splitter = LM_splitters.INSERT_2_Vertical_Openings()
        self.splitter.opening_1_height = g.Top_Drawer_Front_Height - fd.inches(1)
        self.splitter.exterior_1 = LM_exteriors.INSERT_1_Drawer()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.exterior_2 = LM_exteriors.INSERT_Base_Single_Door()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}        

class PRODUCT_2_Door_2_Drawer_Blind_Right_Corner_Base(Blind_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.assembly_name = "2 Door 2 Drawer Blind Right Corner Base"
        self.blind_side = "Right"
        self.width = g.Base_Width_Blind
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Cabinet_Depth
        self.carcass_path = BASE_CARCASS
        self.carcass_type =  "Base"
        self.splitter = LM_splitters.INSERT_2_Vertical_Openings()
        self.splitter.opening_1_height = g.Top_Drawer_Front_Height - fd.inches(1)
        self.splitter.exterior_1 = LM_exteriors.INSERT_Horizontal_Drawers()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.exterior_2 = LM_exteriors.INSERT_Base_Double_Door()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}
        
class PRODUCT_2_Door_2_Drawer_Blind_Left_Corner_Base(Blind_Corner):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.assembly_name = "2 Door 2 Drawer Blind Left Corner Base"
        self.blind_side = "Left"
        self.width = g.Base_Width_Blind
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Cabinet_Depth
        self.carcass_path = BASE_CARCASS
        self.carcass_type =  "Base"
        self.splitter = LM_splitters.INSERT_2_Vertical_Openings()
        self.splitter.opening_1_height = g.Top_Drawer_Front_Height - fd.inches(1)
        self.splitter.exterior_1 = LM_exteriors.INSERT_Horizontal_Drawers()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.exterior_2 = LM_exteriors.INSERT_Base_Double_Door()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}

#---------PRODUCT: TRANSITION CABINETS

class PRODUCT_1_Door_Base_Transition(Transition):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = TRANSITION_CATEGORY_NAME
        self.assembly_name = "1 Door Base Transition"
        self.width = g.Width_1_Door
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Cabinet_Depth
        self.carcass_path = BASE_TRANSITION_CARCASS
        self.carcass_type = "Base"
        self.exterior = LM_exteriors.INSERT_Base_Single_Door()
        self.exterior.prompts = {'Half Overlay Left':True,'Half Overlay Right':True}
        self.interior = None

class PRODUCT_2_Door_Base_Transition(Transition):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = TRANSITION_CATEGORY_NAME
        self.assembly_name = "2 Door Base Transition"
        self.width = g.Width_2_Door
        self.height = g.Base_Cabinet_Height
        self.depth = g.Base_Cabinet_Depth
        self.carcass_path = BASE_TRANSITION_CARCASS
        self.carcass_type = "Base"
        self.exterior = LM_exteriors.INSERT_Base_Double_Door()
        self.exterior.prompts = {'Half Overlay Left':True,'Half Overlay Right':True}
        self.interior = None

class PRODUCT_1_Door_Tall_Transition(Transition):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = TRANSITION_CATEGORY_NAME
        self.assembly_name = "1 Door Tall Transition"
        self.width = g.Width_1_Door
        self.height = g.Tall_Cabinet_Height
        self.depth = g.Tall_Cabinet_Depth
        self.carcass_path = TALL_TRANSITION_CARCASS
        self.carcass_type = "Tall"
        self.exterior = LM_exteriors.INSERT_Tall_Single_Door()
        self.exterior.prompts = {'Half Overlay Left':True,'Half Overlay Right':True}
        self.interior = None

class PRODUCT_2_Door_Tall_Transition(Transition):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = TRANSITION_CATEGORY_NAME
        self.assembly_name = "2 Door Tall Transition"
        self.width = g.Width_2_Door
        self.height = g.Tall_Cabinet_Height
        self.depth = g.Tall_Cabinet_Depth
        self.carcass_path = TALL_TRANSITION_CARCASS
        self.carcass_type = "Tall"
        self.exterior = LM_exteriors.INSERT_Tall_Double_Door()
        self.exterior.prompts = {'Half Overlay Left':True,'Half Overlay Right':True}
        self.interior = None

class PRODUCT_1_Door_Upper_Transition(Transition):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = TRANSITION_CATEGORY_NAME
        self.assembly_name = "1 Door Upper Transition"
        self.width = g.Width_1_Door
        self.height = g.Upper_Cabinet_Height
        self.depth = g.Upper_Cabinet_Depth
        self.mirror_z = True
        self.height_above_floor = g.Height_Above_Floor
        self.carcass_path = UPPER_TRANSITION_CARCASS
        self.carcass_type = "Upper"
        self.exterior = LM_exteriors.INSERT_Upper_Single_Door()
        self.exterior.prompts = {'Half Overlay Left':True,'Half Overlay Right':True}
        self.interior = None

class PRODUCT_2_Door_Upper_Transition(Transition):
    
    def __init__(self):
        g = bpy.context.scene.lm_basic_cabients
        self.library_name = LIBRARY_NAME
        self.category_name = TRANSITION_CATEGORY_NAME
        self.assembly_name = "2 Door Upper Transition"
        self.width = g.Width_2_Door
        self.height = g.Upper_Cabinet_Height
        self.depth = g.Upper_Cabinet_Depth
        self.mirror_z = True
        self.height_above_floor = g.Height_Above_Floor
        self.carcass_path = UPPER_TRANSITION_CARCASS
        self.carcass_type = "Upper"
        self.exterior = LM_exteriors.INSERT_Upper_Double_Door()
        self.exterior.prompts = {'Half Overlay Left':True,'Half Overlay Right':True}
        self.interior = None

class PROPERTIES_Scene_Variables(bpy.types.PropertyGroup):
    Base_Cabinet_Depth = bpy.props.FloatProperty(name="Base Cabinet Depth",
                                                 description="Default depth for base cabinets",
                                                 default=fd.inches(23.0),
                                                 unit='LENGTH')
    
    Base_Cabinet_Height = bpy.props.FloatProperty(name="Base Cabinet Height",
                                                  description="Default height for base cabinets",
                                                  default=fd.inches(34.0),
                                                  unit='LENGTH')
    
    Base_Inside_Corner_Size= bpy.props.FloatProperty(name="Base Inside Corner Size",
                                                     description="Default width and depth for the inside base corner cabinets",
                                                     default=fd.inches(36.0),
                                                     unit='LENGTH')    
    
    Tall_Cabinet_Depth = bpy.props.FloatProperty(name="Tall Cabinet Depth",
                                                 description="Default depth for tall cabinets",
                                                 default=fd.inches(25.0),
                                                 unit='LENGTH')
    
    Tall_Cabinet_Height = bpy.props.FloatProperty(name="Tall Cabinet Height",
                                                  description="Default height for tall cabinets",
                                                  default=fd.inches(84.0),
                                                  unit='LENGTH')
    
    Upper_Cabinet_Depth = bpy.props.FloatProperty(name="Upper Cabinet Depth",
                                                  description="Default depth for upper cabinets",
                                                  default=fd.inches(12.0),
                                                  unit='LENGTH')
    
    Upper_Cabinet_Height = bpy.props.FloatProperty(name="Upper Cabinet Height",
                                                   description="Default height for upper cabinets",
                                                   default=fd.inches(34.0),
                                                   unit='LENGTH')
    
    Upper_Inside_Corner_Size= bpy.props.FloatProperty(name="Upper Inside Corner Size",
                                                      description="Default width and depth for the inside upper corner cabinets",
                                                      default=fd.inches(24.0),
                                                      unit='LENGTH')    
    
    Sink_Cabinet_Depth = bpy.props.FloatProperty(name="Upper Cabinet Depth",
                                                 description="Default depth for sink cabinets",
                                                 default=fd.inches(23.0),
                                                 unit='LENGTH')
    
    Sink_Cabinet_Height = bpy.props.FloatProperty(name="Upper Cabinet Height",
                                                  description="Default height for sink cabinets",
                                                  default=fd.inches(34.0),
                                                  unit='LENGTH')

    Suspended_Cabinet_Depth = bpy.props.FloatProperty(name="Upper Cabinet Depth",
                                                      description="Default depth for suspended cabinets",
                                                      default=fd.inches(23.0),
                                                      unit='LENGTH')
    
    Suspended_Cabinet_Height = bpy.props.FloatProperty(name="Upper Cabinet Height",
                                                       description="Default height for suspended cabinets",
                                                       default=fd.inches(6.0),
                                                       unit='LENGTH')

    Width_1_Door = bpy.props.FloatProperty(name="Width 1 Door",
                                           description="Default width for one door wide cabinets",
                                           default=fd.inches(18.0),
                                           unit='LENGTH')
    
    Width_2_Door = bpy.props.FloatProperty(name="Width 2 Door",
                                           description="Default width for two door wide and open cabinets",
                                           default=fd.inches(36.0),
                                           unit='LENGTH')
    
    Width_Drawer = bpy.props.FloatProperty(name="Width Drawer",
                                           description="Default width for drawer cabinets",
                                           default=fd.inches(18.0),
                                           unit='LENGTH')
    
    Base_Width_Blind = bpy.props.FloatProperty(name="Base Width Blind",
                                               description="Default width for base blind corner cabinets",
                                               default=fd.inches(48.0),
                                               unit='LENGTH')
    
    Tall_Width_Blind = bpy.props.FloatProperty(name="Tall Width Blind",
                                               description="Default width for tall blind corner cabinets",
                                               default=fd.inches(48.0),
                                               unit='LENGTH')
    
    Blind_Panel_Reveal = bpy.props.FloatProperty(name="Blind Panel Reveal",
                                                 description="Default reveal for blind panels",
                                                 default=fd.inches(3.0),
                                                 unit='LENGTH')
    
    Inset_Blind_Panel = bpy.props.BoolProperty(name="Inset Blind Panel",
                                               description="Check this to inset the blind panel into the cabinet carcass",
                                               default=True)
    
    Upper_Width_Blind = bpy.props.FloatProperty(name="Upper Width Blind",
                                                description="Default width for upper blind corner cabinets",
                                                default=fd.inches(36.0),
                                                unit='LENGTH')

    Height_Above_Floor = bpy.props.FloatProperty(name="Height Above Floor",
                                                 description="Default height above floor for upper cabinets",
                                                 default=fd.inches(84.0),
                                                 unit='LENGTH')
    
    Equal_Drawer_Stack_Heights = bpy.props.BoolProperty(name="Equal Drawer Stack Heights", 
                                                        description="Check this make all drawer stack heights equal. Otherwise the Top Drawer Height will be set.", 
                                                        default=True)
    
    Top_Drawer_Front_Height = bpy.props.FloatProperty(name="Top Drawer Front Height",
                                                      description="Default top drawer front height.",
                                                      default=fd.inches(6.0),
                                                      unit='LENGTH')
    
    def draw(self,layout):
        col = layout.column(align=True)
        box = col.box()
        box.label("Standard Face Frame Cabinet Sizes:")
        
        row = box.row(align=True)
        row.label("Base:")
        row.prop(self,"Base_Cabinet_Height",text="Height")
        row.prop(self,"Base_Cabinet_Depth",text="Depth")
        
        row = box.row(align=True)
        row.label("Tall:")
        row.prop(self,"Tall_Cabinet_Height",text="Height")
        row.prop(self,"Tall_Cabinet_Depth",text="Depth")
        
        row = box.row(align=True)
        row.label("Upper:")
        row.prop(self,"Upper_Cabinet_Height",text="Height")
        row.prop(self,"Upper_Cabinet_Depth",text="Depth")

        row = box.row(align=True)
        row.label("Sink:")
        row.prop(self,"Sink_Cabinet_Height",text="Height")
        row.prop(self,"Sink_Cabinet_Depth",text="Depth")
        
        row = box.row(align=True)
        row.label("Suspended:")
        row.prop(self,"Suspended_Cabinet_Height",text="Height")
        row.prop(self,"Suspended_Cabinet_Depth",text="Depth")
        
        row = box.row(align=True)
        row.label("1 Door Wide:")
        row.prop(self,"Width_1_Door",text="Width")
        
        row = box.row(align=True)
        row.label("2 Door Wide:")
        row.prop(self,"Width_2_Door",text="Width")
        
        row = box.row(align=True)
        row.label("Drawer Stack Width:")
        row.prop(self,"Width_Drawer",text="Width")

        box = col.box()
        box.label("Blind Cabinet Widths:")
        
        row = box.row(align=True)
        row.label('Base:')
        row.prop(self,"Base_Width_Blind",text="Width")
        
        row = box.row(align=True)
        row.label('Tall:')
        row.prop(self,"Tall_Width_Blind",text="Width")
        
        row = box.row(align=True)
        row.label('Upper:')
        row.prop(self,"Upper_Width_Blind",text="Width")

        box = col.box()
        box.label("Inside Corner Cabinet Sizes:")
        row = box.row(align=True)
        row.label("Base:")
        row.prop(self,"Base_Inside_Corner_Size",text="")
        
        row = box.row(align=True)
        row.label("Upper:")
        row.prop(self,"Upper_Inside_Corner_Size",text="")
        
        box = col.box()
        box.label("Placement:")
        row = box.row(align=True)
        row.label("Height Above Floor:")
        row.prop(self,"Height_Above_Floor",text="")
        
        box = col.box()
        box.label("Drawer Heights:")
        row = box.row(align=True)
        row.prop(self,"Equal_Drawer_Stack_Heights")
        if not self.Equal_Drawer_Stack_Heights:
            row.prop(self,"Top_Drawer_Front_Height")
                
class PROMPTS_Basic_Cabinet_Prompts(bpy.types.Operator):
    bl_idname = "basic_cabinets.basic_cabinet_prompts"
    bl_label = "Basic Cabinet Prompts" 
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    width = bpy.props.FloatProperty(name="Width",unit='LENGTH',precision=4)
    height = bpy.props.FloatProperty(name="Height",unit='LENGTH',precision=4)
    depth = bpy.props.FloatProperty(name="Depth",unit='LENGTH',precision=4)

    door_rotation = bpy.props.FloatProperty(name="Door Rotation",subtype='ANGLE',min=0,max=math.radians(120))
    
    door_swing = bpy.props.EnumProperty(name="Door Swing",items=[('Left Swing',"Left Swing","Left Swing"),
                                                                 ('Right Swing',"Right Swing","Right Swing")])
    
    product = None
    
    open_door_prompts = []
    
    show_exterior_options = False
    show_interior_options = False
    show_splitter_options = False
    
    inserts = []
    
    @classmethod
    def poll(cls, context):
        return True

    def check(self, context):
        self.product.obj_x.location.x = self.width
        
        if self.product.obj_bp.cabinetlib.mirror_y:
            self.product.obj_y.location.y = -self.depth
        else:
            self.product.obj_y.location.y = self.depth
        
        if self.product.obj_bp.cabinetlib.mirror_z:
            self.product.obj_z.location.z = -self.height
        else:
            self.product.obj_z.location.z = self.height
            
        for open_door_prompt in self.open_door_prompts:
            open_door_prompt.set_value(self.door_rotation)
            
        fd.run_calculators(self.product.obj_bp)
        return True

    def execute(self, context):
        fd.run_calculators(self.product.obj_bp)
        return {'FINISHED'}

    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_product_bp = fd.get_bp(obj,'PRODUCT')
        self.product = fd.Assembly(obj_product_bp)
        if self.product.obj_bp:
            self.depth = math.fabs(self.product.obj_y.location.y)
            self.height = math.fabs(self.product.obj_z.location.z)
            self.width = math.fabs(self.product.obj_x.location.x)
            new_list = []
            self.inserts = fd.get_insert_bp_list(self.product.obj_bp,new_list)
        for insert in self.inserts:
            if "Door Options" in insert.mv.PromptPage.COL_MainTab:
                door = fd.Assembly(insert)
                door_rotation = door.get_prompt("Door Rotation")
                if door_rotation:
                    self.open_door_prompts.append(door_rotation)
                    self.door_rotation = door_rotation.value()
                self.show_exterior_options = True
            if "Drawer Options" in insert.mv.PromptPage.COL_MainTab:
                self.show_exterior_options = True
            if "Interior Options" in insert.mv.PromptPage.COL_MainTab:
                self.show_interior_options = True
            if "Opening Heights" in insert.mv.PromptPage.COL_MainTab:
                self.show_splitter_options = True
            if "Opening Widths" in insert.mv.PromptPage.COL_MainTab:
                self.show_splitter_options = True
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=fd.get_prop_dialog_width(500))

    def draw_product_size(self,layout):
        box = layout.box()
        
        row = box.row()
        
        col = row.column(align=True)
        row1 = col.row(align=True)
        if self.object_has_driver(self.product.obj_x):
            row1.label('Width: ' + str(fd.unit(math.fabs(self.product.obj_x.location.x))))
        else:
            row1.label('Width:')
            row1.prop(self,'width',text="")
            row1.prop(self.product.obj_x,'hide',text="")
        
        row1 = col.row(align=True)
        if self.object_has_driver(self.product.obj_z):
            row1.label('Height: ' + str(fd.unit(math.fabs(self.product.obj_z.location.z))))
        else:
            row1.label('Height:')
            row1.prop(self,'height',text="")
            row1.prop(self.product.obj_z,'hide',text="")
        
        row1 = col.row(align=True)
        if self.object_has_driver(self.product.obj_y):
            row1.label('Depth: ' + str(fd.unit(math.fabs(self.product.obj_y.location.y))))
        else:
            row1.label('Depth:')
            row1.prop(self,'depth',text="")
            row1.prop(self.product.obj_y,'hide',text="")
            
        col = row.column(align=True)
        col.label("Location X:")
        col.label("Location Y:")
        col.label("Location Z:")
            
        col = row.column(align=True)
        col.prop(self.product.obj_bp,'location',text="")
        
        row = box.row()
        row.label('Rotation Z:')
        row.prop(self.product.obj_bp,'rotation_euler',index=2,text="")
        
    def object_has_driver(self,obj):
        if obj.animation_data:
            if len(obj.animation_data.drivers) > 0:
                return True
            
    def draw_carcass_prompts(self,layout):
        for insert in self.inserts:
            if "Carcass Options" in insert.mv.PromptPage.COL_MainTab:
                pass
        
    def draw_opening_prompt(self):
        pass
        
    def draw_door_prompts(self,layout):
        for insert in self.inserts:
            if "Door Options" in insert.mv.PromptPage.COL_MainTab:
                row = layout.row()
                row.label("Open Door")
                row.prop(self,'door_rotation',text="",slider=True)
                break
            
        for insert in self.inserts:
            if "Door Options" in insert.mv.PromptPage.COL_MainTab:
                box = layout.box()
                col = box.column(align=True)
                row = col.row()
                row.label(insert.mv.name_object + " Options:")
                door = fd.Assembly(insert)
                left_swing = door.get_prompt("Left Swing")
                inset_front = door.get_prompt("Inset Front")
                hot = door.get_prompt("Half Overlay Top")
                hob = door.get_prompt("Half Overlay Bottom")
                hol = door.get_prompt("Half Overlay Left")
                hor = door.get_prompt("Half Overlay Right")
                
                row.prop(inset_front,'CheckBoxValue',text="Inset Door")
                
                if left_swing:
                    row.prop(left_swing,'CheckBoxValue',text="Left Swing Door")
                    
                if hot:
                    row = col.row()
                    row.label("Half Overlays:")
                    row.prop(hot,'CheckBoxValue',text="Top")
                    row.prop(hob,'CheckBoxValue',text="Bottom")
                    row.prop(hol,'CheckBoxValue',text="Left")
                    row.prop(hor,'CheckBoxValue',text="Right")
        
    def draw_drawer_prompts(self,layout):
        for insert_bp in self.inserts:
            if "Drawer Options" in insert_bp.mv.PromptPage.COL_MainTab:
                insert = fd.Assembly(insert_bp)
                open_prompt = insert.get_prompt("Open")
                
                if open_prompt:
                    row = layout.row()
                    row.label("Open Drawer")
                    row.prop(open_prompt,"PercentageValue",text="")
                
                box = layout.box()
                col = box.column(align=True)
                row = col.row()
                row.label(insert_bp.mv.name_object + " Options:")
                
                inset_front = insert.get_prompt("Inset Front")
                half_overlay_top = insert.get_prompt("Half Overlay Top")
                
                if inset_front:
                    row.prop(inset_front,'CheckBoxValue',text="Inset Front")
                    
                if half_overlay_top:
                    half_overlay_bottom = insert.get_prompt("Half Overlay Bottom")
                    half_overlay_left = insert.get_prompt("Half Overlay Left")
                    half_overlay_right = insert.get_prompt("Half Overlay Right")
                    row = col.row()
                    row.label("Half Overlays:")
                    row.prop(half_overlay_top,'CheckBoxValue',text="Top")
                    row.prop(half_overlay_bottom,'CheckBoxValue',text="Bottom")
                    row.prop(half_overlay_left,'CheckBoxValue',text="Left")
                    row.prop(half_overlay_right,'CheckBoxValue',text="Right")
                
            if "Drawer Heights" in insert_bp.mv.PromptPage.COL_MainTab:
                insert = fd.Assembly(insert_bp)
                drawer_height_1 = insert.get_prompt("Top Drawer Height")
                drawer_height_2 = insert.get_prompt("Second Drawer Height")
                drawer_height_3 = insert.get_prompt("Third Drawer Height")
                drawer_height_4 = insert.get_prompt("Bottom Drawer Height")
                
                if drawer_height_1:
                    row = box.row()
                    row.label("Drawer 1 Height:")
                    if drawer_height_1.equal:
                        row.label(str(fd.unit(drawer_height_1.DistanceValue)))
                        row.prop(drawer_height_1,'equal',text="")
                    else:
                        row.prop(drawer_height_1,'DistanceValue',text="")
                        row.prop(drawer_height_1,'equal',text="")
                
                if drawer_height_2:
                    row = box.row()
                    row.label("Drawer 2 Height:")
                    if drawer_height_2.equal:
                        row.label(str(fd.unit(drawer_height_2.DistanceValue)))
                        row.prop(drawer_height_2,'equal',text="")
                    else:
                        row.prop(drawer_height_2,'DistanceValue',text="")
                        row.prop(drawer_height_2,'equal',text="")
                
                if drawer_height_3:
                    row = box.row()
                    row.label("Drawer 3 Height:")
                    if drawer_height_3.equal:
                        row.label(str(fd.unit(drawer_height_3.DistanceValue)))
                        row.prop(drawer_height_3,'equal',text="")
                    else:
                        row.prop(drawer_height_3,'DistanceValue',text="")
                        row.prop(drawer_height_3,'equal',text="")
                
                if drawer_height_4:
                    row = box.row()
                    row.label("Drawer 4 Height:")
                    if drawer_height_4.equal:
                        row.label(str(fd.unit(drawer_height_4.DistanceValue)))
                        row.prop(drawer_height_4,'equal',text="")
                    else:
                        row.prop(drawer_height_4,'DistanceValue',text="")
                        row.prop(drawer_height_4,'equal',text="")
        
    def draw_interior_prompts(self,layout):
        for insert in self.inserts:
            if "Interior Options" in insert.mv.PromptPage.COL_MainTab:
                pass
        
    def draw_splitter_prompts(self,layout):
        for insert in self.inserts:
            if "Opening Heights" in insert.mv.PromptPage.COL_MainTab:
                box = layout.box()
                col = box.column(align=True)
                col.label("Splitter Options:")
                splitter = fd.Assembly(insert)
                opening_1 = splitter.get_prompt("Opening 1 Height")
                opening_2 = splitter.get_prompt("Opening 2 Height")
                opening_3 = splitter.get_prompt("Opening 3 Height")
                opening_4 = splitter.get_prompt("Opening 4 Height")
                
                if opening_1:
                    row = box.row()
                    row.label("Opening 1 Height:")
                    if opening_1.equal:
                        row.label(str(fd.unit(opening_1.DistanceValue)))
                        row.prop(opening_1,'equal',text="")
                    else:
                        row.prop(opening_1,'DistanceValue',text="")
                        row.prop(opening_1,'equal',text="")
                if opening_2:
                    row = box.row()
                    row.label("Opening 2 Height:")
                    if opening_2.equal:
                        row.label(str(fd.unit(opening_2.DistanceValue)))
                        row.prop(opening_2,'equal',text="")
                    else:
                        row.prop(opening_2,'DistanceValue',text="")
                        row.prop(opening_2,'equal',text="")
                if opening_3:
                    row = box.row()
                    row.label("Opening 3 Height:")
                    if opening_3.equal:
                        row.label(str(fd.unit(opening_3.DistanceValue)))
                        row.prop(opening_3,'equal',text="")
                    else:
                        row.prop(opening_3,'DistanceValue',text="")
                        row.prop(opening_3,'equal',text="")
                if opening_4:
                    row = box.row()
                    row.label("Opening 4 Height:")
                    if opening_4.equal:
                        row.label(str(fd.unit(opening_4.DistanceValue)))
                        row.prop(opening_4,'equal',text="")
                    else:
                        row.prop(opening_4,'DistanceValue',text="")
                        row.prop(opening_4,'equal',text="")
        
    def draw(self, context):
        layout = self.layout
        if self.product.obj_bp:
            if self.product.obj_bp.name in context.scene.objects:
                box = layout.box()
                
                split = box.split(percentage=.8)
                split.label(self.product.obj_bp.mv.name_object + " | " + self.product.obj_bp.cabinetlib.spec_group_name,icon='LATTICE_DATA')
                split.menu('MENU_Current_Cabinet_Menu',text="Menu",icon='DOWNARROW_HLT')
                
                self.draw_product_size(box)                 
                
def register():
    bpy.utils.register_class(PROPERTIES_Scene_Variables)
    bpy.utils.register_class(PROMPTS_Basic_Cabinet_Prompts)
    bpy.types.Scene.lm_basic_cabients = bpy.props.PointerProperty(type = PROPERTIES_Scene_Variables)

def unregister():
    bpy.utils.unregister_class(PROPERTIES_Scene_Variables)
    bpy.utils.unregister_class(PROMPTS_Basic_Cabinet_Prompts)
