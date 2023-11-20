# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/image/warp_affine_calculator.proto
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
from mediapipe.gpu import gpu_origin_pb2 as mediapipe_dot_gpu_dot_gpu__origin__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n8mediapipe/calculators/image/warp_affine_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\x1a\x1emediapipe/gpu/gpu_origin.proto\"\xd0\x03\n\x1bWarpAffineCalculatorOptions\x12\x46\n\x0b\x62order_mode\x18\x01 \x01(\x0e\x32\x31.mediapipe.WarpAffineCalculatorOptions.BorderMode\x12-\n\ngpu_origin\x18\x02 \x01(\x0e\x32\x19.mediapipe.GpuOrigin.Mode\x12K\n\rinterpolation\x18\x03 \x01(\x0e\x32\x34.mediapipe.WarpAffineCalculatorOptions.Interpolation\"K\n\nBorderMode\x12\x16\n\x12\x42ORDER_UNSPECIFIED\x10\x00\x12\x0f\n\x0b\x42ORDER_ZERO\x10\x01\x12\x14\n\x10\x42ORDER_REPLICATE\x10\x02\"I\n\rInterpolation\x12\x15\n\x11INTER_UNSPECIFIED\x10\x00\x12\x10\n\x0cINTER_LINEAR\x10\x01\x12\x0f\n\x0bINTER_CUBIC\x10\x02\x32U\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xc7\xbb\x98\xb2\x01 \x01(\x0b\x32&.mediapipe.WarpAffineCalculatorOptions')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.calculators.image.warp_affine_calculator_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_WARPAFFINECALCULATOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _WARPAFFINECALCULATOROPTIONS._serialized_start=142
  _WARPAFFINECALCULATOROPTIONS._serialized_end=606
  _WARPAFFINECALCULATOROPTIONS_BORDERMODE._serialized_start=369
  _WARPAFFINECALCULATOROPTIONS_BORDERMODE._serialized_end=444
  _WARPAFFINECALCULATOROPTIONS_INTERPOLATION._serialized_start=446
  _WARPAFFINECALCULATOROPTIONS_INTERPOLATION._serialized_end=519
# @@protoc_insertion_point(module_scope)
