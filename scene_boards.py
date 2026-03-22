import bpy

BOARD_THICKNESS = 0.01  # 1 cm
GAP = 0.05              # 5 cm gap between boards

BOARDS = [
    {
        "name": "board_kill_team",
        "label": "Kill Team (30x22\")",
        "width":  30 * 0.0254,   # 0.762 m
        "length": 22 * 0.0254,   # 0.559 m
    },
    {
        "name": "board_necromunda_tile",
        "label": "Necromunda tile (12x12\")",
        "width":  12 * 0.0254,   # 0.305 m
        "length": 12 * 0.0254,   # 0.305 m
    },
    {
        "name": "board_combat_patrol",
        "label": "Combat Patrol / Incursion (44x30\")",
        "width":  44 * 0.0254,   # 1.118 m
        "length": 30 * 0.0254,   # 0.762 m
    },
    {
        "name": "board_strike_force",
        "label": "Strike Force 2000pts (44x60\")",
        "width":  44 * 0.0254,   # 1.118 m
        "length": 60 * 0.0254,   # 1.524 m
    },
    {
        "name": "board_onslaught",
        "label": "Onslaught 3000pts (44x90\")",
        "width":  44 * 0.0254,   # 1.118 m
        "length": 90 * 0.0254,   # 2.286 m
    },
]

def build(root=None, z_offset=0):
    """Build all game boards laid out side by side on X axis, smallest to largest."""

    # Clean up previous versions
    for board in BOARDS:
        if board["name"] in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[board["name"]], do_unlink=True)

    current_x = 0  # track X position as we place boards

    for board in BOARDS:
        name   = board["name"]
        width  = board["width"]
        length = board["length"]

        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
        obj = bpy.context.active_object
        obj.name = name

        obj.scale = (width, length, BOARD_THICKNESS)
        bpy.ops.object.transform_apply(scale=True)

        # Place board with its left edge at current_x
        obj.location = (
            current_x + width / 2,
            0,
            z_offset + BOARD_THICKNESS / 2  # sit on whatever surface is passed in
        )

        if root:
            obj.parent = root

        current_x += width + GAP

        print(f"  {name}: {width*100:.1f} cm x {length*100:.1f} cm")

    print(f"  scene_boards: {len(BOARDS)} boards placed")