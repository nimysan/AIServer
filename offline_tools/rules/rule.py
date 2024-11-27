rules = {
    "modify_delivery_address": {
        "Shipped": {
            "true": {
                "Shopify": {
                    "rule_for_handle": "该订单已发货，无法处理",
                    "customer_reply_rule": "该订单已发货，请联系物流公司确认，提供该订单物流单号",
                    "agent_action": "无需处理",
                    "target_ticket_status": "solved"
                },
                "Others": {
                    "rule_for_handle": "该订单已发货，无法处理",
                    "customer_reply_rule": "该订单已发货，请联系物流公司确认，提供该订单物流单号",
                    "agent_action": "无需处理",
                    "target_ticket_status": "solved"
                }
            },
            "false": {
                "Shopify": {
                    "rule_for_handle": "该订单已发货，无法处理",
                    "customer_reply_rule": "该订单已发货，请联系物流公司确认，提供该订单物流单号",
                    "agent_action": "无需处理",
                    "target_ticket_status": "solved"
                },
                "Others": {
                    "rule_for_handle": "该订单已发货，无法处理",
                    "customer_reply_rule": "该订单已发货，请联系物流公司确认，提供该订单物流单号",
                    "agent_action": "无需处理",
                    "target_ticket_status": "solved"
                }
            }
        },
        "Pending": {
            "true": {
                "Shopify": {
                    "rule_for_handle": "1.如果用户提及了要修改的地址、姓名或者电话号码,尝试拦截订单\n2.如果未提及要修改的信息，仅需跟用户确认，无需拦截订单",
                    "customer_reply_rule": "1.我们尝试拦截订单，但是拦截失败(Failed Interception)，我们无法修改配送地址，请联系物流公司确认，提供该订单物流单号\n2.我们正在尝试拦截订单（Not Intercepted、Intercepting、Partial Success、Successful Interception），请等待客服处理",
                    "agent_action": "1.订单拦截失败、无需处理\n2.请确认订单拦截结果，并跟进处理",
                    "target_ticket_status": "1.solved\n2.open"
                },
                "Others": {
                    "rule_for_handle": "1.如果用户提及了要修改的地址、姓名或者电话号码,尝试拦截订单\n2.如果未提及要修改的信息，仅需跟用户确认，无需拦截订单",
                    "customer_reply_rule": "1.我们尝试拦截订单，但是拦截失败(Failed Interception)，我们无法修改配送地址，请联系物流公司确认，提供该订单物流单号\n2.我们正在尝试拦截订单（Not Intercepted、Intercepting、Partial Success、Successful Interception），请等待客服处理",
                    "agent_action": "1.订单拦截失败、无需处理\n2.请确认订单拦截结果，并跟进处理",
                    "target_ticket_status": "1.solved\n2.open"
                }
            },
            "false": {
                "Shopify": {
                    "rule_for_handle": "1.如果用户提及了要修改的地址、姓名或者电话号码,尝试拦截订单\n2.如果未提及要修改的信息，仅需跟用户确认，无需拦截订单",
                    "customer_reply_rule": "1.我们尝试拦截订单，但是拦截失败(Failed Interception)，我们无法修改配送地址，请联系物流公司确认，提供该订单物流单号\n2.我们正在尝试拦截订单（Not Intercepted、Intercepting、Partial Success、Successful Interception），请等待客服处理",
                    "agent_action": "1.订单拦截失败、无需处理\n2.请确认订单拦截结果，并跟进处理",
                    "target_ticket_status": "1.solved\n2.open"
                },
                "Others": {
                    "rule_for_handle": "1.如果用户提及了要修改的地址、姓名或者电话号码,尝试拦截订单\n2.如果未提及要修改的信息，仅需跟用户确认，无需拦截订单",
                    "customer_reply_rule": "1.我们尝试拦截订单，但是拦截失败(Failed Interception)，我们无法修改配送地址，请联系物流公司确认，提供该订单物流单号\n2.我们正在尝试拦截订单（Not Intercepted、Intercepting、Partial Success、Successful Interception），请等待客服处理",
                    "agent_action": "1.订单拦截失败、无需处理\n2.请确认订单拦截结果，并跟进处理",
                    "target_ticket_status": "1.solved\n2.open"
                }
            }
        },
        "Awaiting Allocation": {
            "true": {
                "Shopify": {
                    "rule_for_handle": "1.如果用户提及了要修改的地址、姓名或者电话号码,尝试拦截订单\n2.如果未提及要修改的信息，仅需跟用户确认，无需拦截订单",
                    "customer_reply_rule": "1.我们尝试拦截订单，但是拦截失败(Failed Interception)，我们无法修改配送地址，请联系物流公司确认，提供该订单物流单号\n2.我们正在尝试拦截订单（Not Intercepted、Intercepting、Partial Success、Successful Interception），请等待客服处理",
                    "agent_action": "1.订单拦截失败、无需处理\n2.请确认订单拦截结果，并跟进处理",
                    "target_ticket_status": "1.solved\n2.open"
                },
                "Others": {
                    "rule_for_handle": "1.如果用户提及了要修改的地址、姓名或者电话号码,尝试拦截订单\n2.如果未提及要修改的信息，仅需跟用户确认，无需拦截订单",
                    "customer_reply_rule": "1.我们尝试拦截订单，但是拦截失败(Failed Interception)，我们无法修改配送地址，请联系物流公司确认，提供该订单物流单号\n2.我们正在尝试拦截订单（Not Intercepted、Intercepting、Partial Success、Successful Interception），请等待客服处理",
                    "agent_action": "1.订单拦截失败、无需处理\n2.请确认订单拦截结果，并跟进处理",
                    "target_ticket_status": "1.solved\n2.open"
                }
            },
            "false": {
                "Shopify": {
                    "rule_for_handle": "1.如果用户提及了要修改的地址、姓名或者电话号码,尝试拦截订单\n2.如果未提及要修改的信息，仅需跟用户确认，无需拦截订单",
                    "customer_reply_rule": "1.我们尝试拦截订单，但是拦截失败(Failed Interception)，我们无法修改配送地址，请联系物流公司确认，提供该订单物流单号\n2.我们正在尝试拦截订单（Not Intercepted、Intercepting、Partial Success、Successful Interception），请等待客服处理",
                    "agent_action": "1.订单拦截失败、无需处理\n2.请确认订单拦截结果，并跟进处理",
                    "target_ticket_status": "1.solved\n2.open"
                },
                "Others": {
                    "rule_for_handle": "1.如果用户提及了要修改的地址、姓名或者电话号码,尝试拦截订单\n2.如果未提及要修改的信息，仅需跟用户确认，无需拦截订单",
                    "customer_reply_rule": "1.我们尝试拦截订单，但是拦截失败(Failed Interception)，我们无法修改配送地址，请联系物流公司确认，提供该订单物流单号\n2.我们正在尝试拦截订单（Not Intercepted、Intercepting、Partial Success、Successful Interception），请等待客服处理",
                    "agent_action": "1.订单拦截失败、无需处理\n2.请确认订单拦截结果，并跟进处理",
                    "target_ticket_status": "1.solved\n2.open"
                }
            }
        },
        "Ready to Ship": {
            "true": {
                "Shopify": {
                    "rule_for_handle": """
                        1. 确认是否有明确待修改的地址 2. 拦截订单 
                    """,
                    "customer_reply_rule": "确认地址->拦截订单->交由人工坐席处理 1.我们尝试拦截订单，但是拦截失败(Failed Interception)，我们无法修改配送地址，请联系物流公司确认，提供该订单物流单号\n2.我们正在尝试拦截订单（Not Intercepted、Intercepting、Partial Success、Successful Interception），请等待客服处理",
                    "agent_action": "1.订单拦截失败、无需处理\n2.请确认订单拦截结果，并跟进处理",
                    "target_ticket_status": "1.solved\n2.open"
                },
                "Others": {
                    "rule_for_handle": "1.如果用户提及了要修改的地址、姓名或者电话号码,尝试拦截订单\n2.如果未提及要修改的信息，仅需跟用户确认，无需拦截订单",
                    "customer_reply_rule": "1.我们尝试拦截订单，但是拦截失败(Failed Interception)，我们无法修改配送地址，请联系物流公司确认，提供该订单物流单号\n2.我们正在尝试拦截订单（Not Intercepted、Intercepting、Partial Success、Successful Interception），请等待客服处理",
                    "agent_action": "1.订单拦截失败、无需处理\n2.请确认订单拦截结果，并跟进处理",
                    "target_ticket_status": "1.solved\n2.open"
                }
            },
            "false": {
                "Shopify": {
                    "rule_for_handle": "1.如果用户提及了要修改的地址、姓名或者电话号码,尝试拦截订单\n2.如果未提及要修改的信息，仅需跟用户确认，无需拦截订单",
                    "customer_reply_rule": "1.我们尝试拦截订单，但是拦截失败(Failed Interception)，我们无法修改配送地址，请联系物流公司确认，提供该订单物流单号\n2.我们正在尝试拦截订单（Not Intercepted、Intercepting、Partial Success、Successful Interception），请等待客服处理",
                    "agent_action": "1.订单拦截失败、无需处理\n2.请确认订单拦截结果，并跟进处理",
                    "target_ticket_status": "1.solved\n2.open"
                },
                "Others": {
                    "rule_for_handle": "1.如果用户提及了要修改的地址、姓名或者电话号码,尝试拦截订单\n2.如果未提及要修改的信息，仅需跟用户确认，无需拦截订单",
                    "customer_reply_rule": "1.我们尝试拦截订单，但是拦截失败(Failed Interception)，我们无法修改配送地址，请联系物流公司确认，提供该订单物流单号\n2.我们正在尝试拦截订单（Not Intercepted、Intercepting、Partial Success、Successful Interception），请等待客服处理",
                    "agent_action": "1.订单拦截失败、无需处理\n2.请确认订单拦截结果，并跟进处理",
                    "target_ticket_status": "1.solved\n2.open"
                }
            }
        }
    }
}
#通用规则
def get_rule_by_order_status(order_status):
    rules = {
        'Untransferred': {
            'rule_for_handle': '不处理',
            'customer_reply_rule': '订单尚未处理,请耐心等待',
            'agent_action': '订单尚未处理,不需要采取任何行动',
            'target_ticket_status': 'Open',
            'ticket_label': 'ai-auto-require-hum'
        },
        'Cancelled': {
            'rule_for_handle': '无法处理',
            'customer_reply_rule': '订单已取消,无法处理',
            'agent_action': '订单已取消,无需进一步操作',
            'target_ticket_status': 'solved',
            'ticket_label': 'ai-auto-solved'
        },
        'Not_mentioned': {
            'rule_for_handle': '无法处理',
            'customer_reply_rule': '请提供订单号,以便我们协助处理',
            'agent_action': '无法确认订单状态,请联系客户获取更多信息',
            'target_ticket_status': 'solved',
            'ticket_label': 'ai-auto-solved'
        },
        'Not_found': {
            'rule_for_handle': '无法处理',
            'customer_reply_rule': '请提供订单号,以便我们协助处理',
            'agent_action': '无法确认订单状态,请联系客户获取更多信息',
            'target_ticket_status': 'solved',
            'ticket_label': 'ai-auto-solved'
        }
    }

    if order_status in rules:
        return rules[order_status]

def get_rule(intent, order_status, order_channel, is_pre_sales_order):
    try:
        return rules[intent][order_status][is_pre_sales_order][order_channel]
    except KeyError:
        return {
            'rule_for_handle': 'No matching rule found',
            'customer_reply_rule': None,
            'agent_action': None,
            'target_ticket_status': None
        }


def main(intent: str,
         order_status: str,
         is_pre_sales_order: str,
         order_channel: str) -> dict:
    rule = get_rule_by_order_status(order_status)
    if rule is None:
        rule = get_rule(intent, order_status, order_channel, is_pre_sales_order)
        no_rule = str(rule['rule_for_handle'] == 'No matching rule found')
    else:
        no_rule = str(rule['rule_for_handle'] == 'No matching rule found')

    return {
        'rule': rule,  # Object
        'no_rule': no_rule  # String
    }


rule = main("modify_delivery_address","awaiting_shipment","true","Shopify")
print(rule)
