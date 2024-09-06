import logging
from datetime import datetime

from flask import (
    Blueprint, request, jsonify, current_app
)

from model.behavior_log import BehaviorLog

bp = Blueprint("log", __name__, url_prefix='/log')

logger = logging.getLogger(__name__)


@bp.route('', methods=['POST'])
def log():
    repository = current_app.behavior_log_repository
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
        # clean()
        raise
