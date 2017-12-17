#!/bin/bash

export DJANGO_SETTINGS_MODULE='interface_blockchain.settings.local'
cd /srv/projects/interface_blockchain
exec /home/user/.local/share/virtualenvs/interface_blockchain/bin/gunicorn interface_blockchain.wsgi.site  -b 127.0.0.1:800  --timeout=120 -w 2
