#!/bin/bash
echo "Backing up Unified Evidence Graph and Ledger..."
mkdir -p backups
cp src/ueg/*.db backups/ 2>/dev/null || echo "No DB files to backup."
