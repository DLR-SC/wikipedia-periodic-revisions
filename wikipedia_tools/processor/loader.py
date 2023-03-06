import logging

from wikipedia_tools.utils import properties
from wikipedia_tools.utils import utils
from pathlib import Path
from datetime import datetime

import pandas as pd
from glob import glob
import os


def get_wikipedia_page_titles(
    categories: list = ["Climate_change"], corpus: str = properties.CORPUS
):
    wikipedia_pages_df = {}

    for category in categories:
        try:
            all_unique_pages = [
                Path(x).name.replace(".parquet", "")
                for x in glob(os.path.join(corpus, category, "*", "*.parquet"))
            ]
            all_unique_pages = list(set(all_unique_pages))

            wikipedia_pages_df[category] = all_unique_pages
            logging.info(
                f"There are {len(all_unique_pages)} wikipedia pages for the category {category}"
            )
        except:
            logging.error(
                f"Make sure that the corpus parquet files are located here {os.path.join(corpus, category)}"
            )
    return wikipedia_pages_df


def get_wikipedia_page_data(
    wikipedia_page: str,
    category: str = "Climate_change",
    corpus: str = properties.CORPUS,
) -> pd.DataFrame:
    def to_tuple(arr):
        return tuple(map(tuple, arr))

    paths = glob(
        os.path.join(corpus, category, "*", f"{wikipedia_page}.parquet")
    )
    data_df: pd.DataFrame = None
    _all_data_lst = []
    for path in paths:
        _df = pd.read_parquet(path)

        _df["categories"] = _df["categories"].apply(tuple)
        _df["images"] = _df["images"].apply(tuple)
        _df["links"] = _df["links"].apply(tuple)
        _df["urls"] = _df["urls"].apply(tuple)
        _df["sections"] = _df["sections"].apply(to_tuple)

        _all_data_lst.append(_df)

    if len(_all_data_lst) == 1:
        data_df = _all_data_lst[0]
    elif len(_all_data_lst) > 1:
        data_df = pd.concat(_all_data_lst)
        data_df.drop_duplicates(keep="first", inplace=True)

    return data_df
