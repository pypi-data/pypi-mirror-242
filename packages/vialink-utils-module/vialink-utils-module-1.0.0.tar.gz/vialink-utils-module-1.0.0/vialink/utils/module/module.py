import time
from datetime import datetime


from .settings import settings
from .secret import _get_env_config
from .dynamo import _register_module, _get_dynamo_item_by_id, _create_dynamodb_table
from .ecs import _launch_ecs, _list_task

def run_module(id,  cpu, memory):
    config = _get_env_config()
    task_def = config['taskdef']
    subnets = config['subnets']
    cluster_name = config['cluster']
    task_arn = _launch_ecs(cluster_name, subnets, task_def, cpu, memory, id)
    return task_arn

def register_module(module_name, input_data):
    _create_dynamodb_table()
    id = _register_module(module_name=module_name, input_data=input_data)
    return id

def retrieve_module_output(id):
    meta_data = _get_dynamo_item_by_id(id=id)
    return meta_data['output_data']

def waiter_module(task_ids=[], interval=5):
    config = _get_env_config()
    task_def = config['taskdef']
    cluster_name = config['cluster']
    tasks = _list_task(cluster_name, task_def, filter=task_ids)
    while(len(tasks) > 0 ):
        time.sleep(interval)
        tasks = _list_task(cluster_name, task_def, filter=task_ids)
    return tasks