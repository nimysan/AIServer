import logging

from flask import current_app

from model.behavior_log import OpenSearchBehaviorLogRepository
from model.user import UserRepository

print("--------------> model package initialize -------------->")
logger = logging.getLogger(__name__)

user_repository = None


def get_user_repository(refresh=False):
    global user_repository;
    work_region = current_app.config["REGION"]
    if refresh:
        user_repository = None;

    if user_repository is None:
        user_repository = UserRepository(work_region)


    return user_repository;


def init_model_access():
    # print(current_app)
    global user_repository;
    opener_host = current_app.config["OPENSEARCH_HOST"]
    logger.info(f"behavior logs host is: {opener_host}")
    behavior_log_repository = OpenSearchBehaviorLogRepository(opener_host)

    work_region = current_app.config["REGION"]
    # bedrock_client = load_bedrock_client(region=work_region)
    user_repository = UserRepository(work_region)

    return [behavior_log_repository, user_repository]

# __all__ = init_model_access()
