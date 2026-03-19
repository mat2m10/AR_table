import bpy
import sys
import os
import importlib

# --- Path setup (safe to repeat) ---
scripts_dir = os.path.dirname(bpy.data.filepath)
if scripts_dir not in sys.path:
    sys.path.append(scripts_dir)

# --- Imports with reload (picks up edits without restarting Blender) ---
import sandbox_floor
import sandbox_wall_long
import sandbox_wall_short
import sandbox_beams
importlib.reload(sandbox_floor)
importlib.reload(sandbox_wall_long)
importlib.reload(sandbox_wall_short)
importlib.reload(sandbox_beams)

# ------------------------------------------------------------------ #
#  UTILS
# ------------------------------------------------------------------ #

def create_root_empty(name="sandbox_root"):
    """Create or recreate the root Empty that anchors the whole scene."""
    if name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)

    bpy.ops.object.empty_add(type='ARROWS', location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = name
    return root


def parent_to_root(root):
    """Parent all sandbox_ objects (except root itself) to the root empty."""
    for obj in bpy.data.objects:
        if obj.name.startswith("sandbox_") and obj != root:
            obj.parent = root

# ------------------------------------------------------------------ #
#  BUILD
# ------------------------------------------------------------------ #

def build():
    root  = create_root_empty()
    floor = sandbox_floor.build(root)
    walls_long = sandbox_wall_long.build(root=root, floor=floor)
    walls_short = sandbox_wall_short.build(root=root, floor=floor)
    beams = sandbox_beams.build(root=root, floor=floor)
    print("=== Assembly complete ===")

# ------------------------------------------------------------------ #
#  ENTRY POINT
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    build()
