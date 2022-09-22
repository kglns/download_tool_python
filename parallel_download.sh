#!/bin/bash

CONFIG=$1

# Spawn one python process per download, as Python doesn't support multithreading
COMMAND_STRING=""
while read args;do
        COMMAND_STRING+="python3 main.py ${args} & "
done < ${CONFIG}

FINAL_COMMAND=$(sed 's/.\{2\}$//' <<< "$COMMAND_STRING")
echo "final command ${FINAL_COMMAND}"
eval $FINAL_COMMAND


