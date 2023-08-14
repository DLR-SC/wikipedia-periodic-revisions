# Files and folders paths)
import os


class _CONSTANTS_:
    ROOT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..")
    CORPUS = os.path.join(
        "V:", os.sep, "InsightsNet", "Corpora", "Wikipedia", "wikipedia_dump"
    )
    WIKI_PAGES = os.path.join(ROOT_PATH, "data", "wiki_pages")
    OUT = os.path.join(ROOT_PATH, "data", "generated")

    STATS_FOLDER = os.path.join(ROOT_PATH, "data", "stats")

    WIKI_CLIMATE_CHANGE_POPULAR_PAGES = os.path.join(
        "data", "wikipedia_wikiproject_climate_change_popular_pages.csv"
    )

    WIKI_OVERVIEW_CSV = os.path.join(OUT, "wiki_pages_overview.csv")
    WIKI_EDITS_COUNT_CSV = os.path.join(
        OUT, "wiki_pages_edit_number_{}_{}.csv"
    )
    WIKI_EDITS_PERIODIC_CSV = os.path.join(OUT, "wiki_pages_edit_{}_{}.csv")
    FOLDER_WIKI_BATCHES = os.path.join("{}", "data", "{}_wiki_batches")

    WIKI_SCRAPER_DEBUG_FOLDER = os.path.join(ROOT_PATH, "data", "debug")

    # Extracted features)
    EXTRACTED_FEATURES_PATH = os.path.join(OUT, "extracted_features", "")
    FIG_PATH = os.path.join(ROOT_PATH, "data", "figures", "")

    FEATURE_LIWC_PATH = os.path.join(OUT, "extracted_features", "liwc_{}.csv")
    RAW_LIWC_PATH = os.path.join(
        OUT, "extracted_features", "debateorg_arguments_txt", "liwc_{}.csv"
    )

    FEATURE_NRC_PATH = os.path.join(OUT, "extracted_features", "nrc_{}.csv")
    FEATURE_MPQA_ARG_PATH = os.path.join(
        OUT, "extracted_features", "mpqa_arg_{}.csv"
    )
    FEATURE_EMPATH_PATH = os.path.join(
        OUT, "extracted_features", "empath_{}.csv"
    )
    FEATURE_POLITENESS_PATH = os.path.join(
        OUT, "extracted_features", "politeness_{}.csv"
    )

    def __init__(self, ROOT_PATH=ROOT_PATH, CORPUS=CORPUS):
        _CONSTANTS_.ROOT_PATH = ROOT_PATH
        _CONSTANTS_.CORPUS = CORPUS
        _CONSTANTS_.WIKI_PAGES = os.path.join(ROOT_PATH, "data", "wiki_pages")
        _CONSTANTS_.OUT = os.path.join(ROOT_PATH, "data", "generated")

        _CONSTANTS_.STATS_FOLDER = os.path.join(ROOT_PATH, "data", "stats")

        _CONSTANTS_.WIKI_CLIMATE_CHANGE_POPULAR_PAGES = os.path.join(
            "data", "wikipedia_wikiproject_climate_change_popular_pages.csv"
        )

        _CONSTANTS_.WIKI_OVERVIEW_CSV = os.path.join(
            _CONSTANTS_.OUT, "wiki_pages_overview.csv"
        )
        _CONSTANTS_.WIKI_EDITS_COUNT_CSV = os.path.join(
            _CONSTANTS_.OUT, "wiki_pages_edit_number_{}_{}.csv"
        )
        _CONSTANTS_.WIKI_EDITS_PERIODIC_CSV = os.path.join(
            _CONSTANTS_.OUT, "wiki_pages_edit_{}_{}.csv"
        )
        _CONSTANTS_.FOLDER_WIKI_BATCHES = os.path.join(
            "{}", "data", "{}_wiki_batches"
        )

        _CONSTANTS_.WIKI_SCRAPER_DEBUG_FOLDER = os.path.join(
            ROOT_PATH, "data", "debug"
        )

        # Extracted features)
        _CONSTANTS_.EXTRACTED_FEATURES_PATH = os.path.join(
            _CONSTANTS_.OUT, "extracted_features", ""
        )
        _CONSTANTS_.FIG_PATH = os.path.join(ROOT_PATH, "data", "figures", "")

        _CONSTANTS_.FEATURE_LIWC_PATH = os.path.join(
            _CONSTANTS_.OUT, "extracted_features", "liwc_{}.csv"
        )
        _CONSTANTS_.RAW_LIWC_PATH = os.path.join(
            _CONSTANTS_.OUT,
            "extracted_features",
            "debateorg_arguments_txt",
            "liwc_{}.csv",
        )

        _CONSTANTS_.FEATURE_NRC_PATH = os.path.join(
            _CONSTANTS_.OUT, "extracted_features", "nrc_{}.csv"
        )
        _CONSTANTS_.FEATURE_MPQA_ARG_PATH = os.path.join(
            _CONSTANTS_.OUT, "extracted_features", "mpqa_arg_{}.csv"
        )
        _CONSTANTS_.FEATURE_EMPATH_PATH = os.path.join(
            _CONSTANTS_.OUT, "extracted_features", "empath_{}.csv"
        )
        _CONSTANTS_.FEATURE_POLITENESS_PATH = os.path.join(
            _CONSTANTS_.OUT, "extracted_features", "politeness_{}.csv"
        )


