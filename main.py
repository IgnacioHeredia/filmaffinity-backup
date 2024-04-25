"""
Run backup
"""

from pathlib import Path
import shutil

import pandas as pd
from rich import print
import typer

import utils


data_dir = Path(__file__).parent.resolve() / 'data'


def main(
        user_id: str,
        ):
    data = {}

    utils.check_user(user_id)

    # Download lists
    print("Retrieving [hot_pink3 bold]user lists[/hot_pink3 bold]")
    lists = utils.get_user_lists(user_id)

    if not lists:
        print(
            ":name_badge: [yellow bold]Warning[/yellow bold]: No lists were found. " \
            "Make sure to mark your lists as :earth_americas: [b u]public[/b u] to "\
            "be able to backup them.")
        inp = input("   Do you want to continue with watched movies and erase previous list data (if any)? [y/n]")
        if inp != 'y':
            return None

    for name, url in lists.items():
        print(f"Parsing list: [turquoise4 bold]{name}[/turquoise4 bold]")
        _, info = utils.get_list_movies(url)
        data[f'list - {name}'] = info

    # Download watched
    print("Parsing [green bold]watched[/green bold] movies")
    data['watched'] = utils.get_watched_movies(user_id)

    # Clear previous user data
    user_dir = data_dir / user_id
    if user_dir.exists():
        shutil.rmtree(user_dir)
    user_dir.mkdir()

    # Save data to csv
    print('Saving CSV files to [bold]./data[/bold] folder.')
    for k, v in data.items():
        df = pd.DataFrame.from_dict(v)
        df.to_csv(
            user_dir / f'{k}.csv',
            sep = ';',
            index = False,
        )


if __name__ == "__main__":
    typer.run(main)
