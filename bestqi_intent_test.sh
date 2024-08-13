curl -X POST \
  http://localhost:5000/api/bestqi/intent \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic xxxWRtaW46KGBnSHBOfjI=" \
  -d @- <<EOF
{
  "intent_list": [
    {
      "category": "购买咨询",
      "description": "客户对于商品的价格、规格、库存等有疑问,或者询问购买流程和支付方式等相关信息。"
    },
    {
      "category": "使用咨询",
      "description": "客户已经购买了商品,对于商品的使用方法、注意事项、常见问题等有疑问。"
    },
    {
      "category": "投诉",
      "description": "客户对于购买的商品或服务存在不满意的地方,表达了负面情绪。",
      "sub_categories": [
        {
          "category": "安全投诉",
          "description": "客户认为购买的商品存在安全隐患,如产品设计或材质等方面的问题,导致人身或财产受损。"
        },
        {
          "category": "质量投诉",
          "description": "客户认为购买的商品质量不合格,如功能失常、外观缺陷、寿命过短等。"
        },
        {
          "category": "服务投诉",
          "description": "客户对于电商平台或商家的售前、售中、售后服务不满意,如态度差、响应慢、承诺未兑现等。"
        }
      ]
    }
  ],
  "customer_inquiry": "你好，我的桌子买了3天, 现在有一只腿坏掉了?"
}
EOF
