#!/bin/bash

while true; do
    python main.py --sms
    status=$?
    if [ $status -ne 0 ]; then
        echo "Program crashed with exit code $status. Respawning.." >&2
        sleep 1
    fi
done

