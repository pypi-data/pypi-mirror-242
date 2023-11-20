# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qwak/fitness_service/status.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!qwak/fitness_service/status.proto\x12\x14qwak.fitness.service\x1a\x1egoogle/protobuf/wrappers.proto\"\xf3\x01\n\x14RemoteBuildingStatus\x12S\n\x1bremote_building_status_code\x18\x01 \x01(\x0e\x32..qwak.fitness.service.RemoteBuildingStatusCode\x12Q\n\x0f\x66\x61ilure_details\x18\x02 \x01(\x0b\x32\x38.qwak.fitness.service.RemoteBuildingFailureReasonDetails\x12\x33\n\npod_status\x18\x03 \x01(\x0b\x32\x1f.qwak.fitness.service.PodStatus\"\x8c\x01\n\"RemoteBuildingFailureReasonDetails\x12K\n\x0c\x66\x61ilure_code\x18\x01 \x01(\x0e\x32\x35.qwak.fitness.service.RemoteBuildingFailureReasonCode\x12\x19\n\x11technical_details\x18\x02 \x01(\t\"\xa2\x01\n\tPodStatus\x12\x41\n\x12\x63ontainer_statuses\x18\x01 \x03(\x0b\x32%.qwak.fitness.service.ContainerStatus\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\r\n\x05phase\x18\x03 \x01(\t\x12\x0e\n\x06reason\x18\x04 \x01(\t\x12\x12\n\nstart_time\x18\x05 \x01(\t\x12\x0e\n\x06pod_id\x18\x06 \x01(\t\"\x9d\x01\n\x0f\x43ontainerStatus\x12\x14\n\x0c\x63ontainer_id\x18\x01 \x01(\t\x12\r\n\x05image\x18\x02 \x01(\t\x12\x15\n\rrestart_count\x18\x03 \x01(\x05\x12\x0f\n\x07started\x18\x04 \x01(\x08\x12=\n\x0f\x63ontainer_state\x18\x05 \x01(\x0b\x32$.qwak.fitness.service.ContainerState\"\x8f\x02\n\x0e\x43ontainerState\x12N\n\x17\x63ontainer_state_running\x18\x01 \x01(\x0b\x32+.qwak.fitness.service.ContainerStateRunningH\x00\x12T\n\x1a\x63ontainer_state_terminated\x18\x02 \x01(\x0b\x32..qwak.fitness.service.ContainerStateTerminatedH\x00\x12N\n\x17\x63ontainer_state_waiting\x18\x03 \x01(\x0b\x32+.qwak.fitness.service.ContainerStateWaitingH\x00\x42\x07\n\x05state\"+\n\x15\x43ontainerStateRunning\x12\x12\n\nstarted_at\x18\x01 \x01(\t\"\x9d\x01\n\x18\x43ontainerStateTerminated\x12\x14\n\x0c\x63ontainer_id\x18\x01 \x01(\t\x12\x11\n\texit_code\x18\x02 \x01(\x05\x12\x13\n\x0b\x66inished_at\x18\x03 \x01(\t\x12\x0f\n\x07message\x18\x04 \x01(\t\x12\x0e\n\x06reason\x18\x05 \x01(\t\x12\x0e\n\x06signal\x18\x06 \x01(\x05\x12\x12\n\nstarted_at\x18\x07 \x01(\t\"8\n\x15\x43ontainerStateWaiting\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x0e\n\x06reason\x18\x02 \x01(\t*\x98\x01\n\x18RemoteBuildingStatusCode\x12\x12\n\x0eINVALID_STATUS\x10\x00\x12\x10\n\x0cINITIALIZING\x10\x01\x12\x0f\n\x0bIN_PROGRESS\x10\x02\x12\x0e\n\nSUCCESSFUL\x10\x03\x12\n\n\x06\x46\x41ILED\x10\x04\x12\r\n\tCANCELLED\x10\x05\x12\r\n\tTIMED_OUT\x10\x06\x12\x0b\n\x07UNKNOWN\x10\x07*}\n\x1fRemoteBuildingFailureReasonCode\x12\x10\n\x0cINVALID_CODE\x10\x00\x12\x12\n\x0eUNKNOWN_REASON\x10\x01\x12\x1a\n\x16INSUFFICIENT_RESOURCES\x10\x02\x12\x18\n\x14MISSING_DOCKER_IMAGE\x10\x03\x42#\n\x1f\x63om.qwak.ai.fitness.service.apiP\x01\x62\x06proto3')

_REMOTEBUILDINGSTATUSCODE = DESCRIPTOR.enum_types_by_name['RemoteBuildingStatusCode']
RemoteBuildingStatusCode = enum_type_wrapper.EnumTypeWrapper(_REMOTEBUILDINGSTATUSCODE)
_REMOTEBUILDINGFAILUREREASONCODE = DESCRIPTOR.enum_types_by_name['RemoteBuildingFailureReasonCode']
RemoteBuildingFailureReasonCode = enum_type_wrapper.EnumTypeWrapper(_REMOTEBUILDINGFAILUREREASONCODE)
INVALID_STATUS = 0
INITIALIZING = 1
IN_PROGRESS = 2
SUCCESSFUL = 3
FAILED = 4
CANCELLED = 5
TIMED_OUT = 6
UNKNOWN = 7
INVALID_CODE = 0
UNKNOWN_REASON = 1
INSUFFICIENT_RESOURCES = 2
MISSING_DOCKER_IMAGE = 3


