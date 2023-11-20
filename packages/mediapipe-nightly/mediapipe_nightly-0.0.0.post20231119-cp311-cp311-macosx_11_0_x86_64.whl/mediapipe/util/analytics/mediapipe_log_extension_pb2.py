# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/util/analytics/mediapipe_log_extension.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.util.analytics import mediapipe_logging_enums_pb2 as mediapipe_dot_util_dot_analytics_dot_mediapipe__logging__enums__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n6mediapipe/util/analytics/mediapipe_log_extension.proto\x12\x14logs.proto.mediapipe\x1a\x36mediapipe/util/analytics/mediapipe_logging_enums.proto\"\x8b\x01\n\x15MediaPipeLogExtension\x12\x35\n\x0bsystem_info\x18\x01 \x01(\x0b\x32 .logs.proto.mediapipe.SystemInfo\x12;\n\x0esolution_event\x18\x02 \x01(\x0b\x32#.logs.proto.mediapipe.SolutionEvent\"~\n\nSystemInfo\x12\x30\n\x08platform\x18\x01 \x01(\x0e\x32\x1e.logs.proto.mediapipe.Platform\x12\x0e\n\x06\x61pp_id\x18\x02 \x01(\t\x12\x13\n\x0b\x61pp_version\x18\x03 \x01(\t\x12\x19\n\x11mediapipe_version\x18\x04 \x01(\t\"\xa1\x03\n\rSolutionEvent\x12\x39\n\rsolution_name\x18\x01 \x01(\x0e\x32\".logs.proto.mediapipe.SolutionName\x12\x33\n\nevent_name\x18\x02 \x01(\x0e\x32\x1f.logs.proto.mediapipe.EventName\x12\x43\n\rsession_start\x18\x03 \x01(\x0b\x32*.logs.proto.mediapipe.SolutionSessionStartH\x00\x12K\n\x11invocation_report\x18\x04 \x01(\x0b\x32..logs.proto.mediapipe.SolutionInvocationReportH\x00\x12?\n\x0bsession_end\x18\x05 \x01(\x0b\x32(.logs.proto.mediapipe.SolutionSessionEndH\x00\x12<\n\rerror_details\x18\x06 \x01(\x0b\x32#.logs.proto.mediapipe.SolutionErrorH\x00\x42\x0f\n\revent_details\"f\n\x17SolutionInvocationCount\x12<\n\x0finput_data_type\x18\x01 \x01(\x0e\x32#.logs.proto.mediapipe.InputDataType\x12\r\n\x05\x63ount\x18\x02 \x01(\x03\"u\n\x14SolutionSessionStart\x12\x30\n\x04mode\x18\x01 \x01(\x0e\x32\".logs.proto.mediapipe.SolutionMode\x12\x12\n\ngraph_name\x18\x02 \x01(\t\x12\x17\n\x0finit_latency_ms\x18\x03 \x01(\x04\"\x92\x02\n\x18SolutionInvocationReport\x12\x30\n\x04mode\x18\x01 \x01(\x0e\x32\".logs.proto.mediapipe.SolutionMode\x12#\n\x1bpipeline_average_latency_ms\x18\x04 \x01(\x04\x12 \n\x18pipeline_peak_latency_ms\x18\x05 \x01(\x04\x12\x17\n\x0f\x65lapsed_time_ms\x18\x06 \x01(\x04\x12\x0f\n\x07\x64ropped\x18\x07 \x01(\x03\x12G\n\x10invocation_count\x18\x08 \x03(\x0b\x32-.logs.proto.mediapipe.SolutionInvocationCountJ\x04\x08\x02\x10\x03J\x04\x08\x03\x10\x04\"e\n\x12SolutionSessionEnd\x12I\n\x11invocation_report\x18\x02 \x01(\x0b\x32..logs.proto.mediapipe.SolutionInvocationReportJ\x04\x08\x01\x10\x02\"D\n\rSolutionError\x12\x33\n\nerror_code\x18\x01 \x01(\x0e\x32\x1f.logs.proto.mediapipe.ErrorCodeB3\n\x1a\x63om.google.mediapipe.protoB\x15MediaPipeLoggingProto')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.util.analytics.mediapipe_log_extension_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\032com.google.mediapipe.protoB\025MediaPipeLoggingProto'
  _MEDIAPIPELOGEXTENSION._serialized_start=137
  _MEDIAPIPELOGEXTENSION._serialized_end=276
  _SYSTEMINFO._serialized_start=278
  _SYSTEMINFO._serialized_end=404
  _SOLUTIONEVENT._serialized_start=407
  _SOLUTIONEVENT._serialized_end=824
  _SOLUTIONINVOCATIONCOUNT._serialized_start=826
  _SOLUTIONINVOCATIONCOUNT._serialized_end=928
  _SOLUTIONSESSIONSTART._serialized_start=930
  _SOLUTIONSESSIONSTART._serialized_end=1047
  _SOLUTIONINVOCATIONREPORT._serialized_start=1050
  _SOLUTIONINVOCATIONREPORT._serialized_end=1324
  _SOLUTIONSESSIONEND._serialized_start=1326
  _SOLUTIONSESSIONEND._serialized_end=1427
  _SOLUTIONERROR._serialized_start=1429
  _SOLUTIONERROR._serialized_end=1497
# @@protoc_insertion_point(module_scope)
