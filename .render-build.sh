#!/usr/bin/env bash
# Render build script for Rasa

# Always stop on first error
set -o errexit

# Upgrade the build tools before touching Rasa
python3 -m pip install --upgrade pip setuptools wheel packaging

# Now install your normal requirements
pip install -r requirements.txt
