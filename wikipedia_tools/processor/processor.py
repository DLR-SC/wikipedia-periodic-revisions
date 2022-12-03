import logging

import pandas as pd
import os

from glob import glob
from tqdm import tqdm

from wikipedia_tools.utils import properties, utils
from wikipedia_tools.processor import loader
from pathlib import Path


def get_wiki_popular_pages():
    wiki_popular_page_df = pd.read_csv(properties.WIKI_CLIMATE_CHANGE_POPULAR_PAGES)
    return wiki_popular_page_df[wiki_popular_page_df['Page title'].notna()]


def is_popular(title):
    popular_df = get_wiki_popular_pages()
    return len(popular_df[popular_df['Page title'] == title]) > 0


def is_important(title):
    popular_df = get_wiki_popular_pages()
    return popular_df[popular_df['Page title'] == title]['Importance'].values[
        0] if is_popular(title) else 'na'


def get_wiki_pages_overview(category="Climate_change"):
    """
    Processes all wikipages and generates 1 dataframe where each row represents 1 wikipage with info:
    page title, created on, last updated, initial content, latest content, edits numner, content edits count, unique users,
    is_popular (if it exists under Wikipedida Climate Change Project), is_important (if it is popular and flagged important by the wiki project)
    :return:
    """
    path = Path(properties.WIKI_OVERVIEW_CSV)
    if path.is_file():
        return pd.read_csv(properties.WIKI_OVERVIEW_CSV, )

    wiki_titles = loader.get_wikipedia_page_titles(categories=[category], corpus=properties.CORPUS)
    popular_pages_df = get_wiki_popular_pages()
    wiki_page_meta_arr = []

    print('there are {} wiki titles'.format(len(wiki_titles)))
    for title_code in tqdm(wiki_titles[category]):
        original_df = loader.get_wikipedia_page_data(title_code)

        if original_df is None:
            continue
        if len(original_df) == 0:
            print('{} has len 0'.format(title_code))
            continue
        _df = original_df.copy()

        wiki_page_meta = {}

        _df['timestamp_str'] = _df['timestamp']
        _df['timestamp'] = pd.to_datetime(_df['timestamp'], infer_datetime_format=True)
        _df = _df.sort_values(by="timestamp")

        init_content_df = _df[(~_df['content'].isna()) & (_df['content'] != '')].copy()
        init_content_df = init_content_df[init_content_df['timestamp'] == init_content_df['timestamp'].min()]
        if len(init_content_df) == 0:
            print('NO CONTENT: ', title_code)
            continue
        last_content = _df[_df['timestamp'] == _df['timestamp'].max()]['content'].values[0]
        edits_w_latest_content_df = (_df[(_df['content'] == last_content)])
        last_updated_df = edits_w_latest_content_df[
            edits_w_latest_content_df['timestamp'] == edits_w_latest_content_df['timestamp'].min()]

        wiki_page_meta['title_code'] = title_code
        wiki_page_meta['page_title'] = init_content_df['page'].values[0]
        wiki_page_meta['created_on'] = init_content_df['timestamp'].values[0]
        wiki_page_meta['init_content'] = init_content_df['content'].values[0]
        wiki_page_meta['last_updated'] = last_updated_df['timestamp'].values[0]
        wiki_page_meta['latest_content'] = last_updated_df['content'].values[0]
        wiki_page_meta['edits_number'] = (len(original_df['timestamp'].unique()))
        wiki_page_meta['content_edits_number'] = (
            len(_df.drop_duplicates(subset=['content'], keep='first', ignore_index=True)))
        wiki_page_meta['unique_users'] = len(original_df['user'].unique())

        wiki_page_meta['is_popular'] = is_popular(init_content_df['page'].values[0])
        wiki_page_meta['importance'] = popular_pages_df[popular_pages_df['Page title'] == title_code]['Importance'].values[
            0] if wiki_page_meta['is_popular'] else 'na'

        wiki_page_meta_arr.append(wiki_page_meta)

    meta_df = pd.DataFrame(wiki_page_meta_arr)
    meta_df.to_csv(properties.WIKI_OVERVIEW_CSV, index=False)
    return meta_df

