'''
Created on Jan 27, 2017

@author: montes
'''

import bpy
from inspect import *
import mv
import os

class OPS_create_api_doc(bpy.types.Operator):
    bl_idname = "fd_api_doc.create_api_doc"
    bl_label = "Create Fluid API Documentation"
    
    output_path = bpy.props.StringProperty(name="Output Path")
        
    def esc_uscores(self, string):
        if string:
            return string.replace("_", "\_")
        else:
            return
    
    def exclude_builtins(self, classes, module):
        new_classes = []
        
        for cls in classes:
            if module in cls[1].__module__:
                new_classes.append(cls)
        
        return new_classes
    
    def write_sidebar(self, modules):
        filepath = os.path.join(self.output_path, "FD_Sidebar.md")
        file = open(filepath, "w")
        fw = file.write
        
        fw("#Fluid Designer\n")
        fw("*  [Home](Home)\n")
        fw("*  [Understanding the User Interface](Understanding-the-User-Interface)\n")
        fw("*  [Navigating the 3D Viewport](Navigating-the-3D-Viewport)\n")
        fw("*  [Navigating the Library Browser](Navigating-the-Library-Browser)\n")
        fw("*  [The Room Builder Panel](The-Room-Builder-Panel)\n")
        fw("*  [Hotkeys](Fluid-Designer-Hot-Keys)\n\n")
        
        fw("#API Documentation\n")
        
        for mod in modules:
            fw("\n##mv.{}\n".format(mod[0]))
            
            classes = self.exclude_builtins(getmembers(mod[1], predicate=isclass), mod[0])
            
            if len(classes) > 0:
                for cls in classes:
                    fw("* [{}()]({})\n".format(self.esc_uscores(cls[0]), 
                                               self.esc_uscores(cls[0])))
            else:
                fw("* [mv.{}]({})\n".format(mod[0], mod[0]))
                
        file.close()
    
    def write_class_doc(self, cls):
        filepath = os.path.join(self.output_path, cls[0] + ".md")
        file = open(filepath, "w")
        fw = file.write
        
        fw("#class {}{}{}{}\n\n".format(cls[1].__module__, ".", cls[0], "():"))
        
        if getdoc(cls[1]):
            fw(self.esc_uscores(getdoc(cls[1])) + "\n\n")
         
        for func in getmembers(cls[1], predicate=isfunction):
            
            if cls[0] in func[1].__qualname__:
                args = getargspec(func[1])[0]
                args_str = ', '.join(item for item in args if item != 'self')
                 
                fw("##{}{}{}{}\n\n".format(self.esc_uscores(func[0]),
                                           "(",
                                           self.esc_uscores(args_str),
                                           ")"))
                 
                if getdoc(func[1]):
                    fw(self.esc_uscores(getdoc(func[1])) + "\n")
                else:
                    fw("Undocumented.\n\n")
            
        file.close()
        
    def write_mod_doc(self, mod):
        filepath = os.path.join(self.output_path, mod[0] + ".md")
        file = open(filepath, "w")
        fw = file.write       
        
        fw("#module {}{}:\n\n".format("mv.", mod[0]))
        
        if getdoc(mod[1]):
            fw(self.esc_uscores(getdoc(mod[1])) + "\n\n")
            
        for func in getmembers(mod[1], predicate=isfunction):
            args = getargspec(func[1])[0]
            args_str = ', '.join(item for item in args if item != 'self')
            
            fw("##{}{}{}{}\n\n".format(self.esc_uscores(func[0]),
                                       "(",
                                       self.esc_uscores(args_str if args_str else " "),
                                       ")"))
             
            if getdoc(func[1]):
                fw(self.esc_uscores(getdoc(func[1])) + "\n")
            else:
                fw("Undocumented.\n\n")            
        
        file.close() 
    
    def execute(self, context):
        modules = getmembers(mv, predicate=ismodule)
        self.write_sidebar(modules)
        
        for mod in modules:
            classes = self.exclude_builtins(getmembers(mod[1], predicate=isclass), mod[0])
             
            if len(classes) > 0:
                for cls in classes:
                    self.write_class_doc(cls)
            else:
                self.write_mod_doc(mod)             
        
        return {'FINISHED'} 
    
classes = [
           OPS_create_api_doc,
           ]

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()