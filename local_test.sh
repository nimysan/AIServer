curl -X POST \
  http://localhost:5000/suggest \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
  -d @- <<EOF
{
  "input": "几天内可以退货",
  "filter": {
        "equals": {
            "key": "language",
            "value": "japanese"
        }
    }
}
EOF
