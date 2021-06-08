#!/bin/zsh

DB_NAME="store.db"
HERE=`pwd`
TOP=`dirname $HERE`
DB_PATH="$TOP/source/database/"
BK_PATH="$TOP/db_backups/"

FILE_NAME="bk_`date +%m%d%y`.db"

cd "$DB_PATH"
sqlite3 "$DB_NAME" ".backup $FILE_NAME" # create backup

mkdir -p "$BK_PATH" # move backup to db_backups/ folder
mv "$FILE_NAME" "$BK_PATH/$FILE_NAME"
