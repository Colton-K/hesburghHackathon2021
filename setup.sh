#!/usr/bin/env bash

sudo python3 -m pip install flask

# mongodb
sudo python3 -m pip install pymongo
# wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
# echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/4.4 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt-get update
sudo apt-get install mongodb

# ps --no-headers -o comm 1
# sudo systemctl start mongodb
# sudo systemctl daemon-reload
# sudo systemctl enable mongod
# sudo systemctl restart mongod
# mongo # run mongo shell
