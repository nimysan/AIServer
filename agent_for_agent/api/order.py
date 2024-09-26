from flask import Blueprint, request, jsonify
import logging
from mock_data import order_logs_data

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

order_endpoint = Blueprint('order_endpoint', __name__)

# 模拟的订单数据库
orders = {
    'ORD12345': {'status': 'Active', 'customer': 'John Doe'},
    'ORD67890': {'status': 'Shipped', 'customer': 'Jane Smith'},
}


@order_endpoint.route('/cancel', methods=['POST'])
def cancel_order():
    logger.info('------->Received order cancellation request')
    data = request.json
    order_number = data.get('order_number')
    from_requester = data.get('from_requester')

    # 验证输入
    if not order_number or not from_requester:
        logger.warning('Missing required parameters')
        return jsonify({
            'code': 400,
            'message': {'error': 'Missing required parameters'}
        }), 400

    logger.info(f'Attempting to cancel order: {order_number}')

    # 检查订单是否存在
    if order_number not in orders:
        logger.warning(f'Order not found: {order_number}')
        return jsonify({
            'code': 404,
            'message': {'error': 'Order not found'}
        }), 404

    # 检查订单状态
    if orders[order_number]['status'] == 'Shipped':
        logger.warning(f'Cannot cancel shipped order: {order_number}')
        return jsonify({
            'code': 400,
            'message': {'error': 'Cannot cancel shipped order'}
        }), 400

    # 模拟取消订单
    orders[order_number]['status'] = 'Cancelled'
    logger.info(f'Order cancelled successfully: {order_number}')

    return jsonify({
        'code': 200,
        'message': {
            'success': True,
            'order_number': order_number,
            'status': 'Cancelled',
            'cancelled_by': from_requester
        }
    }), 200


@order_endpoint.route('/logistics', methods=['POST'])
def get_order_logistics():
    logger.info('------->get_order_logistics cancellation request')
    data = request.json
    order_number = data.get('order_number')
    if not order_number:
        return jsonify({

            'code': 400,

            'message': {'error': 'Missing required parameter: order_number'}

        }), 400

    if order_number not in order_logs_data:
        return jsonify({

            'code': 404,

            'message': {'error': 'Order not found'}

        }), 404

    order_info = order_logs_data[order_number]

    return jsonify({

        'code': 200,

        'message': {

            'order_number': order_number,

            'status': order_info['status'],

            'shipments': order_info['shipments']

        }

    }), 200
