import logging
import os
import uuid
from string import Template
import boto3
import requests
import tempfile

from flask import Blueprint, request, current_app, jsonify
from brclient.bedrock_client import BedrockClient
from model import get_asr_job_repository

bp = Blueprint("asr", __name__, url_prefix='/asr')

logger = logging.getLogger(__name__)

from boto3_client import get_boto3_config

from model.config import ConfigItemRepository

config_repository = ConfigItemRepository("us-west-2")
config_data = config_repository.list_all()


def remove_rewrite_prompt(string):
    if "_rewrite_prompt" in string:
        return string.replace("_rewrite_prompt", "")
    else:
        return string


def load_bedrock_client(region):
    bedrock_client = BedrockClient(region)
    return bedrock_client


def get_config(prompt_key):
    for data in config_data:
        if data.get('item_key') == prompt_key:
            return data.get('item_value')
    return None


# 创建 S3 和 Transcribe 客户端
region, boto_session = get_boto3_config("us-west-2")
s3_client = boto_session.client('s3')
transcribe_client = boto_session.client('transcribe')


@bp.route('/job', methods=['POST', 'GET'])
def submit_asr():
    data = request.get_json()
    mp4_url = data['mp4_url']+""
    print(mp4_url)
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
    job_name = 'asr_'+str(uuid.uuid4())
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': s3_uri},
        MediaFormat='mp4',
        LanguageCode=language or 'en-US'
    )
    print( response['TranscriptionJob'])
    job_id = response['TranscriptionJob']['TranscriptionJobName']
    job_status = response['TranscriptionJob']['TranscriptionJobStatus']
    asr_job_repository = get_asr_job_repository()
    asr_job_repository.create_item(job_id,s3_uri, job_status)

    return mp4_url
