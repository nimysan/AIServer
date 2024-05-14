import logging
from datetime import datetime

from flask import (
    Blueprint, request, jsonify, current_app
)
from model.behavior_log import BehaviorLog, OpenSearchBehaviorLogRepository
from model import init_model_access

bp = Blueprint("log", __name__, url_prefix='/log')

logger = logging.getLogger(__name__)

behavior_log_repository = None


def load_behavior_log_repository(host):
    global behavior_log_repository;
    if behavior_log_repository is None:
        behavior_log_repository = OpenSearchBehaviorLogRepository(host)
    return behavior_log_repository


def clean():
    logger.info(f"Clean the repository ------><------")
    global behavior_log_repository;
    behavior_log_repository = None;


@bp.route('', methods=['POST'])
def log():
    repository = load_behavior_log_repository(
        current_app.config["OPENSEARCH_HOST"])  # when to initialize it?

    data = request.get_json()
    # logger.info(data)
    behavior_log = BehaviorLog(
        user_id=data['user'],  # 客服
        action=data['action'],  # 采纳/需优化
        timestamp=datetime.now().isoformat(),  # 时间
        input_data=data['input_data']
    )
    logger.info(f"---------> {behavior_log}")
    try:
        res = repository.store_log(behavior_log)
        return jsonify({'result': res})
    except Exception as e:
        clean()
        raise
