# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/core/proto/base_options.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.gpu import gpu_origin_pb2 as mediapipe_dot_gpu_dot_gpu__origin__pb2
from mediapipe.tasks.cc.core.proto import acceleration_pb2 as mediapipe_dot_tasks_dot_cc_dot_core_dot_proto_dot_acceleration__pb2
from mediapipe.tasks.cc.core.proto import external_file_pb2 as mediapipe_dot_tasks_dot_cc_dot_core_dot_proto_dot_external__file__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n0mediapipe/tasks/cc/core/proto/base_options.proto\x12\x1amediapipe.tasks.core.proto\x1a\x1emediapipe/gpu/gpu_origin.proto\x1a\x30mediapipe/tasks/cc/core/proto/acceleration.proto\x1a\x31mediapipe/tasks/cc/core/proto/external_file.proto\"\xe5\x01\n\x0b\x42\x61seOptions\x12=\n\x0bmodel_asset\x18\x01 \x01(\x0b\x32(.mediapipe.tasks.core.proto.ExternalFile\x12\x1e\n\x0fuse_stream_mode\x18\x02 \x01(\x08:\x05\x66\x61lse\x12>\n\x0c\x61\x63\x63\x65leration\x18\x03 \x01(\x0b\x32(.mediapipe.tasks.core.proto.Acceleration\x12\x37\n\ngpu_origin\x18\x04 \x01(\x0e\x32\x19.mediapipe.GpuOrigin.Mode:\x08TOP_LEFTB9\n%com.google.mediapipe.tasks.core.protoB\x10\x42\x61seOptionsProto')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.tasks.cc.core.proto.base_options_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n%com.google.mediapipe.tasks.core.protoB\020BaseOptionsProto'
  _BASEOPTIONS._serialized_start=214
  _BASEOPTIONS._serialized_end=443
# @@protoc_insertion_point(module_scope)
