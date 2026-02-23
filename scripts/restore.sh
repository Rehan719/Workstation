#!/bin/bash
# Article J: Robustness & Reliability - Restore Script
set -e

BACKUP_DIR="backups"
LATEST_BACKUP=$(ls -t $BACKUP_DIR | head -n 1)

if [ -z "$LATEST_BACKUP" ]; then
    echo "No backups found in $BACKUP_DIR"
    exit 1
fi

echo "Restoring system state from $BACKUP_DIR/$LATEST_BACKUP..."

# Restore metadata and graphs
cp -r "$BACKUP_DIR/$LATEST_BACKUP/meta" .
# Restore config
cp -r "$BACKUP_DIR/$LATEST_BACKUP/config" .

echo "Restoration complete. Jules AI v53.0 state recovered."
