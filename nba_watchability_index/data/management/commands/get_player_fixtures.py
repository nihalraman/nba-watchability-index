import json

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate fixtures with player names and info"

    # def handle(self, *args, **kwargs):

    #     # Output the fixture to a JSON file
    #     with open("data/fixtures/player_data.json", "w") as f:
    #         json.dump(fixture_ls, f, indent=4)

    #     self.stdout.write(self.style.SUCCESS("Fixture generated successfully!"))
