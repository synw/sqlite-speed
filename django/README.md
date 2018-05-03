## Django tests

To run the tests with Django copy the `django/sqls` folder into a Django instance.

Add `sqls` to installed apps

Install django_extensions: `pip install django_extensions` and add `django_extensions` to installed apps

To run the tests: `python3 runscript sqlite_speed`  

To adjust the number of runs and records edit `sqls/scripts/sqlite_speed.py`