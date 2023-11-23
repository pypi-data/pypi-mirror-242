import boto3
import uuid
import json
from datetime import datetime

from .settings import settings
from .encoder import ComplexEncoder

dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_REGION)

def _create_dynamodb_table(table_name=None):
    """_summary_

    Args:
        table_name (str, optional): create dynamo table.
    """
    # Auto Table Name
    if not table_name:
        table_name = f'module-{settings.ENVIRONMENT}'
    # Check if the table already exists
    existing_tables = dynamodb.meta.client.list_tables()['TableNames']
    
    if table_name not in existing_tables:
        # Table does not exist, create it
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'  # String
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        # Wait until the table exists
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

        print(f"Table '{table_name}' created successfully.")
    else:
        print(f"Table '{table_name}' already exists.")
    return table_name

def _get_dynamo_item_by_id(table_name=None, id=None):
    """_summary_

    Args:
        table_name (str): table name of dynamo
        id (str): key of item

    Returns:
        Any: dynamo item
    """
    # Auto Table Name
    if not table_name:
        table_name = f'module-{settings.ENVIRONMENT}'
    if not id:
        id = settings.ID
    # Get a reference to the table
    table = dynamodb.Table(table_name)

    # Use get_item to retrieve the item
    response = table.get_item(
        Key={
            'id': id
        }
    )

    # Check if the item was found
    if 'Item' in response:
        item = response['Item']
        return item
    else:
        print("Item not found.")
        return None

def _register_module(module_name, input_data=None, table_name=None):
    """_summary_

    Args:
        module_name (string): specify moduel name. Required
        input_data (string, dict, optional): specify input data parameter. Defaults to None.
        table_name (string, optional): table name of dynamo. Defaults to None.

    Returns:
        string: unique id of module
    """
    # Auto Table Name
    if not table_name:
        table_name = f'module-{settings.ENVIRONMENT}'

    # Get a reference to the table
    table = dynamodb.Table(table_name)

    # Generate a unique ID
    unique_id = str(uuid.uuid4())

    # Add the unique ID to the data
    data_to_insert = {
        'id': unique_id,
        'module_name': module_name,
        'created_at': str(datetime.now()),
        'input_data': None,
        'output_data': None,
        'started_at': None,
        'completed_at': None
    }

    # Add input data
    if input_data:
        if (type(input_data) == str):
            data_to_insert['input_data'] = input_data
        else:
            try:
                data_to_insert['input_data'] = json.dumps(input_data, cls=ComplexEncoder)
            except Exception as err:
                raise ValueError(f"Value must be string or jsonable type. ({err})")

    # Send data to DynamoDB
    response = table.put_item(Item=data_to_insert)

    # Print the response or handle as needed
    print("Put Module succeeded:", response)

    # Return the unique ID for reference
    return unique_id

def _put_value(column, value, table_name=None, id=None):
    # Auto Table Name
    if not table_name:
        table_name = f'module-{settings.ENVIRONMENT}'
    if not id:
        id = settings.ID

    # Specify the table name
    table = dynamodb.Table(table_name)

    # Define the key of the item to be updated
    key = {"id": id}
    if type(value) == datetime:
        value = str(value)
    # Define the update expression and attribute values
    update_expression = "SET " + column + " = :value"
    expression_attribute_values = {":value": value}

    # Update the item
    table.update_item(
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )

def _save_output(output_data, table_name=None, id=None):
    # Auto Table Name
    if not table_name:
        table_name = f'module-{settings.ENVIRONMENT}'
    if not id:
        id = settings.ID

    # Specify the table name
    table = dynamodb.Table(table_name)

    # Define the key of the item to be updated
    key = {"id": id}

    value = None
    # Add input data
    if output_data:
        if (type(output_data) == str):
             value = output_data
        else:
            try:
                value = json.dumps(output_data, cls=ComplexEncoder)
            except Exception as err:
                raise ValueError(f"Value must be string or jsonable type. ({err})")
    # Define the update expression and attribute values
    update_expression = "SET output_data = :value"
    expression_attribute_values = {":value": value}

    # Update the item
    table.update_item(
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )