#!/bin/bash

set -eo pipefail
shopt -s nullglob

start_db() {
    echo "Starting mariadbd temporarily..."
    /usr/sbin/mariadbd --user=root --socket=/run/mysqld/mysqld.sock &
    MARIADB_PID=$!

    echo "Waiting for mariadb to be ready to accept connections..."
    for i in {10..0}; do
        if (echo SELECT 1 | mariadb >/dev/null 2>&1); then
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
    echo "Creating sme_oahpa user..."
    echo "CREATE USER 'sme_oahpa'@'%' IDENTIFIED BY 'smeGOGOsme' PASSWORD EXPIRE NEVER;" | mariadb
    echo "GRANT ALL PRIVILEGES ON *.* TO 'sme_oahpa'@'%' IDENTIFIED BY 'smeGOGOsme';" | mariadb
    echo "Importing data for sme_oahpa..."
    gzip -dc /tmp/sme_oahpa.sql.gz | mariadb --password=smeGOGOsme --user=sme_oahpa sme_oahpa

    echo "Creating database sma_oahpa..."
    echo "CREATE DATABASE sma_oahpa" | mariadb
    echo "Creating sma_oahpa user..."
    echo "CREATE USER 'sma_oahpa'@'%' IDENTIFIED BY 'smaGOGOsma' PASSWORD EXPIRE NEVER;" | mariadb
    echo "GRANT ALL PRIVILEGES ON *.* TO 'sma_oahpa'@'%' IDENTIFIED BY 'smaGOGOsma';" | mariadb
    echo "Importing data for sma_oahpa..."
    gzip -dc /tmp/sma_oahpa.sql.gz | mariadb --password=smaGOGOsma --user=sma_oahpa sma_oahpa

    echo "Creating database sms_oahpa..."
    echo "CREATE DATABASE sms_oahpa" | mariadb
    echo "Creating sms_oahpa user..."
    echo "CREATE USER 'sms_oahpa'@'%' IDENTIFIED BY 'smsGOGOsms' PASSWORD EXPIRE NEVER;" | mariadb
    echo "GRANT ALL PRIVILEGES ON *.* TO 'sms_oahpa'@'%' IDENTIFIED BY 'smsGOGOsms';" | mariadb
    echo "Importing data for sms_oahpa..."
    gzip -dc /tmp/sms_oahpa.sql.gz | mariadb --password=smsGOGOsms --user=sms_oahpa sms_oahpa

    echo "Creating database smn_oahpa..."
    echo "CREATE DATABASE smn_oahpa" | mariadb
    echo "Creating smn_oahpa user..."
    echo "CREATE USER 'smn_oahpa'@'%' IDENTIFIED BY 'smnGOGOsmn' PASSWORD EXPIRE NEVER;" | mariadb
    echo "GRANT ALL PRIVILEGES ON *.* TO 'smn_oahpa'@'%' IDENTIFIED BY 'smnGOGOsmn';" | mariadb
    echo "Importing data for smn_oahpa..."
    gzip -dc /tmp/smn_oahpa.sql.gz | mariadb --password=smnGOGOsmn --user=smn_oahpa smn_oahpa

    echo "Creating database myv_oahpa..."
    echo "CREATE DATABASE myv_oahpa" | mariadb
    echo "Creating myv_oahpa user..."
    echo "CREATE USER 'myv_oahpa'@'%' IDENTIFIED BY 'myvGOGOmyv' PASSWORD EXPIRE NEVER;" | mariadb
    echo "GRANT ALL PRIVILEGES ON *.* TO 'myv_oahpa'@'%' IDENTIFIED BY 'myvGOGOmyv';" | mariadb
    echo "Importing data for myv_oahpa..."
    gzip -dc /tmp/myv_oahpa.sql.gz | mariadb --password=myvGOGOmyv --user=myv_oahpa myv_oahpa

    echo "Creating database vro_oahpa..."
    echo "CREATE DATABASE vro_oahpa" | mariadb
    echo "Creating vro_oahpa user..."
    # note: different password for vro
    echo "CREATE USER 'vro_oahpa'@'%' IDENTIFIED BY 'katsikveleq22' PASSWORD EXPIRE NEVER;" | mariadb
    echo "GRANT ALL PRIVILEGES ON *.* TO 'vro_oahpa'@'%' IDENTIFIED BY 'katsikveleq22';" | mariadb
    echo "Importing data for vro_oahpa..."
    gzip -dc /tmp/vro_oahpa.sql.gz | mariadb --password=katsikveleq22 --user=vro_oahpa vro_oahpa

    echo "Creating database fkv_oahpa..."
    echo "CREATE DATABASE fkv_oahpa" | mariadb
    echo "Creating fkv_oahpa user..."
    # note: different password for fkv
    echo "CREATE USER 'fkv_oahpa'@'%' IDENTIFIED BY 'Kainun%' PASSWORD EXPIRE NEVER;" | mariadb
    echo "GRANT ALL PRIVILEGES ON *.* TO 'fkv_oahpa'@'%' IDENTIFIED BY 'Kainun%';" | mariadb
    echo "Importing data for fkv_oahpa..."
    gzip -dc /tmp/fkv_oahpa.sql.gz | mariadb --password=Kainun% --user=fkv_oahpa fkv_oahpa

    echo "Creating database crk_oahpa..."
    echo "CREATE DATABASE crk_oahpa" | mariadb
    echo "Creating crk_oahpa user..."
    echo "CREATE USER 'crk_oahpa'@'%' IDENTIFIED BY 'crkGOGOcrk' PASSWORD EXPIRE NEVER;" | mariadb
    echo "GRANT ALL PRIVILEGES ON *.* TO 'crk_oahpa'@'%' IDENTIFIED BY 'crkGOGOcrk';" | mariadb
    echo "Importing data for crk_oahpa..."
    gzip -dc /tmp/crk_oahpa.sql.gz | mariadb --password=crkGOGOcrk --user=crk_oahpa crk_oahpa

    echo "Creating database est_oahpa..."
    echo "CREATE DATABASE est_oahpa" | mariadb
    echo "Creating est_oahpa user..."
    echo "CREATE USER 'est_oahpa'@'%' IDENTIFIED BY 'Varbola1343' PASSWORD EXPIRE NEVER;" | mariadb
    echo "GRANT ALL PRIVILEGES ON *.* TO 'est_oahpa'@'%' IDENTIFIED BY 'Varbola1343';" | mariadb
    echo "Importing data for est_oahpa..."
    gzip -dc /tmp/est_oahpa.sql.gz | mariadb --password=Varbola1343 --user=est_oahpa est_oahpa
}

start_db
init_db
stop_db
echo "database created. commit image layer takes a few seconds..."

# when using both ENTRYPOINT and CMD in a Dockerfile, the CMD is treated
# as argument to the ENTRYPOINT... so exec the real CMD to run it
#exec "$@"
