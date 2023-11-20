# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qwak/feature_store/features/deployment.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,qwak/feature_store/features/deployment.proto\x12\x1bqwak.feature.store.features\x1a\x1fgoogle/protobuf/timestamp.proto\"\x9d\x03\n\x1c\x44\x65ploymentUpdateRequestState\x12Y\n\x14invalid_request_type\x18\x01 \x01(\x0b\x32\x39.qwak.feature.store.features.DeploymentInvalidRequestTypeH\x00\x12W\n\x13update_request_type\x18\x02 \x01(\x0b\x32\x38.qwak.feature.store.features.DeploymentUpdateRequestTypeH\x00\x12[\n\x15undeploy_request_type\x18\x03 \x01(\x0b\x32:.qwak.feature.store.features.DeploymentUndeployRequestTypeH\x00\x12\x64\n deployment_update_request_status\x18\x04 \x01(\x0e\x32:.qwak.feature.store.features.DeploymentUpdateRequestStatusB\x06\n\x04type\"\x1e\n\x1c\x44\x65ploymentInvalidRequestType\"\x1d\n\x1b\x44\x65ploymentUpdateRequestType\"\x1f\n\x1d\x44\x65ploymentUndeployRequestType\"\xce\x01\n\x0f\x44\x65ploymentState\x12Z\n\x14\x65xtractor_identifier\x18\x01 \x01(\x0b\x32:.qwak.feature.store.features.ExtractorDeploymentIdentifierH\x00\x12L\n\x0estatus_details\x18\x05 \x01(\x0b\x32\x34.qwak.feature.store.features.DeploymentStatusDetailsB\x11\n\x0fidentifier_type\"m\n\x1d\x45xtractorDeploymentIdentifier\x12\x1f\n\x17\x65xtractor_deployment_id\x18\x01 \x01(\t\x12\x14\n\x0c\x65xtractor_id\x18\x02 \x01(\t\x12\x15\n\rfeatureset_id\x18\x03 \x01(\t\"\xbc\x02\n\x17\x44\x65ploymentStatusDetails\x12g\n!update_in_progress_status_details\x18\x01 \x01(\x0b\x32:.qwak.feature.store.features.UpdateInProgressStatusDetailsH\x00\x12S\n\x16running_status_details\x18\x02 \x01(\x0b\x32\x31.qwak.feature.store.features.RunningStatusDetailsH\x00\x12Q\n\x15\x66\x61iled_status_details\x18\x03 \x01(\x0b\x32\x30.qwak.feature.store.features.FailedStatusDetailsH\x00\x42\x10\n\x0estatus_details\"\xa7\x01\n\x1dUpdateInProgressStatusDetails\x12\x42\n\x0cold_instance\x18\x01 \x01(\x0b\x32,.qwak.feature.store.features.InstanceDetails\x12\x42\n\x0cnew_instance\x18\x02 \x01(\x0b\x32,.qwak.feature.store.features.InstanceDetails\"^\n\x14RunningStatusDetails\x12\x46\n\x10running_instance\x18\x01 \x01(\x0b\x32,.qwak.feature.store.features.InstanceDetails\"\xe6\x01\n\x13\x46\x61iledStatusDetails\x12\x44\n\x0f\x66\x61ilure_details\x18\x01 \x01(\x0b\x32+.qwak.feature.store.features.FailureDetails\x12\x42\n\x0cold_instance\x18\x02 \x01(\x0b\x32,.qwak.feature.store.features.InstanceDetails\x12\x45\n\x0f\x66\x61iled_instance\x18\x03 \x01(\x0b\x32,.qwak.feature.store.features.InstanceDetails\"\x92\x01\n\x0e\x46\x61ilureDetails\x12`\n\x1e\x64\x65ployment_failure_reason_code\x18\x01 \x01(\x0e\x32\x38.qwak.feature.store.features.DeploymentFailureReasonCode\x12\x1e\n\x16\x66\x61ilure_reason_details\x18\x02 \x01(\t\"\x9a\x01\n\x0fInstanceDetails\x12X\n\x14\x65xtractor_identifier\x18\x01 \x01(\x0b\x32\x38.qwak.feature.store.features.ExtractorInstanceIdentifierH\x00\x12\x1a\n\x12\x61vailable_replicas\x18\x04 \x01(\x05\x42\x11\n\x0fidentifier_type\"M\n\x1b\x45xtractorInstanceIdentifier\x12.\n&extractor_deployment_update_request_id\x18\x01 \x01(\t*\xa0\x02\n\x1d\x44\x65ploymentUpdateRequestStatus\x12,\n(DEPLOYMENT_UPDATE_REQUEST_INVALID_STATUS\x10\x00\x12%\n!INVALID_DEPLOYMENT_UPDATE_REQUEST\x10\x01\x12(\n$INITIATING_DEPLOYMENT_UPDATE_REQUEST\x10\x02\x12/\n+FAILED_INITIATING_DEPLOYMENT_UPDATE_REQUEST\x10\x03\x12%\n!PENDING_DEPLOYMENT_UPDATE_REQUEST\x10\x04\x12(\n$SUCCESSFUL_DEPLOYMENT_UPDATE_REQUEST\x10\x05*\x9e\x01\n\x10\x44\x65ploymentStatus\x12\x1d\n\x19\x44\x45PLOYMENT_INVALID_STATUS\x10\x00\x12\x16\n\x12\x44\x45PLOYMENT_RUNNING\x10\x01\x12!\n\x1d\x44\x45PLOYMENT_UPDATE_IN_PROGRESS\x10\x02\x12\x19\n\x15\x44\x45PLOYMENT_UNDEPLOYED\x10\x03\x12\x15\n\x11\x44\x45PLOYMENT_FAILED\x10\x04*\x8d\x02\n\x1b\x44\x65ploymentFailureReasonCode\x12\x18\n\x14INVALID_FAILURE_CODE\x10\x00\x12\x12\n\x0eUNKNOWN_REASON\x10\x01\x12\x1e\n\x1aNO_REPLICA_SETS_PODS_FOUND\x10\x02\x12\x17\n\x13\x43ONTAINER_NOT_FOUND\x10\x03\x12\x11\n\rUNSCHEDULABLE\x10\x04\x12\x1a\n\x16\x44OCKER_IMAGE_NOT_FOUND\x10\x05\x12\x19\n\x15MEMORY_LIMIT_EXCEEDED\x10\x06\x12\x0e\n\nCRASH_LOOP\x10\x07\x12-\n)CONTAINER_FAIL_TO_LOAD_FOR_UNKNOWN_REASON\x10\x08\x42[\n&com.qwak.ai.feature.store.features.apiP\x01Z/qwak/featurestore/features;featurestorefeaturesb\x06proto3')

