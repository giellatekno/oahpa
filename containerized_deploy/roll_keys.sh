#!/bin/bash

# Write random data to the SECRET_KEY variable in all settings_not_in_svn.py
# files.

echo "Rolling new keys..."
for lang in sma sme sms smn myv vro fkv crk est; do
    FILE="/app/${lang}_oahpa_project/${lang}_oahpa/settings_not_in_svn.py"
    KEY=$(tr -dc 'A-Za-z0-9!"#$%()*+,-.:;<=>?@[]^_`{|}~' </dev/urandom | head -c 52)
    sed --in-place "s/^SECRET_KEY\\s*=.*$/SECRET_KEY = '$KEY'/" $FILE
done
