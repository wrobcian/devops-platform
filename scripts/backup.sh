#!/bin/bash
set -e

BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="backup_${DATE}.tar.gz"

echo "======================================"
echo "BACKUP SCRIPT"
echo "Date: $(date)"
echo "======================================"

mkdir -p $BACKUP_DIR

echo "[1/3] Backing up application files..."
tar -czf "$BACKUP_DIR/$BACKUP_NAME" \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='backups' \
    .

SIZE=$(du -h "$BACKUP_DIR/$BACKUP_NAME" | cut -f1)
echo "  Created: $BACKUP_DIR/$BACKUP_NAME ($SIZE)"

echo ""
echo "[2/3] Cleaning old backups (keeping last 5)..."
cd $BACKUP_DIR
ls -t backup_*.tar.gz | tail -n +6 | xargs -r rm
REMAINING=$(ls backup_*.tar.gz 2>/dev/null | wc -l)
echo "  Remaining backups: $REMAINING"
cd ..

echo ""
echo "[3/3] Backup complete!"
echo "======================================"