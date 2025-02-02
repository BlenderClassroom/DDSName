# DDSName - Make naming object and object data easier.
# Copyright (C) 2019 Dwayne Savage
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as 
# published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

import bpy
from bpy.types import Panel, Operator

class DDSObj2Data(Operator):
    bl_idname = "scene.ddsname"
    bl_label = "Name Obj-> Data"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for ob in context.selected_objects:
            if ob.type != "EMPTY":
                ob.data.name = ob.name
        return {'FINISHED'}

class ddsname1(Panel):
    bl_space_type  = "VIEW_3D"
    bl_region_type = "UI"
    bl_category    = "Item"
    bl_label       = "DDS Name"
    
    def draw(self, context):
        def icon_type(ty):
            if ty == "GPENCIL":
                t = "GREASEPENCIL"
            elif ty == "LIGHT_PROBE":
                t = "OUTLINER_OB_LIGHTPROBE"
            elif ty == "SPEAKER":
                t = "SPEAKER"
            elif ty == "EMPTY" and ob.empty_display_type == "IMAGE":
                t = "IMAGE_DATA"
            else:
                #This will work as long as the Icon has type+_DATA for it's naem. 
                #Grease pencil, speaker, and light probe are the only exception I have found.
                t = ob.type+"_DATA"
            return t
        ob = context.active_object
        col = self.layout.column(align=True)
        if ob != None:
            type = icon_type(ob.type)
            row = col.row(align=True)
            row.alignment = "CENTER"
            row.label(text="Active")
            row = col.row(align=True)
            row.prop(ob, 'name', text='', icon='OBJECT_DATA')
            if type !="EMPTY_DATA":
                row = col.row(align=True)
                row.prop(ob.data, 'name', text='', icon=type)
                    
            isbone = context.active_bone
            if isbone != None:
                row = col.row(align=True)
                row.prop(isbone, 'name', text='', icon='BONE_DATA')
        else:
            col.label(text="No Active Objext")


class ddsname2(Panel):
    bl_space_type  = "VIEW_3D"
    bl_region_type = "UI"
    bl_category    = "Item"
    bl_parent_id = "ddsname1"
    bl_label = "Selected"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        col = self.layout.column(align=True)
        obs = context.selected_objects
        ct = len(obs)
        if ct > 0:
            row = col.row(align=True)
            row.operator("scene.ddsname")
            row = col.row(align=True)
            row.label(text="Object")
            row.label(text="Data")
            for obj in obs:
                row = col.row(align=False)
                row.prop(obj, "name", text='')
                if obj.type !="EMPTY":
                    row.prop(obj.data, "name", text="")

classes = [
    DDSObj2Data,
    ddsname1,
    ddsname2,
    ]
    
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if(__name__ == "__main__"):
    register()

