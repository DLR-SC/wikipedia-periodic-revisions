# Inisights Net - Wiki

## Installation
```python 
pip install Wikipedia
pip install -e wikipedia_tools
```

## wikipedia_tools package

This packages is responsible for:
- fetching the wikipages revisions based on a period of time
- load them into proper formats, and
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


### Processor [[wikipedia_tools.processor ](wikipedia_tools/wikipedia_tools/processor )]

###### [[wikipedia_tools.processor.loader ](wikipedia_tools/wikipedia_tools/processor/loader.py )]
- Overview: this is used to load the Wikipedia Climate Change jsonl (corpus) file and save each wiki page as a jsonl. Each line in the main jsonl contains all the revisions of 1 wiki pages except pages with id 189, 1537 and 1589 (check file [multi_pages.txt](data/docs/multi_pages.txt) or see notes below)
- The 'run' method process X number of wiki pages from the corpus and saves each as jsonl file per wiki page. (These files are already uploaded to 'V:\InsightsNet\Corpora\Wikipedia\wiki_pages\wiki_pages_edits')
- **get_wiki_page(wiki_page_title)**: loads 1 wiki page into pandas dataframe where each row represents a revision
- **get_wiki_titles()**: returns a list of the wikipedia titles in the corpus - All the wiki titles are saved here: [wiki_titles.txt](data/docs/wiki_titles.txt)

###### [[wikipedia_tools.processor.processor ](wikipedia_tools/wikipedia_tools/processor/processor.py )]
- **get_wiki_pages_overview()**: loops over all the wikipedia pages in the corpus and gets general overview for each wiki page. In case the data is already processed, it loads it from [wiki_pages_overview.csv](data/docs/wiki_pages_overview.csv).
    - The returned dataframe has the following columns: created on, initial content, last updated, latest content, edits number (total), content edits number, unique users, unique users who changed the content, is popular and importance. 
    - the popularity and importance are defined based on the Wikipedia Project Climate Change popular pages (saved here: [wikipedia_wikiproject_climate_change_popular_pages.csv](data/docs/wikipedia_wikiproject_climate_change_popular_pages.csv))


### Analyzer [[wikipedia_tools.analyzer ](wikipedia_tools/wikipedia_tools/analyzer )]
Conducts feature extraction and analysis on the wikipedia pages revisions.

### [Notebooks](wikipedia_tools/wikipedia_tools/notebooks)
The notebooks demonstrates the usage of these packages


