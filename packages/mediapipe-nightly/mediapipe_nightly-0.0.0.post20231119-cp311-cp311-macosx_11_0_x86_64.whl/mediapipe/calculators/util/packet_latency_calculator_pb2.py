# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/util/packet_latency_calculator.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n:mediapipe/calculators/util/packet_latency_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xef\x01\n\x1ePacketLatencyCalculatorOptions\x12\x19\n\rnum_intervals\x18\x01 \x01(\x03:\x02\x31\x30\x12!\n\x12interval_size_usec\x18\x02 \x01(\x03:\x05\x31\x30\x30\x30\x30\x12\x1f\n\x13reset_duration_usec\x18\x03 \x01(\x03:\x02-1\x12\x15\n\rpacket_labels\x18\x04 \x03(\t2W\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xcd\xd1\xabR \x01(\x0b\x32).mediapipe.PacketLatencyCalculatorOptions')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.calculators.util.packet_latency_calculator_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_PACKETLATENCYCALCULATOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _PACKETLATENCYCALCULATOROPTIONS._serialized_start=112
  _PACKETLATENCYCALCULATOROPTIONS._serialized_end=351
# @@protoc_insertion_point(module_scope)
