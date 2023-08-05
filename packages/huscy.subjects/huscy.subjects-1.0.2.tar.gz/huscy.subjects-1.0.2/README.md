huscy.subjects
======

![PyPi Version](https://img.shields.io/pypi/v/huscy-subjects.svg)
![PyPi Status](https://img.shields.io/pypi/status/huscy-subjects)
![PyPI Downloads](https://img.shields.io/pypi/dm/huscy-subjects)
![PyPI License](https://img.shields.io/pypi/l/huscy-subjects?color=yellow)
![Python Versions](https://img.shields.io/pypi/pyversions/huscy-subjects.svg)
![Django Versions](https://img.shields.io/pypi/djversions/huscy-subjects)



Requirements
------

- Python 3.6+
- A supported version of Django

Tox tests on Django versions 2.1, 2.2, 3.0 and 3.1.



Installation
------

To install `husy.subjects` simply run:
```
pip install huscy.subjects
```



Configuration
------

First of all, the `huscy.subjects` application has to be hooked into the project.

1. Add `huscy.subjects` and further required apps to `INSTALLED_APPS` in settings module:

```python
INSTALLED_APPS = (
	...
	'django_countries',
	'phonenumber_field',
	'rest_framework',
	'rest_framework_nested',

	'huscy.subjects',
)
```

2. Create `huscy.subjects` database tables by running:

```
python manage.py migrate
```



Development
------

After checking out the repository you should activate any virtual environment.
Install all development and test dependencies:

```
make install
```

Create database tables:

```
make migrate
```

We assume you're having a running postgres database with a user `huscy` and a database also called `huscy`.
You can easily create them by running

```
sudo -u postgres createuser -d huscy
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE huscy TO huscy;"
sudo -u postgres psql -c "ALTER USER huscy WITH PASSWORD '123';"
sudo -u postgres createdb huscy
```
