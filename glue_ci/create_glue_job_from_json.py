import boto3
import json
import os

# Detectar si estamos en producción (por ejemplo, rama main)
IS_PROD = os.environ.get("IS_PRODUCTION", "false").lower() == "true"

# Account ID destino si es producción
PROD_ACCOUNT_ID = "573509103457"
PROD_BUCKET_PREFIX = f"s3://aws-glue-assets-{PROD_ACCOUNT_ID}-us-east-1"

# Cliente boto3
glue = boto3.client('glue', region_name='us-east-1')

# Cargar el archivo JSON
with open('Notebooks/script1.json') as f:
    raw_config = json.load(f)

# Si estamos en prod, sobreescribimos ciertos valores
if IS_PROD:
    raw_config["role"] = f"arn:aws:iam::{PROD_ACCOUNT_ID}:role/s3-access-control"
    raw_config["command"]["scriptLocation"] = f"{PROD_BUCKET_PREFIX}/scripts/script1.py"
    raw_config["defaultArguments"]["--spark-event-logs-path"] = f"{PROD_BUCKET_PREFIX}/sparkHistoryLogs/"
    raw_config["defaultArguments"]["--TempDir"] = f"{PROD_BUCKET_PREFIX}/temporary/"

# Extraer comando
command = raw_config.get("command", {})

# Crear el Glue Job
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

print("✅ Glue Job creado o actualizado:", response['Name'])
