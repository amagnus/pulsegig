[PulseGig](https://pulsegig.com)
========

PulseGig is a web app to get text alerts for shows.


APIs used

- Songkick for concert database
- Twilio for texts
- Google for URL shortening in texts


## Installation

- Python 2.6.6+ is required.

- Clone this repo:

```
git clone https://github.com/amagnus/pulsegig.git
```

- Install requirements:

```
pip install -r requirements.txt
```

- Get API keys for [Songkick](https://www.songkick.com/developer), [Twilio](https://www.twilio.com) and [Google](https://developers.google.com/url-shortener/).

- Enter proper settings in /pulsegig/settings. Environment variables are being used. Feel free to use regular settings or whatever you feel comfortable with.

- Synchronize the database state with current models

```
./manage.py migrate app
```

- Start development server

```
./manage.py runserver --settings=pulsegig.settings.local
```


## Scheduled tasks

A few management commands are running as cron jobs to pull data off Songkick and send texts accordingly.

- Pull Songkick for new shows and add alerts to queue:

```
0 */3 * * *  /var/www/pulsegig.com/manage.py cron --settings=blogsc.settings.production >> /var/log/pullshows.log
```

- Process texts queue:

```
*/20 * * * *  /var/www/pulsegig.com/manage.py cron_autosender --settings=blogsc.settings.production >> /var/log/pullshows.log
```

- Update bands similarity bindings in database:

```
0 2 * * *  /var/www/pulsegig.com/manage.py cron_similar --settings=blogsc.settings.production >> /var/log/pullshows.log
```

- Pull Songkick for any new show for bands similar to subscribed bands, and add alerts to queue:

```
0 7 * * *  /var/www/pulsegig.com/manage.py cron_sim_check --settings=blogsc.settings.production >> /var/log/pullshows.log
```
