# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/util/timed_box_list_to_render_data_calculator.proto
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
from mediapipe.util import color_pb2 as mediapipe_dot_util_dot_color__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nImediapipe/calculators/util/timed_box_list_to_render_data_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\x1a\x1amediapipe/util/color.proto\"\xcb\x01\n)TimedBoxListToRenderDataCalculatorOptions\x12#\n\tbox_color\x18\x01 \x01(\x0b\x32\x10.mediapipe.Color\x12\x14\n\tthickness\x18\x02 \x01(\x01:\x01\x31\x32\x63\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xce\x8a\x9e\x8a\x01 \x01(\x0b\x32\x34.mediapipe.TimedBoxListToRenderDataCalculatorOptions')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.calculators.util.timed_box_list_to_render_data_calculator_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_TIMEDBOXLISTTORENDERDATACALCULATOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _TIMEDBOXLISTTORENDERDATACALCULATOROPTIONS._serialized_start=155
  _TIMEDBOXLISTTORENDERDATACALCULATOROPTIONS._serialized_end=358
# @@protoc_insertion_point(module_scope)
