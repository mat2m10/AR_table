import bpy
import math

# Warhammer 40K Onslaught: 44" x 90" converted to meters
WIDTH            = 44 * 0.0254   # ~1.1176 m
LENGTH           = 90 * 0.0254   # ~2.2860 m
DEPTH            = 0.10          # 10 cm slab
NR_HOLES_LENGTH  = 15
NR_HOLES_WIDTH   = 6
# 2 cm radius = 4 cm diameter
# sized to fit: garden hose (~2cm dia), electrical cable (~1cm), arduino (~0.5cm)
# with room for a rubber grommet/plug when not in use
HOLE_RADIUS      = 0.02          # 2 cm radius
HOLE_DEPTH       = DEPTH * 2     # tall enough to cut through

def create_holes(floor):
    """Create a grid of cylindrical holes in the floor using a Boolean modifier."""

    # Spacing between hole centres
    spacing_x = WIDTH  / (NR_HOLES_WIDTH  + 1)
    spacing_y = LENGTH / (NR_HOLES_LENGTH + 1)

    cutters = []

    for col in range(NR_HOLES_WIDTH):
        for row in range(NR_HOLES_LENGTH):
            x = -WIDTH  / 2 + spacing_x * (col + 1)
            y = -LENGTH / 2 + spacing_y * (row + 1)

            bpy.ops.mesh.primitive_cylinder_add(
                radius=HOLE_RADIUS,
                depth=HOLE_DEPTH,
                vertices=16,
                location=(x, y, 0)
            )
            cutter = bpy.context.active_object
            cutter.name = f"hole_cutter_{col}_{row}"
            cutters.append(cutter)

    # Join all cutters into one object for a single Boolean operation
    bpy.ops.object.select_all(action='DESELECT')
    for cutter in cutters:
        cutter.select_set(True)
    bpy.context.view_layer.objects.active = cutters[0]
    bpy.ops.object.join()
    combined_cutter = bpy.context.active_object
    combined_cutter.name = "hole_cutter_combined"
    combined_cutter.hide_set(True)
    
    # Apply Boolean modifier to floor
    bool_mod = floor.modifiers.new(name="Holes", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = combined_cutter

    # Make cutter invisible
    combined_cutter.display_type = 'WIRE'
    combined_cutter.hide_render = True

    print(f"  holes: {NR_HOLES_WIDTH * NR_HOLES_LENGTH} holes ({NR_HOLES_WIDTH}x{NR_HOLES_LENGTH} grid)")


def build(root=None):
    """Build the sandbox floor and optionally parent it to root."""

    # Clean up previous versions
    for name in ["sandbox_floor", "hole_cutter_combined"]:
        if name in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)

    # Clean up any leftover individual cutters
    for obj in [o for o in bpy.data.objects if o.name.startswith("hole_cutter_")]:
        bpy.data.objects.remove(obj, do_unlink=True)

    # Create plane
    bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "sandbox_floor"

    # Scale to table dimensions
    floor.scale = (WIDTH, LENGTH, 1.0)
    bpy.ops.object.transform_apply(scale=True)

    # Thickness via Solidify
    solidify = floor.modifiers.new(name="Solidify", type='SOLIDIFY')
    solidify.thickness = DEPTH
    solidify.offset = -1.0

    # Add holes
    create_holes(floor)

    # Parent to root if provided
    if root:
        floor.parent = root
        # Also parent the cutter so it moves with root
        if "hole_cutter_combined" in bpy.data.objects:
            bpy.data.objects["hole_cutter_combined"].parent = root

    print(f"  sandbox_floor: {WIDTH*100:.1f} cm x {LENGTH*100:.1f} cm")
    return floor