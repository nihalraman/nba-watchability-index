import json
import os

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate a user fixture with a password from .env"

    def handle(self, *args, **kwargs):
        self.load_dotenv("/code/.env")
        # Retrieve password from environment variable
        default_password = make_password(
            os.getenv("DEFAULT_PASSWORD", "defaultpassword")
        )

        # Create the superuser with the password from the .env file
        user_data = [
            {
                "model": "auth.user",
                "pk": 1,
                "fields": {
                    "username": "admin",
                    "password": default_password,
                    "first_name": "",
                    "last_name": "",
                    "email": "",
                    "is_staff": True,
                    "is_active": True,
                    "is_superuser": True,
                    "date_joined": "2025-03-15T12:00:00Z",
                },
            },
            {
                "model": "auth.user",
                "pk": 2,
                "fields": {
                    "username": "nihal",
                    "password": default_password,
                    "first_name": "Nihal",
                    "last_name": "Raman",
                    "email": "nihalraman00@gmail.com",
                    "is_staff": True,
                    "is_active": True,
                    "is_superuser": False,
                    "date_joined": "2025-03-15T12:00:00Z",
                },
            },
            {
                "model": "auth.user",
                "pk": 3,
                "fields": {
                    "username": "duncan",
                    "password": default_password,
                    "first_name": "Duncan",
                    "last_name": "Lamont",
                    "email": "duncanl1000@gmail.com",
                    "is_staff": True,
                    "is_active": True,
                    "is_superuser": False,
                    "date_joined": "2025-03-15T12:00:00Z",
                },
            },
        ]

        # Output the fixture to a JSON file
        with open("users/fixtures/initial_data.json", "w") as f:
            json.dump(user_data, f, indent=4)

        self.stdout.write(self.style.SUCCESS("Fixture generated successfully!"))

    def load_dotenv(self, dotenv_path):
        """
        Load environment variables from a .env file manually.
        This reads the .env file and adds key-value pairs to os.environ.
        """
        if not os.path.exists(dotenv_path):
            raise FileNotFoundError(f"{dotenv_path} not found.")

        with open(dotenv_path) as f:
            for line in f:
                # Skip comments and empty lines
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                # Split by '=' and assign to os.environ
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()
