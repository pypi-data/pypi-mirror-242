# Copyright 2022 The MediaPipe Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""MediaPipe Tasks Text API."""

import mediapipe.tasks.python.text.language_detector
import mediapipe.tasks.python.text.text_classifier
import mediapipe.tasks.python.text.text_embedder

LanguageDetector = language_detector.LanguageDetector
LanguageDetectorOptions = language_detector.LanguageDetectorOptions
LanguageDetectorResult = language_detector.LanguageDetectorResult
TextClassifier = text_classifier.TextClassifier
TextClassifierOptions = text_classifier.TextClassifierOptions
TextClassifierResult = text_classifier.TextClassifierResult
TextEmbedder = text_embedder.TextEmbedder
TextEmbedderOptions = text_embedder.TextEmbedderOptions
TextEmbedderResult = text_embedder.TextEmbedderResult

# Remove unnecessary modules to avoid duplication in API docs.
del mediapipe
del language_detector
del text_classifier
del text_embedder
