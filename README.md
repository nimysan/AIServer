# Amazon Bedrock Knowledge base hosting server

## how to run?

```bash
export ACCESS_KEY=xxx
export SECRET_KEY=xxx
./start_server.sh
```

## Access

http://localhost:5000¬

```bash

# 测试访问知识库
curl -X POST \
     -H "Content-Type: application/json" \
     -H "Authorization: Basic cccc=xxx" \
     -d '{"input": "翻译以下内容为日语：购买后几天可以退货?"}' \
     http://localhost:5000/chat
     
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