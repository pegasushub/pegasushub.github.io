#!/bin/bash

#export PEGASUSHUB_TOKEN=`cat $HOME/.pegasushub.token`
export PEGASUSHUB_TOKEN=""

cd $1 # folder for pegasushub project

git pull origin master
rm -rf _workflows/*.html

python3 scripts/process.py

git add _workflows/*.html

NOW=`date +"%Y-%m-%dT%H-%M-%S"`
git commit -am "[cron] updating workflows $NOW"
git push origin master
