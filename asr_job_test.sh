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
  http://localhost:5000/api/asr/asr_result \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic YWRtaW46KGBnSHBOfjI=" \
  -d @- <<EOF
{
"job_name": "test-a"
}
EOF