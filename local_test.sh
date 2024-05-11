curl -X POST \
  http://localhost:5000/suggest \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
  -d @- <<EOF
{
  "input": "叶筱玮是谁"
}
EOF
