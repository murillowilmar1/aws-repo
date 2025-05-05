#!/bin/bash

INPUT=$1
OUTPUT=$2

jq '{
  Name: .name,
  JobMode: .jobMode,
  Description: .description,
  Role: .role,
  ExecutionProperty: {
    MaxConcurrentRuns: .executionProperty.maxConcurrentRuns
  },
  Command: {
    Name: .command.name,
    ScriptLocation: .command.scriptLocation,
    PythonVersion: .command.pythonVersion
  },
  DefaultArguments: .defaultArguments,
  MaxRetries: .maxRetries,
  AllocatedCapacity: .allocatedCapacity,
  Timeout: .timeout,
  MaxCapacity: .maxCapacity,
  GlueVersion: .glueVersion,
  NumberOfWorkers: .numberOfWorkers,
  WorkerType: .workerType,
  ExecutionClass: .executionClass,
  SourceControlDetails: {
    Provider: .sourceControlDetails.provider,
    Repository: .sourceControlDetails.repository,
    Branch: .sourceControlDetails.branch,
    Folder: .sourceControlDetails.folder
  }
}' "$INPUT" > "$OUTPUT"
