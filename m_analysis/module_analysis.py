import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot(df):
    print('6.- Ploting charts')
    df.plot(kind='scatter',x='position',y='worth_busd',color='green')
    fig1 = plt.gcf()
    plt.draw()
    fig1.savefig('./data/processed/images/position_worthbusd.png', dpi=100)
    plt.close()


    df.plot(kind='scatter',x='GDP $ per capita',y='worth_busd',color='green')
    fig2 = plt.gcf()
    plt.draw()
    fig2.savefig('data/processed/images/worthbusd_GDP.png', dpi=100)
    plt.close()


    df.plot(kind='scatter',x='phones per 1000',y='worth_busd',color='green')
    fig3 = plt.gcf()
    plt.draw()
    fig3.savefig('data/processed/images/worthbusd_phones.png', dpi=100)
    plt.close()


    a = df.groupby('Region')['Country'].nunique()
    a.sort_values(inplace=True,ascending=True)
    a.plot(kind='barh',x='Region',y='Country',color='green')
    fig4 = plt.gcf()
    plt.draw()
    fig4.savefig('data/processed/images/region_numcountries.png',bbox_inches = "tight")
    plt.close()


    c = df.groupby('sector')['corp.'].nunique()
    c.sort_values(inplace=True, ascending=True)
    c.plot(kind='barh',color='green')
    fig5 = plt.gcf()
    plt.draw()
    fig5.savefig('data/processed/images/sector_numcorps.png', bbox_inches = "tight")
    plt.close()


    c = df.groupby('sector')['Country'].nunique()
    c.sort_values(inplace=True, ascending=True)
    c.plot(kind='barh',color='green')
    fig6 = plt.gcf()
    plt.draw()
    fig6.savefig('data/processed/images/sector_numcountries.png',bbox_inches = "tight")
    plt.close()



    x = df.groupby('sector')['area sq. mi.'].agg([np.sum])
    x.sort_values(by=['sum'],inplace=True, ascending=True)
    x.plot(kind='barh',color='green')
    fig7 = plt.gcf()
    plt.draw()
    fig7 = fig7.savefig('data/processed/images/sector_area.png',bbox_inches = "tight")
    plt.close()