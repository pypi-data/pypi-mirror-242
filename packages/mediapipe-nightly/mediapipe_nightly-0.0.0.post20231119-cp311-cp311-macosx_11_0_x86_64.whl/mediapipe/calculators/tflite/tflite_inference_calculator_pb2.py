# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/tflite/tflite_inference_calculator.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n>mediapipe/calculators/tflite/tflite_inference_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xfb\x08\n TfLiteInferenceCalculatorOptions\x12\x12\n\nmodel_path\x18\x01 \x01(\t\x12\x1a\n\x07use_gpu\x18\x02 \x01(\x08:\x05\x66\x61lseB\x02\x18\x01\x12\x1c\n\tuse_nnapi\x18\x03 \x01(\x08:\x05\x66\x61lseB\x02\x18\x01\x12\x1a\n\x0e\x63pu_num_thread\x18\x04 \x01(\x05:\x02-1\x12\x46\n\x08\x64\x65legate\x18\x05 \x01(\x0b\x32\x34.mediapipe.TfLiteInferenceCalculatorOptions.Delegate\x1a\xc9\x06\n\x08\x44\x65legate\x12M\n\x06tflite\x18\x01 \x01(\x0b\x32;.mediapipe.TfLiteInferenceCalculatorOptions.Delegate.TfLiteH\x00\x12G\n\x03gpu\x18\x02 \x01(\x0b\x32\x38.mediapipe.TfLiteInferenceCalculatorOptions.Delegate.GpuH\x00\x12K\n\x05nnapi\x18\x03 \x01(\x0b\x32:.mediapipe.TfLiteInferenceCalculatorOptions.Delegate.NnapiH\x00\x12O\n\x07xnnpack\x18\x04 \x01(\x0b\x32<.mediapipe.TfLiteInferenceCalculatorOptions.Delegate.XnnpackH\x00\x1a\x08\n\x06TfLite\x1a\x9b\x03\n\x03Gpu\x12#\n\x14use_advanced_gpu_api\x18\x01 \x01(\x08:\x05\x66\x61lse\x12N\n\x03\x61pi\x18\x04 \x01(\x0e\x32<.mediapipe.TfLiteInferenceCalculatorOptions.Delegate.Gpu.Api:\x03\x41NY\x12\"\n\x14\x61llow_precision_loss\x18\x03 \x01(\x08:\x04true\x12\x1a\n\x12\x63\x61\x63hed_kernel_path\x18\x02 \x01(\t\x12g\n\x05usage\x18\x05 \x01(\x0e\x32G.mediapipe.TfLiteInferenceCalculatorOptions.Delegate.Gpu.InferenceUsage:\x0fSUSTAINED_SPEED\"&\n\x03\x41pi\x12\x07\n\x03\x41NY\x10\x00\x12\n\n\x06OPENGL\x10\x01\x12\n\n\x06OPENCL\x10\x02\"N\n\x0eInferenceUsage\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x16\n\x12\x46\x41ST_SINGLE_ANSWER\x10\x01\x12\x13\n\x0fSUSTAINED_SPEED\x10\x02\x1a/\n\x05Nnapi\x12\x11\n\tcache_dir\x18\x01 \x01(\t\x12\x13\n\x0bmodel_token\x18\x02 \x01(\t\x1a\"\n\x07Xnnpack\x12\x17\n\x0bnum_threads\x18\x01 \x01(\x05:\x02-1B\n\n\x08\x64\x65legate2Y\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xcd\x8f\xc2o \x01(\x0b\x32+.mediapipe.TfLiteInferenceCalculatorOptions')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.calculators.tflite.tflite_inference_calculator_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_TFLITEINFERENCECALCULATOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _TFLITEINFERENCECALCULATOROPTIONS.fields_by_name['use_gpu']._options = None
  _TFLITEINFERENCECALCULATOROPTIONS.fields_by_name['use_gpu']._serialized_options = b'\030\001'
  _TFLITEINFERENCECALCULATOROPTIONS.fields_by_name['use_nnapi']._options = None
  _TFLITEINFERENCECALCULATOROPTIONS.fields_by_name['use_nnapi']._serialized_options = b'\030\001'
  _TFLITEINFERENCECALCULATOROPTIONS._serialized_start=116
  _TFLITEINFERENCECALCULATOROPTIONS._serialized_end=1263
  _TFLITEINFERENCECALCULATOROPTIONS_DELEGATE._serialized_start=331
  _TFLITEINFERENCECALCULATOROPTIONS_DELEGATE._serialized_end=1172
  _TFLITEINFERENCECALCULATOROPTIONS_DELEGATE_TFLITE._serialized_start=653
  _TFLITEINFERENCECALCULATOROPTIONS_DELEGATE_TFLITE._serialized_end=661
  _TFLITEINFERENCECALCULATOROPTIONS_DELEGATE_GPU._serialized_start=664
  _TFLITEINFERENCECALCULATOROPTIONS_DELEGATE_GPU._serialized_end=1075
  _TFLITEINFERENCECALCULATOROPTIONS_DELEGATE_GPU_API._serialized_start=957
  _TFLITEINFERENCECALCULATOROPTIONS_DELEGATE_GPU_API._serialized_end=995
  _TFLITEINFERENCECALCULATOROPTIONS_DELEGATE_GPU_INFERENCEUSAGE._serialized_start=997
  _TFLITEINFERENCECALCULATOROPTIONS_DELEGATE_GPU_INFERENCEUSAGE._serialized_end=1075
  _TFLITEINFERENCECALCULATOROPTIONS_DELEGATE_NNAPI._serialized_start=1077
  _TFLITEINFERENCECALCULATOROPTIONS_DELEGATE_NNAPI._serialized_end=1124
  _TFLITEINFERENCECALCULATOROPTIONS_DELEGATE_XNNPACK._serialized_start=1126
  _TFLITEINFERENCECALCULATOROPTIONS_DELEGATE_XNNPACK._serialized_end=1160
# @@protoc_insertion_point(module_scope)
