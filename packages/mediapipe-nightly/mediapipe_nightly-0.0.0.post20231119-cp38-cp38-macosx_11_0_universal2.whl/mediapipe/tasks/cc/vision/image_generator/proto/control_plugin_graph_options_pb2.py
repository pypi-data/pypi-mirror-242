# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/vision/image_generator/proto/control_plugin_graph_options.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework import calculator_pb2 as mediapipe_dot_framework_dot_calculator__pb2
try:
  mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe_dot_framework_dot_calculator__options__pb2
except AttributeError:
  mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe.framework.calculator_options_pb2
from mediapipe.tasks.cc.core.proto import base_options_pb2 as mediapipe_dot_tasks_dot_cc_dot_core_dot_proto_dot_base__options__pb2
from mediapipe.tasks.cc.vision.image_generator.proto import conditioned_image_graph_options_pb2 as mediapipe_dot_tasks_dot_cc_dot_vision_dot_image__generator_dot_proto_dot_conditioned__image__graph__options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nRmediapipe/tasks/cc/vision/image_generator/proto/control_plugin_graph_options.proto\x12,mediapipe.tasks.vision.image_generator.proto\x1a$mediapipe/framework/calculator.proto\x1a\x30mediapipe/tasks/cc/core/proto/base_options.proto\x1aUmediapipe/tasks/cc/vision/image_generator/proto/conditioned_image_graph_options.proto\"\xcf\x01\n\x19\x43ontrolPluginGraphOptions\x12=\n\x0c\x62\x61se_options\x18\x01 \x01(\x0b\x32\'.mediapipe.tasks.core.proto.BaseOptions\x12s\n\x1f\x63onditioned_image_graph_options\x18\x02 \x01(\x0b\x32J.mediapipe.tasks.vision.image_generator.proto.ConditionedImageGraphOptionsBX\n6com.google.mediapipe.tasks.vision.imagegenerator.protoB\x1e\x43ontrolPluginGraphOptionsProtob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.tasks.cc.vision.image_generator.proto.control_plugin_graph_options_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n6com.google.mediapipe.tasks.vision.imagegenerator.protoB\036ControlPluginGraphOptionsProto'
  _CONTROLPLUGINGRAPHOPTIONS._serialized_start=308
  _CONTROLPLUGINGRAPHOPTIONS._serialized_end=515
# @@protoc_insertion_point(module_scope)
