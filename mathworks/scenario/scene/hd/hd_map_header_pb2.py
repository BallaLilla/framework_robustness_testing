# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mathworks/scenario/scene/hd/hd_map_header.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mathworks.scenario.common import geometry_pb2 as mathworks_dot_scenario_dot_common_dot_geometry__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n/mathworks/scenario/scene/hd/hd_map_header.proto\x12\x1emathworks.scenario.scene.hdmap\x1a(mathworks/scenario/common/geometry.proto\"\x9c\x01\n\x06Header\x12\x0e\n\x06\x61uthor\x18\x01 \x01(\t\x12\x39\n\nprojection\x18\x02 \x01(\x0b\x32%.mathworks.scenario.common.Projection\x12G\n\x13geographic_boundary\x18\x03 \x01(\x0b\x32*.mathworks.scenario.scene.hdmap.DataBounds\"=\n\nDataBounds\x12/\n\x06\x62ounds\x18\x01 \x01(\x0b\x32\x1f.mathworks.scenario.common.Box3b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mathworks.scenario.scene.hd.hd_map_header_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_HEADER']._serialized_start=126
  _globals['_HEADER']._serialized_end=282
  _globals['_DATABOUNDS']._serialized_start=284
  _globals['_DATABOUNDS']._serialized_end=345
# @@protoc_insertion_point(module_scope)
