#!/bin/bash

FORMAT_DIR=believe

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place "${FORMAT_DIR}" --exclude=__init__.py
black "${FORMAT_DIR}"
isort "${FORMAT_DIR}"