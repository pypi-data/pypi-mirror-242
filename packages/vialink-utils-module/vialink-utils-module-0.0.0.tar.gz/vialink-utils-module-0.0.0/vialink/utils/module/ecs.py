import boto3

from .settings import settings

client = boto3.client('ecs', region_name=settings.AWS_REGION)

def _launch_ecs(cluster_name, subnets, task_def, cpu, memory, id):
    resp = client.run_task(
        cluster=cluster_name,
        launchType="FARGATE",
        taskDefinition=task_def,
        count=1,
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': subnets,
                'assignPublicIp': 'ENABLED',
            },
        },
        overrides={
            "cpu": f"{cpu}",
            "memory": f"{memory}",
            'containerOverrides': [
                {
                    'name': 'main',
                    'cpu': cpu,
                    'memory': memory,
                    'memoryReservation': memory,
                    'environment': [
                        {
                            'name': 'ID',
                            'value': f'{id}'
                        }
                    ]
                }
            ]
        }
    )
    print(f'new task {task_def} started')
    return resp['tasks'][0]['containers'][0]['taskArn']

def _list_task(cluster, task_def, filter=None):
    response = client.list_tasks(
        cluster=cluster,
        family=task_def,
        desiredStatus='RUNNING',
    )
    list_task = response.get('taskArns', [])
    if filter:
        filter_task  = []
        for task in list_task:
            if task in filter:
                filter_task.append(task)
        return filter_task
    return list_task