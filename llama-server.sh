#!/bin/bash

llama-server \
  --jinja \
  -c 8192 \
  --keep 256 \
  -t 8 \
  --mlock \
  --n-gpu-layers 35 \
  -m "$1"