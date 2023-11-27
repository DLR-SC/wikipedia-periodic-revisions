
<h1 align="center">Welcome to the Wikipedia Periodic Revisions <code>(wikipedia_tools)</code> </h1>

<p align="center">
  <a href="https://github.com/DLR-SC/wikipedia-periodic-revisions/blob/master/LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-yellow.svg" target="_blank" />
  </a>
  <a href="https://img.shields.io/badge/Made%20with-Python-1f425f.svg">
    <img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg" alt="Badge: Made with Python"/>
  </a>
  <a href="https://pypi.org/project/wikipedia_tools/"><img src="https://badge.fury.io/py/wikipedia_tools.svg" alt="Badge: PyPI version" height="18"></a>
  <a href="https://twitter.com/dlr_software">
    <img alt="Twitter: DLR Software" src="https://img.shields.io/twitter/follow/dlr_software.svg?style=social" target="_blank" />
  </a>
  <a href="https://open.vscode.dev/DLR-SC/wikipedia_tools">
    <img alt="Badge: Open in VSCode" src="https://img.shields.io/static/v1?logo=visualstudiocode&label=&message=open%20in%20visual%20studio%20code&labelColor=2c2c32&color=007acc&logoColor=007acc" target="_blank" />
  </a>
  

  <a href="https://github.com/psf/black">
    <img alt="Badge: Open in VSCode" src="https://img.shields.io/badge/code%20style-black-000000.svg" target="_blank" />
  </a>
</p>

> `wikipedia_tools` is a Python Package to download wikipedia revisions for pages belonging to certain *categories*, based on a period of time. This package also provides overview stats for the downloaded data.

---

# CITE US

```

  @software{elbaff:2022-software,
            author = "{El Baff, Roxanne and Hecking, Tobias}",
            license = "{MIT}",
            month = "dec",
            title = "{{Wikipedia Revisions Downloader and Analyzer}}",
            url = "{https://github.com/DLR-SC/wikipedia-periodic-revisions}",
            version = "{2.4.1}",
            url = "https://github.com/DLR-SC/wikipedia-periodic-revisions",
            year = 2022
          }

```


## Dependencies and Credits

#### [Wikipedia API](https://github.com/goldsmith/Wikipedia)

This package is built on top of the [Wikipedia API](https://github.com/goldsmith/Wikipedia). This code was forked under the `base` subpackage. 

#### [ajoer/WikiRevParser](https://github.com/ajoer/WikiRevParser)

Also we forked the code from [ajoer/WikiRevParser](https://github.com/ajoer/WikiRevParser) and we modified it to support *from* and *to* datetime to fetch revisions between certain periods; the modified code is `wikipedia_toools.scraper.wikirevparser_with_time.py`. 

Note: No need to download these two projects, they are already integrated as part of this project.

## Installation

Via PIP

``` 
pip install wikipedia_tools
```

Or install manually by cloning and then running

``` 
pip install -e wikipedia_tools
```



## wikipedia_tools package

This packages is responsible for:
- fetching the wikipages revisions based on a period of time
- load them into parquet, and
- provide basic analysis

It contains three main subpackages and the *utils* package which contains few helpers functions:

### Downlaod Wiki Article Revisions [[wikipedia_tools.scraper](wikipedia_tools/wikipedia_tools/scraper.py)]
This subpackage is responsible for downloading the wikipedia revisions from the web.

The code below shows how to download all the revisions of pages:
  - belonging to the *Climate_change* category.
  - revisions between start of 8 months ago (1.1.2022) and now (29.9.2022). The *get_x_months_ago_date* function returns the datetime of the beginning of 8 months ago.
  
    ```python 
    from wikipedia_tools.utils import utils 
    utils.get_x_months_ago_date(8)
    ```
  - if  save_each_page= True: each page is fetched and downloaded on the spot under the folder **data/periodic_wiki_batches/{*categories_names*}/from{month-year}_to{month-year}**. Otherwise, all the page revisions are fetched first and then saved into one jsonl file.
  

```python
from wikipedia_tools.scraper import downloader
from datetime import datetime

wikirevs= downloader.WikiPagesRevision( 
                                        categories = ["Climate_change"],
                                        revisions_from = utils.get_x_months_ago_date(8),
                                        revisions_to=datetime.now(),
                                        save_each_page= True
                                        )

count, destination_folder = wikirevs.download()
```


For german wiki revisions, you can set the *lang* attribute to *de* - For example, you can download the German Wikipedia page revisions for the Climate_change category, as follows:

```python
from wikipedia_tools.scraper import downloader
from datetime import datetime

wikirevs= downloader.WikiPagesRevision( 
                                        categories = ["Klimaveränderung"],
                                        revisions_from = utils.get_x_months_ago_date(1), # beginning of last month, you can use instead datetime.now() + dateutil.relativedelta.relativedelta() to customize past datetime relatively
                                        revisions_to=datetime.now(),
                                        save_each_page= True,
                                        lang="de"
                                        )
count, destination_folder = wikirevs.download()

```

You can then process each file by, for example, reading the parquet file using pandas:

```python
import pandas as pd
from glob import glob
files = f"{destination_folder}/*.parquet"

# Loop over all wiki page revisions with this period and read each wiki page revs as a pandas dataframe
for page_path in glob(files):
    page_revs_df = pd.read_parquet(page_name)
    # dataframe with columns ['page', 'lang', 'timestamp', 'categories', 'content', 'images', 'links', 'sections', 'urls', 'user']
    # process/use file ....

```
### Overview Stats

```python

## Initialize the analyzer object

from wikipedia_tools.analyzer.revisions import WikipediaRevisionAnalyzer
analyzer = WikipediaRevisionAnalyzer(
    category = category,
    period = properties.PERIODS._YEARLY_,
    corpus = CORPUS,
    root = ROOT_PATH
)

# Get the yearly number of articles that were created/edit at least once 
unique_created_updated_articles = analyzer.get_edited_page_count(plot=True, save=True)

# Returned the number of created articles over time
unique_created_articles = analyzer.get_created_page_count(plot=True, save=True)

# Returns the number of revisions over time
rev_overtime_df = analyzer.get_revisions_over_time(save=True)

# Returns the number of words over time
words_overtime_df = analyzer.get_words_over_time(save=True)

# Returns the number of users over time, grouped by user type
users_overtime_df = analyzer.get_users_over_time(save=True)

# return the top n wikipedia articles over time
top_edited = analyzer.get_most_edited_articles(top=4)

# return the articles sorted from most to least edited over time
most_to_least_revised = analyzer.get_periodic_most_to_least_revised(save=True)

```

You can find the full example under the examples folder.
