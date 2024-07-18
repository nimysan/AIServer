curl -X POST \
  http://localhost:5000/api/asr/job \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic YWRtaW46KGBnSHBOfjI=" \
  -d @- <<EOF
{
"mp4_url": "s3://aigc.red.plaza/huabao/Ticket #593149recording.mp3",
"language": "ja-JP"
}
EOF


curl -X POST \
  http://localhost:5000/api/asr/update_asr_job \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic YWRtaW46KGBnSHBOfjI=" \
  -d @- <<EOF
{
"job_name": "asr_ca4961b3-4a24-4bcb-90c5-c73d981e2000"
}
EOF


curl -X POST \
  http://localhost:5000/api/asr/update_asr_job \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic YWRtaW46KGBnSHBOfjI=" \
  -d @- <<EOF
{
"job_name": "asr_7966a124-4612-4fb9-8544-a59718c36f93"
}
EOF