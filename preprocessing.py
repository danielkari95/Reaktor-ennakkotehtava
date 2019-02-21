""""Loads the data using WorldBank API and preprocesses data to desired format."""

import pandas as pd

from pandas_datareader import wb

def load_data(countries='all', start=1990, end=2015):
    df = wb.download(indicator=['NY.GDP.MKTP.KD', 'EN.ATM.CO2E.KT'], country=countries, start=start, end=end)
    
    df = df.reset_index()
    df.columns = ['country', 'year', 'gdp_2010', 'co2_emissions_kt']
    df = df.sort_values(by=['country','year'])
    
    pct_compared_to_year1 = lambda x: x.div(x.iloc[0]).mul(100)
    
    df['co2_vs_year1_percent'] = df.groupby(['country'])['co2_emissions_kt'].apply(pct_compared_to_year1)
    df['gdp_vs_year1_percent'] = df.groupby(['country'])['gdp_2010'].apply(pct_compared_to_year1)

    df['year'] = df['year'].apply(pd.to_numeric, errors ='coerce')

    return df

