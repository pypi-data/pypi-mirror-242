# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorboard/uploader/proto/experiment.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+tensorboard/uploader/proto/experiment.proto\x12\x13tensorboard.service\x1a\x1fgoogle/protobuf/timestamp.proto\"\xa6\x02\n\nExperiment\x12\x15\n\rexperiment_id\x18\x01 \x01(\t\x12/\n\x0b\x63reate_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x0bupdate_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x13\n\x0bnum_scalars\x18\x04 \x01(\x03\x12\x10\n\x08num_runs\x18\x05 \x01(\x03\x12\x10\n\x08num_tags\x18\x06 \x01(\x03\x12\x0c\n\x04name\x18\x07 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x08 \x01(\t\x12\x1a\n\x12total_tensor_bytes\x18\t \x01(\x03\x12\x18\n\x10total_blob_bytes\x18\n \x01(\x03\x12\r\n\x05owner\x18\x0b \x01(\t\"\xf0\x01\n\x0e\x45xperimentMask\x12\x13\n\x0b\x63reate_time\x18\x02 \x01(\x08\x12\x13\n\x0bupdate_time\x18\x03 \x01(\x08\x12\x13\n\x0bnum_scalars\x18\x04 \x01(\x08\x12\x10\n\x08num_runs\x18\x05 \x01(\x08\x12\x10\n\x08num_tags\x18\x06 \x01(\x08\x12\x0c\n\x04name\x18\x07 \x01(\x08\x12\x13\n\x0b\x64\x65scription\x18\x08 \x01(\x08\x12\x1a\n\x12total_tensor_bytes\x18\t \x01(\x08\x12\x18\n\x10total_blob_bytes\x18\n \x01(\x08\x12\r\n\x05owner\x18\x0b \x01(\x08J\x04\x08\x01\x10\x02R\rexperiment_idb\x06proto3')



_EXPERIMENT = DESCRIPTOR.message_types_by_name['Experiment']
_EXPERIMENTMASK = DESCRIPTOR.message_types_by_name['ExperimentMask']
Experiment = _reflection.GeneratedProtocolMessageType('Experiment', (_message.Message,), {
  'DESCRIPTOR' : _EXPERIMENT,
  '__module__' : 'tensorboard.uploader.proto.experiment_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.Experiment)
  })
_sym_db.RegisterMessage(Experiment)

ExperimentMask = _reflection.GeneratedProtocolMessageType('ExperimentMask', (_message.Message,), {
  'DESCRIPTOR' : _EXPERIMENTMASK,
  '__module__' : 'tensorboard.uploader.proto.experiment_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.ExperimentMask)
  })
_sym_db.RegisterMessage(ExperimentMask)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EXPERIMENT._serialized_start=102
  _EXPERIMENT._serialized_end=396
  _EXPERIMENTMASK._serialized_start=399
  _EXPERIMENTMASK._serialized_end=639
# @@protoc_insertion_point(module_scope)
