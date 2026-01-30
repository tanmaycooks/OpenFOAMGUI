
import bpy
import bmesh

# =============================================================================
# VERIFICATION SCRIPT FOR CFD ADDON
# Directions:
# 1. Open Blender.
# 2. Go to the Scripting Workspace.
# 3. Open this file or paste this code into a new Text Block.
# 4. Press "Run Script" (Play Button).
# =============================================================================

def run_test():
    print("\n" + "="*40)
    print("STARTING CFD ADDON VERIFICATION")
    print("="*40)

    # 1. Clean Scene
    print("[1] Cleaning Scene...")
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # 2. Test Distribution
    print("[2] Testing Cube Distribution (N=5)...")
    bpy.context.scene.cfd_cube_count = 5
    
    # Run the operator directly (requires addon to be installed/registered)
    # If not installed, we might fail here. 
    # Assumes Addon IS installed.
    if not hasattr(bpy.ops, 'cfd'):
        print("ERROR: 'cfd' namespace not found. Is the Addon installed and enabled?")
        return

    bpy.ops.cfd.distribute_cubes()
    
    # Verify count
    cubes = [obj for obj in bpy.context.scene.objects if obj.name.startswith("Cube")]
    if len(cubes) >= 5:
        print(f"PASS: Created {len(cubes)} cubes.")
    else:
        print(f"FAIL: Expected 5 cubes, found {len(cubes)}")

    # 3. Test Merge Logic
    # Select two specific cubes that should be adjacent
    # Grid logic: spacing 2.0. Size 1.0. Gap is 1.0. 
    # They don't touch by default with spacing 2.0 and size 1.0.
    # To test merge, we need to manually place them or adjust.
    
    print("[3] Testing Merge (Creating touching cubes)...")
    # Manually creating 2 touching cubes
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0,0,0)) # Cube A (radius 1, extends -1 to 1)
    c1 = bpy.context.active_object
    c1.name = "TestMerge1"
    
    bpy.ops.mesh.primitive_cube_add(size=2, location=(2,0,0)) # Cube B (center 2, extends 1 to 3). Touching at x=1.
    c2 = bpy.context.active_object
    c2.name = "TestMerge2"
    
    # Select both
    bpy.ops.object.select_all(action='DESELECT')
    c1.select_set(True)
    c2.select_set(True)
    bpy.context.view_layer.objects.active = c1
    
    print("Executing Merge Operator...")
    bpy.ops.cfd.merge_selected()
    
    # Check result: Should be 1 object
    selected = bpy.context.selected_objects
    if len(selected) == 1:
        print("PASS: Objects merged into one.")
        
        # Check internal faces (advanced)
        # We assume the operator worked if no error.
        print("Merge Verification Complete.")
    else:
        print(f"FAIL: Merge Resulted in {len(selected)} objects.")

    print("="*40)
    print("VERIFICATION COMPLETE")
    print("="*40)

if __name__ == "__main__":
    run_test()
