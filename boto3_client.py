import logging
import os

import boto3

logger = logging.getLogger("flask.app")

def get_boto3_config(work_region="us-west-2"):
    # 读取环境变量
    ak = os.getenv("ACCESS_KEY")
    if ak is None:
        logger.info("Use EC2 Instance profile as credentials")
        return work_region, boto3.Session(region_name=work_region)
    else:
        # 在程序中使用这些参数
        sk = os.getenv("SECRET_KEY")
        logger.info(f"Region: {work_region}")
        logger.info(f"Access Key: {ak}")
        logger.debug(f"Secret Key: {sk}")
        logger.info("Use Environment variables as credentials")
        return work_region, boto3.Session(
            aws_access_key_id=ak,
            aws_secret_access_key=sk,
            region_name=work_region
        )
