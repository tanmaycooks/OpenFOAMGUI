
# CFD Screening Addon for Blender

# Overview

The CFD Screening Addon is a custom Blender 2.8+ extension designed to assist in computational fluid dynamics (CFD) preprocessing. It provides utilities for generating structured cube grids, deleting objects, and merging meshes while removing internal geometry. The addon is intended to simplify early-stage CFD screening workflows inside Blender.

# Features

## Cube Distribution

The addon allows automatic generation of a specified number of cubes arranged in a grid layout for screening purposes.

## Delete Selected Objects

A utility tool to remove currently selected objects from the scene.

## Merge Selected Objects

Multiple mesh objects can be merged into a single mesh while automatically removing internal faces created due to overlapping or touching geometry.

# Installation Procedure

1. Launch Blender.
2. Navigate to Edit and then Preferences.
3. Open the Add-ons section.
4. Click the Install button located at the top right.
5. Select the cfd_addon.zip file from the task2 directory.
6. Enable the addon by checking the box labeled Object: CFD Screening Addon.

# Usage Instructions

The addon interface is accessible from the 3D View Sidebar. Press the N key to open the sidebar and select the CFD Task tab.

## Cube Generation

1. Adjust the slider to specify the number of cubes to generate.
2. Click the Distribute Cubes button to create the grid.

**  The maximum allowed value for cube generation is limited to 20 to ensure performance stability. **

# Object Tools

## Delete Selected

This option removes all currently selected objects from the scene.

## Merge Selected

1. Select two or more mesh objects that are touching or overlapping.
2. Click the Merge Selected button.

** The addon joins the selected meshes into a single object and removes internal faces created during the merge process. **

![Blender Addon Demo](assets/blender_addon_demo.png)
*(Blender Addon Interface)*

# Verification and Testing

To verify the functionality of the addon through automation:

1. Switch to the Scripting workspace in Blender.
2. Open the file task2/verify_addon_blender.py.
3. Execute the script.
4. Review the output in the System Console by selecting Window and then Toggle System Console.

** The console will display PASS or FAIL messages indicating the verification result. **