_DEPLOYMENTUPDATEREQUESTSTATUS = DESCRIPTOR.enum_types_by_name['DeploymentUpdateRequestStatus']
DeploymentUpdateRequestStatus = enum_type_wrapper.EnumTypeWrapper(_DEPLOYMENTUPDATEREQUESTSTATUS)
_DEPLOYMENTSTATUS = DESCRIPTOR.enum_types_by_name['DeploymentStatus']
DeploymentStatus = enum_type_wrapper.EnumTypeWrapper(_DEPLOYMENTSTATUS)
_DEPLOYMENTFAILUREREASONCODE = DESCRIPTOR.enum_types_by_name['DeploymentFailureReasonCode']
DeploymentFailureReasonCode = enum_type_wrapper.EnumTypeWrapper(_DEPLOYMENTFAILUREREASONCODE)
DEPLOYMENT_UPDATE_REQUEST_INVALID_STATUS = 0
INVALID_DEPLOYMENT_UPDATE_REQUEST = 1
INITIATING_DEPLOYMENT_UPDATE_REQUEST = 2
FAILED_INITIATING_DEPLOYMENT_UPDATE_REQUEST = 3
PENDING_DEPLOYMENT_UPDATE_REQUEST = 4
SUCCESSFUL_DEPLOYMENT_UPDATE_REQUEST = 5
DEPLOYMENT_INVALID_STATUS = 0
DEPLOYMENT_RUNNING = 1
DEPLOYMENT_UPDATE_IN_PROGRESS = 2
DEPLOYMENT_UNDEPLOYED = 3
DEPLOYMENT_FAILED = 4
INVALID_FAILURE_CODE = 0
UNKNOWN_REASON = 1
NO_REPLICA_SETS_PODS_FOUND = 2
CONTAINER_NOT_FOUND = 3
UNSCHEDULABLE = 4
DOCKER_IMAGE_NOT_FOUND = 5
MEMORY_LIMIT_EXCEEDED = 6
CRASH_LOOP = 7
CONTAINER_FAIL_TO_LOAD_FOR_UNKNOWN_REASON = 8


