# vialink-utils-module



## Install Package

```
pip install vialink-utils-module
```

## Launch Serverless

```
from vialink.utils import module

module_id = module.register_module(module_name='plus', input_data={'num1': 1, 'num2': 2})
task_id = module.run_module(module_id, 256, 512)
```

## Launch Serverless (Waiter)

```
from vialink.utils import module

module_id = module.register_module(module_name='plus', input_data={'num1': 1, 'num2': 2})
task_id = module.run_module(module_id, 256, 512)
tasks = module.waiter_module([task_id]) # Wait For Task in this list
result = module.retrieve_module_output(module_id) # Retrieve Result After Task Finish
```
