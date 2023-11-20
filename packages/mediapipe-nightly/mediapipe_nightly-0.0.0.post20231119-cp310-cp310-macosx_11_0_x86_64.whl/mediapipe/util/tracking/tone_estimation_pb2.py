# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/util/tracking/tone_estimation.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.util.tracking import tone_models_pb2 as mediapipe_dot_util_dot_tracking_dot_tone__models__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-mediapipe/util/tracking/tone_estimation.proto\x12\tmediapipe\x1a)mediapipe/util/tracking/tone_models.proto\"\x97\x05\n\nToneChange\x12+\n\tgain_bias\x18\x01 \x01(\x0b\x32\x18.mediapipe.GainBiasModel\x12*\n\x06\x61\x66\x66ine\x18\x02 \x01(\x0b\x32\x1a.mediapipe.AffineToneModel\x12:\n\x11mixture_gain_bias\x18\x03 \x01(\x0b\x32\x1f.mediapipe.MixtureGainBiasModel\x12\x39\n\x0emixture_affine\x18\x04 \x01(\x0b\x32!.mediapipe.MixtureAffineToneModel\x12\x1c\n\x14mixture_domain_sigma\x18\x05 \x01(\x02\x12\x17\n\x0c\x66rac_clipped\x18\x06 \x01(\x02:\x01\x30\x12\x16\n\x0elow_percentile\x18\x08 \x01(\x02\x12\x1a\n\x12low_mid_percentile\x18\t \x01(\x02\x12\x16\n\x0emid_percentile\x18\n \x01(\x02\x12\x1b\n\x13high_mid_percentile\x18\x0b \x01(\x02\x12\x17\n\x0fhigh_percentile\x18\x0c \x01(\x02\x12\x19\n\nlog_domain\x18\r \x01(\x08:\x05\x66\x61lse\x12/\n\x04type\x18\x0e \x01(\x0e\x32\x1a.mediapipe.ToneChange.Type:\x05VALID\x12=\n\x0fstability_stats\x18\x0f \x01(\x0b\x32$.mediapipe.ToneChange.StabilityStats\x1aU\n\x0eStabilityStats\x12\x13\n\x0bnum_inliers\x18\x01 \x01(\x05\x12\x17\n\x0finlier_fraction\x18\x02 \x01(\x02\x12\x15\n\rinlier_weight\x18\x03 \x01(\x01\"\x1e\n\x04Type\x12\t\n\x05VALID\x10\x00\x12\x0b\n\x07INVALID\x10\n\"\xd2\x01\n\x10ToneMatchOptions\x12\"\n\x14min_match_percentile\x18\x01 \x01(\x02:\x04\x30.01\x12\"\n\x14max_match_percentile\x18\x02 \x01(\x02:\x04\x30.99\x12\"\n\x16match_percentile_steps\x18\x03 \x01(\x05:\x02\x31\x30\x12\x18\n\x0cpatch_radius\x18\x04 \x01(\x05:\x02\x31\x38\x12\x1d\n\x10max_frac_clipped\x18\x05 \x01(\x02:\x03\x30.4\x12\x19\n\nlog_domain\x18\x08 \x01(\x08:\x05\x66\x61lse\"\x89\x01\n\x0f\x43lipMaskOptions\x12\x1a\n\x0cmin_exposure\x18\x01 \x01(\x02:\x04\x30.02\x12\x1a\n\x0cmax_exposure\x18\x02 \x01(\x02:\x04\x30.98\x12\x1f\n\x14max_clipped_channels\x18\x04 \x01(\x05:\x01\x31\x12\x1d\n\x12\x63lip_mask_diameter\x18\x05 \x01(\x05:\x01\x35\"\x81\x07\n\x15ToneEstimationOptions\x12\x37\n\x12tone_match_options\x18\x01 \x01(\x0b\x32\x1b.mediapipe.ToneMatchOptions\x12\x35\n\x11\x63lip_mask_options\x18\x02 \x01(\x0b\x32\x1a.mediapipe.ClipMaskOptions\x12\"\n\x14stats_low_percentile\x18\x03 \x01(\x02:\x04\x30.05\x12%\n\x18stats_low_mid_percentile\x18\x04 \x01(\x02:\x03\x30.2\x12!\n\x14stats_mid_percentile\x18\x05 \x01(\x02:\x03\x30.5\x12&\n\x19stats_high_mid_percentile\x18\x06 \x01(\x02:\x03\x30.8\x12#\n\x15stats_high_percentile\x18\x07 \x01(\x02:\x04\x30.95\x12\x1b\n\x0firls_iterations\x18\x08 \x01(\x05:\x02\x31\x30\x12P\n\x17stable_gain_bias_bounds\x18\t \x01(\x0b\x32/.mediapipe.ToneEstimationOptions.GainBiasBounds\x12Y\n\x0f\x64ownsample_mode\x18\n \x01(\x0e\x32/.mediapipe.ToneEstimationOptions.DownsampleMode:\x0f\x44OWNSAMPLE_NONE\x12\x1e\n\x11\x64ownsampling_size\x18\x0b \x01(\x05:\x03\x32\x35\x36\x12\x1c\n\x11\x64ownsample_factor\x18\x0c \x01(\x02:\x01\x32\x1a\xbb\x01\n\x0eGainBiasBounds\x12!\n\x13min_inlier_fraction\x18\x01 \x01(\x02:\x04\x30.75\x12\x1e\n\x11min_inlier_weight\x18\x02 \x01(\x02:\x03\x30.5\x12\x18\n\nlower_gain\x18\x03 \x01(\x02:\x04\x30.75\x12\x19\n\nupper_gain\x18\x04 \x01(\x02:\x05\x31.334\x12\x18\n\nlower_bias\x18\x05 \x01(\x02:\x04-0.2\x12\x17\n\nupper_bias\x18\x06 \x01(\x02:\x03\x30.2\"w\n\x0e\x44ownsampleMode\x12\x13\n\x0f\x44OWNSAMPLE_NONE\x10\x01\x12\x1a\n\x16\x44OWNSAMPLE_TO_MAX_SIZE\x10\x02\x12\x18\n\x14\x44OWNSAMPLE_BY_FACTOR\x10\x03\x12\x1a\n\x16\x44OWNSAMPLE_TO_MIN_SIZE\x10\x04\"/\n\tToneMatch\x12\x10\n\x08\x63urr_val\x18\x01 \x01(\x02\x12\x10\n\x08prev_val\x18\x02 \x01(\x02\"R\n\x0ePatchToneMatch\x12(\n\ntone_match\x18\x01 \x03(\x0b\x32\x14.mediapipe.ToneMatch\x12\x16\n\x0birls_weight\x18\x02 \x01(\x02:\x01\x31')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.util.tracking.tone_estimation_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TONECHANGE._serialized_start=104
  _TONECHANGE._serialized_end=767
  _TONECHANGE_STABILITYSTATS._serialized_start=650
  _TONECHANGE_STABILITYSTATS._serialized_end=735
  _TONECHANGE_TYPE._serialized_start=737
  _TONECHANGE_TYPE._serialized_end=767
  _TONEMATCHOPTIONS._serialized_start=770
  _TONEMATCHOPTIONS._serialized_end=980
  _CLIPMASKOPTIONS._serialized_start=983
  _CLIPMASKOPTIONS._serialized_end=1120
  _TONEESTIMATIONOPTIONS._serialized_start=1123
  _TONEESTIMATIONOPTIONS._serialized_end=2020
  _TONEESTIMATIONOPTIONS_GAINBIASBOUNDS._serialized_start=1712
  _TONEESTIMATIONOPTIONS_GAINBIASBOUNDS._serialized_end=1899
  _TONEESTIMATIONOPTIONS_DOWNSAMPLEMODE._serialized_start=1901
  _TONEESTIMATIONOPTIONS_DOWNSAMPLEMODE._serialized_end=2020
  _TONEMATCH._serialized_start=2022
  _TONEMATCH._serialized_end=2069
  _PATCHTONEMATCH._serialized_start=2071
  _PATCHTONEMATCH._serialized_end=2153
# @@protoc_insertion_point(module_scope)
