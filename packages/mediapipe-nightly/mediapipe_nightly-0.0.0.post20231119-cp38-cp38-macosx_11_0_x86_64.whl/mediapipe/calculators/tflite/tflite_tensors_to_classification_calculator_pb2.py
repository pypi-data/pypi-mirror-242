# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/tflite/tflite_tensors_to_classification_calculator.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nNmediapipe/calculators/tflite/tflite_tensors_to_classification_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xfc\x01\n.TfLiteTensorsToClassificationCalculatorOptions\x12\x1b\n\x13min_score_threshold\x18\x01 \x01(\x02\x12\r\n\x05top_k\x18\x02 \x01(\x05\x12\x16\n\x0elabel_map_path\x18\x03 \x01(\t\x12\x1d\n\x15\x62inary_classification\x18\x04 \x01(\x08\x32g\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xe7\xdd\x83\x7f \x01(\x0b\x32\x39.mediapipe.TfLiteTensorsToClassificationCalculatorOptions')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.calculators.tflite.tflite_tensors_to_classification_calculator_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_TFLITETENSORSTOCLASSIFICATIONCALCULATOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _TFLITETENSORSTOCLASSIFICATIONCALCULATOROPTIONS._serialized_start=132
  _TFLITETENSORSTOCLASSIFICATIONCALCULATOROPTIONS._serialized_end=384
# @@protoc_insertion_point(module_scope)
