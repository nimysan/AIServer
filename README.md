# Amazon Bedrock Knowledge base hosting server

## how to deploy?

[Download yaml template and upload as CloudFormation](./cloudformation/template.yaml)

Get the url from Stack output and copy it to browser

## how to run?

```bash
export ACCESS_KEY=xxx
export SECRET_KEY=xxx
./start_server.sh
```

## Access

http://localhost:5000¬

>
我们如何解决不同语言不同地区的知识库的差异？  [采用metadata和filter来区分](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-ds.html#kb-ds-metadata)

## Frontend

[Static Export方式部署前端](https://nextjs.org/docs/app/building-your-application/deploying/static-exports)

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

## Trace

```bash
# 启动jaeger
docker run -d --name jaeger \
    -e COLLECTOR_ZIPKIN_HTTP_PORT=9411 \
    -p 5775:5775/udp \
    -p 6831:6831/udp \
    -p 6832:6832/udp \
    -p 5778:5778 \
    -p 16686:16686 \
    -p 14268:14268 \
    -p 9411:9411 \
    jaegertracing/all-in-one:latest
    

```

访问UI: http://localhost:16686/search    

## deploy frontend pages

https://blog.miguelgrinberg.com/post/how-to-deploy-a-react--flask-project

```bash
https://blog.miguelgrinberg.com/post/how-to-deploy-a-react--flask-project
```