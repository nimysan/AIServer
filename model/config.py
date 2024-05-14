import logging
import time

from botocore.exceptions import ClientError
from boto3_client import get_boto3_config

logger = logging.getLogger(__name__)


def convert_dynamodb_item(item):
    result = {}
    for key, value in item.items():
        value_type = list(value.keys())[0]
        value_data = list(value.values())[0]
        if value_type == 'S':
            result[key] = value_data
        elif value_type == 'N':
            result[key] = int(value_data)
        elif value_type == 'NULL':
            result[key] = None
        # 您可以根据需要添加其他类型的处理

    # 重命名键
    obj = {
        'item_name': result.get('itemName'),
        'item_key': result.get('itemKey'),
        'item_value': result.get('itemValue'),
    }

    return obj


class ConfigItemRepository:
    def __init__(self, region, user_table_name="ai_configs"):
        self.region, boto_session = get_boto3_config(region)
        self.dynamodb = boto_session.client('dynamodb')  # # 连接DynamoDB
        self.table = user_table_name

        # 创建表
        try:
            table = self.dynamodb.create_table(
                TableName=user_table_name,
                KeySchema=[
                    {
                        'AttributeName': 'itemKey',
                        'KeyType': 'HASH'  # Partition key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'itemKey',
                        'AttributeType': 'S'  # String type
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            logger.info(f"Table created: {table}")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                logger.info("Table already exists")
            else:
                logger.info(e.response['Error']['Message'])

        dynamodb_resource = boto_session.resource("dynamodb")
        self.table_object = dynamodb_resource.Table(user_table_name)

    # 创建配置项
    def create_item(self, item_key, item_name, item_value):
        logger.info(f" {item_key}- {item_name} - {item_value}- ")
        try:
            current_time = int(time.time())  # 获取当前时间戳
            logger.info(f"The value is {item_value}")
            self.table_object.put_item(
                Item={
                    'itemKey': item_key,
                    'itemName': item_name,
                    'itemValue': item_value,
                    'created_at': current_time  # 添加创建时间戳
                }
            )
            logger.info(f"Config Item created: {item_key}")
        except ClientError as e:
            logger.info(e.response['Error']['Message'])

    def list_all(self):
        # 扫描表并获取所有项目
        response = self.dynamodb.scan(
            TableName=self.table
        )
        # 输出所有项目
        list = []
        for item in response['Items']:
            list.append(convert_dynamodb_item(item))
        return list;

    def deleteByKey(self, item_key):
        logger.debug(f"delete the key {item_key}")
        key = {'itemKey': item_key}
        response = self.table_object.delete_item(
            Key=key
        )
