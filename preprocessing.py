import pandas as pd
import xlrd
import os

from pandas_datareader import wb

os.chdir("C:/Users/danie/Documents/Jupyter/Reaktor")

temperatures = pd.read_excel("data/Temperatures.xls")
temperatures.columns = ['avg_temp', 'year', 'month', 'country', 'ISO3', 'ISO2']

countries = list(set(temperatures['country'])) # We only need the data for the countries in the temperatures file 
years = list(range(1991, 2015))
all_countries = wb.get_countries()[['name', 'iso3c']] # These are needed to merge the emissions and GDP data with temperatures data

df = wb.download(indicator=['NY.GDP.MKTP.KD', 'EN.ATM.CO2E.KT'], country=countries, start=1991, end=2014)
df = df.reset_index()
df.columns = ['country', 'year', 'gdp_2010', 'co2_emissions_kt']

temperatures = pd.DataFrame(temperatures.groupby(['country', 'year'])['avg_temp'].mean())
temperatures = temperatures.reset_index()
temperatures = temperatures[temperatures['year'].isin(years)]

pct_compared_to_beginning = lambda x: x.div(x.iloc[-1]).mul(100)

df['co2_vs_1991'] = df.groupby(['country'])['co2_emissions_kt'].apply(pct_compared_to_beginning)
df['gdp_vs_1991'] = df.groupby(['country'])['gdp_2010'].apply(pct_compared_to_beginning)

df['year'] = df['year'].apply(pd.to_numeric, errors ='coerce')

df = df.merge(all_countries, left_on=['country'], right_on=['name']) # Merge to get country codes
df = df.merge(temperatures, left_on=['iso3c', 'year'], right_on=['country', 'year'])

df = df.drop(['name', 'country_y'], axis=1) # Drop unnecessary duplicate columns
df.columns = ['country', 'year', 'gdp_2010', 'co2_emissions_kt', 'co2_vs_1991', 'gdp_vs_1991', 'iso_code', 'avg_temp']