_DEPLOYMENTUPDATEREQUESTSTATE = DESCRIPTOR.message_types_by_name['DeploymentUpdateRequestState']
_DEPLOYMENTINVALIDREQUESTTYPE = DESCRIPTOR.message_types_by_name['DeploymentInvalidRequestType']
_DEPLOYMENTUPDATEREQUESTTYPE = DESCRIPTOR.message_types_by_name['DeploymentUpdateRequestType']
_DEPLOYMENTUNDEPLOYREQUESTTYPE = DESCRIPTOR.message_types_by_name['DeploymentUndeployRequestType']
_DEPLOYMENTSTATE = DESCRIPTOR.message_types_by_name['DeploymentState']
_EXTRACTORDEPLOYMENTIDENTIFIER = DESCRIPTOR.message_types_by_name['ExtractorDeploymentIdentifier']
_DEPLOYMENTSTATUSDETAILS = DESCRIPTOR.message_types_by_name['DeploymentStatusDetails']
_UPDATEINPROGRESSSTATUSDETAILS = DESCRIPTOR.message_types_by_name['UpdateInProgressStatusDetails']
_RUNNINGSTATUSDETAILS = DESCRIPTOR.message_types_by_name['RunningStatusDetails']
_FAILEDSTATUSDETAILS = DESCRIPTOR.message_types_by_name['FailedStatusDetails']
_FAILUREDETAILS = DESCRIPTOR.message_types_by_name['FailureDetails']
_INSTANCEDETAILS = DESCRIPTOR.message_types_by_name['InstanceDetails']
_EXTRACTORINSTANCEIDENTIFIER = DESCRIPTOR.message_types_by_name['ExtractorInstanceIdentifier']
DeploymentUpdateRequestState = _reflection.GeneratedProtocolMessageType('DeploymentUpdateRequestState', (_message.Message,), {
  'DESCRIPTOR' : _DEPLOYMENTUPDATEREQUESTSTATE,
  '__module__' : 'qwak.feature_store.features.deployment_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.features.DeploymentUpdateRequestState)
  })
_sym_db.RegisterMessage(DeploymentUpdateRequestState)

DeploymentInvalidRequestType = _reflection.GeneratedProtocolMessageType('DeploymentInvalidRequestType', (_message.Message,), {
  'DESCRIPTOR' : _DEPLOYMENTINVALIDREQUESTTYPE,
  '__module__' : 'qwak.feature_store.features.deployment_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.features.DeploymentInvalidRequestType)
  })
_sym_db.RegisterMessage(DeploymentInvalidRequestType)

DeploymentUpdateRequestType = _reflection.GeneratedProtocolMessageType('DeploymentUpdateRequestType', (_message.Message,), {
  'DESCRIPTOR' : _DEPLOYMENTUPDATEREQUESTTYPE,
  '__module__' : 'qwak.feature_store.features.deployment_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.features.DeploymentUpdateRequestType)
  })
_sym_db.RegisterMessage(DeploymentUpdateRequestType)

DeploymentUndeployRequestType = _reflection.GeneratedProtocolMessageType('DeploymentUndeployRequestType', (_message.Message,), {
  'DESCRIPTOR' : _DEPLOYMENTUNDEPLOYREQUESTTYPE,
  '__module__' : 'qwak.feature_store.features.deployment_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.features.DeploymentUndeployRequestType)
  })
_sym_db.RegisterMessage(DeploymentUndeployRequestType)

DeploymentState = _reflection.GeneratedProtocolMessageType('DeploymentState', (_message.Message,), {
  'DESCRIPTOR' : _DEPLOYMENTSTATE,
  '__module__' : 'qwak.feature_store.features.deployment_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.features.DeploymentState)
  })
_sym_db.RegisterMessage(DeploymentState)

ExtractorDeploymentIdentifier = _reflection.GeneratedProtocolMessageType('ExtractorDeploymentIdentifier', (_message.Message,), {
  'DESCRIPTOR' : _EXTRACTORDEPLOYMENTIDENTIFIER,
  '__module__' : 'qwak.feature_store.features.deployment_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.features.ExtractorDeploymentIdentifier)
  })
_sym_db.RegisterMessage(ExtractorDeploymentIdentifier)

DeploymentStatusDetails = _reflection.GeneratedProtocolMessageType('DeploymentStatusDetails', (_message.Message,), {
  'DESCRIPTOR' : _DEPLOYMENTSTATUSDETAILS,
  '__module__' : 'qwak.feature_store.features.deployment_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.features.DeploymentStatusDetails)
  })
_sym_db.RegisterMessage(DeploymentStatusDetails)

UpdateInProgressStatusDetails = _reflection.GeneratedProtocolMessageType('UpdateInProgressStatusDetails', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEINPROGRESSSTATUSDETAILS,
  '__module__' : 'qwak.feature_store.features.deployment_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.features.UpdateInProgressStatusDetails)
  })
