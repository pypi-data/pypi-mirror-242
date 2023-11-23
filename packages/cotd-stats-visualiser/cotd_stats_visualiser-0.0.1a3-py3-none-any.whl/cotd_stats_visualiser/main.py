import os

import orjson  # type: ignore[import]

from .const import path
from .utils import generate_plot, get_cotd_data, get_player, parse_data

# TODO make a gui for this but also make a cli-like version
# TODO support for multiple users in the plot (maybe gui exclusive)
# TODO make this usable as a module
# TODO add a system to save the last fetched data and only from the last point we ended on

# for now, just use input() to get the data (husk)


def get_full_cotd_data_and_save(player_name: str, force_refetch: bool = False) -> None:
    existing_data = None
    player = get_player(player_name)
    player_name = player["name"]
    if not force_refetch and os.path.exists(path / f"{player_name.lower()}.json"):
        with open(f"{path / f'{player_name.lower()}.json'}", "rb") as f:
            existing_data = orjson.loads(f.read())

    player_id = player.get("id", player.get("accountid"))
    if not player_id:
        raise ValueError("Could not find player!")  # FIXME proper handling for this case
    cotd_data = get_cotd_data(player_id, existing_data)
    with open(f"{path / f'{player_name.lower()}.json'}", "wb+") as out:
        out.write(orjson.dumps(cotd_data))

    data = parse_data(cotd_data)
    plot = generate_plot(data, player_name)
    plot.show()  # FIXME: make this wait for the user to close the plot


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        # TODO get the player name somehow (input)
        argv = []

    get_full_cotd_data_and_save(argv[0])
