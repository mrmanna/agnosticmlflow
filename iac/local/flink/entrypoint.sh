#!/bin/bash

# Wait until Docker socket is available
while ! docker ps > /dev/null 2>&1; do
    echo "Waiting for Docker socket to be ready..."
    sleep 1
done

echo "Docker socket is ready."

# Execute Flink process
if [ "$1" = "jobmanager" ] || [ "$1" = "taskmanager" ]; then
  exec /opt/flink/bin/"$1".sh start-foreground
else
  echo "Unknown command: $1"
  exit 1
fi