_sym_db.RegisterMessage(UpdateInProgressStatusDetails)

RunningStatusDetails = _reflection.GeneratedProtocolMessageType('RunningStatusDetails', (_message.Message,), {
  'DESCRIPTOR' : _RUNNINGSTATUSDETAILS,
  '__module__' : 'qwak.feature_store.features.deployment_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.features.RunningStatusDetails)
  })
_sym_db.RegisterMessage(RunningStatusDetails)

FailedStatusDetails = _reflection.GeneratedProtocolMessageType('FailedStatusDetails', (_message.Message,), {
  'DESCRIPTOR' : _FAILEDSTATUSDETAILS,
  '__module__' : 'qwak.feature_store.features.deployment_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.features.FailedStatusDetails)
  })
_sym_db.RegisterMessage(FailedStatusDetails)

FailureDetails = _reflection.GeneratedProtocolMessageType('FailureDetails', (_message.Message,), {
  'DESCRIPTOR' : _FAILUREDETAILS,
  '__module__' : 'qwak.feature_store.features.deployment_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.features.FailureDetails)
  })
_sym_db.RegisterMessage(FailureDetails)

InstanceDetails = _reflection.GeneratedProtocolMessageType('InstanceDetails', (_message.Message,), {
  'DESCRIPTOR' : _INSTANCEDETAILS,
  '__module__' : 'qwak.feature_store.features.deployment_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.features.InstanceDetails)
  })
_sym_db.RegisterMessage(InstanceDetails)

ExtractorInstanceIdentifier = _reflection.GeneratedProtocolMessageType('ExtractorInstanceIdentifier', (_message.Message,), {
  'DESCRIPTOR' : _EXTRACTORINSTANCEIDENTIFIER,
  '__module__' : 'qwak.feature_store.features.deployment_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.features.ExtractorInstanceIdentifier)
  })
_sym_db.RegisterMessage(ExtractorInstanceIdentifier)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n&com.qwak.ai.feature.store.features.apiP\001Z/qwak/featurestore/features;featurestorefeatures'
  _DEPLOYMENTUPDATEREQUESTSTATUS._serialized_start=2146
  _DEPLOYMENTUPDATEREQUESTSTATUS._serialized_end=2434
  _DEPLOYMENTSTATUS._serialized_start=2437
  _DEPLOYMENTSTATUS._serialized_end=2595
  _DEPLOYMENTFAILUREREASONCODE._serialized_start=2598
  _DEPLOYMENTFAILUREREASONCODE._serialized_end=2867
  _DEPLOYMENTUPDATEREQUESTSTATE._serialized_start=111
  _DEPLOYMENTUPDATEREQUESTSTATE._serialized_end=524
  _DEPLOYMENTINVALIDREQUESTTYPE._serialized_start=526
  _DEPLOYMENTINVALIDREQUESTTYPE._serialized_end=556
  _DEPLOYMENTUPDATEREQUESTTYPE._serialized_start=558
  _DEPLOYMENTUPDATEREQUESTTYPE._serialized_end=587
  _DEPLOYMENTUNDEPLOYREQUESTTYPE._serialized_start=589
  _DEPLOYMENTUNDEPLOYREQUESTTYPE._serialized_end=620
  _DEPLOYMENTSTATE._serialized_start=623
  _DEPLOYMENTSTATE._serialized_end=829
  _EXTRACTORDEPLOYMENTIDENTIFIER._serialized_start=831
  _EXTRACTORDEPLOYMENTIDENTIFIER._serialized_end=940
  _DEPLOYMENTSTATUSDETAILS._serialized_start=943
  _DEPLOYMENTSTATUSDETAILS._serialized_end=1259
  _UPDATEINPROGRESSSTATUSDETAILS._serialized_start=1262
  _UPDATEINPROGRESSSTATUSDETAILS._serialized_end=1429
  _RUNNINGSTATUSDETAILS._serialized_start=1431
  _RUNNINGSTATUSDETAILS._serialized_end=1525
  _FAILEDSTATUSDETAILS._serialized_start=1528
  _FAILEDSTATUSDETAILS._serialized_end=1758
  _FAILUREDETAILS._serialized_start=1761
  _FAILUREDETAILS._serialized_end=1907
  _INSTANCEDETAILS._serialized_start=1910
  _INSTANCEDETAILS._serialized_end=2064
  _EXTRACTORINSTANCEIDENTIFIER._serialized_start=2066
  _EXTRACTORINSTANCEIDENTIFIER._serialized_end=2143
# @@protoc_insertion_point(module_scope)
