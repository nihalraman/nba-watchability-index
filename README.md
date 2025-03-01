# nba-watchability-index

A web app to assess watchability of NBA games.


Get it started:

```
docker compose build
docker compose up -d
docker compose exec api python manage.py migrate
docker compose exec api python manage.py loaddata initial_dev
```
Access admin site at `http://0.0.0.0:8000/admin/`.
