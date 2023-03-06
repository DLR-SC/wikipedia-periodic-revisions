from mediawiki import MediaWiki
from functools import reduce

MAX_PAGES = 1000  # this is the max

def get_category_pages(category, lang="en", depth=3):
    wikipedia = MediaWiki(lang=lang)
    pages, subcategories = wikipedia.categorymembers(category, MAX_PAGES)
    if (depth == 0) or (len(subcategories) == 0):
        return pages
    else:
        return pages + reduce(
            list.__add__,
            [get_category_pages(c,lang, depth - 1) for c in subcategories],
        )
