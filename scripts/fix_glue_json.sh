#!/bin/bash

INPUT=$1
OUTPUT=$2
JOB_NAME=$(jq -r '.name' "$INPUT")

jq --arg NAME "$JOB_NAME" '
  del(.name) |
  .Name = $NAME |
  .ExecutionProperty.MaxConcurrentRuns = .executionProperty.maxConcurrentRuns |
  .Command.Name = .command.name |
  .Command.ScriptLocation = .command.scriptLocation |
  .Command.PythonVersion = .command.pythonVersion |
  .SourceControlDetails.Provider = .sourceControlDetails.provider |
  .SourceControlDetails.Repository = .sourceControlDetails.repository |
  .SourceControlDetails.Branch = .sourceControlDetails.branch |
  .SourceControlDetails.Folder = .sourceControlDetails.folder |
  del(
    .executionProperty,
    .command,
    .sourceControlDetails
  )
' "$INPUT" > "$OUTPUT"
