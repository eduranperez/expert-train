#!/bin/bash

# this is b/c pipenv stores the virtual env in a different
# directory so we need to get the path to it
SITE_PACKAGES=$(pipenv --venv)/lib/python3.8/site-packages
echo "Library Location: $SITE_PACKAGES"
DIR=$(pwd)

# Make sure pipenv is good to go
echo "Do fresh install to make sure everything is there"
pipenv install

cd $SITE_PACKAGES
chmod -R 777 ./
zip -r9 $DIR/package.zip *

cd $DIR
zip -g package.zip aggie_bot.py

aws lambda update-function-code --function-name  logTest --zip-file fileb://package.zip
