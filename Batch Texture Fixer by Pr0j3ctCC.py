import bpy
import os
from bpy.props import StringProperty, FloatVectorProperty
from bpy.types import Operator, Panel, PropertyGroup

bl_info = {
    "name": "Batch Texture Fixer by Pr0j3ctCC",
    "blender": (3, 0, 0),
    "category": "Object",
    "author": "Pr0j3ctCC",
    "version": (1, 0, 0),
    "description": "Assigns textures to selected objects and allows real-time adjustment of texture mapping.",
    "location": "View3D > Sidebar > Batch Texture Fixer",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "support": "COMMUNITY"
}

# Property group to store texture properties
class TextureProperties(PropertyGroup):
    folder_path: StringProperty(
        name="Folder Path",
        description="Path to the folder containing textures",
        default="",
        subtype='DIR_PATH'
    )
    texture_scale: FloatVectorProperty(
        name="Texture Scale",
        description="Scale the texture size",
        default=(1.0, 1.0),
        subtype='TRANSLATION',
        size=2,
        min=0.001,
        update=lambda self, context: self.update_texture_mapping(context)
    )
    texture_offset: FloatVectorProperty(
        name="Texture Offset",
        description="Offset the texture position",
        default=(0.0, 0.0),
        subtype='TRANSLATION',
        size=2,
        update=lambda self, context: self.update_texture_mapping(context)
    )
    texture_rotation: FloatVectorProperty(
        name="Texture Rotation",
        description="Rotate the texture",
        default=(0.0, 0.0, 0.0),
        subtype='EULER',
        size=3,
        update=lambda self, context: self.update_texture_mapping(context)
    )

    def update_texture_mapping(self, context):
        selected_obj = context.active_object
        if selected_obj:
            for slot in selected_obj.material_slots:
                if slot.material:
                    tree = slot.material.node_tree
                    mapping_node = None
                    for node in tree.nodes:
                        if node.type == 'MAPPING':
                            mapping_node = node
                            break
                    if mapping_node:
                        mapping_node.inputs['Scale'].default_value = (*self.texture_scale, 1.0)
                        mapping_node.inputs['Location'].default_value = (*self.texture_offset, 0.0)
                        mapping_node.inputs['Rotation'].default_value = (self.texture_rotation.x, self.texture_rotation.y, self.texture_rotation.z)

    def apply_to_all(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                for slot in obj.material_slots:
                    if slot.material:
                        tree = slot.material.node_tree
                        mapping_node = None
                        for node in tree.nodes:
                            if node.type == 'MAPPING':
                                mapping_node = node
                                break
                        if mapping_node:
                            mapping_node.inputs['Scale'].default_value = (*self.texture_scale, 1.0)
                            mapping_node.inputs['Location'].default_value = (*self.texture_offset, 0.0)
                            mapping_node.inputs['Rotation'].default_value = (self.texture_rotation.x, self.texture_rotation.y, self.texture_rotation.z)

# Operator to assign textures to selected objects
class OBJECT_OT_assign_textures(Operator):
    bl_idname = "object.assign_textures"
    bl_label = "Assign Textures"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.texture_props
        folder_path = props.folder_path
        
        if not folder_path:
            self.report({'ERROR'}, "No folder path specified")
            return {'CANCELLED'}
        
        # Get the list of image files in the folder
        image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        if not image_files:
            self.report({'ERROR'}, "No image files found in the specified folder")
            return {'CANCELLED'}
        
        # Get the selected objects
        selected_objects = context.selected_objects
        
        if not selected_objects:
            self.report({'ERROR'}, "No objects selected")
            return {'CANCELLED'}
        
        # Assign images as textures to selected objects
        for i, obj in enumerate(selected_objects):
            if obj.type != 'MESH':
                continue
            
            img_path = os.path.join(folder_path, image_files[i % len(image_files)])
            img = bpy.data.images.load(filepath=img_path)
            
            # Check if the object already has a material
            if obj.material_slots:
                mat = obj.material_slots[0].material
            else:
                mat = bpy.data.materials.new(name=f"Material_{obj.name}")
                obj.data.materials.append(mat)
            
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            
            # Remove existing nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            tex_coord_node = nodes.new(type="ShaderNodeTexCoord")
            mapping_node = nodes.new(type="ShaderNodeMapping")
            tex_image_node = nodes.new(type="ShaderNodeTexImage")
            bsdf_node = nodes.new(type="ShaderNodeBsdfPrincipled")
            output_node = nodes.new(type="ShaderNodeOutputMaterial")

            # Position nodes
            tex_coord_node.location = (-600, 300)
            mapping_node.location = (-400, 300)
            tex_image_node.location = (-200, 300)
            bsdf_node.location = (0, 300)
            output_node.location = (200, 300)

            # Link nodes
            links = mat.node_tree.links
            links.new(tex_coord_node.outputs['UV'], mapping_node.inputs['Vector'])
            links.new(mapping_node.outputs['Vector'], tex_image_node.inputs['Vector'])
            links.new(tex_image_node.outputs['Color'], bsdf_node.inputs['Base Color'])
            links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])

            # Set image for texture image node
            tex_image_node.image = img

        self.report({'INFO'}, "Textures assigned successfully")
        return {'FINISHED'}

# Operator to apply mapping settings to all selected objects
class OBJECT_OT_apply_to_all(Operator):
    bl_idname = "object.apply_to_all"
    bl_label = "Apply to All"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.texture_props
        props.apply_to_all(context)
        self.report({'INFO'}, "Mapping settings applied to all selected objects")
        return {'FINISHED'}

# Panel to display texture properties
class VIEW3D_PT_texture_panel(Panel):
    bl_label = "Batch Texture Fixer by Pr0j3ctCC"
    bl_idname = "VIEW3D_PT_texture_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Batch Texture Fixer'
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.texture_props
        
        layout.prop(props, "folder_path")
        layout.operator("object.assign_textures", text="Assign Textures")
        layout.separator()
        layout.label(text="Texture Mapping:")
        layout.prop(props, "texture_scale")
        layout.prop(props, "texture_offset")
        layout.prop(props, "texture_rotation")
        layout.operator("object.apply_to_all", text="Apply to All")

# Register the classes
classes = [TextureProperties, OBJECT_OT_assign_textures, OBJECT_OT_apply_to_all, VIEW3D_PT_texture_panel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.texture_props = bpy.props.PointerProperty(type=TextureProperties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.texture_props

if __name__ == "__main__":
    register()
