#!/bin/bash

# Start the bot using Gunicorn
gunicorn bot:app --bind 0.0.0.0:8000 --workers 3