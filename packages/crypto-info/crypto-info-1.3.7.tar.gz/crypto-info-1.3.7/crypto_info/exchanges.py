# exchanges.py

import os
import json
from typing import Iterable
from pathlib import Path

from attrs import define

import requests

from represent import represent

from pycoingecko import CoinGeckoAPI

from crypto_info.base import assets, source

__all__ = [
    "raw_exchanges",
    "Exchange",
    "load_exchanges",
    "save_exchanges_logos",
    "extract_exchanges_data",
    "load_exchanges_data",
    "get_exchanges_logos",
    "save_exchanges_data",
    "COINS_LOGOS_LOCATION"
]

coin_gecko_api = CoinGeckoAPI()

@define(repr=False, unsafe_hash=True)
@represent
class Exchange:
    """A class to represent exchange data."""

    id: str
    name: str
    url: str
    logo: str
    trust: int
    country: str
    establishment_year: int
    description: str | None = None
# end Exchange

ExchangesData = dict[str, dict[str, str | int | None]]

raw_exchanges: ExchangesData = {}

DATA_LOCATION = f"{source()}/data"
COINS_LOGOS_LOCATION = f"{assets()}/logos/exchanges"

def load_exchanges_data(
        exchanges: Iterable[str] | None = None,
        reload: bool | None = False,
        location: str | None = None
) -> ExchangesData:
    """
    Loads the exchanges from the api.

    :param exchanges: The names of the exchanges to include.
    :param reload: The value to reload the data.
    :param location: The saving location.

    :return: The exchange objects.
    """

    if location is None:
        data_location = DATA_LOCATION

    else:
        data_location = location
    # end if

    data_path = f"{data_location}/exchanges.json"

    if os.path.exists(data_path) and not raw_exchanges:
        with open(data_path, "r") as file:
            raw_exchanges.update(json.load(file))
        # end open
    # end if

    if reload or (not raw_exchanges):
        data = coin_gecko_api.get_exchanges_list()

        for exchange in data:
            if exchange["description"] is not None:
                exchange["description"] = (
                    exchange["description"].
                    replace("\n", " ").
                    replace("\r", "").
                    replace("  ", " ")
                ) or None
            # end if

            exchange["establishment_year"] = exchange["year_established"]
            exchange.pop("year_established")
            exchange.pop("trust_score_rank")
            exchange["trust"] = exchange["trust_score"]
            exchange.pop("trust_score")
            exchange["logo"] = exchange["image"]
            exchange.pop("image")
            exchange.pop("has_trading_incentive")
            exchange.pop("trade_volume_24h_btc")
            exchange.pop("trade_volume_24h_btc_normalized")
        # end for

        raw_exchanges.update(
            {exchange["id"]: exchange for exchange in data}
        )

        save_exchanges_data(data=raw_exchanges)
        save_exchanges_logos(data=raw_exchanges)
    # end if

    data = json.loads(json.dumps(raw_exchanges))

    if exchanges is not None:
        data = {
            key: exchange for key, exchange in data.items()
            if key.lower() in exchanges
        }
    # end if

    return data
# end load_exchanges_data

def load_exchanges(
        data: ExchangesData | None = None,
        exchanges: Iterable[str] | None = None,
        reload: bool | None = False
) -> dict[str, Exchange]:
    """
    Loads the exchanges from the api.

    :param data: The raw exchanges data.
    :param exchanges: The names of the exchanges to include.
    :param reload: The value to reload the data.

    :return: The exchange objects.
    """

    if data is None:
        data = load_exchanges_data(exchanges=exchanges, reload=reload)
    # end if

    return {key: Exchange(**exchange) for key, exchange in data.items()}
# end load_exchanges

def save_exchanges_logos(
        data: ExchangesData | None = None,
        location: str | None = None
) -> dict[str, str]:
    """
    Saves the logos of the exchanges.

    :param data: The exchanges' data.
    :param location: The saving location.

    :return: The paths to the logos of the exchanges.
    """

    if data is None:
        data = load_exchanges_data()
    # end if

    exchanges = load_exchanges(data=data)

    if location is None:
        location = f"{assets()}/logos/exchanges"
    # end if

    os.makedirs(location, exist_ok=True)

    os.makedirs(location, exist_ok=True)

    paths: dict[str, str] = {}

    for exchange in exchanges.values():
        path = f"{location}/{exchange.id}.jpg"

        if os.path.exists(path):
            continue
        # end if

        with open(path, "wb") as file:
            file.write(requests.get(exchange.logo).content)
        # end open

        paths[exchange.id] = path
    # end for

    return paths
# end save_exchanges_logos

def save_exchanges_data(
        data: ExchangesData | None = None,
        location: str | None = None
) -> str:
    """
    Saves the logos of the exchanges.

    :param data: The exchanges' data.
    :param location: The saving location.

    :return: The paths to the logos of the exchanges.
    """

    if data is None:
        data = load_exchanges_data()
    # end if

    if location is None:
        location = DATA_LOCATION
    # end if

    os.makedirs(location, exist_ok=True)

    path = f"{location}/exchanges.json"

    with open(path, "w") as file:
        json.dump(data, file, indent=4)
    # end open

    return path
# end save_exchanges_data

def extract_exchanges_data(
        exchanges: Iterable[Exchange] | dict[str, Exchange]
) -> ExchangesData:
    """
    Extracts the data from the exchanges.

    :param exchanges: The coins to extract.

    :return: The extracted data of the coins.
    """

    if not isinstance(exchanges, dict):
        exchanges = {exchange.id: exchange for exchange in exchanges}
    # end if

    return {
        key: exchange.__dict__.copy()
        for key, exchange in exchanges.items()
    }
# end extract_coins_data

def get_exchanges_logos(
        exchanges: Iterable[str] | None = None,
        location: str | None = None
) -> dict[str, str]:
    """
    Returns the path to the logo files for each exchange.

    :param exchanges: The exchanges to search.
    :param location: The saving location.

    :return: The exchanges and their logos.
    """

    if exchanges is None:
        exchanges = load_exchanges_data().keys()
    # end if

    if location is None:
        location = COINS_LOGOS_LOCATION
    # end if

    return {
        exchange: (
            str(path)
            if (path := Path(f"{location}/{exchange}.jpg")).exists() else
            raw_exchanges[exchange]["logo"]
        )
        for exchange in exchanges
    }
# end get_exchanges_logos