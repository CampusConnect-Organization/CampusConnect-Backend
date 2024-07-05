import json
import os
from django.core.management.base import BaseCommand
from pu_result.models import Result


class Command(BaseCommand):
    help = "Seed the database with the PU Result"

    def handle(self, *args, **kwargs):
        directory = "pu_result/result_data"

        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                filename_parts = os.path.splitext(filename)[0].split("_")
                year = filename_parts[-2]
                season = filename_parts[-1]

                file_path = os.path.join(directory, filename)
                with open(file_path, "r") as file:
                    json_data = json.load(file)

                for symbol_number, subjects in json_data.items():
                    if symbol_number == "nan":
                        continue
                    result = Result(
                        symbol_number = symbol_number,
                        year=year,
                        season=season,
                        result=subjects
                    )

                    result.save()
        self.stdout.write(self.style.SUCCESS("Data stored successfully."))