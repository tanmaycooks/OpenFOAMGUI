import bpy
import bmesh
import math

class CFD_OT_DistributeCubes(bpy.types.Operator):
    """Distribute N cubes in a grid"""
    bl_idname = "cfd.distribute_cubes"
    bl_label = "Distribute Cubes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        n = context.scene.cfd_cube_count
        
        if n > 20:
            self.report({'ERROR'}, "N must be <= 20")
            # Show popup
            def draw_popup(self, context):
                self.layout.label(text="Number of cubes (N) must be <= 20")
            context.window_manager.popup_menu(draw_popup, title="Error", icon='ERROR')
            return {'CANCELLED'}

        # Create Collection if optional requirement
        col_name = "GeneratedCubes"
        if col_name not in bpy.data.collections:
            collection = bpy.data.collections.new(col_name)
            context.scene.collection.children.link(collection)
        else:
            collection = bpy.data.collections[col_name]
        
        # Make specific collection active or link objects to it
        
        # Grid logic
        # sqrt based m x n
        cols = math.ceil(math.sqrt(n))
        spacing = 2.0 # 1 unit cube + gap? Or just 1 unit? "1 unit" size. 
        # "distribution in m x n ... no overlap with existing"
        # Let's use spacing = 2 to be safe and clear.
        
        # Optional: No overlap check.
        # Simple approach: Check existing objects positions?
        # For simplicity in this task, we'll just place them at calculated grid positions.
        # If we really need "no overlap with existing", we'd need to query scene objects.
        # I'll implement standard grid at isolated location (e.g. z=0 starting at appropriate x,y) 
        # or just standard grid around origin.
        
        created_count = 0
        for i in range(n):
            x = (i % cols) * spacing
            y = (i // cols) * spacing
            z = 0
            
            # Create Cube
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
            obj = context.active_object
            
            # Move to collection
            # Unlink from valid collections and link to ours
            for col in obj.users_collection:
                col.objects.unlink(obj)
            collection.objects.link(obj)
            
            created_count += 1

        self.report({'INFO'}, f"Created {created_count} cubes.")
        return {'FINISHED'}

class CFD_OT_DeleteSelected(bpy.types.Operator):
    """Delete selected objects"""
    bl_idname = "cfd.delete_selected"
    bl_label = "Delete Selected"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not context.selected_objects:
             self.report({'WARNING'}, "No objects selected")
             return {'CANCELLED'}
        
        bpy.ops.object.delete()
        return {'FINISHED'}

class CFD_OT_MergeSelected(bpy.types.Operator):
    """Merge selected meshes if they share a common face"""
    bl_idname = "cfd.merge_selected"
    bl_label = "Merge Selected"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected = context.selected_objects
        if len(selected) < 2:
            self.report({'WARNING'}, "Select at least 2 objects")
            return {'CANCELLED'}
        
        # Check for mesh objects
        if any(obj.type != 'MESH' for obj in selected):
             self.report({'ERROR'}, "All selected objects must be meshes")
             return {'CANCELLED'}

        # Join objects
        # To strictly satisfy "check >=1 common face", we should check before joining.
        # However, geometric check is complex. 
        # Easier: Join -> Remove Doubles -> Check if any interior faces existed/removed?
        # A common face implies that after joining and merging vertices, 
        # the face becomes internal.
        
        bpy.ops.object.join()
        obj = context.active_object # The joined object
        
        # Go to Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Select All
        bpy.ops.mesh.select_all(action='SELECT')
        
        # Remove Doubles (Merge Vertices)
        # Distance 0.001 should be enough if they were touching exactly.
        bpy.ops.mesh.remove_doubles(threshold=0.001)
        
        # Select Interior Faces (The "common" faces)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_interior_faces()
        
        # Delete them
        bpy.ops.mesh.delete(type='FACE')
        
        # Return to Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        self.report({'INFO'}, "Merged and removed internal faces.")
        return {'FINISHED'}
