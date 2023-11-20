import boto3
import json
from botocore.exceptions import NoCredentialsError
from datetime import datetime


from .settings import settings

client = boto3.client(
    'secretsmanager',
    region_name=settings.AWS_REGION
)

def _retrieve_config():
    secret_name = 'module-config'
    # Create a Secrets Manager client
    try:
        # Get the secret value
        response = client.get_secret_value(SecretId=secret_name)

        # Your secret is in the response dictionary
        secret_value = response['SecretString']
        return secret_value

    except NoCredentialsError:
        print("Credentials not available")
        # Handle the exception here, e.g., raise an error or log a message
        return None

def _get_env_config():
    config_value = json.loads(_retrieve_config())
    if settings.ENVIRONMENT == 'local':
        prefix = 'dev'
    else:
        prefix = settings.ENVIRONMENT
    cluster = config_value[f"{prefix}-cluster"]
    subnets = json.loads(config_value[f"{prefix}-subnets"])
    taskdef = f"python-module-{prefix}"
    return {"cluster": cluster, "subnets": subnets, "taskdef": taskdef}
