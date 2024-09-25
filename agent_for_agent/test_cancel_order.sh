#!/bin/bash

# 设置API的基础URL
BASE_URL="http://localhost:5000/api"

# 设置API endpoint和方法
API_ENDPOINT="http://localhost:5000/api/order/cancel"
HTTP_METHOD="POST"

# 设置测试数据
ORDER_NUMBER="ORD12345"
FROM_REQUESTER="customer_service"

echo "Testing Order Cancellation API..."
curl -X POST "${BASE_URL}/execute" \
     -H "Content-Type: application/json" \
     -d '{
       "api_endpoint": "'"${API_ENDPOINT}"'",
       "http_method": "'"${HTTP_METHOD}"'",
       "request_payload": {
         "order_number": "'"${ORDER_NUMBER}"'",
         "from_requester": "'"${FROM_REQUESTER}"'"
       }
     }'
#
#echo -e "\n\nTesting with missing order number..."
#curl -X POST "${BASE_URL}/execute" \
#     -H "Content-Type: application/json" \
#     -d '{
#       "api_endpoint": "'"${API_ENDPOINT}"'",
#       "http_method": "'"${HTTP_METHOD}"'",
#       "request_payload": {
#         "from_requester": "'"${FROM_REQUESTER}"'"
#       }
#     }'
#
#echo -e "\n\nTesting with missing from_requester..."
#curl -X POST "${BASE_URL}/execute" \
#     -H "Content-Type: application/json" \
#     -d '{
#       "api_endpoint": "'"${API_ENDPOINT}"'",
#       "http_method": "'"${HTTP_METHOD}"'",
#       "request_payload": {
#         "order_number": "'"${ORDER_NUMBER}"'"
#       }
#     }'
#
#echo -e "\n\nTesting with invalid HTTP method..."
#curl -X POST "${BASE_URL}/execute" \
#     -H "Content-Type: application/json" \
#     -d '{
#       "api_endpoint": "'"${API_ENDPOINT}"'",
#       "http_method": "GET",
#       "request_payload": {
#         "order_number": "'"${ORDER_NUMBER}"'",
#         "from_requester": "'"${FROM_REQUESTER}"'"
#       }
#     }'