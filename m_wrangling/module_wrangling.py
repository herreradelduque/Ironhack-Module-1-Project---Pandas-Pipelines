import numpy as np

import pandas as pd
import matplotlib.pyplot as plt

def wrangling(df):

    print('5.- Starting data wrangling')

    ### Drop all columns but 'country', 'name', 'lastName','wealthSource'

    df_forbes_kag = pd.read_csv('./data/raw/forbes_2018.csv')

    df_forbes_kag.drop(['position','industry','worth','worthChange','realTimeWorth','realTimePosition','image','wealthSource','lastName'], axis=1, inplace=True)

    ### Import the cleaned csv (and drop column 'unnamed0' with index_col=0)

    forbes_df = pd.read_csv('./data/processed/forbes_df.csv',index_col=0)


    forbes_df.drop(['id','image','country','age_years','gender'], axis=1, inplace=True)


    forbes_df = pd.merge(forbes_df,df_forbes_kag, on='name',sort=True)


    ### Identify one space after some strings in 'Country' column of df_countries

    df_countries = pd.read_csv('./data/raw/countries of the world.csv', delimiter=",", decimal=",")


    forbes_df.rename(columns={'country':'Country'}, inplace=True)


    cols_forbes = forbes_df.columns.tolist()


    cols = ['position', 'name', 'gender', 'sector', 'corp.', 'worth_busd', 'age','Country']

    forbes_df = forbes_df[cols]

    df_countries['Region'] = df_countries['Region'].map(lambda x: x.strip())

    df_countries['Country'] = df_countries['Country'].map(lambda x: x.strip())

    forbes_df['Country'] = forbes_df['Country'].map(lambda x: x.strip())


    df_forbes_country = pd.merge(forbes_df,df_countries, on='Country',sort=True)

    df_forbes_country.sort_values(['position'], axis=0, ascending=True, inplace=True)


    df_forbes_country['gender'].replace(to_replace='M', value='Male',inplace=True)
    df_forbes_country['gender'].replace(to_replace='F', value='Female',inplace=True)


    df_forbes_country.drop(['Coastline (coast/area ratio)','Infant mortality (per 1000 births)','Literacy (%)','Climate','Birthrate','Deathrate','Arable (%)','Crops (%)','Other (%)','Agriculture','Industry','Service'],axis=1,inplace=True)

    df_forbes_country.rename(columns={'Area (sq. mi.)':'area sq. mi.','Pop. Density (per sq. mi.)':'pop. density per sq. mi.','GDP ($ per capita)':'GDP $ per capita','Phones (per 1000)':'phones per 1000'}, inplace=True)

    return df_forbes_country