curl -X POST \
  http://localhost:5000/log \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
  -d @- <<EOF
{
  "user": "AWS_TEST",
  "action":"accept",
  "input_data":{
    "ticket_id":"t1",
    "ticket_brand":"t_brand",
    "ticket_channel":"support",
    "question":"xxxxx",
    "kb_reference":{},
    "prompt_template":"elloooo"
  }
}
EOF
