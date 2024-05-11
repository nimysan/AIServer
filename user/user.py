import logging
import time
import uuid

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from boto3_client import get_boto3_config

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, region, user_table_name="ai_users"):
        self.region, boto_session = get_boto3_config(region)
        self.dynamodb = boto_session.client('dynamodb')  # # 连接DynamoDB
        self.table = user_table_name

        # 创建表
        try:
            table = self.dynamodb.create_table(
                TableName=user_table_name,
                KeySchema=[
                    {
                        'AttributeName': 'userId',
                        'KeyType': 'HASH'  # Partition key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'userId',
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

    # 创建用户
    def create_user(self, user_id, email, password, profile):
        try:
            if user_id is None:
                user_id = str(uuid.uuid4())
            current_time = int(time.time())  # 获取当前时间戳
            self.table_object.put_item(
                Item={
                    'userId': user_id,
                    'email': email,
                    'password': password,
                    'profile': profile,
                    'created_at': current_time  # 添加创建时间戳
                }
            )
            logger.info(f"User created: {user_id}")
        except ClientError as e:
            logger.info(e.response['Error']['Message'])

    # 根据用户名加载用户
    def load_user_by_username(self, username):
        try:
            response = self.table_object.query(
                IndexName='UsernameIndex',  # 假设已创建了一个名为 'UsernameIndex' 的全局二级索引
                KeyConditionExpression=Key('username').eq(username)
            )
            if response['Items']:
                return response['Items'][0]
            else:
                return None
        except ClientError as e:
            print(e.response['Error']['Message'])
            return None

    # 修改密码
    def update_password(self, user_id, new_password):
        try:
            response = self.table.update_item(
                Key={
                    'userId': user_id
                },
                UpdateExpression='SET password = :new_password',
                ExpressionAttributeValues={
                    ':new_password': new_password
                },
                ReturnValues='UPDATED_NEW'
            )
            logger.info(f"Password updated for user: {user_id}")
        except ClientError as e:
            logger.info(e.response['Error']['Message'])
