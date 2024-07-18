import logging
import os
import tempfile
import uuid

import requests
from flask import Blueprint, request, current_app

bp = Blueprint("asr", __name__, url_prefix='/asr')

logger = logging.getLogger(__name__)


@bp.route('/test', methods=['POST', 'GET'])
def test():
    print(current_app)
    return "200";


@bp.route('/job', methods=['POST', 'GET'])
def submit_asr():
    s3_client = current_app.aws_s3_client;
    transcribe_client = current_app.aws_transcribe_client;

    data = request.get_json()
    mp4_url = data['mp4_url'] + ""

    language = data['language']
    if mp4_url.startswith("s3"):
        s3_uri = mp4_url
    else:
        # 下载 MP4 文件到临时文件
        response = requests.get(mp4_url, stream=True)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
            for chunk in response.iter_content(chunk_size=8192):
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        # 上传临时文件到 S3
        bucket_name = 'your-bucket-name'
        object_key = 'path/to/object.mp4'
        s3_client.upload_file(temp_file_path, bucket_name, object_key)

        # 获取 S3 对象的 URI
        s3_uri = f's3://{bucket_name}/{object_key}'
        # 删除临时文件
        os.remove(temp_file_path)
    # 提交 Transcribe 作业
    job_name = 'asr_' + str(uuid.uuid4())
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': s3_uri},
        MediaFormat='mp4',
        LanguageCode=language or 'en-US',
        Settings={
            'ShowSpeakerLabels': True,
            'MaxSpeakerLabels': 2
        }
    )
    print(response['TranscriptionJob'])
    job_id = response['TranscriptionJob']['TranscriptionJobName']
    job_status = response['TranscriptionJob']['TranscriptionJobStatus']
    current_app.asr_job_repository.create_item(job_id, s3_uri, job_status)

    return mp4_url


def convert_json_to_format(transcript_json):
    """
    具体代码参考： https://repost.aws/questions/QUjAzM70sgRiGkzI6blytmdg/transcribe-is-missing-conversation-not-identify-speakers
    非常重要
    """
    items = transcript_json['results']['items']
    output_text = ""
    current_speaker = None

    for item in items:
        speaker_label = item.get('speaker_label', None)
        content = item['alternatives'][0]['content']

        # Start the line with the speaker label:
        if speaker_label is not None and speaker_label != current_speaker:
            current_speaker = speaker_label
            output_text += f"\n{current_speaker}: "

        # Add the speech content:
        if item['type'] == 'punctuation':
            output_text = output_text.rstrip()

        output_text += f"{content} "

    return output_text


@bp.route('/update_asr_job', methods=['POST', 'GET'])
def update_asr_result():
    transcribe_client = current_app.aws_transcribe_client;
    data = request.get_json()
    job_name = data['job_name']
    job_result = None
    job_status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)

    if job_status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_file_uri = job_status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        transcript_json = requests.get(transcript_file_uri).json()
        job_result = convert_json_to_format(transcript_json)
        current_app.asr_job_repository.update_item(job_name, job_status, job_result)
    else:
        current_app.asr_job_repository.update_item(job_name, job_status, job_result)

    return "";


@bp.route('/asr_result', methods=['POST', 'GET'])
def get_asr_result():
    transcribe_client = current_app.aws_transcribe_client;
    data = request.get_json()
    job_name = data['job_name']
    job_result = None
    job_status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)

    if job_status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_file_uri = job_status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        transcript_json = requests.get(transcript_file_uri).json()
        job_result = convert_json_to_format(transcript_json)

    else:
        print("Transcription job failed:", job_status)

    return job_result
