import json

import boto3

from src.utils.config import load_config


def get_bedrock_client():
    """Create a Bedrock Runtime client using the configured AWS region."""

    config = load_config()

    return boto3.client(
        "bedrock-runtime",
        region_name=config["aws"]["region"],
    )


def invoke_bedrock(prompt: str) -> str:
    """Send a prompt to Amazon Nova Lite and return the response text."""

    client = get_bedrock_client()

    response = client.converse(
        modelId="amazon.nova-lite-v1:0",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt,
                    }
                ],
            }
        ],
        inferenceConfig={
            "maxTokens": 1000,
            "temperature": 0.2,
        },
    )

    return response["output"]["message"]["content"][0]["text"]