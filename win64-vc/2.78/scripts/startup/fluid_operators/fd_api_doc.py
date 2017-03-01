'''
Created on Jan 27, 2017

@author: montes
'''

import bpy
from inspect import *
import mv
import os
import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import legal,inch,cm
from reportlab.platypus import Image
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Frame, Spacer, PageTemplate, PageBreak
from reportlab.lib import colors
from reportlab.lib.pagesizes import A3, A4, landscape, portrait
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY

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
                                           self.esc_uscores(args_str) if args_str else " ",
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
    
    
class OPS_create_content_overview_doc(bpy.types.Operator):
    bl_idname = "fd_api_doc.create_content_overview"
    bl_label = "Create Fluid Content Overview Documentation"
    
    write_path = bpy.props.StringProperty(name="Write Path", default="")
    elements = []
    package = None
    
    
    def write_html(self):
        pass    
    
    def create_header(self, lib):
        hdr_style = TableStyle([('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
                                ('TOPPADDING', (0, 0), (-1, -1), 15),
                                ('FONTSIZE', (0, 0), (-1, -1), 8),
                                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
                                ('LINEBELOW', (0, 0), (-1, -1), 2, colors.black),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.white)])        
        
        lib_name = Paragraph(lib.name, ParagraphStyle("Library name paragraph style", fontSize=18))
        lib_data = [[lib_name]]
        mod_doc = getdoc(importlib.import_module(lib.package_name + "." + lib.module_name))
        lib_data.append([mod_doc])
        lib_hdr_tbl = Table(lib_data, colWidths = 500, rowHeights = None, repeatRows = 1)
        lib_hdr_tbl.setStyle(hdr_style)
        self.elements.append(lib_hdr_tbl)
    
    def create_item_table(self, lib):
        item_tbl_data = []
        item_tbl_row = []
           
        for i in lib.items:
            if i.has_thumbnail:
                lib_path = lib.lib_path
                img_path = os.path.join(lib_path, i.category_name, i.name + ".png")
                item_img = Image(img_path, inch, inch)
            else:
                item_img = None
                    
            if len(item_tbl_row) == 4:
                item_tbl_data.append(item_tbl_row)
                item_tbl_row = []
                
            i_tbl = Table([[item_img if item_img else ""], [Paragraph(i.name, ParagraphStyle("item name style", wordWrap='CJK'))]])
            item_tbl_row.append(i_tbl)    
          
        if len(item_tbl_data) > 0:
          
            item_tbl = Table(item_tbl_data, colWidths=125)
            self.elements.append(item_tbl)
            self.elements.append(Spacer(1, inch * 0.5))
    
    def write_pdf(self, context):
        print("self.write_path: ", self.write_path)
        file_path = os.path.join(self.write_path if self.write_path != "" else self.package.lib_path, "doc")
        file_name = self.package.name + ".pdf"
        
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        
        doc = SimpleDocTemplate(os.path.join(file_path, file_name), 
                                pagesize = A4,
                                leftMargin = 0.25 * inch,
                                rightMargin = 0.25 * inch,
                                topMargin = 0.25 * inch,
                                bottomMargin = 0.25 * inch)
         
        wm = context.window_manager.cabinetlib
         
        for lib in wm.lib_products:
            self.create_header(lib)
            self.create_item_table(lib)
            
        for lib in wm.lib_inserts:
            self.create_header(lib)
            self.create_item_table(lib)
         
        doc.build(self.elements)
    
    def execute(self, context):
        fd_wm = context.window_manager.mv
        
        for package in fd_wm.library_packages:
            package.enabled = False
            
        for package in fd_wm.library_packages:
            self.package = package
            package.enabled = True
            bpy.ops.fd_general.load_library_modules(external_lib_only=True)
            self.write_pdf(context)
            package.enabled = False
        
        return {'FINISHED'}
    
    
classes = [
           OPS_create_api_doc,
           OPS_create_content_overview_doc,
           ]

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()