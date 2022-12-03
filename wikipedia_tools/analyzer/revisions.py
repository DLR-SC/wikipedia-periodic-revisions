import dataclasses

import pandas as pd

from wikipedia_tools.wikipedia_tools.processor import processor
from wikipedia_tools.utils import properties


@dataclasses.dataclass
class WikipediaRevisionAnalyzer:
    categories : list
    revisions_from : str = "01.01.2001"
    revisions_to : 'str|None' = None
    corpus: str = properties.CORPUS
    download:bool = False

    def __post_init__(self):
        self.wikipages_revisions:pd.DataFrame = self.load_data()



    def get_edited_pages_count(self, period_type:str=""):
        wikipedia_pages_per_category = processor.get_wikipedia_page_titles(categories = self.categories, corpus = self.corpus)
        return

    def get_revisions_count(self):
        return

    def get_revisions_per_user_type_count(self):
        return

    def get_edited_pages_per_user_type_count(self):
        return

    def get_user_type_count(self):
        return