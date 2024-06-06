import base64
import logging
import secrets
import string
import time
import uuid

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from boto3_client import get_boto3_config

logger = logging.getLogger(__name__)


class User:
    def __init__(self, userid, username, password):
        self.userid = userid
        self.username = username
        self.password = password

    def __repr__(self):
        return f"User(userid='{self.userid}', username='{self.username}', password='{self.password}')"

    def check_password_complexity(self):
        # 实现密码复杂性检查逻辑
        # ...
        pass


def generate_password(length=12):
    """
    生成指定长度的随机密码,包含大小写字母、数字和特殊字符
    """
    # 定义所有可能的字符
    characters = string.ascii_letters + string.digits + string.punctuation

    # 选择指定长度的随机字符
    return ''.join(secrets.choice(characters) for _ in range(length))

def print_base64_credentials(username, password, surrounding_char='*'):
    """
    打印用户名和密码的Base64编码值，并用指定的字符环绕。

    Args:
        username (str): 用户名
        password (str): 密码
        surrounding_char (str, optional): 环绕字符，默认为 '*'

    Returns:
        None
    """
    # 将用户名和密码连接成 'username:password' 格式
    credentials = f"{username}:{password}"

    # 使用 Base64 编码
    base64_credentials = base64.b64encode(credentials.encode()).decode()

    # 将编码后的值用指定字符环绕并打印
    surrounded_base64_credentials = f"{surrounding_char}{base64_credentials}{surrounding_char}"
    logger.info(surrounded_base64_credentials)
    logger.info(f"***** password ***** {password} ***** password *****")
    return base64_credentials;

class UserRepository:
    def __init__(self, region, user_table_name="ai_users"):
        self.region, boto_session = get_boto3_config(region)
        self.dynamodb = boto_session.resource('dynamodb', region_name=region)
        self.create_user_table(user_table_name)
        self.user_table = self.dynamodb.Table(user_table_name)
        # self.create_default_admin_user()

    def initialize_default_admin_user(self):
        item = self.load_user_by_userid("1");
        # logger.info(f"----- >  admin user is {item}")
        if not item:
            password = generate_password(8)
            self.create_user("1", "admin", password);
        item = self.load_user_by_userid("1");
        print_base64_credentials(item['userName'], item['password'],"******** api authentication token!!! ******")

    def create_user_table(self, user_table_name):
        # 检查表是否存在
        table = self.dynamodb.Table(user_table_name)
        try:
            table.load()
            logger.info(f"Table '{user_table_name}' already exists.")
            # 检查是否已经存在 userName 索引
            existing_indexes = [index.get('IndexName') for index in table.global_secondary_indexes or []]
            if 'userName-index' not in existing_indexes:
                logger.info("Creating 'userName-index' global secondary index.")
                table.update(
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'userName',
                            'AttributeType': 'S'
                        }
                    ],
                    GlobalSecondaryIndexUpdates=[
                        {
                            'Create': {
                                'IndexName': 'userName-index',
                                'KeySchema': [
                                    {
                                        'AttributeName': 'userName',
                                        'KeyType': 'HASH'
                                    }
                                ],
                                'Projection': {
                                    'ProjectionType': 'ALL'
                                },
                                'ProvisionedThroughput': {
                                    'ReadCapacityUnits': 5,
                                    'WriteCapacityUnits': 5
                                }
                            }
                        }
                    ]
                )
            else:
                logger.info("'userName-index' global secondary index already exists.")
        except self.dynamodb.meta.client.exceptions.ResourceNotFoundException:
            logger.info(f"Creating table '{user_table_name}'.")
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
                    },
                    {
                        'AttributeName': 'userName',
                        'AttributeType': 'S'  # String type
                    }
                ],
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'userName-index',
                        'KeySchema': [
                            {
                                'AttributeName': 'userName',
                                'KeyType': 'HASH'
                            }
                        ],
                        'Projection': {
                            'ProjectionType': 'ALL'
                        },
                        'ProvisionedThroughput': {
                            'ReadCapacityUnits': 5,
                            'WriteCapacityUnits': 5
                        }
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            logger.info(f"Table created: {table}")

    # 创建用户
    def create_user(self, user_id, username, password, profile=None):
        try:
            if user_id is None:
                user_id = str(uuid.uuid4())
            current_time = int(time.time())  # 获取当前时间戳
            self.user_table.put_item(
                Item={
                    'userId': user_id,
                    'userName': username,
                    'password': password,
                    'profile': profile,
                    'created_at': current_time  # 添加创建时间戳
                }
            )
            logger.info(f"User created: {user_id}")
        except ClientError as e:
            logger.info(e.response['Error']['Message'])
            raise e

    def load_user_by_userid(self, user_id):
        try:
            response = self.user_table.query(
                KeyConditionExpression=Key('userId').eq(user_id)
            )
            if response['Items']:
                user = response['Items'][0]
                return user
            else:
                logger.warning(f"User with ID '{user_id}' not found.")
                return None
        except Exception as e:
            logger.error(f"Error loading user with ID '{user_id}': {e}")
            raise e

    # 根据用户名加载用户
    def load_user_by_username(self, username):
        try:
            response = self.user_table.query(
                IndexName='userName-index',  # 假设已创建了一个名为 'UsernameIndex' 的全局二级索引
                KeyConditionExpression=Key('userName').eq(username)
            )
            if response['Items']:
                return response['Items'][0]
            else:
                return None
        except ClientError as e:
            logger.info(e.response['Error']['Message'])
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
