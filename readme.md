
To run:
gunicorn --workers 2 wsgi:app --daemon

To kill:
pkill gunicorn

access to site settings:
/etc/nginx/sites-enabled/gameping

use psql:
sudo -u postgres psql gameping
