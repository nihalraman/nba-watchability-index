import json
import os

import pandas as pd
from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = "Generate fixtures with player names and info"

    def handle(self, *args, **kwargs):

        # read in static CSV of players
        # generated by pulling all players from https://www.basketball-reference.com/players/{LETTER}
        # letter-by-letter

        # Construct the absolute path to the CSV file
        wdir = os.path.dirname(os.path.abspath(__file__))
        player_df = pd.read_csv(os.path.join(wdir, "all_bbref_players.csv"))
        # convert height to inches
        player_df["height_in"] = (
            player_df["Ht"].str.split("-").apply(lambda x: int(x[0]) * 12 + int(x[1]))
        )
        player_df["Birth Date"] = pd.to_datetime(player_df["Birth Date"])

        # create player fixture
        player_fixtures = []
        for _, row in player_df.iterrows():
            cur_player = {}

            # use bbref id as pk
            cur_player["fields"] = {
                "name": row["Player"],
                "position": row["Pos"],
                "height_in": row["height_in"],
            }

            if pd.notna(row["Wt"]):
                cur_player["fields"]["weight"] = int(row["Wt"])

            if pd.notna(row["Birth Date"]):
                # format dob in a Django-friendly way if it exists
                cur_player["fields"]["dob"] = timezone.make_aware(
                    row["Birth Date"]
                ).isoformat()

            # primary key is bbref player id
            cur_player["pk"] = row["Player-additional"]
            cur_player["model"] = "data.player"

            player_fixtures.append(cur_player)

        # create playerteam fixture
        dfs = pd.read_csv(
            "https://drive.usercontent.google.com/download?export=download&confirm=t&id=148vVQMSjlxfTJfxZBWd5pcTzvKpoGBs4"
        )

        player_team = (
            dfs.groupby(["Player", "Tm"])["Date"]
            .apply(lambda x: [x.min(), x.max()])
            .reset_index()
        )
        player_team["first_game_date"] = player_team["Date"].apply(lambda x: x[0])
        player_team["last_game_date"] = player_team["Date"].apply(lambda x: x[1])

        player_team_fixtures = []
        for idx, row in player_team.iterrows():
            player_team_fixtures.append(
                {
                    "model": "data.PlayerTeam",
                    "pk": idx + 1,
                    "fields": {
                        "player": row["Player"],
                        "team": row["Tm"],
                        "first_game": row["first_game_date"],
                        "last_game": row["last_game_date"],
                    },
                }
            )

        # Output the fixture to a JSON file
        with open("data/fixtures/player_data.json", "w") as f:
            json.dump(player_fixtures + player_team_fixtures, f, indent=4)

        self.stdout.write(self.style.SUCCESS("Fixture generated successfully!"))
