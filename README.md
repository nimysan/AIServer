# Amazon Bedrock Knowledge base hosting server

## how to run?
```bash
./start_server.sh
```

## Access

http://localhost:5000¬

```bash
curl -X POST -H "Content-Type: application/json" -d '{"input": "购买后几天可以退货?"}' http://localhost:5000/suggest
```