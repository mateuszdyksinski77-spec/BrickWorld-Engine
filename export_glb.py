"""Export current Blender scene as Android-friendly GLB.
Run: blender -b BrickWorld_Prototype_01.blend --python export_glb.py -- --output output/BrickWorld_Prototype_01.glb
"""
import bpy
import sys
from pathlib import Path


def output_path():
    args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    if '--output' in args:
        return Path(args[args.index('--output') + 1]).expanduser().resolve()
    return (Path.cwd() / 'output' / 'BrickWorld_Prototype_01.glb').resolve()


def main():
    destination = output_path()
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Cameras and lights aren't required for the static Android model viewer.
    bpy.ops.export_scene.gltf(
        filepath=str(destination),
        export_format='GLB',
        use_selection=False,
        export_cameras=False,
        export_lights=False,
        export_apply=True,
    )
    if not destination.is_file() or destination.stat().st_size == 0:
        raise RuntimeError(f'GLB export missing or empty: {destination}')
    print(f'GLB_CREATED: {destination} ({destination.stat().st_size} bytes)')


if __name__ == '__main__':
    main()
