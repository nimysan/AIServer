curl -X POST \
  http://localhost:5000/api/bedrock/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic YWRtaW46KGBnSHBOfjI=" \
  -d @- <<EOF
{
"input": "This email originated from outside of the organization. Do not click links or open attachments unless you can confirm the sender and know the content is safe.",
"ticketBrand": "8151824033807",
"ticketIntent": ""
}
EOF