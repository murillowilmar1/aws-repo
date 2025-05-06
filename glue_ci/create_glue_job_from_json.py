import boto3
import json

# Cliente sin claves embebidas
glue = boto3.client('glue', region_name='us-east-1')

# Leer archivo JSON
with open('glue_ci/script1.json') as f:
    raw_config = json.load(f)

command = raw_config.get("command", {})

response = glue.create_job(
    Name=raw_config.pop("name"),
    Role=raw_config["role"],
    ExecutionProperty={"MaxConcurrentRuns": raw_config["executionProperty"]["maxConcurrentRuns"]},
    Command={
        "Name": command.get("name"),
        "ScriptLocation": command.get("scriptLocation"),
        "PythonVersion": command.get("pythonVersion")
    },
    DefaultArguments=raw_config["defaultArguments"],
    MaxRetries=raw_config["maxRetries"],
    Timeout=raw_config["timeout"],
    GlueVersion=raw_config["glueVersion"],
    NumberOfWorkers=raw_config["numberOfWorkers"],
    WorkerType=raw_config["workerType"],
    ExecutionClass=raw_config["executionClass"]
)

print("✅ Glue Job creado:", response['Name'])
