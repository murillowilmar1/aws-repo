import argparse
import json
import boto3
import os
import sys

def load_mapping(path):
    if path.startswith("s3://"):
        raise NotImplementedError("Solo se admite archivo local por ahora")
    with open(path) as f:
        return json.load(f)

def apply_mapping(obj, mapping):
    if isinstance(obj, dict):
        return {k: apply_mapping(v, mapping) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [apply_mapping(elem, mapping) for elem in obj]
    elif isinstance(obj, str):
        for k, v in mapping.items():
            obj = obj.replace(k, v)
        return obj
    else:
        return obj

def create_or_update_job(glue, job_config):
    job_name = job_config.pop("name")
    try:
        glue.get_job(JobName=job_name)
        print(f"Job '{job_name}' ya existe. Se va a actualizar.")
        glue.update_job(JobName=job_name, JobUpdate=job_config)
    except glue.exceptions.EntityNotFoundException:
        print(f"Creando nuevo job '{job_name}'")
        glue.create_job(Name=job_name, **job_config)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config-path', required=True, help='Ruta del JSON del Glue Job')
    parser.add_argument('--mapping-path', required=True, help='Ruta del archivo de mapeo')
    parser.add_argument('--profile', required=True, help='Perfil AWS de destino')
    parser.add_argument('--region', default='us-east-1', help='Región AWS')
    args = parser.parse_args()

    # Cargar archivos
    with open(args.config_path) as f:
        job_config = json.load(f)
    mapping = load_mapping(args.mapping_path)

    # Aplicar mapeo
    job_config = apply_mapping(job_config, mapping)
    command = job_config.get("command", {})
    job_config["Command"] = {
        "Name": command.get("name"),
        "ScriptLocation": command.get("scriptLocation"),
        "PythonVersion": command.get("pythonVersion")
    }
    job_config["ExecutionProperty"] = {"MaxConcurrentRuns": job_config["executionProperty"]["maxConcurrentRuns"]}

    # Eliminar campos que boto3 no acepta directamente
    job_config.pop("command", None)
    job_config.pop("executionProperty", None)

    # Crear cliente boto3
    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    glue = session.client("glue")

    create_or_update_job(glue, job_config)
    print("✅ Job sincronizado correctamente")

if __name__ == "__main__":
    main()
