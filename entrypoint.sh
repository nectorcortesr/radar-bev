#!/bin/bash
set -e

echo "Starting industrial perception system..."
# We pass all the arguments received by the container to the main.py script
python -m src.main "$@"