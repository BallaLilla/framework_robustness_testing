# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mathworks/scenario/simulation/phase_status.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mathworks.scenario.simulation import action_status_pb2 as mathworks_dot_scenario_dot_simulation_dot_action__status__pb2
from mathworks.scenario.simulation import condition_status_pb2 as mathworks_dot_scenario_dot_simulation_dot_condition__status__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n0mathworks/scenario/simulation/phase_status.proto\x12\x1dmathworks.scenario.simulation\x1a\x31mathworks/scenario/simulation/action_status.proto\x1a\x34mathworks/scenario/simulation/condition_status.proto\"\xbb\x02\n\x0bPhaseStatus\x12\n\n\x02id\x18\x01 \x01(\t\x12>\n\x0bphase_state\x18\x02 \x01(\x0e\x32).mathworks.scenario.simulation.PhaseState\x12N\n\x16start_condition_status\x18\x03 \x01(\x0b\x32..mathworks.scenario.simulation.ConditionStatus\x12L\n\x14\x65nd_condition_status\x18\x04 \x01(\x0b\x32..mathworks.scenario.simulation.ConditionStatus\x12\x42\n\raction_status\x18\x05 \x03(\x0b\x32+.mathworks.scenario.simulation.ActionStatus*\x80\x01\n\nPhaseState\x12\x1b\n\x17PHASE_STATE_UNSPECIFIED\x10\x00\x12\x14\n\x10PHASE_STATE_IDLE\x10\x01\x12\x15\n\x11PHASE_STATE_START\x10\x02\x12\x13\n\x0fPHASE_STATE_RUN\x10\x03\x12\x13\n\x0fPHASE_STATE_END\x10\x04\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mathworks.scenario.simulation.phase_status_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_PHASESTATE']._serialized_start=507
  _globals['_PHASESTATE']._serialized_end=635
  _globals['_PHASESTATUS']._serialized_start=189
  _globals['_PHASESTATUS']._serialized_end=504
# @@protoc_insertion_point(module_scope)
