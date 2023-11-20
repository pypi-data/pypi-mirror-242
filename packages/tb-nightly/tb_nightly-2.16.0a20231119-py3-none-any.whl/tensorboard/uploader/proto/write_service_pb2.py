# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorboard/uploader/proto/write_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from tensorboard.uploader.proto import experiment_pb2 as tensorboard_dot_uploader_dot_proto_dot_experiment__pb2
from tensorboard.uploader.proto import scalar_pb2 as tensorboard_dot_uploader_dot_proto_dot_scalar__pb2
from tensorboard.uploader.proto import tensor_pb2 as tensorboard_dot_uploader_dot_proto_dot_tensor__pb2
from tensorboard.uploader.proto import blob_pb2 as tensorboard_dot_uploader_dot_proto_dot_blob__pb2
from tensorboard.compat.proto import summary_pb2 as tensorboard_dot_compat_dot_proto_dot_summary__pb2
try:
  tensorboard_dot_compat_dot_proto_dot_histogram__pb2 = tensorboard_dot_compat_dot_proto_dot_summary__pb2.tensorboard_dot_compat_dot_proto_dot_histogram__pb2
except AttributeError:
  tensorboard_dot_compat_dot_proto_dot_histogram__pb2 = tensorboard_dot_compat_dot_proto_dot_summary__pb2.tensorboard.compat.proto.histogram_pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.tensorboard/uploader/proto/write_service.proto\x12\x13tensorboard.service\x1a\x1fgoogle/protobuf/timestamp.proto\x1a+tensorboard/uploader/proto/experiment.proto\x1a\'tensorboard/uploader/proto/scalar.proto\x1a\'tensorboard/uploader/proto/tensor.proto\x1a%tensorboard/uploader/proto/blob.proto\x1a&tensorboard/compat/proto/summary.proto\"<\n\x17\x43reateExperimentRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\">\n\x18\x43reateExperimentResponse\x12\x15\n\rexperiment_id\x18\x01 \x01(\t\x12\x0b\n\x03url\x18\x02 \x01(\t\"\x8c\x01\n\x17UpdateExperimentRequest\x12\x33\n\nexperiment\x18\x01 \x01(\x0b\x32\x1f.tensorboard.service.Experiment\x12<\n\x0f\x65xperiment_mask\x18\x02 \x01(\x0b\x32#.tensorboard.service.ExperimentMask\"\x1a\n\x18UpdateExperimentResponse\"0\n\x17\x44\x65leteExperimentRequest\x12\x15\n\rexperiment_id\x18\x01 \x01(\t\"\x1a\n\x18\x44\x65leteExperimentResponse\"\'\n\x10PurgeDataRequest\x12\x13\n\x0b\x62\x61tch_limit\x18\x01 \x01(\x05\"I\n\x11PurgeDataResponse\x12\x34\n\x0bpurge_stats\x18\x01 \x01(\x0b\x32\x1f.tensorboard.service.PurgeStats\">\n\nPurgeStats\x12\x0c\n\x04tags\x18\x01 \x01(\x05\x12\x13\n\x0b\x65xperiments\x18\x02 \x01(\x05\x12\r\n\x05users\x18\x03 \x01(\x05\"\xad\x02\n\x12WriteScalarRequest\x12\x15\n\rexperiment_id\x18\x01 \x01(\t\x12\x39\n\x04runs\x18\x02 \x03(\x0b\x32+.tensorboard.service.WriteScalarRequest.Run\x1aN\n\x03Run\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x39\n\x04tags\x18\x02 \x03(\x0b\x32+.tensorboard.service.WriteScalarRequest.Tag\x1au\n\x03Tag\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x30\n\x06points\x18\x02 \x03(\x0b\x32 .tensorboard.service.ScalarPoint\x12.\n\x08metadata\x18\x03 \x01(\x0b\x32\x1c.tensorboard.SummaryMetadata\"\x15\n\x13WriteScalarResponse\"\xad\x02\n\x12WriteTensorRequest\x12\x15\n\rexperiment_id\x18\x01 \x01(\t\x12\x39\n\x04runs\x18\x02 \x03(\x0b\x32+.tensorboard.service.WriteTensorRequest.Run\x1aN\n\x03Run\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x39\n\x04tags\x18\x02 \x03(\x0b\x32+.tensorboard.service.WriteTensorRequest.Tag\x1au\n\x03Tag\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x30\n\x06points\x18\x02 \x03(\x0b\x32 .tensorboard.service.TensorPoint\x12.\n\x08metadata\x18\x03 \x01(\x0b\x32\x1c.tensorboard.SummaryMetadata\"\x15\n\x13WriteTensorResponse\"\xdd\x01\n\x1eGetOrCreateBlobSequenceRequest\x12\x15\n\rexperiment_id\x18\x01 \x01(\t\x12\x0b\n\x03run\x18\x02 \x01(\t\x12\x0b\n\x03tag\x18\x03 \x01(\t\x12\x0c\n\x04step\x18\x04 \x01(\x03\x12-\n\twall_time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x1d\n\x15\x66inal_sequence_length\x18\x06 \x01(\x03\x12.\n\x08metadata\x18\x07 \x01(\x0b\x32\x1c.tensorboard.SummaryMetadata\";\n\x1fGetOrCreateBlobSequenceResponse\x12\x18\n\x10\x62lob_sequence_id\x18\x01 \x01(\t\"A\n\x16GetBlobMetadataRequest\x12\x18\n\x10\x62lob_sequence_id\x18\x01 \x01(\t\x12\r\n\x05index\x18\x02 \x01(\x03\"k\n\x17GetBlobMetadataResponse\x12\x32\n\nblob_state\x18\x01 \x01(\x0e\x32\x1e.tensorboard.service.BlobState\x12\x0c\n\x04size\x18\x02 \x01(\x03\x12\x0e\n\x06\x63rc32c\x18\x03 \x01(\x07\"\xac\x01\n\x10WriteBlobRequest\x12\x18\n\x10\x62lob_sequence_id\x18\x01 \x01(\t\x12\r\n\x05index\x18\x02 \x01(\x03\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\x0c\x12\x0e\n\x06offset\x18\x04 \x01(\x03\x12\x0e\n\x06\x63rc32c\x18\x05 \x01(\x07\x12\x17\n\x0f\x66inalize_object\x18\x06 \x01(\x08\x12\x14\n\x0c\x66inal_crc32c\x18\x07 \x01(\x07\x12\x12\n\nblob_bytes\x18\x08 \x01(\x03\"U\n\x11WriteBlobResponse\x12\x32\n\nblob_state\x18\x01 \x01(\x0e\x32\x1e.tensorboard.service.BlobState\x12\x0c\n\x04size\x18\x02 \x01(\x03\"\x16\n\x14\x44\x65leteOwnUserRequest\"\x17\n\x15\x44\x65leteOwnUserResponse2\xde\x08\n\x18TensorBoardWriterService\x12q\n\x10\x43reateExperiment\x12,.tensorboard.service.CreateExperimentRequest\x1a-.tensorboard.service.CreateExperimentResponse\"\x00\x12q\n\x10UpdateExperiment\x12,.tensorboard.service.UpdateExperimentRequest\x1a-.tensorboard.service.UpdateExperimentResponse\"\x00\x12q\n\x10\x44\x65leteExperiment\x12,.tensorboard.service.DeleteExperimentRequest\x1a-.tensorboard.service.DeleteExperimentResponse\"\x00\x12\\\n\tPurgeData\x12%.tensorboard.service.PurgeDataRequest\x1a&.tensorboard.service.PurgeDataResponse\"\x00\x12\x62\n\x0bWriteScalar\x12\'.tensorboard.service.WriteScalarRequest\x1a(.tensorboard.service.WriteScalarResponse\"\x00\x12\x62\n\x0bWriteTensor\x12\'.tensorboard.service.WriteTensorRequest\x1a(.tensorboard.service.WriteTensorResponse\"\x00\x12\x86\x01\n\x17GetOrCreateBlobSequence\x12\x33.tensorboard.service.GetOrCreateBlobSequenceRequest\x1a\x34.tensorboard.service.GetOrCreateBlobSequenceResponse\"\x00\x12n\n\x0fGetBlobMetadata\x12+.tensorboard.service.GetBlobMetadataRequest\x1a,.tensorboard.service.GetBlobMetadataResponse\"\x00\x12`\n\tWriteBlob\x12%.tensorboard.service.WriteBlobRequest\x1a&.tensorboard.service.WriteBlobResponse\"\x00(\x01\x30\x01\x12h\n\rDeleteOwnUser\x12).tensorboard.service.DeleteOwnUserRequest\x1a*.tensorboard.service.DeleteOwnUserResponse\"\x00\x62\x06proto3')



