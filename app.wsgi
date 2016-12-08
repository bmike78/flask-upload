activate_this = '/var/www/flask-upload/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, "/var/www/flask-upload")

from app import app
application = app

