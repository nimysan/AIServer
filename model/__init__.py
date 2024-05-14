from flask import current_app

from model.behavior_log import OpenSearchBehaviorLogRepository

print("model packge")


def init_model_access():
    print(current_app)
    behavior_log_repository = OpenSearchBehaviorLogRepository("")

    return behavior_log_repository
