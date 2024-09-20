#!/bin/bash

set -eo pipefail
shopt -s nullglob

start_db() {
    echo "Starting mariadbd temporarily..."
    /usr/sbin/mariadbd --user=root --socket=/tmp/mysql.sock &
    MARIADB_PID=$!

    echo "Waiting for mariadb to be ready to accept connections..."
    for i in {10..0}; do
        if (echo SELECT 1 | mariadb &>/dev/null); then
            break
        fi
        sleep 1
    done

    if [ "$i" = 0 ]; then
        echo "Unable to start mariadbd, aborting"
        exit 1
    fi
}

stop_db() {
    echo "Stopping mariadbd..."
    kill "$MARIADB_PID"
    wait "$MARIADB_PID"
}

init_db() {
    echo "Creating database sme_oahpa..."
    echo "CREATE DATABASE sme_oahpa" | mariadb
    echo "Creating sme_oahpa user"
    echo "CREATE USER 'sme_oahpa'@'%' IDENTIFIED BY 'smeGOGOsme' PASSWORD EXPIRE NEVER;" | mariadb
    echo "GRANT ALL PRIVILEGES ON *.* TO 'sme_oahpa'@'%' IDENTIFIED BY 'smeGOGOsme';" | mariadb
}

import_data() {
    echo "Importing data"
    gzip -dc /tmp/sme_oahpa.sql.gz | mariadb --password=smeGOGOsme --user=sme_oahpa sme_oahpa
}

start_db
init_db
import_data
stop_db
echo "database created"

# when using both ENTRYPOINT and CMD in a Dockerfile, the CMD is treated
# as argument to the ENTRYPOINT... so exec the real CMD to run it
#exec "$@"
