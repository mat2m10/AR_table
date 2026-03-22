import bpy
import sys
import os
import importlib

scripts_dir = os.path.dirname(bpy.data.filepath)
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

import scene_boards
import sandbox_floor
importlib.reload(scene_boards)
importlib.reload(sandbox_floor)

def build():
    # Z=0 is the top of the sandbox floor (Solidify grows downward)
    # so boards sitting on top of the sandbox surface = Z=0
    sandbox_top_z = 0

    scene_boards.build(z_offset=sandbox_top_z)
    print("=== Board size generation complete ===")

if __name__ == "__main__":
    build()