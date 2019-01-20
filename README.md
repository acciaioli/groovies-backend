# Groovies Backend
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Build Status](https://travis-ci.com/Chi-Acci/groovies-backend.svg?branch=master)](https://travis-ci.com/Chi-Acci/groovies-backend)
[![codecov](https://codecov.io/gh/Chi-Acci/groovies-backend/branch/master/graph/badge.svg)](https://codecov.io/gh/Chi-Acci/groovies-backend/branch/master)

Backend for the Groovies Project

## Prerequisites
```bash
$ docker --version
Docker version 17.05.0-ce, build 89658be
 
$ docker-compose --version
docker-compose version 1.22.0, build f46880fe
 
$ make --version
GNU Make 4.1
```

## Development
```bash
$ make start-dev
```

Inside the container now:
```bash
$ make run-tests
$ history -r .history
$ cd backend; 
$ ./manage.py migrate
$ ./manage.py runserver 0.0.0.0:8000
```

Test it from outside:
```bash
$ curl -X GET http://0.0.0.0:8000/
{"image":"backend","tag":"dev","up_time":"00:00:45"}
```

Ready for dev both on new backend feature or frontend features

---
_Bootstrapped with https://github.com/Spin14/django-rest-jwt-service-cookiecutter.git_
