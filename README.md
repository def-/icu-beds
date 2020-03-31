# Development of ICU Beds by German Federal State

Live on https://hookrace.net/icu-beds/

Run with a cron-job, [data from DIVI](https://www.divi.de/register/kartenansicht) is updated daily:

```
0 11 * * * cd /var/www-hookrace/icu-beds && ./fetch.sh && ./update.sh
```
