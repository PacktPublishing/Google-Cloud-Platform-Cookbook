#!/usr/bin/env python
# Cloned from GoogleCloudPlatform/python-docs-samples/speech/cloud-client/transcribe.py
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def run_quickstart():
    # [START speech_quickstart]
    import io

    # Imports the Google Cloud client library
    # [START migration_import]
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    # [END migration_import]

    # Instantiates a client
    # [START migration_client]
    client = speech.SpeechClient()
    # [END migration_client]

    # The name of the audio file to transcribe
    file_name = 'record.flac'

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding='FLAC',
        sample_rate_hertz=16000,
        language_code='en-US')

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))
    # [END speech_quickstart]


if __name__ == '__main__':
    run_quickstart()
