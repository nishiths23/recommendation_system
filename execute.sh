#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo $SCRIPT_DIR
cd $SCRIPT_DIR/backend
pip3 install -r requirements.txt
open http://localhost:5000
python3 main.py