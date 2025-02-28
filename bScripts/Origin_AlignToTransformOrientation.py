import bpy
import bmesh

"""
To use this script:

1. Open Blender and go to the Scripting workspace.
2. Create a new text block and paste the script above into the text editor.
3. Select the mesh object you want to modify and enter Edit mode.
4. Select the vertices or faces you want to use for alignment.
5. Press the "Run Script" button in the text editor to execute the script.

This script will align the origin's orientation to match the average normal direction of the selected points without changing the origin's location.
"""

def align_origin_orientation_to_selection():
    obj = bpy.context.object
    # Ensure we're in edit mode and the object is a mesh
    if obj.mode != 'EDIT' or obj.type != 'MESH':
        print("Object is not a mesh or not in edit mode.")
        return
    # Create a BMesh from the mesh data
    bm = bmesh.from_edit_mesh(obj.data)
    
    # Check if there are any selected vertices
    if not any(v.select for v in bm.verts):
        print("No vertices selected.")
        return
    
    # Save the current mode
    current_mode = bpy.context.object.mode
    
    # Create a new transform orientation from the selected vertices
    bpy.ops.transform.create_orientation(name='TempOrientation', overwrite=True)
    
    # Exit edit mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Affect only the origin
    bpy.context.scene.tool_settings.use_transform_data_origin = True
    
    # Align the object to the new transform orientation
    bpy.ops.transform.transform(
        mode='ALIGN',
        orient_type='TempOrientation'
    )
    
    # Reset the transform setting to its previous state
    bpy.context.scene.tool_settings.use_transform_data_origin = False
    
    # Change the transform orientation TempOrientation
    bpy.context.scene.transform_orientation_slots[0].type = 'TempOrientation'
    
    # Clean up the temporary transform orientation
    bpy.ops.transform.delete_orientation()

    # Change the transform orientation back to Local
    bpy.context.scene.transform_orientation_slots[0].type = 'LOCAL'
    
    
# Execute the function
align_origin_orientation_to_selection()
