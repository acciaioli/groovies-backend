# backend

## Rest Api Service

Where to go from here ? 

### 0. Install docker

https://docs.docker.com/install/

don't want to use docker ? check the notes at the end

### 1. Create keys for jwt

```bash
make create-keys
```

this will generate a private / public key pair that we will use to sign our jwts.

notes:
1) you don't need to run this if you already have keys
2) you only need a public key if the service is not signing the tokens


### 2. Run Tests

run tests, static type checker and linter

```bash
make test
make type-check
make lint
```

### 3. Try it out

```bash
make start-dev

curl -X GET 0.0.0.0:8000 \
 -H "Content-type: application/json" \
 -H "Accept: application/json" 


```

### 4. CI

setup travis ci
setup codecov
set codecov env variable on travis

### 5. Initial commit

### 6. Notes

if you don't want to use docker you can:

#### create/activate a virtual env
```bash
pyhton3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

#### explore the Makefile
the Makefile relies on docker but check you can run all the commands without it.

#### export variables to your env:

```bash
set -a 
source .env_vars/django 
source .env_vars/postgres 
set +a 
```
#### deal with the database

you can:
1) install/setup postgres on your machine
3) use sqlite (requires changing the settings)



Bootstrapped with https://github.com/Spin14/django-rest-jwt-service-cookiecutter.git
