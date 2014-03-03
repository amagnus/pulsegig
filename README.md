PulseGig
========

PulseGig is a web app to get text alerts for shows.


APIs used

- Songkick for concert database
- Twilio for texts
- Google for URL shortening in texts


Installation

- Python 2.6.6+ is required.

- Clone this repo:

```
git clone https://github.com/amagnus/pulsegig.git
```

- Install requirements:

pip install -r requirements.txt

- Get API keys for Songkick, Twilio and Google:

https://www.songkick.com/developer
https://www.twilio.com/
https://developers.google.com/url-shortener/

- Enter proper settings in /pulsegig/settings. Environment variables are being used. Feel free to use regular settings or whatever you feel comfortable with.

- Synchronize the database state with current models

./manage.py migrate app

- Start development server

./manage.py runserver --settings=pulsegig.settings.local


Cron jobs

- A few cron jobs are running to pull data off Songkick and send texts accordingly
