from math import sin, cos, sqrt, pi

def general_torus(r1, r2, u, v):
  x = (r1 + r2*cos(v*2*pi))*cos(u*2*pi)
  y = (r1 + r2*cos(v*2*pi))*sin(u*2*pi)
  z = r2*sin(v*2*pi)
  return [x, y, z]

def normalize_value(v):
  if (v < 0.0):
    while (v < 0.0):
      v += 1.0
  else:
    while (v > 1.0):
      v -= 1.0
  return v

def warp_var(v, factor):
  # For any factor, maps 0-->0, 1-->1
  # factor = 0 is identity
  # factor > 0 for a wee pinch at v = 1/2
  v = normalize_value(v)
  h = 2 * (v - 0.5)
  i = h + factor*h**3
  return 0.5*(1.0 + i / (1.0 + factor))

def torus(u, v):
  r1 = 5.0
  r2 = 1.0
  return general_torus(r1, r2, u, warp_var(v, 0.2))

def other_torus(u, v):
  return torus(v, u)

def general_cylinder(r, h, u, v):
  x = r*cos(u*2*pi)
  y = r*sin(u*2*pi)
  z = h*(v - 0.5)
  return [x, y, z]

def cylinder(u, v):
  r = 5.0
  h = 5.0
  return general_cylinder(r, h, u, v)

def other_cylinder(u, v):
  return cylinder(v, u)

def general_mobius(r, h, u, v):
   
  offset = h*(v-0.5)*sin(u*pi)
  x = (r + offset)*cos(u*2*pi)
  y = (r + offset)*sin(u*2*pi)
  z = h*(v-0.5)*cos(u*pi)
  return [x, y, z]

def mobius(u, v):
  r = 5.0
  h = 2.0
  return general_mobius(r, h, v, u)

def plane(u, v):
  return [u, v, 0]


def general_klein(scale, u, v):
  # Adapted from http://paulbourke.net/geometry/klein/
  u1 = 2*pi*normalize_value(warp_var(u + 0.5, 0.4)-0.5)

  v1 = 2*pi*normalize_value(v)

  c1 = cos(u1)
  c2 = sin(u1)
  r = 4.0 - 2.0*c1

  if u1 <= pi:
    x = 6*c1*(1.0 + c2) + r*c1*cos(v1)
    y = 16*c2 + r*c2*cos(v1)
  else:
    x = 6*c1*(1.0 + c2) + r*cos(v1+pi)
    y = 16*c2
  z = r * sin(v1)
  return [scale*x, scale*y, scale*z]

def klein(u,v):
  return general_klein(0.25, u, v)
