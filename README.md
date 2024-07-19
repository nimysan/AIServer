# Amazon Bedrock Knowledge base hosting server

## 功能说明

### 提供API， 对接Amazon Bedrock 和 Knowledge base for Amazon Bedrock
```bash
/api/log
/api/bedrock/rag
/api/bedrock/rag_with_rewrite
/api/bedrock/chat
/api/config
/api/config/<item_key>
/api/config
/api/asr/test
/api/asr/job
/api/asr/update_asr_job
/api/asr/asr_result

```

### 提供配置修改能力

![img.png](img.png)

### 提供测试页面
![img_1.png](img_1.png)


## 部署和启动 

> config.json 程序配置文件， 里面关联的是程序启动时候需要的region信息等， 服务启动后不可更改

### app config

> 此部分配置存在于Dynamic表中，可以修改

### how to deploy?

[Download yaml template and upload as CloudFormation](https://console.aws.amazon.com/cloudformation/home?region=us-east-1)

Get the url from Stack output and copy it to browser

### 部署成功后

> 服务启动在5000端口

1. 拿到alb的访问路径， 直接访问
2. http://{alb.domain}/api/bedrock/chat  #调用Amazon Bedrock托管的Sonnet模型

```bash
export ACCESS_KEY=xxx
export SECRET_KEY=xxx
./start_server.sh
```

### 几个本地测试的例子

```bash

## 测试访问知识库



## 从英文资料获取的答案
curl -X POST \
     http://localhost:5000/suggest \
     -H "Content-Type: application/json" \
     -H "Authorization: Basic xxxxx=" \
     -d @- << EOF
{
  "input": "购买后几天可以退货?",
  "filter": {
        "equals": {
            "key": "language",
            "value": "japanese"
        }
    }
}
EOF

# answer
{
  "result": {
    "text": "根据搜索结果,我没有找到关于这款产品的退货政策的具体信息。搜索结果主要介绍了产品的一些技术参数和特点,但没有提及退货期限。"
  }
}


## 从日语资料库获取的答案
curl -X POST \
     http://localhost:5000/suggest \
     -H "Content-Type: application/json" \
     -H "Authorization: Basic xxxxx=" \
     -d @- << EOF
{
  "input": "购买后几天可以退货?",
  "filter": {
        "equals": {
            "key": "language",
            "value": "english"
        }
    }
}
EOF
# answer
{
  "result": {
    "text": "根据搜索结果,如果您想退货,必须在收到货物后的30天内申请退货。一旦收到退货包裹,Jackery将在2-4个工作日内将款项退还至您的原始付款方式。"
  }
}




curl -X POST \
     -H "Content-Type: application/json" \
     -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
     -d '{"input": "翻译以下内容为日语：购买后几天可以退货?", "market":"Japan"}' \
     http://localhost:5000/suggest
     
     
#with prompt
curl -X POST \
     -H "Content-Type: application/json" \
     -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
     -d '{"input": "翻译以下内容为日语：购买后几天可以退货?", "market":"Japan", "prompt":"test"}' \
     http://localhost:5000/suggest

# without tempalte
curl -X POST \
     -H "Content-Type: application/json" \
     -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
     -d '{"input": "购买后几天可以退货?", "market":"Japan"}' \
     http://localhost:5000/suggest
     
# 测试直接调用模型
curl -X POST -H "Content-Type: application/json" -d '{"input": "翻译以下内容为日语：购买后几天可以退货?"}' http://localhost:5000/chat


```

### ASR Job Test

```bash
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
```