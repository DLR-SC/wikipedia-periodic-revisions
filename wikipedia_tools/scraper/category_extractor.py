from mediawiki import MediaWiki
from functools import reduce

MAX_PAGES = 1000  # this is the max

wikipedia = MediaWiki()


def get_category_pages(category, depth=3):
    pages, subcategories = wikipedia.categorymembers(category, MAX_PAGES)
    if (depth == 0) or (len(subcategories) == 0):
        return pages
    else:
        return pages + reduce(
            list.__add__,
            [get_category_pages(c, depth - 1) for c in subcategories],
        )