_CREATEEXPERIMENTREQUEST = DESCRIPTOR.message_types_by_name['CreateExperimentRequest']
_CREATEEXPERIMENTRESPONSE = DESCRIPTOR.message_types_by_name['CreateExperimentResponse']
_UPDATEEXPERIMENTREQUEST = DESCRIPTOR.message_types_by_name['UpdateExperimentRequest']
_UPDATEEXPERIMENTRESPONSE = DESCRIPTOR.message_types_by_name['UpdateExperimentResponse']
_DELETEEXPERIMENTREQUEST = DESCRIPTOR.message_types_by_name['DeleteExperimentRequest']
_DELETEEXPERIMENTRESPONSE = DESCRIPTOR.message_types_by_name['DeleteExperimentResponse']
_PURGEDATAREQUEST = DESCRIPTOR.message_types_by_name['PurgeDataRequest']
_PURGEDATARESPONSE = DESCRIPTOR.message_types_by_name['PurgeDataResponse']
_PURGESTATS = DESCRIPTOR.message_types_by_name['PurgeStats']
_WRITESCALARREQUEST = DESCRIPTOR.message_types_by_name['WriteScalarRequest']
_WRITESCALARREQUEST_RUN = _WRITESCALARREQUEST.nested_types_by_name['Run']
_WRITESCALARREQUEST_TAG = _WRITESCALARREQUEST.nested_types_by_name['Tag']
_WRITESCALARRESPONSE = DESCRIPTOR.message_types_by_name['WriteScalarResponse']
_WRITETENSORREQUEST = DESCRIPTOR.message_types_by_name['WriteTensorRequest']
_WRITETENSORREQUEST_RUN = _WRITETENSORREQUEST.nested_types_by_name['Run']
_WRITETENSORREQUEST_TAG = _WRITETENSORREQUEST.nested_types_by_name['Tag']
_WRITETENSORRESPONSE = DESCRIPTOR.message_types_by_name['WriteTensorResponse']
_GETORCREATEBLOBSEQUENCEREQUEST = DESCRIPTOR.message_types_by_name['GetOrCreateBlobSequenceRequest']
_GETORCREATEBLOBSEQUENCERESPONSE = DESCRIPTOR.message_types_by_name['GetOrCreateBlobSequenceResponse']
_GETBLOBMETADATAREQUEST = DESCRIPTOR.message_types_by_name['GetBlobMetadataRequest']
_GETBLOBMETADATARESPONSE = DESCRIPTOR.message_types_by_name['GetBlobMetadataResponse']
_WRITEBLOBREQUEST = DESCRIPTOR.message_types_by_name['WriteBlobRequest']
_WRITEBLOBRESPONSE = DESCRIPTOR.message_types_by_name['WriteBlobResponse']
_DELETEOWNUSERREQUEST = DESCRIPTOR.message_types_by_name['DeleteOwnUserRequest']
_DELETEOWNUSERRESPONSE = DESCRIPTOR.message_types_by_name['DeleteOwnUserResponse']
CreateExperimentRequest = _reflection.GeneratedProtocolMessageType('CreateExperimentRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEEXPERIMENTREQUEST,
  '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.CreateExperimentRequest)
  })
