#!/bin/bash

cd $SERVER/../ > /dev/null 2>&1

   echo "Starting Backup" >> $BACKUP_LOG
NAME="Backup_["$(date '+%Y-%m-%d')"].tar.gz"
if [ -f $BACKUPS/$NAME ]; then
   echo "Backup already exists, creating another!" >> $BACKUP_LOG
   NAME="Backup_["$(date '+%Y-%m-%d_%H.%M.%S')"].tar.gz"
fi

echo "Compressing backup... " $NAME >> $BACKUP_LOG
tar czfv $BACKUPS/$NAME server
echo "Done!"  >> $BACKUP_LOG

cd - > /dev/null 2>&1
