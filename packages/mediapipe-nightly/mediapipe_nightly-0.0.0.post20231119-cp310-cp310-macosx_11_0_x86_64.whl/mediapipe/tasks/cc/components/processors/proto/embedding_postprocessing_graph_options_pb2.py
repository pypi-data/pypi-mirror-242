# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/components/processors/proto/embedding_postprocessing_graph_options.proto
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
from mediapipe.tasks.cc.components.calculators import tensors_to_embeddings_calculator_pb2 as mediapipe_dot_tasks_dot_cc_dot_components_dot_calculators_dot_tensors__to__embeddings__calculator__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n[mediapipe/tasks/cc/components/processors/proto/embedding_postprocessing_graph_options.proto\x12+mediapipe.tasks.components.processors.proto\x1a$mediapipe/framework/calculator.proto\x1aPmediapipe/tasks/cc/components/calculators/tensors_to_embeddings_calculator.proto\"\x9d\x02\n#EmbeddingPostprocessingGraphOptions\x12V\n\x1dtensors_to_embeddings_options\x18\x01 \x01(\x0b\x32/.mediapipe.TensorsToEmbeddingsCalculatorOptions\x12\x1d\n\x15has_quantized_outputs\x18\x02 \x01(\x08\x32\x7f\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xae\xf4\x91\xe3\x01 \x01(\x0b\x32P.mediapipe.tasks.components.processors.proto.EmbeddingPostprocessingGraphOptions')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.tasks.cc.components.processors.proto.embedding_postprocessing_graph_options_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_EMBEDDINGPOSTPROCESSINGGRAPHOPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _EMBEDDINGPOSTPROCESSINGGRAPHOPTIONS._serialized_start=261
  _EMBEDDINGPOSTPROCESSINGGRAPHOPTIONS._serialized_end=546
# @@protoc_insertion_point(module_scope)
