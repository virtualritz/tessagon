from tessagon.core.abstract_tile import AbstractTile

class Tile(AbstractTile):
  def __init__(self, tessagon, **kwargs):
    super().__init__(tessagon, **kwargs)

    self.mesh_adaptor = tessagon.mesh_adaptor

    self.verts = self.init_verts()
    self.faces = self.init_faces()

  def add_vert(self, index_keys, ratio_u, ratio_v, **kwargs):
    # Use the mesh adaptor to create a vertex.
    # In reality, multiple vertices may get defined if symmetry is declared
    vert = self._get_vert(index_keys)
    if not vert:
      coords = self.f(*self._blend(ratio_u, ratio_v))
      vert = self.mesh_adaptor.create_vert(coords)

      self._set_vert(index_keys, vert)
      if 'vert_type' in kwargs:
        if not kwargs['vert_type'] in self.tessagon.vert_types:
          self.tessagon.vert_types[kwargs['vert_type']] = []
          self.tessagon.vert_types[kwargs['vert_type']].append(face)

    # We add additional vertices by flipping 'left', 'right' etc
    # if the tile has some kind of symmetry defined
    self._create_symmetric_verts(index_keys, ratio_u, ratio_v, **kwargs)
    
    # On the boundary, make sure equivalent vertices are set on neighbor tiles
    self._set_equivalent_neighbor_verts(index_keys, vert, **kwargs)

    return vert

  def set_equivalent_vert(self, neighbor_keys, index_keys, vert, **kwargs):
    # On boundary, the vert on a neighbor is equivalent to this vert
    # This is usually only called indirectly via add_vert, but check out
    # PythagoreanTile for an example of direct usage
    if not vert:
      return None
    tile = self.get_neighbor_tile(neighbor_keys)
    if not tile:
      return None

    tile._set_vert(self._index_path(index_keys, neighbor_keys), vert)

  def add_face(self, index_keys, vert_index_keys_list, **kwargs):
    # Use the mesh adaptor to create a face.
    # In reality, multiple faces may get defined if symmetry is declared
    if self._get_face(index_keys):
      return None

    verts = self._get_verts_from_list(vert_index_keys_list)
    if not verts: return None

    face = self.mesh_adaptor.create_face(verts)
    self._set_face(index_keys, face)

    # The tessagon might keep a list of specific face types
    if 'face_type' in kwargs:
      if not kwargs['face_type'] in self.tessagon.face_types:
        self.tessagon.face_types[kwargs['face_type']] = []
      self.tessagon.face_types[kwargs['face_type']].append(face)

    # We add additional faces by flipping 'left', 'right' etc
    # if the tile has some kind of symmetry defined
    self._create_symmetric_faces(index_keys, vert_index_keys_list, **kwargs)

    # On the boundary, make sure equivalent faces are set on neighbor tiles
    self._set_equivalent_neighbor_faces(index_keys, face, **kwargs)

    return face

  def set_equivalent_face(self, neighbor_keys, index_keys, face, **kwargs):
    # On boundary, the face on a neighbor is equivalent to this face
    # This is usually only called indirectly via add_face, but check out
    # PythagoreanTile for an example of direct usage
    tile = self.get_neighbor_tile(neighbor_keys)
    if not tile:
      return None
    tile._set_face(self._index_path(index_keys, neighbor_keys), face)

  ### Below are protected

  def _get_vert(self, index_keys):
    return self._get_nested_list_value(self.verts, index_keys)

  def _set_vert(self, index_keys, value):
    self._set_nested_list_value(self.verts, index_keys, value)

  def _get_face(self, index_keys):
    return self._get_nested_list_value(self.faces, index_keys)

  def _set_face(self, index_keys, value):
    self._set_nested_list_value(self.faces, index_keys, value)

  def _get_neighbor_vert(self, neighbor_keys, index_keys):
    # See comment about neighbors in AbstractTile
    tile = self.get_neighbor_tile(neighbor_keys)
    if not tile:
      return None
    return tile._get_vert(self._index_path(index_keys, neighbor_keys))

  def _create_symmetric_verts(self, index_keys, ratio_u, ratio_v, **kwargs):
    # The 'symmetry' keyword is just to ensure we don't recurse forever
    if not 'symmetry' in kwargs:
      extra_args = { 'symmetry': True}
      if self.u_symmetric:
        # Add reflection about u
        u_flip_keys = self._u_flip(index_keys)
        self.add_vert(u_flip_keys, 1.0 - ratio_u, ratio_v,
                      **{**kwargs, **extra_args})
        if self.v_symmetric:
          # Add diagonally across
          uv_flip_keys = self._v_flip(u_flip_keys)
          self.add_vert(uv_flip_keys, 1.0 - ratio_u, 1.0 - ratio_v,
                        **{**kwargs, **extra_args})
      if self.v_symmetric:
        # Add reflection about v
        v_flip_keys = self._v_flip(index_keys)
        self.add_vert(v_flip_keys, ratio_u, 1.0 - ratio_v,
                      **{**kwargs, **extra_args})

  def _set_equivalent_neighbor_verts(self, index_keys, vert, **kwargs):
    if 'u_boundary' in kwargs:
      self._set_u_equivalent_vert(index_keys, vert, **kwargs)
    if 'v_boundary' in kwargs:
      self._set_v_equivalent_vert(index_keys, vert, **kwargs)
    if 'corner' in kwargs:
      self._set_u_equivalent_vert(index_keys, vert, **kwargs)
      self._set_v_equivalent_vert(index_keys, vert, **kwargs)
      self._set_uv_equivalent_vert(index_keys, vert, **kwargs)

  # Handle vert on left/right boundary
  def _set_u_equivalent_vert(self, index_keys, vert, **kwargs):
    u_index = self._u_index(index_keys)
    u_flip_keys = self._u_flip(index_keys)
    self.set_equivalent_vert([u_index], u_flip_keys, vert, **kwargs)

  # Handle vert on top/bottom boundary
  def _set_v_equivalent_vert(self, index_keys, vert, **kwargs):
    v_index = self._v_index(index_keys)
    v_flip_keys = self._v_flip(index_keys)
    self.set_equivalent_vert([v_index], v_flip_keys, vert, **kwargs)

  # Handle vert on corner, equivalent to vert on diagonal tile
  def _set_uv_equivalent_vert(self, index_keys, vert, **kwargs):
    u_index = self._u_index(index_keys)
    v_index = self._v_index(index_keys)
    u_flip_keys = self._u_flip(index_keys)
    uv_flip_keys = self._v_flip(u_flip_keys)
    self.set_equivalent_vert([u_index, v_index], uv_flip_keys, vert, **kwargs)

  def _get_verts_from_list(self, vert_index_keys_list):
    verts = []
    for vert_index_keys in vert_index_keys_list:
      if isinstance(vert_index_keys[0], list):
        vert = self._get_neighbor_vert(vert_index_keys[0], vert_index_keys[1])
      else:
        vert = self._get_vert(vert_index_keys)
      if not vert: return None
      verts.append(vert)

    return verts
    
  def _create_symmetric_faces(self, index_keys, vert_index_keys_list, **kwargs):
    # The 'symmetry' keyword is just to ensure we don't recurse forever
    if not 'symmetry' in kwargs:
      extra_args = { 'symmetry': True}
      if self.u_symmetric:
        # Add reflection about u
        u_flip_keys = self._u_flip(index_keys)
        u_flip_vert_index_keys_list = self._u_flip(vert_index_keys_list)
        self.add_face(u_flip_keys, u_flip_vert_index_keys_list,
                      **{**kwargs, **extra_args})
        if self.v_symmetric:
          # Add diagonally across
          uv_flip_keys = self._v_flip(u_flip_keys)
          uv_flip_vert_index_keys_list = self._v_flip(u_flip_vert_index_keys_list)
          self.add_face(uv_flip_keys, uv_flip_vert_index_keys_list,
                        **{**kwargs, **extra_args})
      if self.v_symmetric:
        # Add reflection about v
        v_flip_keys = self._v_flip(index_keys)
        v_flip_vert_index_keys_list = self._v_flip(vert_index_keys_list)
        self.add_face(v_flip_keys, v_flip_vert_index_keys_list,
                      **{**kwargs, **extra_args})

  def _set_equivalent_neighbor_faces(self, index_keys, face, **kwargs):
    if 'u_boundary' in kwargs:
      self._set_u_equivalent_face(index_keys, face, **kwargs)
    if 'v_boundary' in kwargs:
      self._set_v_equivalent_face(index_keys, face, **kwargs)
    if 'corner' in kwargs:
      self._set_u_equivalent_face(index_keys, face, **kwargs)
      self._set_v_equivalent_face(index_keys, face, **kwargs)
      self._set_uv_equivalent_face(index_keys, face, **kwargs)

  # Handle face on left/right boundary
  def _set_u_equivalent_face(self, index_keys, face, **kwargs):
    u_index = self._u_index(index_keys)
    u_flip_keys = self._u_flip(index_keys)
    self.set_equivalent_face([u_index], u_flip_keys, face, **kwargs)

  # Handle face on top/bottom boundary
  def _set_v_equivalent_face(self, index_keys, face, **kwargs):
    v_index = self._v_index(index_keys)
    v_flip_keys = self._v_flip(index_keys)
    self.set_equivalent_face([v_index], v_flip_keys, face, **kwargs)

  # Handle face on corner, equivalent to face on diagonal tile
  def _set_uv_equivalent_face(self, index_keys, face, **kwargs):
    u_index = self._u_index(index_keys)
    v_index = self._v_index(index_keys)
    u_flip_keys = self._u_flip(index_keys)
    uv_flip_keys = self._v_flip(u_flip_keys)
    self.set_equivalent_face([u_index, v_index], uv_flip_keys, face, **kwargs)
