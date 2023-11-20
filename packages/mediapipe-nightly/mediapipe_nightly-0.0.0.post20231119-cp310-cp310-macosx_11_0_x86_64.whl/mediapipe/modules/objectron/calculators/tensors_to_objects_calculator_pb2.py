# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/modules/objectron/calculators/tensors_to_objects_calculator.proto
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
from mediapipe.modules.objectron.calculators import belief_decoder_config_pb2 as mediapipe_dot_modules_dot_objectron_dot_calculators_dot_belief__decoder__config__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nKmediapipe/modules/objectron/calculators/tensors_to_objects_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\x1a\x43mediapipe/modules/objectron/calculators/belief_decoder_config.proto\"\x88\x02\n!TensorsToObjectsCalculatorOptions\x12\x13\n\x0bnum_classes\x18\x01 \x01(\x05\x12\x15\n\rnum_keypoints\x18\x02 \x01(\x05\x12\"\n\x17num_values_per_keypoint\x18\x03 \x01(\x05:\x01\x32\x12\x36\n\x0e\x64\x65\x63oder_config\x18\x04 \x01(\x0b\x32\x1e.mediapipe.BeliefDecoderConfig2[\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xd4\xea\xb7\x9f\x01 \x01(\x0b\x32,.mediapipe.TensorsToObjectsCalculatorOptions')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.modules.objectron.calculators.tensors_to_objects_calculator_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_TENSORSTOOBJECTSCALCULATOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _TENSORSTOOBJECTSCALCULATOROPTIONS._serialized_start=198
  _TENSORSTOOBJECTSCALCULATOROPTIONS._serialized_end=462
# @@protoc_insertion_point(module_scope)
