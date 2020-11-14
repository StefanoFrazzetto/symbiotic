#!/usr/bin/env bash

SCRIPTS_DIR="$(dirname $0)"
ROOT_DIR="$SCRIPTS_DIR/.."

# re-create venv dir
pushd "$ROOT_DIR"
    rm -rf venv
    python3 -m venv venv
    source ./venv/bin/activate
    python -m pip install -r requirements.txt
popd
