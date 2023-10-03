from flask_apscheduler import APScheduler

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.absolute()))
# We need to add the child paths to the project! This is so BS...

from gameping import create_app, db
from gameping.jobs.confirm import check_inbox_for_confirmations
from gameping.jobs.scraper import scrape


class Config:
    SCHEDULER_API_ENABLED = True


app = create_app()
app.config.from_object(Config())


def confirm():
    with app.app_context():
        check_inbox_for_confirmations()


def scraper():
    with app.app_context():
        scrape()


scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
scheduler.add_job("confirmation", confirm, trigger="cron", minute="*/2", jitter=60)
scheduler.add_job("scraper", scraper, trigger="cron", hour="*", jitter=120)

app.run(host="127.0.0.1", port=8000, debug=True)
