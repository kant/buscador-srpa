#!/bin/bash

server_folder_path=$(dirname $0)

sqlite3 "$server_folder_path/../app/db.sqlite" .schema > schema.sql
sqlite3 "$server_folder_path/../app/db.sqlite" .dump > dump.sql
rm "$server_folder_path/../app/db.sqlite"

grep -vx -f schema.sql dump.sql > data.sql
rm dump.sql schema.sql

export SMTP_PASS=''
. "$server_folder_path/../venv/bin/activate"
python "$server_folder_path/../main.py" create_db
sqlite3 "$server_folder_path/../app/db.sqlite" < data.sql
rm data.sql
