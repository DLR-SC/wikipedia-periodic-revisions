# Wikipedia Periodic Revisions

## Installation
Install manually by cloning and then running

``` 
pip install -e wikipedia_tools
```

or by running

``` 
pip install git+https://github.com/DLR-SC/wikipedia-periodic-revisions.git
```

## wikipedia_tools package

This packages is responsible for:
- fetching the wikipages revisions based on a period of time
- load them into parquet, and
- provide basic analysis

It contains three main subpackages and the *utils* package which contains few helpers functions:

### Scraper [[wikipedia_tools.scraper](wikipedia_tools/wikipedia_tools/scraper.py)]
This subpackage is responsible for downloading the wikipedia revisions from the web.

The code below shows how to download all the revisions of pages:
  - belonging to the *Climate_change* category.
  - revisions between start of 8 months ago (1.1.2022) and now (29.9.2022). The *get_last_month* function returns the datetime of the beginning of 8 months ago.
  
    ```python 
    from wikipedia_tools.utils import utils 
    utils.get_last_month(8)
    ```
  - if  save_each_page= True: each page is fetched and downloaded on the spot under the folder **data/periodic_wiki_batches/{*categories_names*}/from{month-year}_to{month-year}**. Otherwise, all the page revisions are fetched first and then saved into one jsonl file.
  


```python
from wikipedia_tools.scraper import downloader
from datetime import datetime

wikirevs= downloader.WikiPagesRevision( 
                                        categories = ["Climate_change"],
                                        revisions_from = utils.get_last_month(8),
                                        revisions_to=datetime.now(),
                                        save_each_page= True
                                        )
```


