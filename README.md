# nba-watchability-index

A web app to assess watchability of NBA games.


Get it started:

```
docker compose build
docker compose up -d
docker compose exec api python manage.py migrate
docker compose exec api python manage.py loaddata initial_data
```
Browse API at `http://0.0.0.0:8000/data/`.


## Development

If you change `models.py` and want to recreate the migration:

```
docker-compose exec api python manage.py makemigrations
docker compose exec api python manage.py migrate
```

You may also need to delete any file in the /app/migrations folder EXCEPT for `__init__.py` and rerun `docker compose`.


## Troubleshooting

If API isn't browsable, you may need to restart the docker container.
