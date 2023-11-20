# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/vision/pose_landmarker/proto/pose_landmarks_detector_graph_options.proto
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
from mediapipe.framework import calculator_options_pb2 as mediapipe_dot_framework_dot_calculator__options__pb2
from mediapipe.tasks.cc.core.proto import base_options_pb2 as mediapipe_dot_tasks_dot_cc_dot_core_dot_proto_dot_base__options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n[mediapipe/tasks/cc/vision/pose_landmarker/proto/pose_landmarks_detector_graph_options.proto\x12,mediapipe.tasks.vision.pose_landmarker.proto\x1a$mediapipe/framework/calculator.proto\x1a,mediapipe/framework/calculator_options.proto\x1a\x30mediapipe/tasks/cc/core/proto/base_options.proto\"\xa3\x02\n!PoseLandmarksDetectorGraphOptions\x12=\n\x0c\x62\x61se_options\x18\x01 \x01(\x0b\x32\'.mediapipe.tasks.core.proto.BaseOptions\x12%\n\x18min_detection_confidence\x18\x02 \x01(\x02:\x03\x30.5\x12\x18\n\x10smooth_landmarks\x18\x03 \x01(\x08\x32~\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\x80\xf0\xb8\xf7\x01 \x01(\x0b\x32O.mediapipe.tasks.vision.pose_landmarker.proto.PoseLandmarksDetectorGraphOptionsB`\n6com.google.mediapipe.tasks.vision.poselandmarker.protoB&PoseLandmarksDetectorGraphOptionsProto')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.tasks.cc.vision.pose_landmarker.proto.pose_landmarks_detector_graph_options_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_POSELANDMARKSDETECTORGRAPHOPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n6com.google.mediapipe.tasks.vision.poselandmarker.protoB&PoseLandmarksDetectorGraphOptionsProto'
  _POSELANDMARKSDETECTORGRAPHOPTIONS._serialized_start=276
  _POSELANDMARKSDETECTORGRAPHOPTIONS._serialized_end=567
# @@protoc_insertion_point(module_scope)
