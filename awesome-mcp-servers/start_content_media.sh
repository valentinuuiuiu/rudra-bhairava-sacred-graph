#!/bin/bash
# Start Content Media Agent on port 8003

cd /home/shiva/Desktop/piata-ro-project/awesome-mcp-servers
source ../venv/bin/activate

export PYTHONPATH=/home/shiva/Desktop/piata-ro-project:$PYTHONPATH
export DJANGO_SETTINGS_MODULE=piata_ro.settings

# Replace port in the script and run it
sed 's/port=8002/port=8003/g; s/localhost:8002/localhost:8003/g' content_media_agent.py > temp_content_media_agent.py

python temp_content_media_agent.py

# Cleanup
rm temp_content_media_agent.py