_sym_db.RegisterMessage(CreateExperimentRequest)

CreateExperimentResponse = _reflection.GeneratedProtocolMessageType('CreateExperimentResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEEXPERIMENTRESPONSE,
  '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.CreateExperimentResponse)
  })
_sym_db.RegisterMessage(CreateExperimentResponse)

UpdateExperimentRequest = _reflection.GeneratedProtocolMessageType('UpdateExperimentRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEEXPERIMENTREQUEST,
  '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.UpdateExperimentRequest)
  })
_sym_db.RegisterMessage(UpdateExperimentRequest)

UpdateExperimentResponse = _reflection.GeneratedProtocolMessageType('UpdateExperimentResponse', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEEXPERIMENTRESPONSE,
  '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.UpdateExperimentResponse)
  })
_sym_db.RegisterMessage(UpdateExperimentResponse)

DeleteExperimentRequest = _reflection.GeneratedProtocolMessageType('DeleteExperimentRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEEXPERIMENTREQUEST,
  '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.DeleteExperimentRequest)
  })
_sym_db.RegisterMessage(DeleteExperimentRequest)

DeleteExperimentResponse = _reflection.GeneratedProtocolMessageType('DeleteExperimentResponse', (_message.Message,), {
  'DESCRIPTOR' : _DELETEEXPERIMENTRESPONSE,
  '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.DeleteExperimentResponse)
  })
_sym_db.RegisterMessage(DeleteExperimentResponse)

PurgeDataRequest = _reflection.GeneratedProtocolMessageType('PurgeDataRequest', (_message.Message,), {
  'DESCRIPTOR' : _PURGEDATAREQUEST,
  '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.PurgeDataRequest)
  })
_sym_db.RegisterMessage(PurgeDataRequest)

