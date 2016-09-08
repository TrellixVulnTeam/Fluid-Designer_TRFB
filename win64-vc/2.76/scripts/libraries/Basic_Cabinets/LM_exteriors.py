"""
Microvellum 
Exteriors
Stores the logic and insert defs for all exterior components for cabinets and closets.
Doors, Drawers, Hampers
"""

import bpy
import math
import os
from mv import fd_types, unit, utils

PART = os.path.join(os.path.dirname(__file__),"Parts","Part with Edgebanding.blend")
DRAWER_BOX = os.path.join(os.path.dirname(__file__),"Drawer Boxes","Wood Drawer Box.blend")
PULL = os.path.join(os.path.dirname(__file__),"Cabinet Pulls","Wire Straight 3_5 Inch.blend")

#---------FUNCTIONS
    
def add_common_door_prompts(assembly):
    g = bpy.context.scene.lm_exteriors
    
    door_location = 0
    
    if assembly.door_type == 'Base':
        door_location = 0
    elif assembly.door_type == 'Tall':
        door_location = 1
    else:
        door_location = 2
    
    assembly.add_prompt(name="Door Rotation",prompt_type='ANGLE',value=0,tab_index=0)
    
    if assembly.door_swing in {"Left Swing","Right Swing"}:
        assembly.add_prompt(name="Left Swing",prompt_type='CHECKBOX',value=True if assembly.door_swing == 'Left Swing' else False,tab_index=0)
        assembly.add_prompt(name="Right Swing",prompt_type='CHECKBOX',value=False,tab_index=1) # CALCULATED
        
        #CALCULATE RIGHT SWING PROMPT NEEDED FOR MV EXPORT
        Left_Swing = assembly.get_var("Left Swing")
        assembly.prompt('Right Swing','IF(Left_Swing,True,False)',[Left_Swing])
        
    assembly.add_prompt(name="Inset Front",prompt_type='CHECKBOX',value=g.Inset_Door,tab_index=0)
    assembly.add_prompt(name="Inset Reveal",prompt_type='DISTANCE',value=g.Inset_Reveal,tab_index=0)
    assembly.add_prompt(name="Door to Cabinet Gap",prompt_type='DISTANCE',value=g.Door_To_Cabinet_Gap,tab_index=0)
    assembly.add_prompt(name="No Pulls",prompt_type='CHECKBOX',value=g.No_Pulls,tab_index=0)
    assembly.add_prompt(name="Pull Rotation",prompt_type='ANGLE',value=g.Pull_Rotation,tab_index=0)
    assembly.add_prompt(name="Pull From Edge",prompt_type='DISTANCE',value=g.Pull_From_Edge,tab_index=0)
    assembly.add_prompt(name="Pull Location",prompt_type='COMBOBOX',value=door_location,tab_index=0,items=['Base','Tall','Upper'],columns=3)
    assembly.add_prompt(name="Base Pull Location",prompt_type='DISTANCE',value=g.Base_Pull_Location,tab_index=0)
    assembly.add_prompt(name="Tall Pull Location",prompt_type='DISTANCE',value=g.Tall_Pull_Location,tab_index=0)
    assembly.add_prompt(name="Upper Pull Location",prompt_type='DISTANCE',value=g.Upper_Pull_Location,tab_index=0)
    assembly.add_prompt(name="Lock Door",prompt_type='CHECKBOX',value=False,tab_index=0)
    assembly.add_prompt(name="Pull Length",prompt_type='DISTANCE',value=0,tab_index=1)
    assembly.add_prompt(name="Door Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
    assembly.add_prompt(name="Edgebanding Thickness",prompt_type='DISTANCE',value=unit.inch(.02),tab_index=1)
    
def add_common_drawer_prompts(assembly):
    g = bpy.context.scene.lm_exteriors

    assembly.add_prompt(name="No Pulls",prompt_type='CHECKBOX',value=g.No_Pulls,tab_index=0)
    assembly.add_prompt(name="Center Pulls on Drawers",prompt_type='CHECKBOX',value=g.Center_Pulls_on_Drawers,tab_index=0)
    assembly.add_prompt(name="Drawer Pull From Top",prompt_type='DISTANCE',value=g.Drawer_Pull_From_Top,tab_index=0)
    assembly.add_prompt(name="Pull Double Max Span",prompt_type='DISTANCE',value=unit.inch(30),tab_index=0)
    assembly.add_prompt(name="Lock From Top",prompt_type='DISTANCE',value=unit.inch(1.0),tab_index=0)
    assembly.add_prompt(name="Lock Drawer",prompt_type='CHECKBOX',value=False,tab_index=0)
    assembly.add_prompt(name="Inset Front",prompt_type='CHECKBOX',value=False,tab_index=0)
    assembly.add_prompt(name="Open",prompt_type='PERCENTAGE',value=0,tab_index=0)

    assembly.add_prompt(name="Inset Reveal",prompt_type='DISTANCE',value=unit.inch(0.125),tab_index=0) 
    assembly.add_prompt(name="Door to Cabinet Gap",prompt_type='DISTANCE',value=unit.inch(0.125),tab_index=0)   
    assembly.add_prompt(name="Drawer Box Top Gap",prompt_type='DISTANCE',value=unit.inch(0.5),tab_index=0)
    assembly.add_prompt(name="Drawer Box Bottom Gap",prompt_type='DISTANCE',value=unit.inch(0.5),tab_index=0)
    assembly.add_prompt(name="Drawer Box Slide Gap",prompt_type='DISTANCE',value=unit.inch(0.5),tab_index=0)
    assembly.add_prompt(name="Drawer Box Rear Gap",prompt_type='DISTANCE',value=unit.inch(0.5),tab_index=0)
    
    assembly.add_prompt(name="Front Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
    assembly.add_prompt(name="Edgebanding Thickness",prompt_type='DISTANCE',value=unit.inch(.02),tab_index=1)

class Standard_Pull(fd_types.Assembly):
    
    library_name = "Cabinet Doors"
    type_assembly = "INSERT"
    property_id = "" #TODO: Create Prompts Page
    
    door_type = "" # Base, Tall, Upper, Sink, Suspended
    door_swing = "" # Left Swing, Right Swing, Double Door, Flip up

    def draw(self):
        self.create_assembly()

        pull = self.add_object(PULL)
        
        self.add_tab(name='Main Options',tab_type='VISIBLE')
        self.add_prompt(name="Pull Price",prompt_type='PRICE',value=0,tab_index=0)
        self.add_prompt(name="Hide",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Pull Length",prompt_type='DISTANCE',value=pull.obj.dimensions.x,tab_index=0)
        self.add_prompt(name="Pull X Location",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Pull Z Location",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Pull Rotation",prompt_type='ANGLE',value=0,tab_index=0)
        self.add_prompt(name="Pull Quantity",prompt_type='QUANTITY',value=1,tab_index=0)
        
        Width = self.get_var("dim_x","Width")
        Height = self.get_var("dim_z","Height")
        Depth = self.get_var("dim_y","Depth")
        Pull_X_Location = self.get_var("Pull X Location")
        Pull_Z_Location = self.get_var("Pull Z Location")
        Hide = self.get_var("Hide")
        
        pull.set_name(self.door_type + " Cabinet Pull")
        pull.obj.mv.is_cabinet_pull = True
        pull.x_loc('Width-Pull_Z_Location',[Width,Pull_Z_Location])
        pull.y_loc('Depth+IF(Depth<0,Pull_X_Location,-Pull_X_Location)',[Depth,Pull_X_Location,Pull_Z_Location])
        pull.z_loc('Height',[Height])
        pull.x_rot(value = -90)
        if self.door_swing == 'Left Swing':
            pull.z_rot(value = 180)
        pull.material("Basic_Cabinet_Pull_Material")
        pull.hide('Hide',[Hide])
        
        self.update()
        
class Doors(fd_types.Assembly):
    
    library_name = "Cabinet Exteriors"
    type_assembly = 'INSERT'
    placement_type = "EXTERIOR"
    property_id = "exteriors.door_prompts"
    door_type = "" # {Base, Tall, Upper}
    door_swing = "" # {Left Swing, Right Swing, Double Door, Flip up}

    false_front_qty = 0 # 0, 1, 2

    def add_doors_prompts(self):
        g = bpy.context.scene.lm_exteriors
        
        self.add_tab(name='Door Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        add_common_door_prompts(self)
        
        if self.false_front_qty > 0:
            self.add_prompt(name="False Front Height",prompt_type='DISTANCE',value=unit.inch(6),tab_index=0)
        
        self.add_prompt(name="Half Overlay Top",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Half Overlay Bottom",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Half Overlay Left",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Half Overlay Right",prompt_type='CHECKBOX',value=False,tab_index=0)
        
        self.add_prompt(name="Vertical Gap",prompt_type='DISTANCE',value=g.Vertical_Gap,tab_index=0)
        self.add_prompt(name="Top Reveal",prompt_type='DISTANCE',value=unit.inch(.25),tab_index=0)
        self.add_prompt(name="Bottom Reveal",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Left Reveal",prompt_type='DISTANCE',value=g.Left_Reveal,tab_index=0)
        self.add_prompt(name="Right Reveal",prompt_type='DISTANCE',value=g.Right_Reveal,tab_index=0)

        #CALCULATED
        self.add_prompt(name="Top Overlay",prompt_type='DISTANCE',value=unit.inch(.6875),tab_index=1)
        self.add_prompt(name="Bottom Overlay",prompt_type='DISTANCE',value=unit.inch(.6875),tab_index=1)
        self.add_prompt(name="Left Overlay",prompt_type='DISTANCE',value=unit.inch(.6875),tab_index=1)
        self.add_prompt(name="Right Overlay",prompt_type='DISTANCE',value=unit.inch(.6875),tab_index=1)
        
        #INHERITED
        self.add_prompt(name="Extend Top Amount",prompt_type='DISTANCE',value=0,tab_index=1)
        self.add_prompt(name="Extend Bottom Amount",prompt_type='DISTANCE',value=0,tab_index=1)
        self.add_prompt(name="Top Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Bottom Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Left Side Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Right Side Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Division Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        
        inset = self.get_var("Inset Front",'inset')
        ir = self.get_var("Inset Reveal",'ir')
        tr = self.get_var("Top Reveal",'tr')
        br = self.get_var("Bottom Reveal",'br')
        lr = self.get_var("Left Reveal",'lr')
        rr = self.get_var("Right Reveal",'rr')
        vg = self.get_var("Vertical Gap",'vg')
        hot = self.get_var("Half Overlay Top",'hot')
        hob = self.get_var("Half Overlay Bottom",'hob')
        hol = self.get_var("Half Overlay Left",'hol')
        hor = self.get_var("Half Overlay Right",'hor')
        tt = self.get_var("Top Thickness",'tt')
        lst = self.get_var("Left Side Thickness",'lst')
        rst = self.get_var("Right Side Thickness",'rst')
        bt = self.get_var("Bottom Thickness",'bt')
        
        self.prompt('Top Overlay','IF(inset,-ir,IF(hot,(tt/2)-(vg/2),tt-tr))',[inset,ir,hot,tt,tr,vg])
        self.prompt('Bottom Overlay','IF(inset,-ir,IF(hob,(bt/2)-(vg/2),bt-br))',[inset,ir,hob,bt,br,vg])
        self.prompt('Left Overlay','IF(inset,-ir,IF(hol,(lst/2)-(vg/2),lst-lr))',[inset,ir,hol,lst,lr,vg])
        self.prompt('Right Overlay','IF(inset,-ir,IF(hor,(rst/2)-(vg/2),rst-rr))',[inset,ir,hor,rst,rr,vg])
        
    def set_standard_drivers(self,assembly):
        Height = self.get_var('dim_z','Height')
        Inset_Front = self.get_var("Inset Front")
        Door_Gap = self.get_var("Door to Cabinet Gap",'Door_Gap')
        tt = self.get_var("Top Thickness",'tt')
        bt = self.get_var("Bottom Thickness",'bt')
        Top_Overlay = self.get_var("Top Overlay")
        Bottom_Overlay = self.get_var("Bottom Overlay")
        eta = self.get_var("Extend Top Amount",'eta')
        eba = self.get_var("Extend Bottom Amount",'eba')
        Door_Thickness = self.get_var("Door Thickness")
        False_Front_Height = self.get_var("False Front Height")
        Vertical_Gap = self.get_var("Vertical Gap")
        
        assembly.y_loc('IF(Inset_Front,Door_Thickness,-Door_Gap)',[Inset_Front,Door_Gap,Door_Thickness])
        assembly.z_loc('IF(OR(eba==0,Inset_Front==True),-Bottom_Overlay,-eba)',
                       [Inset_Front,eba,bt,Bottom_Overlay])
        assembly.x_rot(value = 0)
        assembly.y_rot(value = -90)
        if self.false_front_qty > 0:
            assembly.x_dim('Height+IF(OR(eta==0,Inset_Front==True),Top_Overlay,eta)+IF(OR(eba==0,Inset_Front==True),Bottom_Overlay,eba)-False_Front_Height-Vertical_Gap',
                           [Inset_Front,Height,Top_Overlay,Bottom_Overlay,eta,eba,tt,bt,False_Front_Height,Vertical_Gap])
        else:
            assembly.x_dim('Height+IF(OR(eta==0,Inset_Front==True),Top_Overlay,eta)+IF(OR(eba==0,Inset_Front==True),Bottom_Overlay,eba)',
                           [Inset_Front,Height,Top_Overlay,Bottom_Overlay,eta,eba,tt,bt])
        assembly.z_dim('Door_Thickness',[Door_Thickness])
        
    def set_pull_drivers(self,assembly):
        self.set_standard_drivers(assembly)
        
        Height = self.get_var('dim_z','Height')
        Pull_Length = assembly.get_var("Pull Length")
        Pull_From_Edge = self.get_var("Pull From Edge")
        Base_Pull_Location = self.get_var("Base Pull Location")
        Tall_Pull_Location = self.get_var("Tall Pull Location")
        Upper_Pull_Location = self.get_var("Upper Pull Location")
        eta = self.get_var("Extend Top Amount",'eta')
        eba = self.get_var("Extend Bottom Amount",'eba')
        World_Z = self.get_var('world_loc_z','World_Z',transform_type='LOC_Z')
        
        assembly.prompt("Pull X Location",'Pull_From_Edge',[Pull_From_Edge])
        if self.door_type == "Base":
            assembly.prompt("Pull Z Location",'Base_Pull_Location+(Pull_Length/2)',[Base_Pull_Location,Pull_Length])
        if self.door_type == "Tall":
            assembly.prompt("Pull Z Location",'Height-Tall_Pull_Location+(Pull_Length/2)+World_Z',[Height,World_Z,Tall_Pull_Location,Pull_Length])
        if self.door_type == "Upper":
            assembly.prompt("Pull Z Location",'Height+(eta+eba)-Upper_Pull_Location-(Pull_Length/2)',[Height,eta,eba,Upper_Pull_Location,Pull_Length])
    
    def draw(self):
        g = bpy.context.scene.lm_exteriors
        self.create_assembly()
        
        self.add_doors_prompts()
        
        Height = self.get_var('dim_z','Height')
        Width = self.get_var('dim_x','Width')
        Left_Overlay = self.get_var("Left Overlay")
        Right_Overlay = self.get_var("Right Overlay")
        Left_Swing = self.get_var("Left Swing")
        Vertical_Gap = self.get_var("Vertical Gap")
        Door_Rotation = self.get_var("Door Rotation")
        No_Pulls = self.get_var("No Pulls")
        False_Front_Height = self.get_var("False Front Height")
        Door_Thickness = self.get_var("Door Thickness")
        eta = self.get_var("Extend Top Amount",'eta')
        
        if self.false_front_qty > 0:
            false_front = self.add_assembly(PART)  
            false_front.set_name("False Front")
            false_front.x_loc('-Left_Overlay',[Left_Overlay])
            false_front.y_loc(value = 0)
            false_front.z_loc('Height+eta',[Height,eta])
            false_front.x_rot(value = 90)
            false_front.y_rot(value = 0)
            false_front.z_rot(value = 0)
            if self.false_front_qty > 1:
                false_front.x_dim('(Width+Left_Overlay+Right_Overlay-Vertical_Gap)/2',[Width,Left_Overlay,Right_Overlay,Vertical_Gap])
            else:
                false_front.x_dim('Width+Left_Overlay+Right_Overlay',[Width,Left_Overlay,Right_Overlay])
            false_front.y_dim('-False_Front_Height',[False_Front_Height])
            false_front.z_dim('Door_Thickness',[Door_Thickness])
            false_front.material("Basic_Cabinet_Material")
            false_front.obj_bp.mv.is_cabinet_door = True
            
            if self.false_front_qty > 1:
                false_front_2 = self.add_assembly(PART)
                false_front_2.set_name("False Front")
                false_front_2.x_loc('Width+Right_Overlay',[Width,Right_Overlay])
                false_front_2.y_loc(value = 0)
                false_front_2.z_loc('Height+eta',[Height,eta])
                false_front_2.x_rot(value = 90)
                false_front_2.y_rot(value = 0)
                false_front_2.z_rot(value = 0)
                if self.false_front_qty > 1:
                    false_front_2.x_dim('((Width+Left_Overlay+Right_Overlay-Vertical_Gap)/2)*-1',[Width,Left_Overlay,Right_Overlay,Vertical_Gap])
                else:
                    false_front_2.x_dim('(Width+Left_Overlay+Right_Overlay)*-1',[Width,Left_Overlay,Right_Overlay])
                false_front_2.y_dim('-False_Front_Height',[False_Front_Height])
                false_front_2.z_dim('Door_Thickness',[Door_Thickness])
                false_front_2.material("Basic_Cabinet_Material")
                false_front_2.obj_bp.mv.is_cabinet_door = True
                
        #LEFT DOOR
        left_door = self.add_assembly(PART)
        left_door.set_name("Cabinet Left Door")
        self.set_standard_drivers(left_door)
        left_door.x_loc('-Left_Overlay',[Left_Overlay])
        left_door.z_rot('radians(90)-Door_Rotation',[Door_Rotation])
        if self.door_swing == 'Double Door':
            left_door.y_dim('((Width+Left_Overlay+Right_Overlay-Vertical_Gap)/2)*-1',[Width,Left_Overlay,Right_Overlay,Vertical_Gap])
        else:
            left_door.y_dim('(Width+Left_Overlay+Right_Overlay)*-1',[Width,Left_Overlay,Right_Overlay])
            left_door.prompt('Hide','IF(Left_Swing,False,True)',[Left_Swing])
        left_door.material("Basic_Cabinet_Material")
        left_door.obj_bp.mv.is_cabinet_door = True
        
        #LEFT PULL
        left_pull = Standard_Pull()
        left_pull.door_type = self.door_type
        left_pull.door_swing = "Left Swing"
        left_pull.draw()
        left_pull.set_name('Left Cabinet Pull')
        left_pull.obj_bp.parent = self.obj_bp
        self.set_pull_drivers(left_pull)
        left_pull.x_loc('-Left_Overlay',[Left_Overlay])
        left_pull.z_rot('radians(90)-Door_Rotation',[Door_Rotation])
        if self.door_swing == 'Double Door':
            left_pull.y_dim('((Width+Left_Overlay+Right_Overlay-Vertical_Gap)/2)*-1',[Width,Left_Overlay,Right_Overlay,Vertical_Gap])
            left_pull.prompt('Hide','IF(No_Pulls,True,False)',[No_Pulls])
        else:
            left_pull.y_dim('(Width+Left_Overlay+Right_Overlay)*-1',[Width,Left_Overlay,Right_Overlay])
            left_pull.prompt('Hide','IF(Left_Swing,IF(No_Pulls,True,False),True)',[Left_Swing,No_Pulls])

        #RIGHT DOOR
        right_door = self.add_assembly(PART)  
        right_door.set_name("Cabinet Right Door")
        self.set_standard_drivers(right_door)
        right_door.x_loc('Width+Right_Overlay',[Width,Right_Overlay])
        right_door.z_rot('radians(90)+Door_Rotation',[Door_Rotation])
        if self.door_swing == 'Double Door':
            right_door.y_dim('(Width+Left_Overlay+Right_Overlay-Vertical_Gap)/2',[Width,Left_Overlay,Right_Overlay,Vertical_Gap])
        else:
            right_door.y_dim('Width+Left_Overlay+Right_Overlay',[Width,Left_Overlay,Right_Overlay])
            right_door.prompt('Hide','IF(Left_Swing,True,False)',[Left_Swing])
        right_door.material("Basic_Cabinet_Material")
        right_door.obj_bp.mv.is_cabinet_door = True
        
        #RIGHT PULL
        right_pull = Standard_Pull()
        right_pull.door_type = self.door_type
        right_pull.door_swing = "Right Swing"
        right_pull.draw()
        right_pull.set_name('Right Cabinet Pull')
        right_pull.obj_bp.parent = self.obj_bp
        self.set_pull_drivers(right_pull)
        right_pull.x_loc('Width+Right_Overlay',[Width,Right_Overlay])
        right_pull.z_rot('radians(90)+Door_Rotation',[Door_Rotation])
        if self.door_swing == "Double Door":
            right_pull.y_dim('(Width+Left_Overlay+Right_Overlay-Vertical_Gap)/2',[Width,Left_Overlay,Right_Overlay,Vertical_Gap])
            right_pull.prompt('Hide','IF(No_Pulls,True,False)',[No_Pulls])
        else:
            right_pull.y_dim('(Width+Left_Overlay+Right_Overlay)',[Width,Left_Overlay,Right_Overlay])
            right_pull.prompt('Hide','IF(Left_Swing,True,IF(No_Pulls,True,False))',[Left_Swing,No_Pulls])

        self.update()
        
class Pie_Cut_Doors(fd_types.Assembly):
    
    library_name = "Cabinet Exteriors"
    type_assembly = 'INSERT'
    placement_type = "EXTERIOR"
    property_id = "exteriors.door_prompts"
    door_type = "" # {Base, Tall, Upper}
    door_swing = "" # {Left Swing, Right Swing, Double Door, Flip up}

    def add_doors_prompts(self):
        g = bpy.context.scene.lm_exteriors
        
        self.add_tab(name='Door Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        add_common_door_prompts(self)
        
        self.add_prompt(name="Half Overlay Top",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Half Overlay Bottom",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Half Overlay Left",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Half Overlay Right",prompt_type='CHECKBOX',value=False,tab_index=0)
        
        self.add_prompt(name="Vertical Gap",prompt_type='DISTANCE',value=g.Vertical_Gap,tab_index=0)
        self.add_prompt(name="Top Reveal",prompt_type='DISTANCE',value=unit.inch(.25),tab_index=0)
        self.add_prompt(name="Bottom Reveal",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Left Reveal",prompt_type='DISTANCE',value=g.Left_Reveal,tab_index=0)
        self.add_prompt(name="Right Reveal",prompt_type='DISTANCE',value=g.Right_Reveal,tab_index=0)
        
        #CALCULATED
        self.add_prompt(name="Top Overlay",prompt_type='DISTANCE',value=unit.inch(.6875),tab_index=1)
        self.add_prompt(name="Bottom Overlay",prompt_type='DISTANCE',value=unit.inch(.6875),tab_index=1)
        self.add_prompt(name="Left Overlay",prompt_type='DISTANCE',value=unit.inch(.6875),tab_index=1)
        self.add_prompt(name="Right Overlay",prompt_type='DISTANCE',value=unit.inch(.6875),tab_index=1)
        self.add_prompt(name="Hinge Quantity",prompt_type='QUANTITY',value=0,tab_index=1)
        
        #INHERITED
        self.add_prompt(name="Extend Top Amount",prompt_type='DISTANCE',value=0,tab_index=1)
        self.add_prompt(name="Extend Bottom Amount",prompt_type='DISTANCE',value=0,tab_index=1)
        self.add_prompt(name="Top Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Bottom Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Left Side Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Right Side Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Division Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        
        inset = self.get_var("Inset Front",'inset')
        ir = self.get_var("Inset Reveal",'ir')
        tr = self.get_var("Top Reveal",'tr')
        br = self.get_var("Bottom Reveal",'br')
        lr = self.get_var("Left Reveal",'lr')
        rr = self.get_var("Right Reveal",'rr')
        vg = self.get_var("Vertical Gap",'vg')
        hot = self.get_var("Half Overlay Top",'hot')
        hob = self.get_var("Half Overlay Bottom",'hob')
        hol = self.get_var("Half Overlay Left",'hol')
        hor = self.get_var("Half Overlay Right",'hor')
        tt = self.get_var("Top Thickness",'tt')
        lst = self.get_var("Left Side Thickness",'lst')
        rst = self.get_var("Right Side Thickness",'rst')
        bt = self.get_var("Bottom Thickness",'bt')
        height = self.get_var("dim_z",'height')
        
        if self.door_swing == 'Double Door':
            self.prompt('Hinge Quantity','MV_CALCULATE_HINGE_QTY(height)*2',[height])
        else:
            self.prompt('Hinge Quantity','MV_CALCULATE_HINGE_QTY(height)',[height])
        self.prompt('Top Overlay','IF(inset,-ir,IF(hot,(tt/2)-(vg/2),tt-tr))',[inset,ir,hot,tt,tr,vg])
        self.prompt('Bottom Overlay','IF(inset,-ir,IF(hob,(bt/2)-(vg/2),bt-br))',[inset,ir,hob,bt,br,vg])
        self.prompt('Left Overlay','IF(inset,-ir,IF(hol,(lst/2)-(vg/2),lst-lr))',[inset,ir,hol,lst,lr,vg])
        self.prompt('Right Overlay','IF(inset,-ir,IF(hor,(rst/2)-(vg/2),rst-rr))',[inset,ir,hor,rst,rr,vg])
        
    def set_standard_drivers(self,assembly):
        Height = self.get_var('dim_z','Height')
        Inset_Front = self.get_var("Inset Front")
        Door_Gap = self.get_var("Door to Cabinet Gap",'Door_Gap')
        tt = self.get_var("Top Thickness",'tt')
        bt = self.get_var("Bottom Thickness",'bt')
        Top_Overlay = self.get_var("Top Overlay")
        Bottom_Overlay = self.get_var("Bottom Overlay")
        eta = self.get_var("Extend Top Amount",'eta')
        eba = self.get_var("Extend Bottom Amount",'eba')
        Door_Thickness = self.get_var("Door Thickness")
        
#         assembly.y_loc('IF(Inset_Front,Door_Thickness,-Door_Gap)',[Inset_Front,Door_Gap,Door_Thickness])
        assembly.z_loc('IF(OR(eba==0,Inset_Front==True),-Bottom_Overlay,-eba)',
                       [Inset_Front,eba,bt,Bottom_Overlay])
        assembly.x_rot(value = 0)
        assembly.y_rot(value = -90)
        assembly.z_rot(value = 90)
#         assembly.x_dim('Height+IF(OR(eta==0,Inset_Front==True),Top_Overlay,tt+eta)+IF(OR(eba==0,Inset_Front==True),Bottom_Overlay,bt+eba)',
#                        [Inset_Front,Height,Top_Overlay,Bottom_Overlay,eta,eba,tt,bt])
        assembly.x_dim('Height+IF(OR(eta==0,Inset_Front==True),Top_Overlay,eta)+IF(OR(eba==0,Inset_Front==True),Bottom_Overlay,eba)',
                       [Inset_Front,Height,Top_Overlay,Bottom_Overlay,eta,eba,tt,bt])
        assembly.z_dim('Door_Thickness',[Door_Thickness])
        
    def set_pull_drivers(self,assembly):
        self.set_standard_drivers(assembly)
        
        Height = self.get_var('dim_z','Height')
        Pull_Length = assembly.get_var("Pull Length")
        Pull_From_Edge = self.get_var("Pull From Edge")
        Base_Pull_Location = self.get_var("Base Pull Location")
        Tall_Pull_Location = self.get_var("Tall Pull Location")
        Upper_Pull_Location = self.get_var("Upper Pull Location")
        eta = self.get_var("Extend Top Amount",'eta')
        eba = self.get_var("Extend Bottom Amount",'eba')
        
        assembly.prompt("Pull X Location",'Pull_From_Edge',[Pull_From_Edge])
        if self.door_type == "Base":
            assembly.prompt("Pull Z Location",'Base_Pull_Location+(Pull_Length/2)',[Base_Pull_Location,Pull_Length])
        if self.door_type == "Tall":
            assembly.prompt("Pull Z Location",'Tall_Pull_Location+(Pull_Length/2)',[Tall_Pull_Location,Pull_Length])
        if self.door_type == "Upper":
            assembly.prompt("Pull Z Location",'Height+(eta+eba)-Upper_Pull_Location-(Pull_Length/2)',[Height,eta,eba,Upper_Pull_Location,Pull_Length])
    
    def draw(self):
        g = bpy.context.scene.lm_exteriors
        self.create_assembly()
        
        self.add_doors_prompts()
        
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        Height = self.get_var('dim_z','Height')
        Left_Overlay = self.get_var("Left Overlay")
        Right_Overlay = self.get_var("Right Overlay")
        Left_Swing = self.get_var("Left Swing")
        Vertical_Gap = self.get_var("Vertical Gap")
        Door_Rotation = self.get_var("Door Rotation")
        No_Pulls = self.get_var("No Pulls")
        Door_to_Cabinet_Gap = self.get_var("Door to Cabinet Gap")
        Door_Thickness = self.get_var("Door Thickness")
        Inset_Front = self.get_var("Inset Front")
        
        #LEFT DOOR
        left_door = self.add_assembly(PART)  
        left_door.set_name("Left Cabinet Door")
        self.set_standard_drivers(left_door)
        left_door.x_loc('IF(Inset_Front,-Door_Thickness,Door_to_Cabinet_Gap)',[Door_to_Cabinet_Gap,Door_Thickness,Inset_Front])
        left_door.y_loc('Depth-Left_Overlay',[Depth,Left_Overlay])
        left_door.x_rot(value = 90)
        left_door.y_dim('(fabs(Depth)+Left_Overlay-IF(Inset_Front,0,Door_Thickness+Door_to_Cabinet_Gap))*-1',[Depth,Left_Overlay,Inset_Front,Right_Overlay,Door_Thickness,Door_to_Cabinet_Gap])
        left_door.cutpart("Slab_Door")
        left_door.edgebanding('Door_Edges',l1 = True, w1 = True, l2 = True, w2 = True)
        left_door.obj_bp.mv.is_cabinet_door = True
        left_door.material("Basic_Cabinet_Material")
        
        #LEFT PULL
        left_pull = Standard_Pull()
        left_pull.door_type = self.door_type
        left_pull.draw()
        left_pull.set_name("Left Cabinet Pull")
        left_pull.obj_bp.parent = self.obj_bp
        self.set_pull_drivers(left_pull)
        left_pull.x_loc('IF(Inset_Front,-Door_Thickness,Door_to_Cabinet_Gap)',[Door_to_Cabinet_Gap,Door_Thickness,Inset_Front])
        left_pull.y_loc('-Door_to_Cabinet_Gap',[Door_to_Cabinet_Gap])
        left_pull.x_rot(value = 90)
        left_pull.y_dim('fabs(Depth)+Left_Overlay-Door_Thickness-Door_to_Cabinet_Gap',[Depth,Left_Overlay,Right_Overlay,Door_Thickness,Door_to_Cabinet_Gap])
        left_pull.prompt('Hide','IF(Left_Swing,True,IF(No_Pulls,True,False))',[Left_Swing,No_Pulls])

        #RIGHT DOOR
        right_door = self.add_assembly(PART)  
        right_door.set_name("Right Cabinet Door")
        self.set_standard_drivers(right_door)
        right_door.x_loc('IF(Inset_Front,0,Door_to_Cabinet_Gap+Door_Thickness)',[Inset_Front,Door_to_Cabinet_Gap,Door_Thickness])
        right_door.y_loc('IF(Inset_Front,Door_Thickness,-Door_to_Cabinet_Gap)',[Inset_Front,Door_to_Cabinet_Gap,Door_Thickness])
        right_door.y_dim('(Width+Right_Overlay-IF(Inset_Front,0,Door_Thickness+Door_to_Cabinet_Gap))*-1',[Width,Inset_Front,Right_Overlay,Door_Thickness,Door_to_Cabinet_Gap])
        right_door.cutpart("Slab_Door")
        right_door.edgebanding('Door_Edges',l1 = True, w1 = True, l2 = True, w2 = True)
        right_door.obj_bp.mv.is_cabinet_door = True
        right_door.material("Basic_Cabinet_Material")
        
        #RIGHT PULL
        right_pull = Standard_Pull()
        right_pull.door_type = self.door_type
        right_pull.draw()
        right_pull.set_name("Right Cabinet Pull")
        right_pull.obj_bp.parent = self.obj_bp
        self.set_pull_drivers(right_pull)
        right_pull.x_loc('IF(Inset_Front,0,Door_to_Cabinet_Gap+Door_Thickness)',[Inset_Front,Door_to_Cabinet_Gap,Door_Thickness])
        right_pull.y_loc('IF(Inset_Front,Door_Thickness,-Door_to_Cabinet_Gap)',[Inset_Front,Door_to_Cabinet_Gap,Door_Thickness])
        right_pull.y_dim('(Width+Right_Overlay-IF(Inset_Front,0,Door_Thickness+Door_to_Cabinet_Gap))*-1',[Width,Inset_Front,Right_Overlay,Door_Thickness,Door_to_Cabinet_Gap])
        right_pull.prompt('Hide','IF(Left_Swing,IF(No_Pulls,True,False),True)',[Left_Swing,No_Pulls])

        self.update()
        
class Drawers(fd_types.Assembly):
    
    library_name = "Cabinet Exteriors"
    property_id = "exteriors.drawer_prompts"
    type_assembly = 'INSERT'
    placement_type = "EXTERIOR"
    
    door_type = "Drawer"
    direction = 'Vertical'
    add_drawer = True
    add_pull = True
    add_slide = True
    drawer_qty = 1
    top_drawer_front_height = 0

    def add_common_prompts(self):
        g = bpy.context.scene.lm_exteriors
        self.add_tab(name='Drawer Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        add_common_drawer_prompts(self)
        
        self.add_prompt(name="Half Overlay Top",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Half Overlay Bottom",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Half Overlay Left",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Half Overlay Right",prompt_type='CHECKBOX',value=False,tab_index=0)
        
        self.add_prompt(name="Top Reveal",prompt_type='DISTANCE',value=unit.inch(0.125),tab_index=0)
        self.add_prompt(name="Bottom Reveal",prompt_type='DISTANCE',value=unit.inch(0.0),tab_index=0)
        self.add_prompt(name="Left Reveal",prompt_type='DISTANCE',value=unit.inch(0.0625),tab_index=0)
        self.add_prompt(name="Right Reveal",prompt_type='DISTANCE',value=unit.inch(0.0625),tab_index=0)
        self.add_prompt(name="Inset Reveal",prompt_type='DISTANCE',value=unit.inch(0.125),tab_index=0) 
        self.add_prompt(name="Horizontal Gap",prompt_type='DISTANCE',value=unit.inch(0.125),tab_index=0)
        
        self.add_prompt(name="Door to Cabinet Gap",prompt_type='DISTANCE',value=unit.inch(0.125),tab_index=0)   
        self.add_prompt(name="Drawer Box Top Gap",prompt_type='DISTANCE',value=unit.inch(0.5),tab_index=0)
        self.add_prompt(name="Drawer Box Bottom Gap",prompt_type='DISTANCE',value=unit.inch(0.5),tab_index=0)
        self.add_prompt(name="Drawer Box Slide Gap",prompt_type='DISTANCE',value=unit.inch(0.5),tab_index=0)
        self.add_prompt(name="Drawer Box Rear Gap",prompt_type='DISTANCE',value=unit.inch(0.5),tab_index=0)
        
        #INHERITED
        self.add_prompt(name="Left Side Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
        self.add_prompt(name="Right Side Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
        self.add_prompt(name="Top Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
        self.add_prompt(name="Bottom Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
        self.add_prompt(name="Back Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
        self.add_prompt(name="Front Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
        self.add_prompt(name="Division Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
        
        #CALCULATED
        self.add_prompt(name="Top Overlay",prompt_type='DISTANCE',value=0,tab_index=1)
        self.add_prompt(name="Bottom Overlay",prompt_type='DISTANCE',value=0,tab_index=1)
        self.add_prompt(name="Left Overlay",prompt_type='DISTANCE',value=0,tab_index=1)
        self.add_prompt(name="Right Overlay",prompt_type='DISTANCE',value=0,tab_index=1)
        
        inset = self.get_var('Inset Front','inset')
        inset_reveal = self.get_var('Inset Reveal','inset_reveal')
        lst = self.get_var('Left Side Thickness','lst')
        rst = self.get_var('Right Side Thickness','rst')
        tt = self.get_var('Top Thickness','tt')
        bt = self.get_var('Bottom Thickness','bt')
        hot = self.get_var("Half Overlay Top",'hot')
        hob = self.get_var("Half Overlay Bottom",'hob')
        hol = self.get_var("Half Overlay Left",'hol')
        hor = self.get_var("Half Overlay Right",'hor')  
        tr = self.get_var("Top Reveal",'tr')
        br = self.get_var("Bottom Reveal",'br')
        lr = self.get_var("Left Reveal",'lr')
        rr = self.get_var("Right Reveal",'rr')
        
        self.prompt("Top Overlay","IF(inset,-inset_reveal,IF(hot,(tt/2)-(tr/2),tt-tr))",
                    [inset,inset_reveal,hot,tt,tr])
        
        self.prompt("Bottom Overlay","IF(inset,-inset_reveal,IF(hob,(bt/2)-(br/2),bt-br))",
                    [inset,inset_reveal,hob,bt,br])
        
        self.prompt("Left Overlay","IF(inset,-inset_reveal,IF(hol,(lst/2)-(lr/2),lst-lr))",
                    [inset,inset_reveal,hol,lst,lr])
        
        self.prompt("Right Overlay","IF(inset,-inset_reveal,IF(hor,(rst/2)-(rr/2),rst-rr))",
                    [inset,inset_reveal,hor,rst,rr])
    
    def add_drawer_height_prompts(self):
        self.add_tab(name='Drawer Heights',tab_type='CALCULATOR',calc_type="ZDIM")
        
        top_drawer_front_equal = True
        
        if self.top_drawer_front_height != 0:
            top_drawer_front_equal = False
        
        if self.drawer_qty == 2 and self.direction == 'Vertical':
            self.add_prompt(name="Top Drawer Height",prompt_type='DISTANCE',value=self.top_drawer_front_height,tab_index=2,equal=top_drawer_front_equal)
            self.add_prompt(name="Bottom Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            
        if self.drawer_qty == 3 and self.direction == 'Vertical':
            self.add_prompt(name="Top Drawer Height",prompt_type='DISTANCE',value=self.top_drawer_front_height,tab_index=2,equal=top_drawer_front_equal)
            self.add_prompt(name="Second Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            self.add_prompt(name="Bottom Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            
        if self.drawer_qty == 4 and self.direction == 'Vertical':
            self.add_prompt(name="Top Drawer Height",prompt_type='DISTANCE',value=self.top_drawer_front_height,tab_index=2,equal=top_drawer_front_equal)
            self.add_prompt(name="Second Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            self.add_prompt(name="Third Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            self.add_prompt(name="Bottom Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            
        if self.drawer_qty == 5 and self.direction == 'Vertical':
            self.add_prompt(name="Top Drawer Height",prompt_type='DISTANCE',value=self.top_drawer_front_height,tab_index=2,equal=top_drawer_front_equal)
            self.add_prompt(name="Second Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            self.add_prompt(name="Third Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            self.add_prompt(name="Fourth Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            self.add_prompt(name="Bottom Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
        
        if self.drawer_qty == 6 and self.direction == 'Vertical':
            self.add_prompt(name="Top Drawer Height",prompt_type='DISTANCE',value=self.top_drawer_front_height,tab_index=2,equal=top_drawer_front_equal)
            self.add_prompt(name="Second Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            self.add_prompt(name="Third Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            self.add_prompt(name="Fourth Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            self.add_prompt(name="Fifth Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            self.add_prompt(name="Bottom Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            
        if self.drawer_qty == 7 and self.direction == 'Vertical':
            self.add_prompt(name="Top Drawer Height",prompt_type='DISTANCE',value=self.top_drawer_front_height,tab_index=2,equal=top_drawer_front_equal)
            self.add_prompt(name="Second Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            self.add_prompt(name="Third Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            self.add_prompt(name="Fourth Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            self.add_prompt(name="Fifth Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            self.add_prompt(name="Sixth Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            self.add_prompt(name="Bottom Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            
        if self.drawer_qty == 8 and self.direction == 'Vertical':
            self.add_prompt(name="Top Drawer Height",prompt_type='DISTANCE',value=self.top_drawer_front_height,tab_index=2,equal=top_drawer_front_equal)
            self.add_prompt(name="Second Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            self.add_prompt(name="Third Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            self.add_prompt(name="Fourth Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            self.add_prompt(name="Fifth Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            self.add_prompt(name="Sixth Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            self.add_prompt(name="Seventh Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            self.add_prompt(name="Bottom Drawer Height",prompt_type='DISTANCE',value=0,tab_index=2,equal=True)
            
        inset_reveal = self.get_var('Inset Reveal','inset_reveal')
        to = self.get_var("Top Overlay",'to')
        bo = self.get_var("Bottom Overlay",'bo')
        
        self.calculator_deduction("inset_reveal*(" + str(self.drawer_qty) +"-1)-bo-to",[inset_reveal,bo,to])

    def get_assemblies(self,name):
        """ Add a Drawer Front, Drawer Box, and Pull
            To this insert
            RETURNS: drawer front, drawer box, pull
        """
        g = bpy.context.scene.lm_exteriors
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z',"Height")
        Depth = self.get_var('dim_y',"Depth")
        Left_Overlay = self.get_var("Left Overlay")
        Right_Overlay = self.get_var("Right Overlay")
        Top_Overlay = self.get_var("Top Overlay")
        Bottom_Overlay = self.get_var("Bottom Overlay")
        Drawer_Box_Slide_Gap = self.get_var("Drawer Box Slide Gap")
        Door_to_Cabinet_Gap = self.get_var("Door to Cabinet Gap")
        Front_Thickness = self.get_var("Front Thickness")
        Drawer_Box_Rear_Gap = self.get_var("Drawer Box Rear Gap")
        Drawer_Box_Top_Gap = self.get_var("Drawer Box Top Gap")
        Drawer_Box_Bottom_Gap = self.get_var("Drawer Box Bottom Gap")
        Center_Pulls_on_Drawers = self.get_var("Center Pulls on Drawers")
        Drawer_Pull_From_Top = self.get_var("Drawer Pull From Top")
        No_Pulls = self.get_var("No Pulls")
        Inset_Front = self.get_var("Inset Front")
        Open = self.get_var("Open")
        
        front = self.add_assembly(PART)
        front.set_name(name + " Drawer Front")
        front.x_loc('-Left_Overlay',[Left_Overlay])
        front.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(Depth*Open)',[Inset_Front,Door_to_Cabinet_Gap,Front_Thickness,Depth,Open])
        front.z_loc('-Bottom_Overlay',[Bottom_Overlay])
        front.x_rot(value = 90)
        front.y_rot(value = 0)
        front.z_rot(value = 0)
        front.x_dim('Width+Left_Overlay+Right_Overlay',[Width,Left_Overlay,Right_Overlay])
        front.y_dim('Height+Top_Overlay+Bottom_Overlay',[Height,Top_Overlay,Bottom_Overlay])
        front.z_dim('Front_Thickness',[Front_Thickness])
        front.material("Basic_Cabinet_Material")
        front.obj_bp.mv.is_cabinet_door = True
        
        drawer = None
        pull = None
        
        if self.add_drawer:
            drawer = self.add_assembly(DRAWER_BOX)
            drawer.set_name(name + " Drawer Box")
            drawer.x_loc('Drawer_Box_Slide_Gap',[Drawer_Box_Slide_Gap])
            drawer.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(Depth*Open)',[Inset_Front,Door_to_Cabinet_Gap,Front_Thickness,Depth,Open])
            drawer.z_loc('Drawer_Box_Bottom_Gap',[Drawer_Box_Bottom_Gap])
            drawer.x_rot(value = 0)
            drawer.y_rot(value = 0)
            drawer.z_rot(value = 0)
            drawer.x_dim('Width-(Drawer_Box_Slide_Gap*2)',[Width,Drawer_Box_Slide_Gap])
            drawer.y_dim('Depth-Drawer_Box_Rear_Gap-IF(Inset_Front,Front_Thickness,0)',[Depth,Drawer_Box_Rear_Gap,Inset_Front,Front_Thickness])
            drawer.z_dim('Height-Drawer_Box_Top_Gap-Drawer_Box_Bottom_Gap',[Height,Drawer_Box_Top_Gap,Drawer_Box_Bottom_Gap])
            
        if self.add_pull:
            pull = Standard_Pull()
            pull.door_type = self.door_type
            pull.draw()
            pull.set_name('Cabinet Pull')
            pull.obj_bp.parent = self.obj_bp
            pull.x_loc('-Left_Overlay',[Left_Overlay])
            pull.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(Depth*Open)',[Inset_Front,Door_to_Cabinet_Gap,Front_Thickness,Depth,Open])
            pull.z_loc('-Bottom_Overlay',[Bottom_Overlay])
            pull.x_rot(value = 90)
            pull.y_rot(value = 0)
            pull.z_rot(value = 0)
            pull.x_dim('Width+Left_Overlay+Right_Overlay',[Width,Left_Overlay,Right_Overlay])
            pull.y_dim('Height+Top_Overlay+Bottom_Overlay',[Height,Top_Overlay,Bottom_Overlay])
            pull.z_dim('Front_Thickness',[Front_Thickness])
            pull.prompt("Pull X Location",'IF(Center_Pulls_on_Drawers,Height/2,Drawer_Pull_From_Top)',[Center_Pulls_on_Drawers,Height,Drawer_Pull_From_Top])
            pull.prompt("Pull Z Location",'(Width/2)+Right_Overlay',[Width,Right_Overlay])
            pull.prompt("Hide",'IF(No_Pulls,True,False)',[No_Pulls])
        
        return front, drawer, pull
    
    def add_vertical_drawers(self):
        Height = self.get_var('dim_z','Height')
        Drawer_Box_Top_Gap = self.get_var('Drawer Box Top Gap')
        Drawer_Box_Bottom_Gap = self.get_var('Drawer Box Bottom Gap')
        Center_Pulls_On_Drawers = self.get_var("Center Pulls on Drawers")
        Top_Overlay = self.get_var("Top Overlay")
        Bottom_Overlay = self.get_var("Bottom Overlay")
        Drawer_Pull_From_Top = self.get_var("Drawer Pull From Top")
        Horizontal_Gap = self.get_var("Horizontal Gap")
        H1 = self.get_var("Top Drawer Height",'H1')
        H0 = self.get_var("Bottom Drawer Height",'H0')
        
        front, box, pull = self.get_assemblies('Bottom')
        front.z_loc("-Bottom_Overlay",[Bottom_Overlay])
        front.y_dim("H0",[H0])
        if box:
            box.z_loc("Drawer_Box_Bottom_Gap",[Drawer_Box_Bottom_Gap])
            box.z_dim("H0-Drawer_Box_Top_Gap-Drawer_Box_Bottom_Gap-Bottom_Overlay",[H0,Drawer_Box_Top_Gap,Drawer_Box_Bottom_Gap,Bottom_Overlay])
        if pull:
            pull.z_loc("-Bottom_Overlay",[Bottom_Overlay])
            pull.y_dim("H0",[H0])
            pull.prompt("Pull X Location",'IF(Center_Pulls_on_Drawers,H0/2,Drawer_Pull_From_Top)',[Center_Pulls_On_Drawers,H0,Drawer_Pull_From_Top])
            
        front, box, pull = self.get_assemblies('Top')
        front.z_loc("Height+Top_Overlay-H1",[Height,Top_Overlay,H1])
        front.y_dim("H1",[H1])
        Front_Z_Loc = front.get_var("loc_z","Front_Z_Loc")
        if box:
            box.z_loc("Front_Z_Loc+Drawer_Box_Bottom_Gap",[Front_Z_Loc,Drawer_Box_Bottom_Gap])
            box.z_dim("H1-Drawer_Box_Top_Gap-Drawer_Box_Bottom_Gap-Top_Overlay",[H1,Drawer_Box_Top_Gap,Drawer_Box_Bottom_Gap,Top_Overlay])
        if pull:
            pull.z_loc("Height+Top_Overlay-H1",[Height,Top_Overlay,H1])
            pull.y_dim("H1",[H1])
            pull.prompt("Pull X Location",'IF(Center_Pulls_on_Drawers,H1/2,Drawer_Pull_From_Top)',[Center_Pulls_On_Drawers,H1,Drawer_Pull_From_Top])
            
        if self.drawer_qty > 2:
            H2 = self.get_var("Second Drawer Height",'H2')
            front, box, pull = self.get_assemblies('Second')
            front.z_loc("Height+Top_Overlay-H1-H2-Horizontal_Gap",[Height,Top_Overlay,H1,H2,Drawer_Box_Bottom_Gap,Horizontal_Gap])
            front.y_dim("H2",[H2])
            Front_Z_Loc = front.get_var("loc_z","Front_Z_Loc")
            if box:
                box.z_loc("Front_Z_Loc+Drawer_Box_Bottom_Gap",[Front_Z_Loc,Drawer_Box_Bottom_Gap])
                box.z_dim("H2-Drawer_Box_Top_Gap-Drawer_Box_Bottom_Gap",[H2,Drawer_Box_Top_Gap,Drawer_Box_Bottom_Gap])
            if pull:
                pull.z_loc("Front_Z_Loc",[Front_Z_Loc])
                pull.y_dim("H2",[H2])
                pull.prompt("Pull X Location",'IF(Center_Pulls_on_Drawers,H2/2,Drawer_Pull_From_Top)',[Center_Pulls_On_Drawers,H2,Drawer_Pull_From_Top])
            
        if self.drawer_qty > 3:
            H3 = self.get_var("Third Drawer Height",'H3')
            front, box, pull = self.get_assemblies('Third')
            front.z_loc("Height+Top_Overlay-H1-H2-H3-(Horizontal_Gap*2)",[Height,Top_Overlay,H1,H2,H3,Drawer_Box_Bottom_Gap,Horizontal_Gap])
            front.y_dim("H3",[H3])
            Front_Z_Loc = front.get_var("loc_z","Front_Z_Loc")
            if box:
                box.z_loc("Front_Z_Loc+Drawer_Box_Bottom_Gap",[Front_Z_Loc,Drawer_Box_Bottom_Gap])
                box.z_dim("H3-Drawer_Box_Top_Gap-Drawer_Box_Bottom_Gap",[H3,Drawer_Box_Top_Gap,Drawer_Box_Bottom_Gap])
            if pull:
                pull.z_loc("Front_Z_Loc",[Front_Z_Loc])
                pull.y_dim("H3",[H3])
                pull.prompt("Pull X Location",'IF(Center_Pulls_on_Drawers,H3/2,Drawer_Pull_From_Top)',[Center_Pulls_On_Drawers,H3,Drawer_Pull_From_Top])

    def draw(self):
        self.create_assembly()
        self.add_common_prompts()

        if self.drawer_qty == 1:
            self.get_assemblies("Single")
        else:
            self.add_drawer_height_prompts()
            self.add_vertical_drawers()
        self.update()
        
class Horizontal_Drawers(fd_types.Assembly):
    
    library_name = "Cabinet Exteriors"
    property_id = "exteriors.drawer_prompts"
    type_assembly = 'INSERT'
    placement_type = "EXTERIOR"
    
    door_type = "Drawer"
    add_drawer = True
    add_pull = True
    drawer_qty = 1
    top_drawer_front_height = 0

    def add_common_prompts(self):
        g = bpy.context.scene.lm_exteriors
        self.add_tab(name='Drawer Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        add_common_drawer_prompts(self)
        
        self.add_prompt(name="Half Overlay Top",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Half Overlay Bottom",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Half Overlay Left",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Half Overlay Right",prompt_type='CHECKBOX',value=False,tab_index=0)
        
        self.add_prompt(name="Vertical Gap",prompt_type='DISTANCE',value=g.Vertical_Gap,tab_index=0)
        self.add_prompt(name="Top Reveal",prompt_type='DISTANCE',value=unit.inch(.25),tab_index=0)
        self.add_prompt(name="Bottom Reveal",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Left Reveal",prompt_type='DISTANCE',value=g.Left_Reveal,tab_index=0)
        self.add_prompt(name="Right Reveal",prompt_type='DISTANCE',value=g.Right_Reveal,tab_index=0)

        #CALCULATED
        self.add_prompt(name="Top Overlay",prompt_type='DISTANCE',value=unit.inch(.6875),tab_index=1)
        self.add_prompt(name="Bottom Overlay",prompt_type='DISTANCE',value=unit.inch(.6875),tab_index=1)
        self.add_prompt(name="Left Overlay",prompt_type='DISTANCE',value=unit.inch(.6875),tab_index=1)
        self.add_prompt(name="Right Overlay",prompt_type='DISTANCE',value=unit.inch(.6875),tab_index=1)
        self.add_prompt(name="Drawer Slide Quantity",prompt_type='QUANTITY',value=2,tab_index=1)
        
        #INHERITED
        self.add_prompt(name="Extend Top Amount",prompt_type='DISTANCE',value=0,tab_index=1)
        self.add_prompt(name="Extend Bottom Amount",prompt_type='DISTANCE',value=0,tab_index=1)
        self.add_prompt(name="Top Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Bottom Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Left Side Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Right Side Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Division Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        
        inset = self.get_var("Inset Front",'inset')
        ir = self.get_var("Inset Reveal",'ir')
        tr = self.get_var("Top Reveal",'tr')
        br = self.get_var("Bottom Reveal",'br')
        lr = self.get_var("Left Reveal",'lr')
        rr = self.get_var("Right Reveal",'rr')
        vg = self.get_var("Vertical Gap",'vg')
        hot = self.get_var("Half Overlay Top",'hot')
        hob = self.get_var("Half Overlay Bottom",'hob')
        hol = self.get_var("Half Overlay Left",'hol')
        hor = self.get_var("Half Overlay Right",'hor')
        tt = self.get_var("Top Thickness",'tt')
        lst = self.get_var("Left Side Thickness",'lst')
        rst = self.get_var("Right Side Thickness",'rst')
        bt = self.get_var("Bottom Thickness",'bt')
        
        self.prompt('Top Overlay','IF(inset,-ir,IF(hot,(tt/2)-(vg/2),tt-tr))',[inset,ir,hot,tt,tr,vg])
        self.prompt('Bottom Overlay','IF(inset,-ir,IF(hob,(bt/2)-(vg/2),bt-br))',[inset,ir,hob,bt,br,vg])
        self.prompt('Left Overlay','IF(inset,-ir,IF(hol,(lst/2)-(vg/2),lst-lr))',[inset,ir,hol,lst,lr,vg])
        self.prompt('Right Overlay','IF(inset,-ir,IF(hor,(rst/2)-(vg/2),rst-rr))',[inset,ir,hor,rst,rr,vg])
        
    def get_assemblies(self,name):
        """ Add a Drawer Front, Drawer Box, and Pull
            To this insert
            RETURNS: drawer front, drawer box, pull
        """
        g = bpy.context.scene.lm_exteriors
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z',"Height")
        Depth = self.get_var('dim_y',"Depth")
        Left_Overlay = self.get_var("Left Overlay")
        Right_Overlay = self.get_var("Right Overlay")
        Top_Overlay = self.get_var("Top Overlay")
        Bottom_Overlay = self.get_var("Bottom Overlay")
        Drawer_Box_Slide_Gap = self.get_var("Drawer Box Slide Gap")
        Door_to_Cabinet_Gap = self.get_var("Door to Cabinet Gap")
        Front_Thickness = self.get_var("Front Thickness")
        Drawer_Box_Rear_Gap = self.get_var("Drawer Box Rear Gap")
        Drawer_Box_Top_Gap = self.get_var("Drawer Box Top Gap")
        Drawer_Box_Bottom_Gap = self.get_var("Drawer Box Bottom Gap")
        Center_Pulls_on_Drawers = self.get_var("Center Pulls on Drawers")
        Drawer_Pull_From_Top = self.get_var("Drawer Pull From Top")
        No_Pulls = self.get_var("No Pulls")
        Vertical_Gap = self.get_var("Vertical Gap")
        Division_Thickness = self.get_var("Division Thickness")
        Open = self.get_var("Open")
        Inset_Front = self.get_var("Inset Front")
        
        front = self.add_assembly(PART)
        front.set_name(name + " Drawer Front")
        if name == "Left":
            front.x_loc('-Left_Overlay',[Left_Overlay])
        if name == "Right":
            front.x_loc('(Width/2)+(Vertical_Gap/2)',[Width,Vertical_Gap])
        front.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(Depth*Open)',[Inset_Front,Door_to_Cabinet_Gap,Front_Thickness,Depth,Open])
        front.z_loc('-Bottom_Overlay',[Bottom_Overlay])
        front.x_rot(value = 90)
        front.y_rot(value = 0)
        front.z_rot(value = 0)
        if name == "Left":
            front.x_dim('((Width-Vertical_Gap)/2)+Left_Overlay',[Width,Vertical_Gap,Left_Overlay])
        if name == "Right":
            front.x_dim('((Width-Vertical_Gap)/2)+Right_Overlay',[Width,Vertical_Gap,Right_Overlay])
        front.y_dim('Height+Top_Overlay+Bottom_Overlay',[Height,Top_Overlay,Bottom_Overlay])
        front.z_dim('Front_Thickness',[Front_Thickness])
        front.material("Basic_Cabinet_Material")
        front.obj_bp.mv.is_cabinet_door = True
        
        drawer = self.add_assembly(DRAWER_BOX)
        drawer.set_name(name + " Drawer Box")
        if name == "Left":
            drawer.x_loc('Drawer_Box_Slide_Gap',[Drawer_Box_Slide_Gap])
        if name == "Right":
            drawer.x_loc('(Width/2)+(Division_Thickness/2)+Drawer_Box_Slide_Gap',[Width,Division_Thickness,Drawer_Box_Slide_Gap])
        drawer.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(Depth*Open)',[Inset_Front,Door_to_Cabinet_Gap,Front_Thickness,Depth,Open])
        drawer.z_loc('Drawer_Box_Bottom_Gap',[Drawer_Box_Bottom_Gap])
        drawer.x_rot(value = 0)
        drawer.y_rot(value = 0)
        drawer.z_rot(value = 0)
        drawer.x_dim('((Width-Division_Thickness)/2)-(Drawer_Box_Slide_Gap*2)',[Width,Division_Thickness,Drawer_Box_Slide_Gap])
        drawer.y_dim('Depth-Drawer_Box_Rear_Gap',[Depth,Drawer_Box_Rear_Gap])
        drawer.z_dim('Height-Drawer_Box_Top_Gap-Drawer_Box_Bottom_Gap',[Height,Drawer_Box_Top_Gap,Drawer_Box_Bottom_Gap])
        
        pull = Standard_Pull()
        pull.door_type = self.door_type
        pull.draw()
        pull.obj_bp.parent = self.obj_bp
        pull.set_name(name + " Cabinet Pull")
        if name == "Left":
            pull.x_loc('-Left_Overlay',[Left_Overlay])
        if name == "Right":
            pull.x_loc('(Width/2)+(Vertical_Gap/2)',[Width,Vertical_Gap])
        pull.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(Depth*Open)',[Inset_Front,Door_to_Cabinet_Gap,Front_Thickness,Depth,Open])
        pull.z_loc('-Bottom_Overlay',[Bottom_Overlay])
        pull.x_rot(value = 90)
        pull.y_rot(value = 0)
        pull.z_rot(value = 0)
        if name == "Left":
            pull.x_dim('((Width-Vertical_Gap)/2)+Left_Overlay',[Width,Vertical_Gap,Left_Overlay])
        if name == "Right":
            pull.x_dim('((Width-Vertical_Gap)/2)+Right_Overlay',[Width,Vertical_Gap,Right_Overlay])
        pull.y_dim('Height+Top_Overlay+Bottom_Overlay',[Height,Top_Overlay,Bottom_Overlay])
        pull.z_dim('Front_Thickness',[Front_Thickness])
        pull.prompt("Pull X Location",'IF(Center_Pulls_on_Drawers,Height/2,Drawer_Pull_From_Top)',[Center_Pulls_on_Drawers,Height,Drawer_Pull_From_Top])
        pull.prompt("Pull Z Location",'(Width/4)',[Width,Right_Overlay])
        pull.prompt("Hide",'IF(No_Pulls,True,False)',[No_Pulls])
        
        return front, drawer, pull
    
    def add_horizontal_drawers(self):
        self.get_assemblies("Left")
        self.get_assemblies("Right")

    def draw(self):
        self.create_assembly()
        self.add_common_prompts()
        
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z',"Height")
        Depth = self.get_var('dim_y',"Depth")
        Division_Thickness = self.get_var("Division Thickness")
        Inset_Front = self.get_var("Inset Front")
        Front_Thickness = self.get_var("Front Thickness")
        
        division = self.add_assembly(PART)
        division.set_name("Drawer Division")
        division.x_loc('(Width/2)-(Division_Thickness/2)',[Width,Division_Thickness])
        division.y_loc('IF(Inset_Front,Front_Thickness,0)',[Inset_Front,Front_Thickness])
        division.z_loc(value = 0)
        division.x_rot(value = 90)
        division.y_rot(value = 0)
        division.z_rot(value = 90)
        division.x_dim('Depth-IF(Inset_Front,Front_Thickness,0)',[Depth,Inset_Front,Front_Thickness])
        division.y_dim('Height',[Height])
        division.z_dim('Division_Thickness',[Division_Thickness])
        division.material("Basic_Cabinet_Material")
        
        self.add_horizontal_drawers()
        self.update()

#---------OPERATORS

class PROMPTS_Door_Prompts(bpy.types.Operator):
    bl_idname = "exteriors.door_prompts"
    bl_label = "Door Prompts" 
    bl_description = "This shows all of the available door options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    assembly = None
    
    door_rotation = bpy.props.FloatProperty(name="Door Rotation",subtype='ANGLE',min=0,max=math.radians(120))
    
    door_swing = bpy.props.EnumProperty(name="Door Swing",items=[('Left Swing',"Left Swing","Left Swing"),
                                                                 ('Right Swing',"Right Swing","Right Swing"),
                                                                 ('Double Door',"Double Door","Double Door")])
    
    @classmethod
    def poll(cls, context):
        return True
        
    def check(self, context):
        swing = self.assembly.get_prompt('Swing')
        door_rotation = self.assembly.get_prompt('Door Rotation')
        if swing:
            swing.set_value(self.door_swing)
        if door_rotation:
            door_rotation.set_value(self.door_rotation)
        self.assembly.obj_bp.location = self.assembly.obj_bp.location # Redraw Viewport
        return True
        
    def execute(self, context):
        return {'FINISHED'}
        
    def set_default_properties(self):
        swing = self.assembly.get_prompt("Swing")
        door_pull = self.assembly.get_prompt("Door Pull")
        door_rotation = self.assembly.get_prompt("Door Rotation")
        if swing:
            self.door_swing = swing.value()
        if door_rotation:
            self.door_rotation = door_rotation.value()
            
    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj,'INSERT')
        self.assembly = fd_types.Assembly(obj_insert_bp)
        self.set_default_properties()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=330)
        
    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                box = layout.box()
                row = box.row()
                row.label("Open Door")
                row.prop(self,'door_rotation',slider=True,text="")
                row = box.row()
                row.label("Door Swing")
                row.prop(self,'door_swing',text="")

                inset_front = self.assembly.get_prompt('Inset Front')
                
                half_overlay_top = self.assembly.get_prompt('Half Overlay Top')
                half_overlay_bottom = self.assembly.get_prompt('Half Overlay Bottom')
                half_overlay_left = self.assembly.get_prompt('Half Overlay Left')
                half_overlay_right = self.assembly.get_prompt('Half Overlay Right')
                
                inset_reveal = self.assembly.get_prompt('Inset Reveal')
                top_reveal = self.assembly.get_prompt('Top Reveal')
                bottom_reveal = self.assembly.get_prompt('Bottom Reveal')
                left_reveal = self.assembly.get_prompt('Left Reveal')
                right_reveal = self.assembly.get_prompt('Right Reveal')
                
                vertical_gap = self.assembly.get_prompt('Vertical Gap')
                door_gap = self.assembly.get_prompt('Door to Cabinet Gap')
                
                row = box.row()
                row.label("Inset Front")
                row.prop(inset_front,'CheckBoxValue',text="")
                
                if not inset_front.value():
                    box = layout.box()
                    box.label("Half Overlays:")
                    row = box.row()
                    row.prop(half_overlay_top,'CheckBoxValue',text="Top")
                    row.prop(half_overlay_bottom,'CheckBoxValue',text="Bottom")
                    row.prop(half_overlay_left,'CheckBoxValue',text="Left")
                    row.prop(half_overlay_right,'CheckBoxValue',text="Right")
                    
                box = layout.box()
                box.label("Reveal and Gaps")
                
                if inset_front.value():
                    box.prop(inset_reveal,'DistanceValue',text="Inset Reveal")
                else:
                    col = box.column(align=True)
                    col.prop(top_reveal,'DistanceValue',text="Top Reveal")
                    col.prop(bottom_reveal,'DistanceValue',text="Bottom Reveal")
                    col.prop(left_reveal,'DistanceValue',text="Left Reveal")
                    col.prop(right_reveal,'DistanceValue',text="Right Reveal")
                 
                box.prop(vertical_gap,'DistanceValue',text="Horizontal Gap")
                box.prop(door_gap,'DistanceValue',text="Door To Cabinet Gap")

class PROMPTS_Drawer_Prompts(bpy.types.Operator):
    bl_idname = "exteriors.drawer_prompts"
    bl_label = "Drawer Prompts" 
    bl_description = "This shows all of the available drawer options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    assembly = None
    
    drawer_tabs = bpy.props.EnumProperty(name="Main Tabs",
                                         items=[('DRAWER_FRONTS',"Drawer Fronts",'Set the Drawer Front Heights'),
                                                ('DRAWER_OPTIONS',"Drawer Options",'Set the Drawer Options')],
                                         default = 'DRAWER_FRONTS')
    
    open = bpy.props.FloatProperty(name="Open",min=0,max=100,subtype='PERCENTAGE')
    
    door_swing = bpy.props.EnumProperty(name="Door Swing",items=[('Left Swing',"Left Swing","Left Swing"),
                                                                 ('Right Swing',"Right Swing","Right Swing"),
                                                                 ('Double Door',"Double Door","Double Door")])
    
    @classmethod
    def poll(cls, context):
        return True
        
    def check(self, context):
        utils.run_calculators(self.assembly.obj_bp)
        swing = self.assembly.get_prompt('Swing')
        if swing:
            swing.set_value(self.door_swing)
        self.assembly.obj_bp.location = self.assembly.obj_bp.location # Redraw Viewport
        return True
        
    def execute(self, context):
        return {'FINISHED'}
        
    def set_default_properties(self):
        pass

    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj,'INSERT')
        self.assembly = fd_types.Assembly(obj_insert_bp)
        self.set_default_properties()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=330)
    
    def draw_drawer_heights(self,layout):
        top = self.assembly.get_prompt("Top Drawer Height")
        second = self.assembly.get_prompt("Second Drawer Height")
        third = self.assembly.get_prompt("Third Drawer Height")
        bottom = self.assembly.get_prompt("Bottom Drawer Height")
        
        if top:
            row = layout.row()
            row.label("Top Drawer Height:")
            if top.equal:
                row.label(str(unit.meter_to_active_unit(top.DistanceValue)))
                row.prop(top,'equal',text="")
            else:
                row.prop(top,'DistanceValue',text="")
                row.prop(top,'equal',text="")
        
        if second:
            row = layout.row()
            row.label("Second Drawer Height:")
            if second.equal:
                row.label(str(unit.meter_to_active_unit(second.DistanceValue)))
                row.prop(second,'equal',text="")
            else:
                row.prop(second,'DistanceValue',text="")
                row.prop(second,'equal',text="")
        
        if third:
            row = layout.row()
            row.label("Third Drawer Height:")
            if third.equal:
                row.label(str(unit.meter_to_active_unit(third.DistanceValue)))
                row.prop(third,'equal',text="")
            else:
                row.prop(third,'DistanceValue',text="")
                row.prop(third,'equal',text="")
        
        if bottom:
            row = layout.row()
            row.label("Bottom Drawer Height:")
            if bottom.equal:
                row.label(str(unit.meter_to_active_unit(bottom.DistanceValue)))
                row.prop(bottom,'equal',text="")
            else:
                row.prop(bottom,'DistanceValue',text="")
                row.prop(bottom,'equal',text="")
        
    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                box = layout.box()
                row = box.row()
                row.prop(self,'drawer_tabs',expand=True)
                if self.drawer_tabs == 'DRAWER_FRONTS':
                    self.draw_drawer_heights(box)
                if self.drawer_tabs == 'DRAWER_OPTIONS':
                    inset_front = self.assembly.get_prompt('Inset Front')
                    open = self.assembly.get_prompt('Open')
                    
                    half_overlay_top = self.assembly.get_prompt('Half Overlay Top')
                    half_overlay_bottom = self.assembly.get_prompt('Half Overlay Bottom')
                    half_overlay_left = self.assembly.get_prompt('Half Overlay Left')
                    half_overlay_right = self.assembly.get_prompt('Half Overlay Right')
                    
                    inset_reveal = self.assembly.get_prompt('Inset Reveal')
                    top_reveal = self.assembly.get_prompt('Top Reveal')
                    bottom_reveal = self.assembly.get_prompt('Bottom Reveal')
                    left_reveal = self.assembly.get_prompt('Left Reveal')
                    right_reveal = self.assembly.get_prompt('Right Reveal')
                    
                    horizontal_gap  = self.assembly.get_prompt('Horizontal Gap')
                    door_gap = self.assembly.get_prompt('Door to Cabinet Gap')
                    
                    row = box.row()
                    row.label("Inset Door")
                    row.prop(inset_front,'CheckBoxValue',text="")
                    
                    row = box.row()
                    row.label("Open")
                    row.prop(open,'PercentageValue',text="")
                    
                    if not inset_front.value():
                        box = layout.box()
                        box.label("Half Overlays:")
                        row = box.row()
                        row.prop(half_overlay_top,'CheckBoxValue',text="Top")
                        row.prop(half_overlay_bottom,'CheckBoxValue',text="Bottom")
                        row.prop(half_overlay_left,'CheckBoxValue',text="Left")
                        row.prop(half_overlay_right,'CheckBoxValue',text="Right")
                        
                    box = layout.box()
                    box.label("Reveal and Gaps")
                    
                    if inset_front.value():
                        box.prop(inset_reveal,'DistanceValue',text="Inset Reveal")
                    else:
                        col = box.column(align=True)
                        col.prop(top_reveal,'DistanceValue',text="Top Reveal")
                        col.prop(bottom_reveal,'DistanceValue',text="Bottom Reveal")
                        col.prop(left_reveal,'DistanceValue',text="Left Reveal")
                        col.prop(right_reveal,'DistanceValue',text="Right Reveal")
                     
                    box.prop(horizontal_gap,'DistanceValue',text="Vertical Gap")
                    box.prop(door_gap,'DistanceValue',text="Door To Cabinet Gap")

class PROPERTIES_Scene_Variables(bpy.types.PropertyGroup):
    Inset_Door = bpy.props.BoolProperty(name="Inset Door", 
                              description="Check this to use inset doors", 
                              default=False)
    
    Inset_Reveal = bpy.props.FloatProperty(name="Inset Reveal",
                                 description="This sets the reveal for inset doors.",
                                 default=unit.inch(.125),
                                 unit='LENGTH',
                                 precision=4)
    
    Left_Reveal = bpy.props.FloatProperty(name="Left Reveal",
                                description="This sets the left reveal for overlay doors.",
                                default=unit.inch(.0625),
                                unit='LENGTH',
                                precision=4)
    
    Right_Reveal = bpy.props.FloatProperty(name="Right Reveal",
                                 description="This sets the right reveal for overlay doors.",
                                 default=unit.inch(.0625),
                                 unit='LENGTH',
                                 precision=4)
    
    Base_Top_Reveal = bpy.props.FloatProperty(name="Base Top Reveal",
                                    description="This sets the top reveal for base overlay doors.",
                                    default=unit.inch(.25),
                                    unit='LENGTH',
                                    precision=4)
    
    Tall_Top_Reveal = bpy.props.FloatProperty(name="Tall Top Reveal",
                                    description="This sets the top reveal for tall overlay doors.",
                                    default=unit.inch(0),
                                    unit='LENGTH',
                                    precision=4)
    
    Upper_Top_Reveal = bpy.props.FloatProperty(name="Upper Top Reveal",
                                     description="This sets the top reveal for upper overlay doors.",
                                     default=unit.inch(0),
                                     unit='LENGTH',
                                     precision=4)
    
    Base_Bottom_Reveal = bpy.props.FloatProperty(name="Base Bottom Reveal",
                                       description="This sets the bottom reveal for base overlay doors.",
                                       default=unit.inch(0),
                                       unit='LENGTH',
                                       precision=4)
    
    Tall_Bottom_Reveal = bpy.props.FloatProperty(name="Tall Bottom Reveal",
                                       description="This sets the bottom reveal for tall overlay doors.",
                                       default=unit.inch(0),
                                       unit='LENGTH',
                                       precision=4)
    
    Upper_Bottom_Reveal = bpy.props.FloatProperty(name="Upper Bottom Reveal",
                                        description="This sets the bottom reveal for upper overlay doors.",
                                        default=unit.inch(.25),
                                        unit='LENGTH',
                                        precision=4)
    
    Vertical_Gap = bpy.props.FloatProperty(name="Vertical Gap",
                                 description="This sets the distance between double doors.",
                                 default=unit.inch(.125),
                                 unit='LENGTH',
                                 precision=4)
    
    Door_To_Cabinet_Gap = bpy.props.FloatProperty(name="Door to Cabinet Gap",
                                        description="This sets the distance between the back of the door and the front cabinet edge.",
                                        default=unit.inch(.125),
                                        unit='LENGTH',
                                        precision=4)
    
    #PULL OPTIONS
    Base_Pull_Location = bpy.props.FloatProperty(name="Base Pull Location",
                                       description="Z Distance from the top of the door edge to the top of the pull",
                                       default=unit.inch(2),
                                       unit='LENGTH') 
    
    Tall_Pull_Location = bpy.props.FloatProperty(name="Tall Pull Location",
                                       description="Z Distance from the bottom of the door edge to the center of the pull",
                                       default=unit.inch(40),
                                       unit='LENGTH')
    
    Upper_Pull_Location = bpy.props.FloatProperty(name="Upper Pull Location",
                                        description="Z Distance from the bottom of the door edge to the bottom of the pull",
                                        default=unit.inch(2),
                                        unit='LENGTH') 
    
    Center_Pulls_on_Drawers = bpy.props.BoolProperty(name="Center Pulls on Drawers",
                                           description="Center pulls on the drawer heights. Otherwise the pull z location is controlled with Drawer Pull From Top",
                                           default=False) 
    
    No_Pulls = bpy.props.BoolProperty(name="No Pulls",
                            description="Check this option to turn off pull hardware",
                            default=False) 
    
    Pull_From_Edge = bpy.props.FloatProperty(name="Pull From Edge",
                                   description="X Distance from the door edge to the pull",
                                   default=unit.inch(1.5),
                                   unit='LENGTH') 
    
    Drawer_Pull_From_Top = bpy.props.FloatProperty(name="Drawer Pull From Top",
                                         description="When Center Pulls on Drawers is off this is the amount from the top of the drawer front to the enter pull",
                                         default=unit.inch(1.5),unit='LENGTH') 
    
    Pull_Rotation = bpy.props.FloatProperty(name="Pull Rotation",
                                  description="Rotation of pulls on doors",
                                  default=math.radians(0),
                                  subtype='ANGLE') 

    Pull_Name = bpy.props.StringProperty(name="Pull Name",default="Test Pull")

    def draw(self,layout):
        col = layout.column(align=True)
        
        box = col.box()
        box.label("Door & Drawer Defaults:")
        
        row = box.row(align=True)
        row.prop(self,"Inset_Door")
        row.prop(self,"No_Pulls")
        
        if not self.No_Pulls:
            box = col.box()
            box.label("Pull Placement:")
            
            row = box.row(align=True)
            row.label("Base Doors:")
            row.prop(self,"Base_Pull_Location",text="From Top of Door")
            
            row = box.row(align=True)
            row.label("Tall Doors:")
            row.prop(self,"Tall_Pull_Location",text="From Bottom of Door")
            
            row = box.row(align=True)
            row.label("Upper Doors:")
            row.prop(self,"Upper_Pull_Location",text="From Bottom of Door")
            
            row = box.row(align=True)
            row.label("Distance From Edge:")
            row.prop(self,"Pull_From_Edge",text="")
            
            row = box.row(align=True)
            row.prop(self,"Center_Pulls_on_Drawers")
    
            if not self.Center_Pulls_on_Drawers:
                row.prop(self,"Drawer_Pull_From_Top",text="Distance From Top")
        
        box = col.box()
        box.label("Door & Drawer Reveals:")
        
        if self.Inset_Door:
            row = box.row(align=True)
            row.label("Inset Reveals:")
            row.prop(self,"Inset_Reveal",text="")
        else:
            row = box.row(align=True)
            row.label("Standard Reveals:")
            row.prop(self,"Left_Reveal",text="Left")
            row.prop(self,"Right_Reveal",text="Right")
            
            row = box.row(align=True)
            row.label("Base Door Reveals:")
            row.prop(self,"Base_Top_Reveal",text="Top")
            row.prop(self,"Base_Bottom_Reveal",text="Bottom")
            
            row = box.row(align=True)
            row.label("Tall Door Reveals:")
            row.prop(self,"Tall_Top_Reveal",text="Top")
            row.prop(self,"Tall_Bottom_Reveal",text="Bottom")
            
            row = box.row(align=True)
            row.label("Upper Door Reveals:")
            row.prop(self,"Upper_Top_Reveal",text="Top")
            row.prop(self,"Upper_Bottom_Reveal",text="Bottom")
            
        row = box.row(align=True)
        row.label("Vertical Gap:")
        row.prop(self,"Vertical_Gap",text="")
    
        row = box.row(align=True)
        row.label("Door To Cabinet Gap:")
        row.prop(self,"Door_To_Cabinet_Gap",text="")

def register():
    bpy.utils.register_class(PROPERTIES_Scene_Variables)
    bpy.utils.register_class(PROMPTS_Door_Prompts)
    bpy.utils.register_class(PROMPTS_Drawer_Prompts)
    
    bpy.types.Scene.lm_exteriors = bpy.props.PointerProperty(type = PROPERTIES_Scene_Variables)

    
    