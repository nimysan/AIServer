import json
import logging
import time

import boto3

import os

from botocore.client import logger
from botocore.exceptions import ClientError

from boto3_client import get_boto3_config

logger = logging.getLogger("bedrock")

# default search configuration for kb recall
default_vector_search_configuration = {
    'numberOfResults': 4,
    'overrideSearchType': 'HYBRID'
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
        self.region, boto_session = get_boto3_config()
        self.bedrock_agent_runtime = boto_session.client('bedrock-agent-runtime')
        self.bedrock_runtime = boto_session.client('bedrock-runtime')

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
        model_id = bedrock_sonnet_model_id

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

    def refineQuestion(self, question):
        refine_question = question
        if len(question) >= 900:
            summary_response = self.invoke_claude_3_with_text(
                f"Compress the following content about Jackery customer service inquiries into a 800-character response, without including any explanatory phrases. Just provide the condensed content directly. content is:{question}");
            # print(summary_response)
            refine_question = summary_response['content'][0]['text']
            # print(f"---------->{refine_question}")
        return refine_question;

    def ask_knowledge_base(self, question, knowledge_base_id, vector_search_filter=None,
                           vector_search_configuration=default_vector_search_configuration,
                           prompt_template=default_prompt_template):
        start_time = time.time()
        refine_question = self.refineQuestion(question)
        model_id = bedrock_sonnet_model_id
        model_arn = f'arn:aws:bedrock:{self.region}::foundation-model/{model_id}'

        search_config = default_vector_search_configuration
        if vector_search_filter and len(vector_search_filter) > 0:
            search_config = default_vector_search_configuration.copy()
            search_config['filter'] = vector_search_filter

        # search_config.update(filter)
        logger.info(f"vector_search_configuration {search_config}")

        response = self.bedrock_agent_runtime.retrieve_and_generate(
            input={
                'text': refine_question
            },
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'generationConfiguration': {
                        'promptTemplate': {
                            'textPromptTemplate': prompt_template
                        }
                    },
                    'knowledgeBaseId': knowledge_base_id,
                    'modelArn': model_arn,
                    'retrievalConfiguration': {
                        'vectorSearchConfiguration': search_config
                    }
                }
            }
        )
        end_time = time.time()  # 记录函数执行结束的时间
        execution_time = end_time - start_time  # 计算函数执行时间
        return {
            'cost_time': execution_time,
            'response': response,
            'prompt': prompt_template
        }
