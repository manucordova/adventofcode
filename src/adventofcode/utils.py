import os
import pathlib as pl


def get_year_day_from_path(file_path: str):
    """
    Get the challenge year and day from the current path

    Returns
    -------
    int
        Challenge year
    int
        Challenge day
    """

    this_path = str(pl.Path(file_path).resolve())
    year = int(this_path.split(os.sep)[-3])
    day = int(this_path.split("day_")[1].split(os.sep)[0])

    return year, day
