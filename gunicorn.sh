#!/bin/bash

export DJANGO_SETTINGS_MODULE='config.settings.local'
cd /srv/projects/interface_blockchain
exec /home/user/.local/share/virtualenvs/interface_blockchain/bin/gunicorn config.wsgi  -b 127.0.0.1:8000  --timeout=120 -w 1