PurgeDataResponse = _reflection.GeneratedProtocolMessageType('PurgeDataResponse', (_message.Message,), {
  'DESCRIPTOR' : _PURGEDATARESPONSE,
  '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.PurgeDataResponse)
  })
_sym_db.RegisterMessage(PurgeDataResponse)

PurgeStats = _reflection.GeneratedProtocolMessageType('PurgeStats', (_message.Message,), {
  'DESCRIPTOR' : _PURGESTATS,
  '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.PurgeStats)
  })
_sym_db.RegisterMessage(PurgeStats)

WriteScalarRequest = _reflection.GeneratedProtocolMessageType('WriteScalarRequest', (_message.Message,), {

  'Run' : _reflection.GeneratedProtocolMessageType('Run', (_message.Message,), {
    'DESCRIPTOR' : _WRITESCALARREQUEST_RUN,
    '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.service.WriteScalarRequest.Run)
    })
  ,

  'Tag' : _reflection.GeneratedProtocolMessageType('Tag', (_message.Message,), {
    'DESCRIPTOR' : _WRITESCALARREQUEST_TAG,
    '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.service.WriteScalarRequest.Tag)
    })
  ,
  'DESCRIPTOR' : _WRITESCALARREQUEST,
  '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.WriteScalarRequest)
  })
_sym_db.RegisterMessage(WriteScalarRequest)
_sym_db.RegisterMessage(WriteScalarRequest.Run)
_sym_db.RegisterMessage(WriteScalarRequest.Tag)

WriteScalarResponse = _reflection.GeneratedProtocolMessageType('WriteScalarResponse', (_message.Message,), {
  'DESCRIPTOR' : _WRITESCALARRESPONSE,
  '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.WriteScalarResponse)
  })
_sym_db.RegisterMessage(WriteScalarResponse)

WriteTensorRequest = _reflection.GeneratedProtocolMessageType('WriteTensorRequest', (_message.Message,), {

  'Run' : _reflection.GeneratedProtocolMessageType('Run', (_message.Message,), {
    'DESCRIPTOR' : _WRITETENSORREQUEST_RUN,
    '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.service.WriteTensorRequest.Run)
    })
  ,

  'Tag' : _reflection.GeneratedProtocolMessageType('Tag', (_message.Message,), {
    'DESCRIPTOR' : _WRITETENSORREQUEST_TAG,
    '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.service.WriteTensorRequest.Tag)
    })
  ,
  'DESCRIPTOR' : _WRITETENSORREQUEST,
  '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.WriteTensorRequest)
  })
_sym_db.RegisterMessage(WriteTensorRequest)
_sym_db.RegisterMessage(WriteTensorRequest.Run)
_sym_db.RegisterMessage(WriteTensorRequest.Tag)

WriteTensorResponse = _reflection.GeneratedProtocolMessageType('WriteTensorResponse', (_message.Message,), {
  'DESCRIPTOR' : _WRITETENSORRESPONSE,
  '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.WriteTensorResponse)
  })
_sym_db.RegisterMessage(WriteTensorResponse)

GetOrCreateBlobSequenceRequest = _reflection.GeneratedProtocolMessageType('GetOrCreateBlobSequenceRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETORCREATEBLOBSEQUENCEREQUEST,
  '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.GetOrCreateBlobSequenceRequest)
  })
_sym_db.RegisterMessage(GetOrCreateBlobSequenceRequest)

GetOrCreateBlobSequenceResponse = _reflection.GeneratedProtocolMessageType('GetOrCreateBlobSequenceResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETORCREATEBLOBSEQUENCERESPONSE,
  '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.GetOrCreateBlobSequenceResponse)
  })
_sym_db.RegisterMessage(GetOrCreateBlobSequenceResponse)

GetBlobMetadataRequest = _reflection.GeneratedProtocolMessageType('GetBlobMetadataRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETBLOBMETADATAREQUEST,
  '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.GetBlobMetadataRequest)
  })
_sym_db.RegisterMessage(GetBlobMetadataRequest)

GetBlobMetadataResponse = _reflection.GeneratedProtocolMessageType('GetBlobMetadataResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETBLOBMETADATARESPONSE,
  '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.GetBlobMetadataResponse)
  })
_sym_db.RegisterMessage(GetBlobMetadataResponse)

WriteBlobRequest = _reflection.GeneratedProtocolMessageType('WriteBlobRequest', (_message.Message,), {
  'DESCRIPTOR' : _WRITEBLOBREQUEST,
  '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.WriteBlobRequest)
  })
_sym_db.RegisterMessage(WriteBlobRequest)

