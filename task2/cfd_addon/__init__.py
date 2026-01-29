bl_info = {
    "name": "CFD Screening Addon",
    "author": "Candidate Name",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > CFD Tab",
    "description": "Distribute, Delete, and Merge Cubes",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

import bpy
from .panel import CFD_PT_Panel
from .operators import CFD_OT_DistributeCubes, CFD_OT_DeleteSelected, CFD_OT_MergeSelected

classes = (
    CFD_OT_DistributeCubes,
    CFD_OT_DeleteSelected,
    CFD_OT_MergeSelected,
    CFD_PT_Panel
)

def register():
    # Register property
    bpy.types.Scene.cfd_cube_count = bpy.props.IntProperty(
        name="N",
        description="Number of Cubes",
        default=5,
        min=1,
        max=100 # Allow input >20 to trigger check in operator
    )
    
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Scene.cfd_cube_count

if __name__ == "__main__":
    register()
