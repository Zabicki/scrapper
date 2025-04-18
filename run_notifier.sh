#!/usr/bin/fish
source {$SCRAPPER_HOME}/venv/bin/activate.fish
pip install -r {$SCRAPPER_HOME}/requirements.txt

set -x DISPLAY :1
set -x XAUTHORITY /run/user/1000/gdm/Xauthority

{$SCRAPPER_HOME}/venv/bin/python {$SCRAPPER_HOME}/pl/zabicki/scrapper/notifier.py >> {$SCRAPPER_LOGS}/notifier.log 2>&1
