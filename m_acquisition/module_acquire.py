import pandas as pd
import numpy as np
import kaggle

from sqlalchemy import create_engine




sqlitedb_path = './data/raw/herreradelduque.db'
engine = create_engine(f'sqlite:///{sqlitedb_path}')

pd.read_sql_query("SELECT * FROM sqlite_master WHERE type='table'", engine)


path = './data/raw/herreradelduque.db'


def acquisition(path):
    print('1.- Starting data acquisition')
    rank_info = pd.read_sql_query("SELECT * FROM rank_info", engine)
    personal_info = pd.read_sql_query("SELECT * FROM personal_info", engine)
    business_info = pd.read_sql_query("SELECT * FROM business_info", engine)

    ### Drop columns and rows

    business_info.drop(['realTimeWorth'], axis=1, inplace=True)

    rank_info.drop(['Unnamed: 0'], axis=1, inplace=True)

    personal_info.drop(['Unnamed: 0'], axis=1, inplace=True)

    rank_info.dropna(inplace=True)

    ### Fill null values

    personal_info['age'].fillna(0, inplace=True)
    personal_info['gender'].fillna(0, inplace=True)

    ### String columns to title format:

    rank_info['name'] = rank_info['name'].str.title()
    personal_info['lastName'] = personal_info['lastName'].str.title()
    personal_info['country'] = personal_info['country'].str.title()
    personal_info['gender'] = personal_info['gender'].str.title()

    business_info['Source'] = business_info['Source'].str.title()

    ### Split columns:

    business_info_temp = business_info['Source'].str.split(' ==> ', n=1, expand=True)

    business_info['sector'] = business_info_temp[0]
    business_info['corp.'] = business_info_temp[1]

    business_info.drop(['Source'], axis=1, inplace=True)

    business_info_temp = business_info['worthChange'].str.split(' ', n=1, expand=True)

    business_info['worth_change_musd'] = business_info_temp[0]
    business_info['worth_to_drop'] = business_info_temp[1]

    business_info.drop(['worth_to_drop'], axis=1, inplace=True)
    business_info.drop(['worthChange'], axis=1, inplace=True)

    business_info_temp = business_info['worth'].str.split(' ', n=1, expand=True)

    business_info['worth_busd'] = business_info_temp[0]
    business_info['worth_to_drop'] = business_info_temp[1]

    business_info.drop(['worth_to_drop'], axis=1, inplace=True)
    business_info.drop(['worth'], axis=1, inplace=True)

    personal_info_temp = personal_info['age'].str.split(' ', n=1, expand=True)

    personal_info['age_years'] = personal_info_temp[0]
    personal_info['age_to_drop'] = personal_info_temp[1]

    personal_info.drop(['age'], axis=1, inplace=True)
    personal_info.drop(['age_to_drop'], axis=1, inplace=True)

    ### Rename columns to lowercase:

    business_info.rename(columns={'realTimePosition': 'real_time_position'}, inplace=True)

    business_info.drop(['real_time_position'], axis=1, inplace=True)

    ### DataFrame adjust "astype()"

    rank_info = rank_info.astype({'position': int})

    business_info = business_info.astype({'worth_change_musd': float}, {'worth_busd': float})

    ### DataFrame replace values:

    personal_info['gender'].replace(to_replace='M', value='Male', inplace=True)
    personal_info['gender'].replace(to_replace='F', value='Female', inplace=True)

    personal_info['age_years'].replace(to_replace='nan', value=-9999, inplace=True)

    personal_info['age_years'].fillna(-9999, inplace=True)
    personal_info['gender'].fillna('none', inplace=True)

    ### ...dataFrame adjust "astype()"
    personal_info = personal_info.astype({'age_years': int})

    ### Year replacing by age:
    personal_info.loc[personal_info['age_years'] > 125, 'age_years'] = 2018 - personal_info['age_years']

    ### We need to merge the 3 dataframes in order to make our job eassyer:

    forbes_df_intermediate_merge = pd.merge(rank_info, personal_info, on='id', how='outer')

    forbes_df = pd.merge(forbes_df_intermediate_merge, business_info, on='id', how='outer')

    ''' ...in our new dataframe we can identify some duplicated information as: 'name' <->'lastName' 
    ... so that, let's remove it!'''

    forbes_df.drop(['lastName'], axis=1, inplace=True)

    forbes_df.drop(['worth_change_musd'], axis=1, inplace=True)

    cols = forbes_df.columns.tolist()

    cols = ['id', 'position', 'name', 'age_years', 'gender', 'country', 'sector', 'corp.', 'worth_busd', 'image']
    forbes_df = forbes_df[cols]

    forbes_df = forbes_df.sort_values('position', ascending=True)

    (forbes_df['country'] == 'None').sum()

    ### Standarized 'Gender' to Male/Female

    forbes_df.replace(to_replace='M', value='Male', inplace=True)
    forbes_df.replace(to_replace='F', value='Female', inplace=True)

    return forbes_df


### API Kaggle datasets download (autentication requierd):

def api_kaggle():
    print('3.- Calling API Kaggle')
    ### API Kaggle datasets download (autentication requierd):

    kaggle.api.authenticate()

    kaggle.api.dataset_download_files('fernandol/countries-of-the-world', path='./data/raw/', unzip=True)

    kaggle.api.dataset_download_files('soubenz/forbes-top-billionaires-list-2018', path='./data/raw/', unzip=True)

    print('4.- Datasets saved')


def save_table(df,file_name):

    df.to_csv('./data/processed/{}.csv'.format(file_name))
    print('2.- Data saved')