# CONSTANTS
DATE_MONTHLY = "%m-%Y"
DATE_YEAR = "%Y"


class PERIODS:
    _YEARLY_ = {"format": DATE_YEAR, "description": "YEAR"}
    _MONTHLY_ = {"format": DATE_MONTHLY, "description": "MONTH"}


# FOR BACKWARD COMPATIBILITY
ROOT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..")
CORPUS = os.path.join(
    "V:", os.sep, "InsightsNet", "Corpora", "Wikipedia", "wikipedia_dump"
)
WIKI_PAGES = os.path.join(ROOT_PATH, "data", "wiki_pages")
OUT = os.path.join(ROOT_PATH, "data", "generated")

STATS_FOLDER = os.path.join(ROOT_PATH, "data", "stats")

WIKI_CLIMATE_CHANGE_POPULAR_PAGES = os.path.join(
    "data", "wikipedia_wikiproject_climate_change_popular_pages.csv"
)

WIKI_OVERVIEW_CSV = os.path.join(OUT, "wiki_pages_overview.csv")
WIKI_EDITS_COUNT_CSV = os.path.join(OUT, "wiki_pages_edit_number_{}_{}.csv")
WIKI_EDITS_PERIODIC_CSV = os.path.join(OUT, "wiki_pages_edit_{}_{}.csv")
FOLDER_WIKI_BATCHES = os.path.join("{}", "data", "{}_wiki_batches")

WIKI_SCRAPER_DEBUG_FOLDER = os.path.join(ROOT_PATH, "data", "debug")

# Extracted features)
EXTRACTED_FEATURES_PATH = os.path.join(OUT, "extracted_features", "")
FIG_PATH = os.path.join(ROOT_PATH, "data", "figures", "")

FEATURE_LIWC_PATH = os.path.join(OUT, "extracted_features", "liwc_{}.csv")
RAW_LIWC_PATH = os.path.join(
    OUT, "extracted_features", "debateorg_arguments_txt", "liwc_{}.csv"
)

FEATURE_NRC_PATH = os.path.join(OUT, "extracted_features", "nrc_{}.csv")
FEATURE_MPQA_ARG_PATH = os.path.join(
    OUT, "extracted_features", "mpqa_arg_{}.csv"
)
FEATURE_EMPATH_PATH = os.path.join(OUT, "extracted_features", "empath_{}.csv")
FEATURE_POLITENESS_PATH = os.path.join(
    OUT, "extracted_features", "politeness_{}.csv"
)
