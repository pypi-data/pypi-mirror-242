__all__ = ("path", "headers", "API_URL")

import os
import pathlib

path = pathlib.Path(os.path.expanduser("~/documents")).absolute()
if not os.path.exists(path / "cotd_stats_visualiser_cache"):
    os.mkdir(path / "cotd_stats_visualiser_cache")
path /= "cotd_stats_visualiser_cache"

headers: dict[str, str] = {
    "User-Agent": "COTD Stats Visualiser / 0.0.1-alpha.1 A script that generates a visualisation of the COTD "
    "stats/results for certain players in a given time period. ("
    "https://github.com/EdVraz/COTDStatsVisualiser) / contact: @edvraz (discord)"
}

API_URL: str = "https://trackmania.io/api/"
