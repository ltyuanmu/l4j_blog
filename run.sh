#!/bin/bash

pip install -r requirement.txt
mkdir logs
python run.py init_data
python run.py insert_admin
gunicorn -w4 -b 0.0.0.0:8080 run:app