#get_wiki_edits_num
def get_revision_count(only_popular=False, date_granularity=properties.DATE_MONTHLY, desc='MONTH-YEAR', category="Climate_change"):
    fname = properties.WIKI_EDITS_COUNT_CSV.format(('POPULAR' if only_popular else 'ALL'), desc)
    path = Path(fname)
    if path.is_file():
        return pd.read_csv(fname, index_col='abstracted_date')

    wiki_titles = loader.get_wikipedia_page_titles(categories=[category], corpus=properties.CORPUS)

    print('there are {} wiki titles'.format(len(wiki_titles)))

    result_df = pd.DataFrame()

    for title_code in tqdm(wiki_titles[category]):
        original_df = loader.get_wikipedia_page_data(title_code)
        title = original_df["page"].values[0]
        if (only_popular and not is_popular(title)) or (original_df is None) or len(original_df) == 0:
            continue

        _df = original_df.copy()

        _df['timestamp_str'] = _df['timestamp']
        _df['timestamp'] = pd.to_datetime(_df['timestamp'], infer_datetime_format=True)
        _df['abstracted_date'] = _df['timestamp'].dt.strftime(date_granularity)

        edits_count_df = _df['abstracted_date'].value_counts().to_frame(name='edits_count')
        edits_count_df.index.name = 'abstracted_date'
        result_df = pd.concat([result_df, edits_count_df]).groupby(['abstracted_date']).sum()

    result_df.reset_index().to_csv(fname, index=False)
    return result_df


#

def batch_wiki_edits_per_period(period=properties.DATE_MONTHLY, desc='monthly', category="Climate_change"):
    folder_root = properties.FOLDER_WIKI_BATCHES.format(desc)

    wiki_titles = loader.get_wikipedia_page_titles(categories=[category], corpus=properties.CORPUS)

    print('there are {} wiki titles'.format(len(wiki_titles)))

    for title_code in tqdm(wiki_titles[category]):
        original_df = loader.get_wikipedia_page_data(title_code)
        if (original_df is None) or len(original_df) == 0:
            continue
        _df = original_df.copy()

        _df['timestamp_str'] = _df['timestamp']
        _df['timestamp'] = pd.to_datetime(_df['timestamp'], infer_datetime_format=True)
        _df['abstracted_date'] = _df['timestamp'].dt.strftime(period)
        for period_val, period_df in _df.groupby('abstracted_date'):
            destination = f"{folder_root}/{period_val}/{title_code}.parquet"
            utils.create_folder(f"{folder_root}/{period_val}")
            period_df.to_parquet(destination, index=False)


# get_wiki_edits_per_period
def get_wikipedia_page_periodic_overview(only_popular=False, period=properties.DATE_YEAR, desc='YEAR', category="Climate_change"):
    fname = properties.WIKI_EDITS_PERIODIC_CSV.format(('POPULAR' if only_popular else 'ALL'), desc)
    path = Path(fname)
    if path.is_file():
        return pd.read_csv(fname)

    wiki_titles = loader.get_wikipedia_page_titles(categories=[category], corpus=properties.CORPUS)

    print('there are {} wiki titles'.format(len(wiki_titles)))

    result_arr = []
    for title_code in tqdm(wiki_titles[category]):
        original_df = loader.get_wikipedia_page_data(title_code)
        if (only_popular and not is_popular(original_df["page"].values[0])) or (original_df is None) or len(original_df) == 0:
            continue
        _df = original_df.copy()

        _df['timestamp_str'] = _df['timestamp']
        _df['timestamp'] = pd.to_datetime(_df['timestamp'], infer_datetime_format=True)
        _df['abstracted_date'] = _df['timestamp'].dt.strftime(period)

        for period_val, period_df in _df.groupby('abstracted_date'):
            latest_df = period_df[period_df['timestamp'] == period_df['timestamp'].max()]
            revision_per_period = {}
            revision_per_period['content'] = latest_df['content'].values[0]
            revision_per_period['title'] = latest_df['page'].values[0]
            revision_per_period['title_code'] = title_code
            revision_per_period['period'] = period_val
            revision_per_period['user_count'] = len(period_df['user'].unique())
            revision_per_period['users'] = period_df['user'].values.tolist()
            revision_per_period['revision_count'] = len(period_df)
            revision_per_period['timestamp'] = latest_df['timestamp'].values[0]
            revision_per_period['links'] = latest_df['links'].values[0]
            revision_per_period['categories'] = latest_df['categories'].values[0]
            revision_per_period['urls'] = latest_df['urls'].values[0]
            result_arr.append(revision_per_period)

    result_df = pd.DataFrame(result_arr)  # , index = ['period', 'title'])

    result_df.to_csv(fname, index=False)
    return result_df

