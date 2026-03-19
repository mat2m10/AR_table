import bpy
from sandbox_floor import WIDTH, LENGTH, DEPTH
from sandbox_wall_long import WALL_THICKNESS, WALL_HEIGHT

NR_BEAMS    = 3
BEAM_HEIGHT = 0.10  # 10 cm tall
BEAM_WIDTH  = WALL_THICKNESS  # same thickness as walls for consistency

def build(root=None, floor=None):
    """Build cross beams underneath the floor at 25%, 50%, 75% along the length."""

    # Clean up previous versions
    for obj in [o for o in bpy.data.objects if o.name.startswith("sandbox_beam_")]:
        bpy.data.objects.remove(obj, do_unlink=True)

    beams = []

    for i in range(NR_BEAMS):
        # Evenly spaced at 25%, 50%, 75% of LENGTH
        fraction = (i + 1) / (NR_BEAMS + 1)
        y = -LENGTH / 2 + fraction * LENGTH

        name = f"sandbox_beam_{i+1}"

        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
        beam = bpy.context.active_object
        beam.name = name

        # Beam runs along X (short axis), wall to wall
        beam.scale = (WIDTH + 2 * WALL_THICKNESS, BEAM_WIDTH, BEAM_HEIGHT)
        bpy.ops.object.transform_apply(scale=True)

        # Top of beam flush with floor bottom (Z = -DEPTH)
        beam.location = (
            0,
            y,
            -DEPTH - BEAM_HEIGHT / 2
        )

        if root:
            beam.parent = root

        beams.append(beam)
        print(f"  {name}: y={y*100:.1f} cm  ({fraction*100:.0f}% of length)")

    print(f"  beams: {NR_BEAMS} cross beams  {WIDTH*100:.1f} cm x {BEAM_WIDTH*100:.1f} cm x {BEAM_HEIGHT*100:.1f} cm")
    return beams