from pathlib import Path

from setuptools import find_packages, setup  # type: ignore[import]

extras_require = {"GUI": ["imgui[full]"]}
requirements = [
    "matplotlib",
    "orjson",
    "pandas",
    "ratelimiter",
    "requests",
    "setuptools>=61.0",
]

setup(
    name="cotd-stats-visualiser",
    description="A script that generates a visualisation of the Trackmania COTD stats for a given player.",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    author="EdVraz",
    author_email="edvraz12@gmail.com",
    url="https://github.com/EdVraz/COTDStatsVisualiser",
    version="0.0.1-alpha.1",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=requirements,  # FIXME go back to automatic reading later
    license="LICENSE"
    # extras_require=extras_require,
)
