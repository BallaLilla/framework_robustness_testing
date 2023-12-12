# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mathworks/scenario/simulation/event.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mathworks.scenario.simulation import action_pb2 as mathworks_dot_scenario_dot_simulation_dot_action__pb2
from mathworks.scenario.simulation import actor_pb2 as mathworks_dot_scenario_dot_simulation_dot_actor__pb2
from mathworks.scenario.simulation import custom_command_pb2 as mathworks_dot_scenario_dot_simulation_dot_custom__command__pb2
from mathworks.scenario.simulation import scenario_pb2 as mathworks_dot_scenario_dot_simulation_dot_scenario__pb2
from mathworks.scenario.simulation import simulation_settings_pb2 as mathworks_dot_scenario_dot_simulation_dot_simulation__settings__pb2
from mathworks.scenario.simulation import simulation_status_pb2 as mathworks_dot_scenario_dot_simulation_dot_simulation__status__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)mathworks/scenario/simulation/event.proto\x12\x1dmathworks.scenario.simulation\x1a*mathworks/scenario/simulation/action.proto\x1a)mathworks/scenario/simulation/actor.proto\x1a\x32mathworks/scenario/simulation/custom_command.proto\x1a,mathworks/scenario/simulation/scenario.proto\x1a\x37mathworks/scenario/simulation/simulation_settings.proto\x1a\x35mathworks/scenario/simulation/simulation_status.proto\"\xa9\x0c\n\x05\x45vent\x12\x10\n\x08priority\x18\x01 \x01(\x05\x12\x16\n\x0eneed_set_ready\x18\x02 \x01(\x08\x12\x11\n\tsender_id\x18\x03 \x01(\t\x12\x14\n\x0creceiver_ids\x18\x04 \x03(\t\x12S\n\x15server_shutdown_event\x18\x65 \x01(\x0b\x32\x32.mathworks.scenario.simulation.ServerShutdownEventH\x00\x12W\n\x17\x63lient_subscribed_event\x18\x66 \x01(\x0b\x32\x34.mathworks.scenario.simulation.ClientSubscribedEventH\x00\x12[\n\x19\x63lient_unsubscribed_event\x18g \x01(\x0b\x32\x36.mathworks.scenario.simulation.ClientUnsubscribedEventH\x00\x12O\n\x13scene_changed_event\x18o \x01(\x0b\x32\x30.mathworks.scenario.simulation.SceneChangedEventH\x00\x12U\n\x16scenario_changed_event\x18p \x01(\x0b\x32\x33.mathworks.scenario.simulation.ScenarioChangedEventH\x00\x12j\n!simulation_settings_changed_event\x18q \x01(\x0b\x32=.mathworks.scenario.simulation.SimulationSettingsChangedEventH\x00\x12\x66\n\x1fsimulation_status_changed_event\x18r \x01(\x0b\x32;.mathworks.scenario.simulation.SimulationStatusChangedEventH\x00\x12U\n\x16simulation_start_event\x18y \x01(\x0b\x32\x33.mathworks.scenario.simulation.SimulationStartEventH\x00\x12S\n\x15simulation_stop_event\x18z \x01(\x0b\x32\x32.mathworks.scenario.simulation.SimulationStopEventH\x00\x12S\n\x15simulation_step_event\x18{ \x01(\x0b\x32\x32.mathworks.scenario.simulation.SimulationStepEventH\x00\x12\\\n\x1asimulation_post_step_event\x18| \x01(\x0b\x32\x36.mathworks.scenario.simulation.SimulationPostStepEventH\x00\x12S\n\x15scenario_update_event\x18} \x01(\x0b\x32\x32.mathworks.scenario.simulation.ScenarioUpdateEventH\x00\x12N\n\x12\x63reate_actor_event\x18\xc9\x01 \x01(\x0b\x32/.mathworks.scenario.simulation.CreateActorEventH\x00\x12R\n\x12remove_actor_event\x18\xca\x01 \x01(\x0b\x32\x33.mathworks.scenario.simulation.WillRemoveActorEventH\x00\x12\x43\n\x0c\x61\x63tion_event\x18\xd3\x01 \x01(\x0b\x32*.mathworks.scenario.simulation.ActionEventH\x00\x12T\n\x15\x61\x63tion_complete_event\x18\xd4\x01 \x01(\x0b\x32\x32.mathworks.scenario.simulation.ActionCompleteEventH\x00\x12K\n\x12user_defined_event\x18\xd5\x01 \x01(\x0b\x32,.mathworks.scenario.simulation.CustomCommandH\x00\x42\x06\n\x04type\"\x15\n\x13ServerShutdownEvent\"*\n\x15\x43lientSubscribedEvent\x12\x11\n\tclient_id\x18\x01 \x01(\t\",\n\x17\x43lientUnsubscribedEvent\x12\x11\n\tclient_id\x18\x01 \x01(\t\"\x13\n\x11SceneChangedEvent\"\x16\n\x14ScenarioChangedEvent\"p\n\x1eSimulationSettingsChangedEvent\x12N\n\x13simulation_settings\x18\x01 \x01(\x0b\x32\x31.mathworks.scenario.simulation.SimulationSettings\"j\n\x1cSimulationStatusChangedEvent\x12J\n\x11simulation_status\x18\x01 \x01(\x0e\x32/.mathworks.scenario.simulation.SimulationStatus\"c\n\x14SimulationStartEvent\x12K\n\x0fsimulation_mode\x18\x01 \x01(\x0e\x32\x32.mathworks.scenario.simulation.SimulationStartMode\"\x82\x01\n\x13SimulationStopEvent\x12\x19\n\x11stop_time_seconds\x18\x01 \x01(\x01\x12\r\n\x05steps\x18\x02 \x01(\x03\x12\x41\n\x05\x63\x61use\x18\x03 \x01(\x0b\x32\x32.mathworks.scenario.simulation.SimulationStopCause\"B\n\x13SimulationStepEvent\x12\x1c\n\x14\x65lapsed_time_seconds\x18\x01 \x01(\x01\x12\r\n\x05steps\x18\x02 \x01(\x03\"\x19\n\x17SimulationPostStepEvent\"\x15\n\x13ScenarioUpdateEvent\"\xbf\x01\n\x10\x43reateActorEvent\x12\x33\n\x05\x61\x63tor\x18\x01 \x01(\x0b\x32$.mathworks.scenario.simulation.Actor\x12\x39\n\x0b\x64\x65scendants\x18\x02 \x03(\x0b\x32$.mathworks.scenario.simulation.Actor\x12;\n\rinitial_phase\x18\x03 \x01(\x0b\x32$.mathworks.scenario.simulation.Phase\"@\n\x14WillRemoveActorEvent\x12\x10\n\x08\x61\x63tor_id\x18\x01 \x01(\t\x12\x16\n\x0e\x64\x65scendant_ids\x18\x02 \x03(\t\"B\n\x0b\x41\x63tionEvent\x12\x33\n\x05phase\x18\x01 \x01(\x0b\x32$.mathworks.scenario.simulation.Phase\"\x82\x01\n\x13\x41\x63tionCompleteEvent\x12\x11\n\taction_id\x18\x01 \x01(\t\x12\x10\n\x08\x61\x63tor_id\x18\x02 \x01(\t\x12\x46\n\x0c\x66inal_status\x18\x03 \x01(\x0e\x32\x30.mathworks.scenario.simulation.ActionEventStatus*\x80\x01\n\x13SimulationStartMode\x12%\n!SIMULATION_START_MODE_UNSPECIFIED\x10\x00\x12 \n\x1cSIMULATION_START_MODE_NORMAL\x10\x01\x12 \n\x1cSIMULATION_START_MODE_REPLAY\x10\x02\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mathworks.scenario.simulation.event_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_SIMULATIONSTARTMODE']._serialized_start=3147
  _globals['_SIMULATIONSTARTMODE']._serialized_end=3275
  _globals['_EVENT']._serialized_start=374
  _globals['_EVENT']._serialized_end=1951
  _globals['_SERVERSHUTDOWNEVENT']._serialized_start=1953
  _globals['_SERVERSHUTDOWNEVENT']._serialized_end=1974
  _globals['_CLIENTSUBSCRIBEDEVENT']._serialized_start=1976
  _globals['_CLIENTSUBSCRIBEDEVENT']._serialized_end=2018
  _globals['_CLIENTUNSUBSCRIBEDEVENT']._serialized_start=2020
  _globals['_CLIENTUNSUBSCRIBEDEVENT']._serialized_end=2064
  _globals['_SCENECHANGEDEVENT']._serialized_start=2066
  _globals['_SCENECHANGEDEVENT']._serialized_end=2085
  _globals['_SCENARIOCHANGEDEVENT']._serialized_start=2087
  _globals['_SCENARIOCHANGEDEVENT']._serialized_end=2109
  _globals['_SIMULATIONSETTINGSCHANGEDEVENT']._serialized_start=2111
  _globals['_SIMULATIONSETTINGSCHANGEDEVENT']._serialized_end=2223
  _globals['_SIMULATIONSTATUSCHANGEDEVENT']._serialized_start=2225
  _globals['_SIMULATIONSTATUSCHANGEDEVENT']._serialized_end=2331
  _globals['_SIMULATIONSTARTEVENT']._serialized_start=2333
  _globals['_SIMULATIONSTARTEVENT']._serialized_end=2432
  _globals['_SIMULATIONSTOPEVENT']._serialized_start=2435
  _globals['_SIMULATIONSTOPEVENT']._serialized_end=2565
  _globals['_SIMULATIONSTEPEVENT']._serialized_start=2567
  _globals['_SIMULATIONSTEPEVENT']._serialized_end=2633
  _globals['_SIMULATIONPOSTSTEPEVENT']._serialized_start=2635
  _globals['_SIMULATIONPOSTSTEPEVENT']._serialized_end=2660
  _globals['_SCENARIOUPDATEEVENT']._serialized_start=2662
  _globals['_SCENARIOUPDATEEVENT']._serialized_end=2683
  _globals['_CREATEACTOREVENT']._serialized_start=2686
  _globals['_CREATEACTOREVENT']._serialized_end=2877
  _globals['_WILLREMOVEACTOREVENT']._serialized_start=2879
  _globals['_WILLREMOVEACTOREVENT']._serialized_end=2943
  _globals['_ACTIONEVENT']._serialized_start=2945
  _globals['_ACTIONEVENT']._serialized_end=3011
  _globals['_ACTIONCOMPLETEEVENT']._serialized_start=3014
  _globals['_ACTIONCOMPLETEEVENT']._serialized_end=3144
# @@protoc_insertion_point(module_scope)