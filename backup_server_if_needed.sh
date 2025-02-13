#!/bin/bash

TIME_ELAPSED=$(($(date -r $SERVER"/world" +%s) - $(date -r $BACKUPS +%s)))
TIME_THRESHOLD=$(((23 * 60) * 60)) # 23 hours in seconds

echo $(date) >> $BACKUP_LOG
echo $(date)
echo "Starting autobackup..." >> $BACKUP_LOG
echo "Starting autobackup..."


if [[ $TIME_ELAPSED -ge 0 ]]; then
    echo "The server is newer than the backup by:" $(date -u -d @${TIME_ELAPSED} +"%T") >> $BACKUP_LOG
    echo "The server is newer than the backup by:" $(date -u -d @${TIME_ELAPSED} +"%T")
else
    TIME_ELAPSED=$((0 - $TIME_ELAPSED))
    echo "The backup is newer than the server by:" $(date -u -d @${TIME_ELAPSED} +"%T") >> $BACKUP_LOG
    echo "The backup is newer than the server by:" $(date -u -d @${TIME_ELAPSED} +"%T")
    TIME_ELAPSED=$((0 - $TIME_ELAPSED))
fi

if [[ $TIME_ELAPSED -ge $TIME_THRESHOLD ]]; then
    echo "Backing up server..." >> $BACKUP_LOG
    echo "Backing up server..."
    bash $SCRIPTS/backup_server.sh
else
    echo "No backup needed!" >> $BACKUP_LOG
    echo "No backup needed!" >> $BACKUP_LOG
fi

echo "" >> $BACKUP_LOG
echo ""

cd - > /dev/null 2>&1
