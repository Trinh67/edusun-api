# EduSun Service.
This api for EduSun.

## Migrations
### Create migration versions
```
$ alembic revision --autogenerate
```
### Upgrade head migration
```
alembic upgrade head
```

## Install and running app
### Run web app
```
$ uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Run test
To run test
```
    py.test --cov=app
```
