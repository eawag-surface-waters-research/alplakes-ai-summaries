#!/bin/bash

# Initialize Conda
. /opt/conda/etc/profile.d/conda.sh

# Activate the Conda environment
conda activate ai

# Execute your Python script or desired command
python -u /repository/src/main.py "$@"
