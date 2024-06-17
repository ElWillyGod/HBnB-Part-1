
"""
    Defines countries getter
"""

import csv
from pathlib import Path

current_dir = Path(__file__).parent.resolve()

filename = f"{current_dir}/countries.csv"


class CountryManager():
    """
        Get gets list of countries as dict.
    """

    @staticmethod
    def get() -> list[dict]:
        output = []

        with open(filename, "r", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                output.append(row)

        return output
