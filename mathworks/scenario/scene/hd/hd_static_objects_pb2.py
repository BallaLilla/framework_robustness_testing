# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mathworks/scenario/scene/hd/hd_static_objects.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mathworks.scenario.scene.hd import common_attributes_pb2 as mathworks_dot_scenario_dot_scene_dot_hd_dot_common__attributes__pb2
from mathworks.scenario.common import geometry_pb2 as mathworks_dot_scenario_dot_common_dot_geometry__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n3mathworks/scenario/scene/hd/hd_static_objects.proto\x12\x1emathworks.scenario.scene.hdmap\x1a\x33mathworks/scenario/scene/hd/common_attributes.proto\x1a(mathworks/scenario/common/geometry.proto\"o\n\x1aStaticObjectTypeDefinition\x12\n\n\x02id\x18\x01 \x01(\t\x12\x45\n\nasset_path\x18\x02 \x01(\x0b\x32\x31.mathworks.scenario.scene.hdmap.RelativeAssetPath\"\xa3\x01\n\x0cStaticObject\x12\n\n\x02id\x18\x01 \x01(\t\x12\x43\n\x08geometry\x18\x02 \x01(\x0b\x32\x31.mathworks.scenario.common.GeoOrientedBoundingBox\x12\x42\n\x0fobject_type_ref\x18\x03 \x01(\x0b\x32).mathworks.scenario.scene.hdmap.Referenceb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mathworks.scenario.scene.hd.hd_static_objects_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_STATICOBJECTTYPEDEFINITION']._serialized_start=182
  _globals['_STATICOBJECTTYPEDEFINITION']._serialized_end=293
  _globals['_STATICOBJECT']._serialized_start=296
  _globals['_STATICOBJECT']._serialized_end=459
# @@protoc_insertion_point(module_scope)
