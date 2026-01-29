import bpy

class CFD_PT_Panel(bpy.types.Panel):
    """Creates a Panel in the View3D UI"""
    bl_label = "CFD Task Panel"
    bl_idname = "CFD_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CFD Task'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Cube Generation:")
        layout.prop(scene, "cfd_cube_count")
        layout.operator("cfd.distribute_cubes")

        layout.separator()
        layout.label(text="Tools:")
        layout.operator("cfd.delete_selected")
        layout.operator("cfd.merge_selected")
