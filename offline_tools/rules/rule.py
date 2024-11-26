rules = {
    'modify_order_item_details': {
        'not_converted': {
            'shopify': {'rule': '该订单未支付或者预售订单,请等待客服处理', 'next_ticket_status': 'open'},
            'others': {'rule': '该订单未支付或者预售订单,请等待客服处理', 'next_ticket_status': 'open'}
        },
        'canceled': {
            'shopify': {'rule': '订单已取消,不支持处理', 'next_ticket_status': 'solved'},
            'others': {'rule': '订单已取消,不支持处理', 'next_ticket_status': 'solved'}
        }
    },
    'increase_order_item_quantity': {
        'pending': {
            'shopify': {'rule': '可尝试联系shopify单后重新下单', 'next_ticket_status': 'solved'},
            'others': {'rule': '不支持处理', 'next_ticket_status': 'solved'}
        }
    },
    'modify_payment_method': {
        'pending': {
            'shopify': {'rule': 'Shopify订单可尝试联系订单员#Shopify订单不支持任何操作',
                        'next_ticket_status': 'solved'},
            'others': {'rule': '可尝试控制订单后人工修改', 'next_ticket_status': 'solved'}
        },
        'awaiting_shipment': {
            'shopify': {'rule': '建议取消后重新下单', 'next_ticket_status': 'solved'},
            'others': {'rule': '不可做任何操作', 'next_ticket_status': 'solved'}
        }
    },
    'modify_delivery_address': {
        'pending': {
            'shopify': {'rule': 'Shopify订单可尝试联系订单员#Shopify订单不支持任何操作',
                        'next_ticket_status': 'solved'},
            'others': {'rule': '可尝试控制订单后人工修改', 'next_ticket_status': 'solved'}
        },
        'awaiting_shipment': {
            'shopify': {'rule': '获取用户新地址， 拦截订单，根据拦截订单状态回复客户', 'next_ticket_status': 'solved'},
            'others': {'rule': '获取用户新地址， 拦截订单，根据拦截订单状态回复客户', 'next_ticket_status': 'solved'}
        }
    },
    'modify_delivery_time': {
        'pending': {
            'shopify': {'rule': 'Shopify订单可尝试联系订单员#Shopify订单不支持任何操作',
                        'next_ticket_status': 'solved'},
            'others': {'rule': '可尝试控制订单后人工修改', 'next_ticket_status': 'solved'}
        }
    },
    'decrease_order_item_quantity': {
        'canceled': {
            'shopify': {'rule': '订单已终极,提供物流信息,建议用户自行联系物流公司', 'next_ticket_status': 'solved'},
            'others': {'rule': '订单已终极,提供物流信息,建议用户自行联系物流公司', 'next_ticket_status': 'solved'}
        }
    }
}


def get_rule(intent, order_status, order_channel):
    if intent in rules and order_status in rules[intent] and order_channel in rules[intent][order_status]:
        return rules[intent][order_status][order_channel]
    else:
        return {
            "rule": "no matched rule",
            "next_ticket_status": "open"
        }


def main(intent: str, status: str, order_channel: str) -> dict:
    return {
        'rule': get_rule(intent, status, order_channel)
    }
