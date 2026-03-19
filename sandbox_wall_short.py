import bpy
from sandbox_floor import WIDTH, LENGTH, DEPTH
from sandbox_wall_long import WALL_THICKNESS, WALL_HEIGHT

def build(root=None, floor=None):

    short_wall_length = WIDTH

    walls = []

    for side in ["left", "right"]:
        name = f"sandbox_wall_short_{side}"
        if name in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)

        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
        wall = bpy.context.active_object
        wall.name = name

        wall.scale = (short_wall_length, WALL_THICKNESS, WALL_HEIGHT)
        bpy.ops.object.transform_apply(scale=True)

        y_sign = 1 if side == "right" else -1
        wall.location = (
            0,
            y_sign * (LENGTH / 2 + WALL_THICKNESS / 2),
            WALL_HEIGHT / 2 - DEPTH
        )

        if root:
            wall.parent = root

        walls.append(wall)
        print(f"  {name}: {short_wall_length*100:.1f} cm x {WALL_THICKNESS*100:.1f} cm x {WALL_HEIGHT*100:.1f} cm")

    return walls