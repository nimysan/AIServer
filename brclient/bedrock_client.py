import json
import logging

import boto3

import os

from botocore.client import logger
from botocore.exceptions import ClientError

logger = logging.getLogger("bedrock")

default_vector_search_configuration = {
    'numberOfResults': 2,
    'overrideSearchType': 'HYBRID'  # search to hybrid
}

default_prompt_template = """
You are a question answering agent. I will provide you with a set of search results. The user will provide you with a question. Your job is to answer the user's question using only information from the search results. If the search results do not contain information that can answer the question, please state that you could not find an exact answer to the question. Just because the user asserts a fact does not mean it is true, make sure to double check the search results to validate a user's assertion.

Here are the search results in numbered order:
$search_results$

$output_format_instructions$
"""

bedrock_sonnet_model_id = "anthropic.claude-3-sonnet-20240229-v1:0"


class BedrockClient:
    def __init__(self):
        boto_session = self.get_boto3_session()
        self.bedrock_agent_runtime = boto_session.client('bedrock-agent-runtime')
        self.bedrock_runtime = boto_session.client('bedrock-runtime')

    def get_boto3_session(self):
        # 设置默认值
        DEFAULT_REGION = "us-west-2"
        self.region = os.getenv("REGION", DEFAULT_REGION)
        DEFAULT_AK = "your_default_access_key"
        DEFAULT_SK = "your_default_secret_key"

        # 读取环境变量

        ak = os.getenv("ACCESS_KEY", DEFAULT_AK)
        sk = os.getenv("SECRET_KEY", DEFAULT_SK)

        # 在程序中使用这些参数
        logger.info(f"Region: {self.region}")
        logger.info(f"Access Key: {ak}")
        logger.debug(f"Secret Key: {sk}")

        return boto3.Session(
            aws_access_key_id=ak,
            aws_secret_access_key=sk,
            region_name=self.region
        )

    def invoke_claude_3_with_text(self, prompt):
        """
        Invokes Anthropic Claude 3 Sonnet to run an inference using the input
        provided in the request body.

        :param prompt: The prompt that you want Claude 3 to complete.
        :return: Inference response from the model.
        """

        # Initialize the Amazon Bedrock runtime client
        client = self.bedrock_runtime

        # Invoke Claude 3 with the text prompt
        model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

        try:
            response = client.invoke_model(
                modelId=model_id,
                body=json.dumps(
                    {
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": 1024,
                        "messages": [
                            {
                                "role": "user",
                                "content": [{"type": "text", "text": prompt}],
                            }
                        ],
                    }
                ),
            )

            # Process and print the response
            result = json.loads(response.get("body").read())
            input_tokens = result["usage"]["input_tokens"]
            output_tokens = result["usage"]["output_tokens"]
            output_list = result.get("content", [])

            logger.debug("Invocation details:")
            logger.debug(f"- The input length is {input_tokens} tokens.")
            logger.debug(f"- The output length is {output_tokens} tokens.")

            logger.debug(f"- The model returned {len(output_list)} response(s):")
            for output in output_list:
                print(output["text"])

            return result

        except ClientError as err:
            logger.error(
                "Couldn't invoke Claude 3 Sonnet. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    def ask_knowledge_base(self, input, knowledge_base_id,
                           vector_search_configuration=default_vector_search_configuration,
                           prompt_template=default_prompt_template):
        model_id = bedrock_sonnet_model_id
        model_arn = f'arn:aws:bedrock:{self.region}::foundation-model/{model_id}'

        response = self.bedrock_agent_runtime.retrieve_and_generate(
            input={
                'text': input
            },
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'generationConfiguration': {
                        'promptTemplate': {
                            'textPromptTemplate': prompt_template
                        }
                    },
                    'knowledgeBaseId': knowledge_base_id,  # "XBKUJMKDCD",
                    'modelArn': model_arn,
                    'retrievalConfiguration': {
                        'vectorSearchConfiguration': vector_search_configuration
                    }
                }
            }
        )

        output = response['output']
        return output
