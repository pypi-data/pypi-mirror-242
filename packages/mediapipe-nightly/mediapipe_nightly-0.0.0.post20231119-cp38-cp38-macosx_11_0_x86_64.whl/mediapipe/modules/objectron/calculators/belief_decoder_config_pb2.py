# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/modules/objectron/calculators/belief_decoder_config.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nCmediapipe/modules/objectron/calculators/belief_decoder_config.proto\x12\tmediapipe\"\xc4\x01\n\x13\x42\x65liefDecoderConfig\x12\x1e\n\x11heatmap_threshold\x18\x01 \x01(\x02:\x03\x30.9\x12\x1e\n\x12local_max_distance\x18\x02 \x01(\x02:\x02\x31\x30\x12\"\n\x11offset_scale_coef\x18\x03 \x01(\x02:\x03\x30.5B\x02\x18\x01\x12\x15\n\rvoting_radius\x18\x04 \x01(\x05\x12\x18\n\x10voting_allowance\x18\x05 \x01(\x05\x12\x18\n\x10voting_threshold\x18\x06 \x01(\x02')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.modules.objectron.calculators.belief_decoder_config_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _BELIEFDECODERCONFIG.fields_by_name['offset_scale_coef']._options = None
  _BELIEFDECODERCONFIG.fields_by_name['offset_scale_coef']._serialized_options = b'\030\001'
  _BELIEFDECODERCONFIG._serialized_start=83
  _BELIEFDECODERCONFIG._serialized_end=279
# @@protoc_insertion_point(module_scope)
