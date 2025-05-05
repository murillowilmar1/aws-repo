#!/bin/bash

INPUT=$1
OUTPUT=$2

jq 'with_entries(
  .key as $k |
  {
    ([
      "name","role","command","defaultArguments","executionProperty",
      "maxRetries","allocatedCapacity","timeout","maxCapacity",
      "glueVersion","numberOfWorkers","workerType","executionClass",
      "jobMode","description","sourceControlDetails"
    ] | index($k) // $k): .value
  }
) | with_entries(
  .key |=
    if . == "name" then "Name"
    elif . == "role" then "Role"
    elif . == "command" then "Command"
    elif . == "defaultArguments" then "DefaultArguments"
    elif . == "executionProperty" then "ExecutionProperty"
    elif . == "maxRetries" then "MaxRetries"
    elif . == "allocatedCapacity" then "AllocatedCapacity"
    elif . == "timeout" then "Timeout"
    elif . == "maxCapacity" then "MaxCapacity"
    elif . == "glueVersion" then "GlueVersion"
    elif . == "numberOfWorkers" then "NumberOfWorkers"
    elif . == "workerType" then "WorkerType"
    elif . == "executionClass" then "ExecutionClass"
    elif . == "jobMode" then "JobMode"
    elif . == "description" then "Description"
    elif . == "sourceControlDetails" then "SourceControlDetails"
    else .
    end
)' "$INPUT" > "$OUTPUT"
