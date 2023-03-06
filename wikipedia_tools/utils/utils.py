import dateutil
import pathlib
import os
from IPy import IP
from datetime import datetime


def create_folder(folder_path):
    pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)


def file_exists(file_path):
    return os.path.isfile(file_path)


def get_alphanumeric(wiki_page_title):
    return (
        "".join(c for c in wiki_page_title if (c.isalnum() or c == " "))
        .lower()
        .replace(" ", "-")
    )


def is_ip(s):
    valid = True
    try:
        IP(s)
 
    except:
        valid = False
    return valid


def get_x_months_ago_date(decreased_month=0):
    now = datetime.now()
    last_month = now.replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    last_month = dateutil.relativedelta.relativedelta(months=-decreased_month)
    print(last_month.strftime("%Y-%m-%dT%H:%M:%SZ"))
    return last_month
