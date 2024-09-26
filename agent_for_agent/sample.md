# Test user case and data

## 查询物流

### 查询物流-订单号存在 ---
Hello, I'd like to know when my order will arrive?  Order number: JP-123-123-123

### Agent Response -----
Dear customer,

Thank you for your inquiry. I've looked up the details for your order JP-123-123-123. According to the information, your order is currently partially shipped through two different carriers:

1. The first shipment is being handled by Yamato Transport with tracking number S231231412412414. It is currently in transit and estimated to be delivered on 2024-09-28.

2. The second shipment is being handled by Sagawa Express with tracking number S3123123123. This shipment has been shipped and is estimated to be delivered on 2024-09-29.

You can track the shipments using the tracking URLs provided:

Yamato Transport: https://tracking.yamato-transport.com/jizen/servlet/tracking?number=S231231412412414
Sagawa Express: https://k2k.sagawa-exp.co.jp/p/sagawa/web/okurijosearch.jsp?okurijoNo=S3123123123

Please let me know if you need any other assistance regarding your order.

Best regards,
[Your name]


### 查询物流-订单号不存在 ---
Hello, I'd like to know when my order will arrive?  Order number: 114-3614528-8765807

### Agent Response:
Dear customer, thank you for your inquiry about your order. Unfortunately, I could not find any order with the number JP-123-123-4344 in our system. Please double check the order number and provide the correct one so that I can look up the logistics details and delivery status for you. I'd be happy to assist further once I have the right order information.


## multiple language

### 查询物流 日语 ---

より丁寧な場合:
    大変恐れ入りますが、...
すみません、注文した商品の到着予定を教えていただけますでしょうか。
注文番号は114-3614528-8765807です。

### Agent return:

申し訳ありませんが、注文番号 JP-123-123-123 の商品は複数の荷物に分けて出荷されています。 

最初の荷物はヤマト運輸で配送中で、追跡番号は S231231412412414 です。このお荷物の配達予定日は2024年9月28日となっています。

2つ目の荷物はサガワ急便で出荷済みで、追跡番号は S3123123123 です。この荷物の配達予定日は2024年9月29日となっています。

配送業者の追跡サイトから現在の配送状況をご確認いただけます。ご不便をおかけして申し訳ございません。商品の到着をお待ちいただけますと幸いです。
