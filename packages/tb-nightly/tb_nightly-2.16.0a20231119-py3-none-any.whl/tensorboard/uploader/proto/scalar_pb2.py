# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorboard/uploader/proto/scalar.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from tensorboard.compat.proto import summary_pb2 as tensorboard_dot_compat_dot_proto_dot_summary__pb2
try:
  tensorboard_dot_compat_dot_proto_dot_histogram__pb2 = tensorboard_dot_compat_dot_proto_dot_summary__pb2.tensorboard_dot_compat_dot_proto_dot_histogram__pb2
except AttributeError:
  tensorboard_dot_compat_dot_proto_dot_histogram__pb2 = tensorboard_dot_compat_dot_proto_dot_summary__pb2.tensorboard.compat.proto.histogram_pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'tensorboard/uploader/proto/scalar.proto\x12\x13tensorboard.service\x1a\x1fgoogle/protobuf/timestamp.proto\x1a&tensorboard/compat/proto/summary.proto\"Y\n\x0bScalarPoint\x12\x0c\n\x04step\x18\x01 \x01(\x03\x12-\n\twall_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\r\n\x05value\x18\x03 \x01(\x01\"\x92\x01\n\x13ScalarPointMetadata\x12\x10\n\x08max_step\x18\x01 \x01(\x03\x12\x31\n\rmax_wall_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x36\n\x10summary_metadata\x18\x03 \x01(\x0b\x32\x1c.tensorboard.SummaryMetadatab\x06proto3')



_SCALARPOINT = DESCRIPTOR.message_types_by_name['ScalarPoint']
_SCALARPOINTMETADATA = DESCRIPTOR.message_types_by_name['ScalarPointMetadata']
ScalarPoint = _reflection.GeneratedProtocolMessageType('ScalarPoint', (_message.Message,), {
  'DESCRIPTOR' : _SCALARPOINT,
  '__module__' : 'tensorboard.uploader.proto.scalar_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.ScalarPoint)
  })
_sym_db.RegisterMessage(ScalarPoint)

ScalarPointMetadata = _reflection.GeneratedProtocolMessageType('ScalarPointMetadata', (_message.Message,), {
  'DESCRIPTOR' : _SCALARPOINTMETADATA,
  '__module__' : 'tensorboard.uploader.proto.scalar_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.ScalarPointMetadata)
  })
_sym_db.RegisterMessage(ScalarPointMetadata)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SCALARPOINT._serialized_start=137
  _SCALARPOINT._serialized_end=226
  _SCALARPOINTMETADATA._serialized_start=229
  _SCALARPOINTMETADATA._serialized_end=375
# @@protoc_insertion_point(module_scope)
