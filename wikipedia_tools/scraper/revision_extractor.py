import os
import traceback
from datetime import datetime

from wikipedia_tools.scraper.wikirevparser_with_time import ProcessRevisions

from wikipedia_w_time.exceptions import DisambiguationError
from functools import reduce
from tqdm import tqdm

from wikipedia_tools.utils import properties

start_collecting = False


def process_page_revisions(page_name, lang, rev_from: datetime = None, rev_to: datetime = None):
    res = None
    error = False
    disambiguity = {}
    data = None
    try:

        parser_instance = ProcessRevisions(lang, page_name, rev_from, rev_to)
        try:
            parser_instance.wikipedia_page()
        except DisambiguationError as e:
            print(f'..found disambiguity for page *{page_name}*, fetching  revisions for options: {e.options}')
            disambiguity[page_name] = e.options if page_name not in disambiguity.keys() else disambiguity[
                page_name].extend(e.options)
            dict_ = {}
            for p in e.options:
                print(f"Getting page {p}")
                if p != page_name:
                    dict_.update(process_page_revisions(p, lang, rev_from, rev_to))
            return dict_

        data = parser_instance.parse_revisions()
        if data is not None:
            res = [{**{'page': page_name, 'lang': lang, 'timestamp': item[0]}, **dict(item[1])}
                   for item in reversed(data.items())]
        else:
            print(f"No revisions were found for {page_name} for the chose period of time")
    except Exception as other_exc:
        error = True
        print(
            f"\t* An unknown exception occurred for page {page_name}: {other_exc.__repr__()}, {traceback.format_exc()}")
    return {page_name: (res, error, disambiguity)}


def get_revisions_all_pages(pages, lang, rev_from, rev_to):
    print('calling *get_revisions_all_pages* for each page')
    revs = []
    no_revs = []
    downloaded = []
    error_pages = []

    for page in tqdm(pages):
        dict_ = process_page_revisions(page, lang, rev_from, rev_to)
        for page_name, result in dict_.items():
            processed, error, disambiguities = result
            if processed is not None:
                revs.append(processed)
                downloaded.append(page)
            if error:
                error_pages.append(page)
            elif not error and processed is None:
                no_revs.append(page)
    print("End of *get_revisions_all_pages*.")
    _save_debug(downloaded, no_revs, error_pages, rev_from, rev_to)
    return revs


def _save_debug(downloaded, no_revs, error_pages, rev_from, rev_to):
    prefix = f"from{rev_from.strftime('%d-%m-%Y')}" \
             f"_{rev_to.strftime('%d-%m-%Y')}" \
        if rev_from is not None and rev_to is not None \
        else ""

    with open(os.path.join(properties.WIKI_SCRAPER_DEBUG_FOLDER, f"{prefix}_downloaded.txt"), "w") as f:
        f.write(f"{downloaded}\n")
    with open(os.path.join(properties.WIKI_SCRAPER_DEBUG_FOLDER, f"{prefix}_no_revs.txt"), "w") as f:
        f.write(f"{no_revs}\n")
    with open(os.path.join(properties.WIKI_SCRAPER_DEBUG_FOLDER, f"{prefix}_error_pages.txt"), "w") as f:
        f.write(f"{error_pages}\n")
