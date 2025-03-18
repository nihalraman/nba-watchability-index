# nba-watchability-index

A web app to assess watchability of NBA games.


Get it started:

- Create .env file with 'DEFAULT_PASSWORD={your_password_here}'

```
docker compose build
docker compose up -d
```
Browse API at `http://0.0.0.0:8000/data/`.

Log into the API with username set to 'admin', 'nihal', or 'duncan'. Password will be default password set in the .env file.


## Development

If you change `models.py` and want to recreate the migration:

```
docker-compose exec api python manage.py makemigrations
docker compose exec api python manage.py migrate
```

You may also need to delete any file in the /app/migrations folder EXCEPT for `__init__.py` and rerun `docker compose`.
