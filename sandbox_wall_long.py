import bpy
from sandbox_floor import WIDTH, LENGTH, DEPTH

WALL_THICKNESS = 0.08  # 8 cm
WALL_HEIGHT    = 0.15  # 15 cm

def build(root=None, floor=None):
    """Build the two long walls, sized relative to the floor."""

    # Use constants directly — dimensions unreliable with unapplied modifiers
    floor_length = LENGTH  # 90" side
    floor_width  = WIDTH   # 44" side

    long_wall_length = floor_length + 2 * WALL_THICKNESS

    walls = []

    for side in ["front", "back"]:
        name = f"sandbox_wall_long_{side}"
        if name in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)

        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
        wall = bpy.context.active_object
        wall.name = name
        wall.scale = (WALL_THICKNESS, long_wall_length, WALL_HEIGHT)
        bpy.ops.object.transform_apply(scale=True)
        x_sign = 1 if side == "front" else -1
        wall.location = (
            x_sign * (WIDTH / 2 + WALL_THICKNESS / 2),
            0,
            WALL_HEIGHT / 2 - DEPTH
        )
        if root:
            wall.parent = root

        walls.append(wall)
        print(f"  {name}: {long_wall_length*100:.1f} cm x {WALL_THICKNESS*100:.1f} cm x {WALL_HEIGHT*100:.1f} cm")

    return walls