curl -X POST \
  http://localhost:5000/api/bedrock/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=x" \
  -d @- <<EOF
{
  "input": "叶筱玮是谁"
}
EOF
