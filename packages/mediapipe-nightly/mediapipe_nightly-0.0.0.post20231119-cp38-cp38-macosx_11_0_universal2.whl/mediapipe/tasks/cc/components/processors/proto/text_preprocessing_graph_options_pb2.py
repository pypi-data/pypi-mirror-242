# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/components/processors/proto/text_preprocessing_graph_options.proto
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
from mediapipe.tasks.cc.components.processors.proto import text_model_type_pb2 as mediapipe_dot_tasks_dot_cc_dot_components_dot_processors_dot_proto_dot_text__model__type__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nUmediapipe/tasks/cc/components/processors/proto/text_preprocessing_graph_options.proto\x12+mediapipe.tasks.components.processors.proto\x1a$mediapipe/framework/calculator.proto\x1a\x44mediapipe/tasks/cc/components/processors/proto/text_model_type.proto\"\xac\x02\n\x1dTextPreprocessingGraphOptions\x12X\n\nmodel_type\x18\x01 \x01(\x0e\x32\x44.mediapipe.tasks.components.processors.proto.TextModelType.ModelType\x12\x13\n\x0bmax_seq_len\x18\x02 \x01(\x05\x12!\n\x19has_dynamic_input_tensors\x18\x03 \x01(\x08\x32y\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xbf\xbc\xb8\xe3\x01 \x01(\x0b\x32J.mediapipe.tasks.components.processors.proto.TextPreprocessingGraphOptions')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.tasks.cc.components.processors.proto.text_preprocessing_graph_options_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_TEXTPREPROCESSINGGRAPHOPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _TEXTPREPROCESSINGGRAPHOPTIONS._serialized_start=243
  _TEXTPREPROCESSINGGRAPHOPTIONS._serialized_end=543
# @@protoc_insertion_point(module_scope)
