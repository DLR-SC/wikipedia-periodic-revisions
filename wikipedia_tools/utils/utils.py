import dateutil
import pathlib
import os
from IPy import IP
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib


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
    last_month = last_month + dateutil.relativedelta.relativedelta(
        months=-decreased_month
    )
    print(last_month.strftime("%Y-%m-%dT%H:%M:%SZ"))
    return last_month


# Helpers
def barplot(
    x, y, data, xlabel="Year", ylabel="Count", hue=None, title="", dodge=True
):
    sns.set(font_scale=1)
    plt.style.use("fivethirtyeight")
    palette = (
        [sns.color_palette("PuBuGn_d")[0], sns.color_palette("PuBuGn_d")[-3]]
        if hue
        else [sns.color_palette("PuBuGn_d")[0]]
    )
    fig, axes = plt.subplots(figsize=(7, 5))
    sns.barplot(
        x=x,
        y=y,
        data=data,
        palette=palette,  # sns.color_palette("PuBuGn_d"),#["#9ecae1", "#cccccc"],
        hue=hue,
        dodge=dodge
        # palette=('Blues_d' if hue is not None else None)
    )
    plt.title(title, fontsize=14)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)

    for label in axes.xaxis.get_ticklabels():
        label.set_rotation(60)

    axes.yaxis.set_major_formatter(
        matplotlib.ticker.StrMethodFormatter("{x:,.0f}")
    )

    plt.show()