WriteBlobResponse = _reflection.GeneratedProtocolMessageType('WriteBlobResponse', (_message.Message,), {
  'DESCRIPTOR' : _WRITEBLOBRESPONSE,
  '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.WriteBlobResponse)
  })
_sym_db.RegisterMessage(WriteBlobResponse)

DeleteOwnUserRequest = _reflection.GeneratedProtocolMessageType('DeleteOwnUserRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEOWNUSERREQUEST,
  '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.DeleteOwnUserRequest)
  })
_sym_db.RegisterMessage(DeleteOwnUserRequest)

DeleteOwnUserResponse = _reflection.GeneratedProtocolMessageType('DeleteOwnUserResponse', (_message.Message,), {
  'DESCRIPTOR' : _DELETEOWNUSERRESPONSE,
  '__module__' : 'tensorboard.uploader.proto.write_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.service.DeleteOwnUserResponse)
  })
_sym_db.RegisterMessage(DeleteOwnUserResponse)

_TENSORBOARDWRITERSERVICE = DESCRIPTOR.services_by_name['TensorBoardWriterService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CREATEEXPERIMENTREQUEST._serialized_start=310
  _CREATEEXPERIMENTREQUEST._serialized_end=370
  _CREATEEXPERIMENTRESPONSE._serialized_start=372
  _CREATEEXPERIMENTRESPONSE._serialized_end=434
  _UPDATEEXPERIMENTREQUEST._serialized_start=437
  _UPDATEEXPERIMENTREQUEST._serialized_end=577
  _UPDATEEXPERIMENTRESPONSE._serialized_start=579
  _UPDATEEXPERIMENTRESPONSE._serialized_end=605
  _DELETEEXPERIMENTREQUEST._serialized_start=607
  _DELETEEXPERIMENTREQUEST._serialized_end=655
  _DELETEEXPERIMENTRESPONSE._serialized_start=657
  _DELETEEXPERIMENTRESPONSE._serialized_end=683
  _PURGEDATAREQUEST._serialized_start=685
  _PURGEDATAREQUEST._serialized_end=724
  _PURGEDATARESPONSE._serialized_start=726
  _PURGEDATARESPONSE._serialized_end=799
  _PURGESTATS._serialized_start=801
  _PURGESTATS._serialized_end=863
  _WRITESCALARREQUEST._serialized_start=866
  _WRITESCALARREQUEST._serialized_end=1167
  _WRITESCALARREQUEST_RUN._serialized_start=970
  _WRITESCALARREQUEST_RUN._serialized_end=1048
  _WRITESCALARREQUEST_TAG._serialized_start=1050
  _WRITESCALARREQUEST_TAG._serialized_end=1167
  _WRITESCALARRESPONSE._serialized_start=1169
  _WRITESCALARRESPONSE._serialized_end=1190
  _WRITETENSORREQUEST._serialized_start=1193
  _WRITETENSORREQUEST._serialized_end=1494
  _WRITETENSORREQUEST_RUN._serialized_start=1297
  _WRITETENSORREQUEST_RUN._serialized_end=1375
  _WRITETENSORREQUEST_TAG._serialized_start=1377
  _WRITETENSORREQUEST_TAG._serialized_end=1494
  _WRITETENSORRESPONSE._serialized_start=1496
  _WRITETENSORRESPONSE._serialized_end=1517
  _GETORCREATEBLOBSEQUENCEREQUEST._serialized_start=1520
  _GETORCREATEBLOBSEQUENCEREQUEST._serialized_end=1741
  _GETORCREATEBLOBSEQUENCERESPONSE._serialized_start=1743
  _GETORCREATEBLOBSEQUENCERESPONSE._serialized_end=1802
  _GETBLOBMETADATAREQUEST._serialized_start=1804
  _GETBLOBMETADATAREQUEST._serialized_end=1869
  _GETBLOBMETADATARESPONSE._serialized_start=1871
  _GETBLOBMETADATARESPONSE._serialized_end=1978
  _WRITEBLOBREQUEST._serialized_start=1981
  _WRITEBLOBREQUEST._serialized_end=2153
  _WRITEBLOBRESPONSE._serialized_start=2155
  _WRITEBLOBRESPONSE._serialized_end=2240
  _DELETEOWNUSERREQUEST._serialized_start=2242
  _DELETEOWNUSERREQUEST._serialized_end=2264
  _DELETEOWNUSERRESPONSE._serialized_start=2266
  _DELETEOWNUSERRESPONSE._serialized_end=2289
  _TENSORBOARDWRITERSERVICE._serialized_start=2292
  _TENSORBOARDWRITERSERVICE._serialized_end=3410
# @@protoc_insertion_point(module_scope)
