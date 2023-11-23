__all__ = ("get_player", "get_cotd_data", "parse_data", "generate_plot")

from typing import Any

import matplotlib.pyplot as plt  # type: ignore[import]
import pandas as pd
import requests
from matplotlib import ticker as pltticker
from ratelimiter import RateLimiter  # type: ignore[import]

from .const import API_URL, headers


def get_player(player_name: str) -> dict[str, str]:
    data = requests.get(f"{API_URL}players/find?search={player_name}", headers=headers)
    players: list[dict[str, dict[str, str]]] = data.json()
    if len(players) == 1:
        player = players[0]
    else:
        valid_players = [
            player for player in players if player["player"]["name"].lower() == player_name.lower()
        ]
        player = valid_players[0] if valid_players else players[0]
        # if no player with exact name is found, just use the first one,
        # so if you search for "scrapie" and there is only "scrapie98" and "scrapie99", return the first one
        # (TODO maybe I should add something that asks the user which one they want to use)
        # but if there is "scrapie" and "scrapie98", return "scrapie"
    return player["player"]


def get_cotd_data(
    account_id: str, existing_data: list[dict[str, Any]] | None = None
) -> list[dict[str, Any]]:
    def _check_and_add_to_existing_data(curr: list[dict[str, Any]]) -> bool:
        nonlocal existing_data
        if existing_data:
            exit_: bool = False
            for curr_cotd, existing in zip(
                curr, existing_data
            ):  # slow, but less api requests, so it's fine
                if curr_cotd["id"] == existing["id"]:
                    exit_ = True
                    continue
                existing_data.append(curr_cotd)
            return exit_

        return False

    cotd_data: list[dict[str, Any]] = []
    data = requests.get(f"{API_URL}player/{account_id}/cotd/0", headers=headers).json()
    cotd_data.extend(
        cotd for cotd in data["cotds"] if "T18" in cotd["timestamp"] or "T17" in cotd["timestamp"]
    )
    if _check_and_add_to_existing_data(cotd_data):
        return existing_data  # type: ignore[return-value] # this cant be none, checked for in the func...

    i = 1
    limiter = RateLimiter(max_calls=35, period=60)
    while data["cotds"]:
        with limiter:
            data = requests.get(
                f"{API_URL}player/{account_id}/cotd/{i}",
                headers=headers,
            ).json()

            if _check_and_add_to_existing_data(
                [
                    cotd
                    for cotd in data["cotds"]
                    if "T18" in cotd["timestamp"] or "T17" in cotd["timestamp"]
                ]
            ):
                return existing_data  # type: ignore[return-value] # this cant be none, checked for in the func...
            cotd_data.extend(
                cotd
                for cotd in data["cotds"]
                if "T18" in cotd["timestamp"] or "T17" in cotd["timestamp"]
            )

            i += 1

    return cotd_data


def parse_data(data: list[dict[str, Any]]) -> pd.DataFrame:
    df = pd.DataFrame(
        filter(lambda dct: dct["totalplayers"] != 0, sorted(data, key=lambda x: x["id"]))  # type: ignore[arg-type, call-overload, index]
    )
    df["date"] = pd.to_datetime(df["timestamp"], format="ISO8601")
    del df["timestamp"], df["name"], df["mapuid"], df["mapname"], df["mapgroup"]
    df["divrank"] = df["divrank"].astype(int)
    df["div"] = df["div"].astype(int)
    df["rank"] = df["rank"].astype(int)
    df["qualificationrank"] = df["qualificationrank"].astype(int)
    df["totalplayers"] = df["totalplayers"].astype(int)

    # TODO add options:
    #   - rolling average (amount of days)
    #   - amount of data points (1 per day, 1 per week, 1 per month, ...)
    #   - x axis range (1 month, 5 month, all, ...)
    #   - y axis range (0-50, 0-100, ...)

    # also ignore this below its just fucked, but we keep whole month average for alpha.2

    d = {
        "months": sorted(
            list({f"{date.year}-{date.month}" for date in df["date"]}),
            key=lambda x: int(x.replace("-", "_")),
        ),
    }
    d["average div"] = [[] for _ in range(len(d["months"]))]  # type: ignore[misc]
    d["average top %"] = [[] for _ in range(len(d["months"]))]  # type: ignore[misc]

    graph_data = pd.DataFrame(d)

    for pos, date in enumerate(df["date"]):
        month_string = f"{date.year}-{date.month}"
        curr_pos = d["months"].index(month_string)
        graph_data["average div"][curr_pos].append(df["div"][pos])
        graph_data["average top %"][curr_pos].append(
            (64 * (df["div"][pos] - 1) + df["qualificationrank"][pos]) / df["totalplayers"][pos]
        )

        # FIXME average top % broken.

    graph_data["months"] = graph_data["months"].astype(str)
    graph_data["average div"] = graph_data["average div"].apply(lambda x: sum(x) / len(x))
    graph_data["average top %"] = graph_data["average top %"].apply(lambda x: sum(x) / len(x))
    # df["top %"] = (64 * (df["div"] - 1) + df["qualificationrank"]) / df["totalplayers"]

    return graph_data


def generate_plot(data: pd.DataFrame, player_name: str) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.plot(data["months"], data["average div"], label="Avg Div")
    ax.plot(data["months"], data["average top %"], label="Avg top%")

    ax.set_title(f"COTD results {player_name}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Div/Top %")

    # FIXME figure out how to have less x axis ticks than there is data points

    ax.set_ylim([0, 50])  # TODO make this configurable

    loc = pltticker.MultipleLocator(base=2.0)  # TODO make this configurable
    ax.xaxis.set_major_locator(loc)

    ax.legend()

    return fig
