#!/bin/bash
source ${SCRAPPER_HOME}/.venv/bin/activate
pip install -r ${SCRAPPER_HOME}/requirements.txt

export DISPLAY=:1
#export XAUTHORITY=/run/user/1000/gdm/Xauthority

# create logs file if does not exist
mkdir -p $SCRAPPER_LOGS
touch ${SCRAPPER_LOGS}/notifier.log

${SCRAPPER_HOME}/.venv/bin/python ${SCRAPPER_HOME}/pl/zabicki/scrapper/notifier.py >> ${SCRAPPER_LOGS}/notifier.log 2>&1
