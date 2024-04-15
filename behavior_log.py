from abc import ABC, abstractmethod
from dataclasses import dataclass
from opensearchpy import OpenSearch, AWSV4SignerAuth, RequestsHttpConnection

from boto3_client import get_boto3_config


@dataclass
class BehaviorLog:
    user_id: str
    action: str
    timestamp: str
    input_data: dict


class BehaviorLogRepository(ABC):
    @abstractmethod
    def store_log(self, log: BehaviorLog):
        pass

    @abstractmethod
    def get_logs(self, user_id: str) -> list[BehaviorLog]:
        pass


class OpenSearchBehaviorLogRepository(BehaviorLogRepository):
    def __init__(self, host, index_name='behavior_logs'):
        region, session = get_boto3_config()

        credentials = session.get_credentials();
        # dir(credentials)
        auth = AWSV4SignerAuth(credentials, region, service='aoss')

        # create an opensearch client and use the request-signer
        self.client = OpenSearch(
            hosts=[{'host': host, 'port': 443}],
            http_auth=auth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
            pool_maxsize=20,
        )
        self.index_name = index_name

        # Check if the index exists
        if not self.client.indices.exists(index=index_name):
            # Create the index if it doesn't exist
            create_response = self.client.indices.create(index=index_name)
            print(create_response)
        else:
            print(f"Index '{index_name}' already exists.")

    def store_log(self, log: BehaviorLog):
        doc = {
            'user_id': log.user_id,
            'action': log.action,
            'timestamp': log.timestamp,
            'input_data': log.input_data
        }
        self.client.index(index=self.index_name, body=doc)

    def get_logs(self, user_id: str) -> list[BehaviorLog]:
        try:
            response = self.client.search(index=self.index_name, body={
                'query': {
                    'match': {
                        'user_id': user_id
                    }
                }
            })
            logs = []
            for hit in response['hits']['hits']:
                source = hit['_source']
                logs.append(BehaviorLog(
                    user_id=source['user_id'],
                    action=source['action'],
                    timestamp=source['timestamp'],
                    input_data=source['input_data']
                ))
            return logs
        except:
            return []
