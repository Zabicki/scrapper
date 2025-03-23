#!/usr/bin/fish
source /home/krzysztof/git/scrapper/venv/bin/activate.fish
pip install -r /home/krzysztof/git/scrapper/requirements.txt
/home/krzysztof/git/scrapper/venv/bin/python /home/krzysztof/git/scrapper/pl/zabicki/scrapper/notifier.py >> /home/krzysztof/scrapper/logs/notifier.log 2>&1
