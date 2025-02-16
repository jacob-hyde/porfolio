#!/bin/bash

# Get current date for backup file name
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="/backups/backup_${DATE}.sql"

# Create backup using mysqldump
mysqldump -u root -p"$MYSQL_ROOT_PASSWORD" --all-databases > "$BACKUP_FILE"

# Compress the backup
gzip "$BACKUP_FILE"

# Remove backups older than 30 days
find /backups -name "backup_*.sql.gz" -mtime +30 -delete

echo "Backup completed: ${BACKUP_FILE}.gz"
