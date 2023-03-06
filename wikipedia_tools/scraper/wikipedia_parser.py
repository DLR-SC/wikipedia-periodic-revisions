import argparse
import wikipedia_tools.scraper.revision_extractor as re
import wikipedia_tools.scraper.category_extractor as ce
import json
from functools import reduce

REVISIONS_FILE_POSTFIX = "_revisions.jsonl"


def read_pages_file(pages_file):
    with open(pages_file) as f:
        lines = f.readlines()

    return lines


def main():
    parser = argparse.ArgumentParser(
        prog="Wikipedia Parser",
        description="Parser to extract Wikipedia discourse.",
    )

    parser.add_argument(
        "-c", "--categories", type=str, nargs="*", help="Categories to parse."
    )

    parser.add_argument(
        "-p",
        "--pages_file",
        type=str,
        help="File with a list of pages to parse. One page per line.",
    )

    parser.add_argument(
        "-o",
        "--outfile_prefix",
        type=str,
        required=True,
        help="Prefix for output files.",
    )

    parser.add_argument(
        "-g",
        action="store_true",
        help="Flag indicating if a revision and pagelink graph should be extracted",
    )

    parser.add_argument(
        "-l",
        "--language",
        type=str,
        required=False,
        default="en",
        help="Wikipedia language, default en.",
    )

    args = parser.parse_args()

    if args.pages_file:
        pages = read_pages_file(args.pages_file)
    else:
        pages = []

    if args.categories:
        pages = set(
            pages
            + reduce(
                list.__add__,
                [ce.get_category_pages(c) for c in args.categories],
            )
        )

    if len(pages) == 0:
        raise Exception(
            "No pages to parse. Please specify a proper category or a file with page names."
        )
    else:
        print("parsing " + str(len(pages)) + "...")
        revisions_df = re.get_revisions_all_pages(pages, args.lang)

        with open(args.outfile_prefix + REVISIONS_FILE_POSTFIX, "w") as f:
            for r in revisions_df:
                f.write(json.dumps(r) + "\n")


if __name__ == "__main__":
    main()
