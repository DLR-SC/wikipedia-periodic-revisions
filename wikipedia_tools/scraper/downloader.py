import dataclasses
from typing import ClassVar, List

from datetime import datetime
from functools import reduce
from tqdm import tqdm
import json
import os
import pandas as pd
import wikipedia_tools.scraper.category_extractor as ce
import wikipedia_tools.scraper.revision_extractor as re
from wikipedia_tools.utils import properties
from wikipedia_tools.utils import utils
import random


@dataclasses.dataclass
class WikiPagesRevision:
    output_file: str = "all"
    root_folder: str = properties.ROOT_PATH
    categories: List = dataclasses.field(default_factory=lambda: ["Climate_change"])
    revisions_from: datetime = None
    revisions_to: datetime = datetime.now()
    save_each_page: bool = False
    category_depth: int = 3
    out_version: str = "parquet"  # or jsonl
    page_limit: int = -1
    lang: str = "en"
    REVISIONS_FILE_POSTFIX: ClassVar = "revisions.{}"
    

    # categories_str:str = ""
    def __post_init__(self):
        utils.create_folder(properties.WIKI_SCRAPER_DEBUG_FOLDER)
        self.categories_str = (
            "-".join(self.categories)
            if self.categories is not None and len(self.categories) > 0
            else ""
        )

        if self.out_version not in ["parquet", "jsonl"]:
            self.out_version = "jsonl"
        WikiPagesRevision.REVISIONS_FILE_POSTFIX = (
            WikiPagesRevision.REVISIONS_FILE_POSTFIX.format(self.out_version)
        )

        self.pages = []
        self.pages = set(
            self.pages
            + reduce(
                list.__add__,
                [
                    ce.get_category_pages(c, self.category_depth)
                    for c in self.categories
                ],
            )
        )
        print(f"Fetching pages for the following categories: {self.categories}")

        if len(self.pages) == 0:
            raise Exception(
                "No pages to parse. Please specify a proper category or a file with page names."
            )

        if self.page_limit > 0:
            self.pages = random.sample(self.pages, self.page_limit)
            print(
                f"page limit is set to {self.page_limit}. Selecting {self.page_limit} random wikipedia pages"
            )

        self.period_str = ""
        if self.revisions_from is not None:
            self.period_str = f'{self.revisions_from.strftime("%d%b%Y")}'
            rev_to = (
                self.revisions_to if self.revisions_to is not None else datetime.now()
            )
            self.period_str = f'{self.period_str}-{rev_to.strftime("%d%b%Y")}'
        print(self._get_filename("test"))

        downloaded_pages = [
            p for p in self.pages if utils.file_exists(self._get_filename(p))
        ]
        self.pages = [
            p for p in self.pages if not utils.file_exists(self._get_filename(p))
        ]
        print(
            f"There are {len(downloaded_pages)} downloaded pages and {len(self.pages)} pages to download"
        )

    def download(self):
        failed_pages = []
        downloaded_pages = []

        print(f"parsing {len(self.pages)} pages")
        if self.save_each_page:
            out_folder = self._get_root_folder("")

            for page in tqdm(self.pages, leave=True):
                if utils.file_exists(self._get_filename(page)):
                    print(f"{page} already downloaded for this time period.")
                    continue

                pages_dict = re.process_page_revisions(
                    page, self.lang, self.revisions_from, self.revisions_to
                )

                for page_name, result in pages_dict.items():
                    page_revs, error, disambguities = result

                    if page_revs is None or len(page_revs) == 0:
                        failed_pages.append(page)
                        with open(
                            os.path.join(
                                properties.WIKI_SCRAPER_DEBUG_FOLDER,
                                f"{self.period_str}_failed.txt",
                            ),
                            "a+",
                            encoding="utf-8",
                        ) as f:
                            f.write(f"page_name:{page}, error:{error}\n")
                        continue

                    # no error
                    df = pd.DataFrame(page_revs)
                    if "page" not in df.columns.values:
                        print(
                            f"page is not part of the key for page {page}: {page_revs}"
                        )
                        continue
                    for page_, group in df.groupby("page"):
                        # save downlaoded page
                        downloaded_pages.append(page_)
                        with open(
                            os.path.join(
                                properties.WIKI_SCRAPER_DEBUG_FOLDER,
                                f"{self.period_str}_downloaded.txt",
                            ),
                            "a+",
                            encoding="utf-8",
                        ) as f:
                            f.write(f"{page_}\n")

                        # get file path for this page
                        file_path = self._get_filename(page_)
                        if self.out_version == "parquet":
                            pd.DataFrame(group).to_parquet(file_path, index=False)
                        else:
                            with open(file_path, "w", encoding="utf-8") as file:
                                file.write(json.dumps(group.to_json()))

        else:
            out_folder = self._get_filename()
            revisions_df = re.get_revisions_all_pages(
                self.pages, self.lang, self.revisions_from, self.revisions_to
            )
            with open(out_folder, "w", encoding="utf-8") as f:
                for r in revisions_df:
                    f.write(json.dumps(r) + "\n")

        print(
            f"downloaded {len(downloaded_pages)} page revisions out of {(len(failed_pages) + len(downloaded_pages))}"
        )
        return len(downloaded_pages), out_folder

    ###########################
    ######    HELPERS   #######
    ###########################
    def _get_filename(self, page: str = None):
        root = self._get_root_folder(page)

        file_name = os.path.join(
            root, f"{self.output_file}_{WikiPagesRevision.REVISIONS_FILE_POSTFIX}"
        )

        utils.create_folder(root)
        return file_name

    def _get_root_folder(self, page: str = None):
        self.output_file = (
            self.output_file if page is None else utils.get_alphanumeric(page)
        )

        root = properties.FOLDER_WIKI_BATCHES.format(self.root_folder, "periodic")
        root = (
            os.path.join(root, self.categories_str)
            if self.categories_str is not None
            else root
        )

        if self.revisions_from is not None:
            if page is not None:
                root = os.path.join(root, self.period_str)
            else:
                self.output_file = f"{self.period_str}_{self.output_file}"

        return root
