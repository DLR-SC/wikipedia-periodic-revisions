# Files and folders paths)
import os
ROOT_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..')
CORPUS = os.path.join("V:", os.sep, "InsightsNet", "Corpora", "Wikipedia", "wikipedia_dump")
WIKI_PAGES =os.path.join(ROOT_PATH,  "data", "wiki_pages")
OUT= os.path.join( ROOT_PATH , "data", "generated")



STATS_FOLDER = os.path.join(ROOT_PATH,  "data",  "stats")

WIKI_TITLES_PATH = os.path.join(  ROOT_PATH , "data", "docs", "wiki_pages_titles.txt")
WIKI_CLIMATE_CHANGE_POPULAR_PAGES = os.path.join( ROOT_PATH , "data", "docs", "wikipedia_wikiproject_climate_change_popular_pages.csv")
WIKI_MULTI_PAGES = os.path.join(  ROOT_PATH , "data", "docs", "multi_pages.txt")

WIKI_OVERVIEW_CSV = os.path.join( OUT ,  "wiki_pages_overview.csv")
WIKI_EDITS_COUNT_CSV= os.path.join( OUT ,  "wiki_pages_edit_number_{}_{}.csv")
WIKI_EDITS_PERIODIC_CSV= os.path.join( OUT ,  "wiki_pages_edit_{}_{}.csv")
FOLDER_WIKI_BATCHES= os.path.join(  "data" ,  "processed_{}_wiki_batches")

WIKI_SCRAPER_DEBUG_FOLDER= os.path.join( ROOT_PATH, "data" ,  "debug")

# Extracted features)
EXTRACTED_FEATURES_PATH = os.path.join( OUT  ,  "extracted_features", "")
FIG_PATH = os.path.join( ROOT_PATH , "data", "figures", "")

FEATURE_LIWC_PATH = os.path.join( OUT  ,  "extracted_features", "liwc_{}.csv")
RAW_LIWC_PATH = os.path.join( OUT  ,  "extracted_features", "debateorg_arguments_txt", "liwc_{}.csv")

FEATURE_NRC_PATH = os.path.join( OUT  ,  "extracted_features", "nrc_{}.csv")
FEATURE_MPQA_ARG_PATH = os.path.join( OUT  ,  "extracted_features", "mpqa_arg_{}.csv")
FEATURE_EMPATH_PATH = os.path.join( OUT  ,  "extracted_features", "empath_{}.csv")
FEATURE_POLITENESS_PATH = os.path.join( OUT  ,  "extracted_features", "politeness_{}.csv")

# CONSTANTS
DATE_MONTHLY = "%m-%Y"
DATE_YEAR = "%Y"