_REMOTEBUILDINGSTATUS = DESCRIPTOR.message_types_by_name['RemoteBuildingStatus']
_REMOTEBUILDINGFAILUREREASONDETAILS = DESCRIPTOR.message_types_by_name['RemoteBuildingFailureReasonDetails']
_PODSTATUS = DESCRIPTOR.message_types_by_name['PodStatus']
_CONTAINERSTATUS = DESCRIPTOR.message_types_by_name['ContainerStatus']
_CONTAINERSTATE = DESCRIPTOR.message_types_by_name['ContainerState']
_CONTAINERSTATERUNNING = DESCRIPTOR.message_types_by_name['ContainerStateRunning']
_CONTAINERSTATETERMINATED = DESCRIPTOR.message_types_by_name['ContainerStateTerminated']
_CONTAINERSTATEWAITING = DESCRIPTOR.message_types_by_name['ContainerStateWaiting']
RemoteBuildingStatus = _reflection.GeneratedProtocolMessageType('RemoteBuildingStatus', (_message.Message,), {
  'DESCRIPTOR' : _REMOTEBUILDINGSTATUS,
  '__module__' : 'qwak.fitness_service.status_pb2'
  # @@protoc_insertion_point(class_scope:qwak.fitness.service.RemoteBuildingStatus)
  })
_sym_db.RegisterMessage(RemoteBuildingStatus)

RemoteBuildingFailureReasonDetails = _reflection.GeneratedProtocolMessageType('RemoteBuildingFailureReasonDetails', (_message.Message,), {
  'DESCRIPTOR' : _REMOTEBUILDINGFAILUREREASONDETAILS,
  '__module__' : 'qwak.fitness_service.status_pb2'
  # @@protoc_insertion_point(class_scope:qwak.fitness.service.RemoteBuildingFailureReasonDetails)
  })
_sym_db.RegisterMessage(RemoteBuildingFailureReasonDetails)

PodStatus = _reflection.GeneratedProtocolMessageType('PodStatus', (_message.Message,), {
  'DESCRIPTOR' : _PODSTATUS,
  '__module__' : 'qwak.fitness_service.status_pb2'
  # @@protoc_insertion_point(class_scope:qwak.fitness.service.PodStatus)
  })
_sym_db.RegisterMessage(PodStatus)

ContainerStatus = _reflection.GeneratedProtocolMessageType('ContainerStatus', (_message.Message,), {
  'DESCRIPTOR' : _CONTAINERSTATUS,
  '__module__' : 'qwak.fitness_service.status_pb2'
  # @@protoc_insertion_point(class_scope:qwak.fitness.service.ContainerStatus)
  })
_sym_db.RegisterMessage(ContainerStatus)

ContainerState = _reflection.GeneratedProtocolMessageType('ContainerState', (_message.Message,), {
  'DESCRIPTOR' : _CONTAINERSTATE,
  '__module__' : 'qwak.fitness_service.status_pb2'
  # @@protoc_insertion_point(class_scope:qwak.fitness.service.ContainerState)
  })
_sym_db.RegisterMessage(ContainerState)

ContainerStateRunning = _reflection.GeneratedProtocolMessageType('ContainerStateRunning', (_message.Message,), {
  'DESCRIPTOR' : _CONTAINERSTATERUNNING,
  '__module__' : 'qwak.fitness_service.status_pb2'
  # @@protoc_insertion_point(class_scope:qwak.fitness.service.ContainerStateRunning)
  })
_sym_db.RegisterMessage(ContainerStateRunning)

ContainerStateTerminated = _reflection.GeneratedProtocolMessageType('ContainerStateTerminated', (_message.Message,), {
  'DESCRIPTOR' : _CONTAINERSTATETERMINATED,
  '__module__' : 'qwak.fitness_service.status_pb2'
  # @@protoc_insertion_point(class_scope:qwak.fitness.service.ContainerStateTerminated)
  })
_sym_db.RegisterMessage(ContainerStateTerminated)

ContainerStateWaiting = _reflection.GeneratedProtocolMessageType('ContainerStateWaiting', (_message.Message,), {
  'DESCRIPTOR' : _CONTAINERSTATEWAITING,
  '__module__' : 'qwak.fitness_service.status_pb2'
  # @@protoc_insertion_point(class_scope:qwak.fitness.service.ContainerStateWaiting)
  })
_sym_db.RegisterMessage(ContainerStateWaiting)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\037com.qwak.ai.fitness.service.apiP\001'
  _REMOTEBUILDINGSTATUSCODE._serialized_start=1343
  _REMOTEBUILDINGSTATUSCODE._serialized_end=1495
  _REMOTEBUILDINGFAILUREREASONCODE._serialized_start=1497
  _REMOTEBUILDINGFAILUREREASONCODE._serialized_end=1622
  _REMOTEBUILDINGSTATUS._serialized_start=92
  _REMOTEBUILDINGSTATUS._serialized_end=335
  _REMOTEBUILDINGFAILUREREASONDETAILS._serialized_start=338
  _REMOTEBUILDINGFAILUREREASONDETAILS._serialized_end=478
  _PODSTATUS._serialized_start=481
  _PODSTATUS._serialized_end=643
  _CONTAINERSTATUS._serialized_start=646
  _CONTAINERSTATUS._serialized_end=803
  _CONTAINERSTATE._serialized_start=806
  _CONTAINERSTATE._serialized_end=1077
  _CONTAINERSTATERUNNING._serialized_start=1079
  _CONTAINERSTATERUNNING._serialized_end=1122
  _CONTAINERSTATETERMINATED._serialized_start=1125
  _CONTAINERSTATETERMINATED._serialized_end=1282
  _CONTAINERSTATEWAITING._serialized_start=1284
  _CONTAINERSTATEWAITING._serialized_end=1340
# @@protoc_insertion_point(module_scope)
