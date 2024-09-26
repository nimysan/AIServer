# 模拟订单数据

order_logs_data = {

    'JP-123-123-123': {

        'status': 'Partially Shipped',

        'shipments': [

            {

                'tracking_number': 'S231231412412414',

                'carrier': 'Yamato Transport',

                'status': 'In Transit',

                'estimated_delivery': (datetime.now() + timedelta(days=2)).isoformat(),

                'tracking_url': 'https://tracking.yamato-transport.com/jizen/servlet/tracking?number=S231231412412414'

            },

            {

                'tracking_number': 'S3123123123',

                'carrier': 'Sagawa Express',

                'status': 'Shipped',

                'estimated_delivery': (datetime.now() + timedelta(days=3)).isoformat(),

                'tracking_url': 'https://k2k.sagawa-exp.co.jp/p/sagawa/web/okurijosearch.jsp?okurijoNo=S3123123123'

            }

        ]

    },

    'JP-124-124-124': {

        'status': 'Shipped',

        'shipments': [

            {

                'tracking_number': 'JTXKSDF',

                'carrier': 'Japan Post',

                'status': 'Out for Delivery',

                'estimated_delivery': (datetime.now() + timedelta(days=1)).isoformat(),

                'tracking_url': 'https://trackings.post.japanpost.jp/services/srv/search/?requestNo=JTXKSDF'

            }

        ]

    }

}
