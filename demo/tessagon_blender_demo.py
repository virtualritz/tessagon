import bpy
from importlib import reload
import tessagon
reload(tessagon)

from tessagon.adaptors.blender_adaptor import BlenderAdaptor
from tessagon.types.hex_tessagon import HexTessagon
from tessagon.types.tri_tessagon import TriTessagon
from tessagon.types.octo_tessagon import OctoTessagon
from tessagon.types.rhombus_tessagon import RhombusTessagon
from tessagon.types.hex_tri_tessagon import HexTriTessagon
from tessagon.types.hex_square_tri_tessagon import HexSquareTriTessagon
from tessagon.types.square_tessagon import SquareTessagon
from tessagon.types.pythagorean_tessagon import PythagoreanTessagon
from tessagon.types.brick_tessagon import BrickTessagon
from tessagon.types.dodeca_tessagon import DodecaTessagon

from tessagon.misc.shapes import torus, other_torus, cylinder, \
  other_cylinder, mobius, plane, klein

# Optional, for the wire_skin demos
# https://github.com/cwant/wire_skin
is_wire_skin_loaded = False
try:
  import wire_skin
  reload(wire_skin)
  from wire_skin import WireSkin
  is_wire_skin_loaded = True
except:
  print('Could not load wire_skin, some demoes skipped')

def main():
  # A bunch of layers have demos

  # Hexagon Torii
  layer1()
  
  # Triangle Torii
  layer2()
  
  # RhombusTessagon
  layer3()

  # OctoTessagon
  layer4()

  # HexTriTessagon
  layer5()

  # HexSquareTriTessagon
  layer6()

  # SquareTessagon
  layer7()

  # PythagoreanTessagon
  layer8()

  # BrickTessagon
  layer9()

  # DodecaTessagon
  layer10()

  # Non-cyclic Torus
  layer18()

  # Mobius Tessagon
  layer19()

  if is_wire_skin_loaded:
    # WireSkin demo, hexagons
    layer20()

def tessellate(out_name, f, tessagon_class, **kwargs):
  output_object = bpy.data.objects[out_name]
  me = output_object.data
  output_materials = me.materials

  extra_args = {'adaptor_class' : BlenderAdaptor}
  tessagon = tessagon_class(f, **{**kwargs, **extra_args})

  bm = tessagon.create_mesh()
  bm.to_mesh(me)
  output_object.data = me
  me.update()
  
def layer1():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 35,
    'v_num': 5
  }
  tessellate("HexTorus1", torus, HexTessagon, **options)

  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 8,
    'v_num': 20
  }
  tessellate("HexTorus2", other_torus, HexTessagon, **options)

  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 3,
    'v_num': 2,
    'u_cyclic': False,
    'v_cyclic': False
  }
  tessellate("HexPlane1", plane, HexTessagon, **options)

def layer2():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 35,
    'v_num': 12
  }
  tessellate("TriTorus1", torus, TriTessagon, **options)

  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 6,
    'v_num': 35
  }
  tessellate("TriTorus2", other_torus, TriTessagon, **options)

  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 2,
    'v_num': 4,
    'u_cyclic': False,
    'v_cyclic': False
  }
  tessellate("TriPlane1", plane, TriTessagon, **options)

def layer3():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 30,
    'v_num': 4
  }
  tessellate("RhombusTorus1", torus, RhombusTessagon, **options)

  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 3,
    'v_num': 2,
    'u_cyclic': False,
    'v_cyclic': False
  }
  tessellate("RhombusPlane1", plane, RhombusTessagon, **options)

def layer4():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 40,
    'v_num': 8
  }
  tessellate("OctoTorus1", torus, OctoTessagon, **options)

  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 3,
    'v_num': 3,
    'u_cyclic': False,
    'v_cyclic': False
  }
  tessellate("OctoPlane1", plane, OctoTessagon, **options)

def layer5():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 40,
    'v_num': 6
  }
  tessellate("HexTriTorus1", torus, HexTriTessagon, **options)

  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 3,
    'v_num': 2,
    'u_cyclic': False,
    'v_cyclic': False
  }
  tessellate("HexTriPlane1", plane, HexTriTessagon, **options)

def layer6():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 45,
    'v_num': 5
  }
  tessellate("HexSquareTriTorus1", torus, HexSquareTriTessagon, **options)

  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 3,
    'v_num': 2,
    'u_cyclic': False,
    'v_cyclic': False
  }
  tessellate("HexSquareTriPlane1", plane, HexSquareTriTessagon, **options)

def layer7():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 15,
    'v_num': 4,
    'rot_factor': 2
  }
  tessellate("SquareTorus1", torus, SquareTessagon, **options)

  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 2,
    'v_num': 2,
    'u_cyclic': False,
    'v_cyclic': False
  }
  tessellate("SquarePlane1", plane, SquareTessagon, **options)

def layer8():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 25,
    'v_num': 6
  }
  tessellate("PythagoreanTorus1", torus, PythagoreanTessagon, **options)

  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 2,
    'v_num': 2,
    'u_cyclic': False,
    'v_cyclic': False
  }
  tessellate("PythagoreanPlane1", plane, PythagoreanTessagon, **options)

def layer9():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 15,
    'v_num': 3,
    'rot_factor': 3
  }
  tessellate("BrickTorus1", torus, BrickTessagon, **options)

  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 4,
    'v_num': 4,
    'u_cyclic': False,
    'v_cyclic': False
  }
  tessellate("BrickPlane1", plane, BrickTessagon, **options)

def layer10():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 25,
    'v_num': 3,
  }
  tessellate("DodecaTorus1", torus, DodecaTessagon, **options)

  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 3,
    'v_num': 2,
    'u_cyclic': False,
    'v_cyclic': False
  }
  tessellate("DodecaPlane1", plane, DodecaTessagon, **options)

def wire_to_skin(in_name, out_name, **kwargs):
  input_object = bpy.data.objects[in_name]
  output_object = bpy.data.objects[out_name]
  output_materials = output_object.data.materials

  wire_skin = \
    WireSkin(input_object.data, **kwargs)

  me = wire_skin.create_mesh()
  for material in output_materials:
    me.materials.append(material)
  output_object.data = me

def layer18():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 40,
    'v_num': 5,
    'u_cyclic': True,
    'v_cyclic': False
  }
  tessellate("HexCylinder1", cylinder, HexTessagon, **options)

def layer19():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 5,
    'v_num': 40,
    'u_cyclic': False,
    'v_cyclic': False
  }
  tessellate("HexMobius1", mobius, HexTessagon, **options)

  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 40,
    'v_num': 10,
    'u_cyclic': False,
  }
  #tessellate("Klein1", klein, BrickTessagon, **options)

def layer20():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 8,
    'v_num': 20
  }
  tessellate("HexTorusIn", other_torus, HexTessagon, **options)

  options = {
    'width': 0.1,
    'height': 0.4,
    'inside_radius': 0.1,
    'outside_radius': 0.2,
    'dist': 0.1,
    'crease': 1.0
  }
  wire_to_skin("HexTorusIn", "WireTorusOut", **options)
