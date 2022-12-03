import pandas as pd

import wikipedia_tools.processor.loader as loader
import wikipedia_tools.utils.properties as prop
import wikipedia_tools.utils.utils as utils
import textmining_utility.lexicons as lexicons


## HELPERS

def _add_id(row):
    row['numeric_id'] = int(row['Filename'].split('_')[1].split('.')[0])
    return row

## END OF HELPERS


def extract_nrc_emotion_for_all_revisions(wiki_page_title, content_col='content', save = False):

    file_path = prop.FEATURE_NRC_PATH.format(utils.get_alphanumeric(wiki_page_title))

    if utils.file_exists(file_path):
        return pd.read_csv(file_path, index_col='numeric_id')

    print('file not saved, getting original data...')
    contents_df = loader.get_wiki_page(wiki_page_title)#ADD GET CONTENT HERE

    nrc_df = contents_df[[content_col]].copy()

    print('calculating lexicon cound for nrc...')
    nrc_df = lexicons.count_nrc_emotions_and_sentiments(nrc_df, text_column=content_col)

    if save:
        nrc_df.reset_index().to_csv(file_path, index=False)
    return nrc_df

def extract_nrc_emotion(df, content_cols, file_path = None):

    data_df = df[content_cols].copy()
    nrc_res_arr = []
    for col in content_cols:
        print('calculating lexicon count for nrc...')
        nrc_col_df = lexicons.count_nrc_emotions_and_sentiments(data_df, text_column=col, prefix='nrc_'+col+'_')
        nrc_res_arr.append(nrc_col_df)
    nrc_df = pd.concat(nrc_res_arr, axis=1, join="inner")
    if file_path is not None:
        nrc_df.reset_index().to_csv(file_path, index=False)
    return nrc_df

def extract_empath(wiki_page_title, content_col='content', file_path = None):

    file_path = prop.FEATURE_EMPATH_PATH.format(utils.get_alphanumeric(wiki_page_title))

    if utils.file_exists(file_path):
        return pd.read_csv(file_path, index_col='numeric_id')

    print('file not saved, getting original data...')
    contents_df = loader.get_wiki_page(wiki_page_title)#ADD GET CONTENT HERE

    empath_df = contents_df[[content_col]].copy()


    print('calculating lexicon count for empath...')
    empath_df = lexicons.count_empath(empath_df, text_column=content_col,prefix='empath_')
    empath_df.reset_index().to_csv(file_path, index=False)
    return empath_df



def extract_mpqa_arg(df, content_cols, file_path = None):
    file_path = prop.FEATURE_MPQA_ARG_PATH.format(file_path)

    if utils.file_exists(file_path):
        return pd.read_csv(file_path)

    data_df = df[content_cols].copy()
    mpqa_arg_arr = []
    for col in content_cols:
        print('calculating lexicon count for mpqa arg...')
        nrc_col_df = lexicons.count_mpqa_arg(data_df, text_column=col, prefix='mpqa_arg_'+col+'_')
        mpqa_arg_arr.append(nrc_col_df)
    mpqa_arg_df = pd.concat(mpqa_arg_arr, axis=1, join="inner")
    if file_path is not None:
        mpqa_arg_df.reset_index().to_csv(file_path, index=False)


    return mpqa_arg_df