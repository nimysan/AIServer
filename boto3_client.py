import logging
import os

import boto3

logger = logging.getLogger("flask.app")


def get_boto3_config():
    # 设置默认值
    DEFAULT_REGION = "us-west-2"
    region = os.getenv("REGION", DEFAULT_REGION)
    DEFAULT_AK = "your_default_access_key"
    DEFAULT_SK = "your_default_secret_key"

    # 读取环境变量

    ak = os.getenv("ACCESS_KEY", DEFAULT_AK)
    sk = os.getenv("SECRET_KEY", DEFAULT_SK)

    # 在程序中使用这些参数
    logger.info(f"Region: {region}")
    logger.info(f"Access Key: {ak}")
    logger.debug(f"Secret Key: {sk}")

    return region, boto3.Session(
        aws_access_key_id=ak,
        aws_secret_access_key=sk,
        region_name=region
    )
