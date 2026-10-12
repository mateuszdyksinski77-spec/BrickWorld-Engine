"""BrickWorld Engine: Stone Age greybox. Blender 3.6+/4.x, run with Blender Python."""
import bpy
import math
import random
import sys
from pathlib import Path
from mathutils import Vector

random.seed(14)


def mat(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value = (*color, 1)
    return m


def cube(name, loc, scale, material, bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(material)
    if bevel:
        mod = o.modifiers.new('Soft edges', 'BEVEL')
        mod.width = bevel
        mod.segments = 2
        o.modifiers.new('Weighted normals', 'WEIGHTED_NORMAL')
    return o


def sphere(name, loc, radius, material, segments=12, rings=8):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, radius=radius, location=loc)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(material)
    return o


def cylinder(name, loc, radius, depth, material, vertices=10):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(material)
    return o


def tree(x, y, height, wood, leaf):
    cylinder('TREE_Trunk', (x, y, height * .27), .22, height * .54, wood)
    for i in range(3):
        sphere('TREE_Canopy', (x + .13 * i, y, height * (.59 + .13*i)), height * (.23 - .035*i), leaf)


def character(x, y, skin, clothing):
    # Head top at z=1.80m; simple greybox character, no armature yet.
    cube('PLAYER_Torso', (x, y, 1.09), (.52, .3, .7), clothing, .08)
    sphere('PLAYER_Head', (x, y, 1.63), .17, skin)
    for s in (-1, 1):
        cube('PLAYER_Leg', (x+s*.15, y, .37), (.2, .24, .74), clothing, .05)
        cube('PLAYER_Arm', (x+s*.37, y, 1.05), (.18, .22, .65), skin, .05)


def animal(name, x, y, body, length, height):
    cube(name+'_Body', (x, y, height*.65), (length, .38, height*.45), body, .12)
    sphere(name+'_Head', (x+length*.55, y, height*.78), .24, body)
    for dx in (-length*.3, length*.3):
        for dy in (-.13, .13):
            cube(name+'_Leg', (x+dx, y+dy, height*.22), (.12, .12, height*.44), body)


def look_at(obj, point):
    direction = Vector(point) - obj.location
    obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()


def build():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    terrain = mat('Ground_Olive', (.30,.39,.25))
    cave = mat('Rock_Grey', (.32,.32,.34))
    dirt = mat('Path_Earth', (.43,.34,.24))
    wood = mat('Wood', (.32,.20,.11))
    leaf = mat('Leaves', (.17,.32,.16))
    water = mat('Water', (.16,.49,.66))
    skin = mat('Skin', (.79,.55,.35))
    cloth = mat('Clothing', (.48,.30,.17))
    deer = mat('Deer', (.60,.38,.19))
    wolf = mat('Wolf', (.42,.43,.45))
    highlight = mat('Resource_Marker', (.91,.69,.22))
    warning = mat('Blocked_Path', (.66,.22,.19))

    cube('GROUND_Main', (0, 0, -.3), (72, 60, .6), terrain)
    cube('PATH_Cave_To_Meadow', (0, 0, .012), (3, 35, .025), dirt)
    cube('ZONE_Hunting_Meadow', (0, 14, .015), (24, 15, .02), dirt)

    # Cave is a visually hollow greybox built from separate walls, floor and roof.
    # Entrance faces south (negative Y); opening is 3.6m tall, 4m wide.
    cube('CAVE_Floor', (-13, -13, .08), (15, 15, .18), cave)
    cube('CAVE_Wall_Left', (-20.5, -13, 2.8), (1, 15, 5.6), cave)
    cube('CAVE_Wall_Right', (-5.5, -13, 2.8), (1, 15, 5.6), cave)
    cube('CAVE_Back', (-13, -5.5, 2.8), (16, 1, 5.6), cave)
    cube('CAVE_Roof', (-13, -13, 5.75), (16, 15, .8), cave)
    cube('CAVE_Entrance_Left', (-18.5, -20.5, 2.8), (5, 1, 5.6), cave)
    cube('CAVE_Entrance_Right', (-7.5, -20.5, 2.8), (5, 1, 5.6), cave)
    cube('CAVE_Entrance_Header', (-13, -20.5, 4.6), (4, 1, 2), cave)
    # 4m opening between x=-15 and x=-11; header bottom = 3.6m.
    sphere('CAVE_Spring', (-16, -9, .27), 1.1, water)
    cube('CAVE_Collapse_Boulder_Placeholder', (-9, -9, 1.15), (2.2, 2.2, 2.3), warning, .15)
    cube('CAVE_Firepit', (-13, -15, .22), (1.4, 1.4, .35), dirt, .12)

    character(0, -9, skin, cloth)
    animal('DEER_Placeholder', 9, 15, deer, 1.3, 1.5)
    animal('WOLF_Placeholder', -6, 6, wolf, 1.1, 1.05)
    for x, y, h in [(-27,15,6),(-24,22,7),(-17,24,5),(-8,26,7),(2,27,6),(16,24,7),(24,19,6),(28,8,7),(23,-7,6),(-27,-3,6),(-25,-25,6),(20,-22,6)]:
        tree(x, y, h, wood, leaf)
    for i, (x, y) in enumerate([(-2,-3),(5,3),(11,5),(-8,11)]):
        cube('RESOURCE_Stone_%02d'%i, (x,y,.25), (.6,.5,.5), cave, .08)
        cylinder('RESOURCE_Wood_%02d'%i, (x+1,y+1,.2), .13, .8, wood)
        sphere('RESOURCE_Fiber_%02d'%i, (x-1,y+.6,.25), .28, highlight)
    cube('FOREST_Blocked_Gate', (0, 28, 2.2), (10, 1.2, 4.4), warning)
    for x in (-4,-2,0,2,4):
        cylinder('FOREST_Obstruction', (x,28,2.3), .3, 4.6, wood)

    # Render preview from an elevated overview angle; not a live gameplay camera.
    bpy.ops.object.camera_add(location=(38, -51, 47))
    cam = bpy.context.object
    cam.name = 'CAMERA_Overview_16x9'
    look_at(cam, (-3, 2, 0))
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = 83
    bpy.context.scene.camera = cam
    bpy.ops.object.light_add(type='AREA', location=(0, -6, 35))
    light = bpy.context.object
    light.name = 'LIGHT_Daylight'
    light.data.energy = 4500
    light.data.shape = 'DISK'
    light.data.size = 25
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 12
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.world.color = (.45,.49,.54)
    return scene


def main():
    scene = build()
    args = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    outdir = Path(args[args.index('--output')+1]) if '--output' in args else Path.cwd() / 'output'
    outdir.mkdir(parents=True, exist_ok=True)
    blend_file = outdir / 'BrickWorld_Prototype_01.blend'
    png_file = outdir / 'BrickWorld_Preview_01.png'
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_file))
    scene.render.filepath = str(png_file)
    scene.render.image_settings.file_format = 'PNG'
    if '--render' in args:
        bpy.ops.render.render(write_still=True)
        print('CREATED:', png_file)
    print('CREATED:', blend_file)


if __name__ == '__main__':
    main()
