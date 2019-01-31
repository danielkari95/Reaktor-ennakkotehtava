import pandas as pd
import xlrd

emissions = pd.read_csv("data/C02 emissions.csv", header = 2)
gdp = pd.read_csv("data/GDP.csv", header = 2)
temperatures = pd.read_excel("data/Temperatures.xls")

filter_out = lambda df, column, values: df[df[column].isin(values)]

years = map(str, list(range(1960, 2016)))  

temperatures.columns = ['Average temperature', 'Year', 'Month', 'Country', 'ISO3', 'ISO2']
countries = set(temperatures['Country'])

def preprocess(df):
    df = df.melt(id_vars=['Country Name', 'Country Code'], value_vars=years, 
                           var_name='Year', value_name=df['Indicator Name'][0])
    df['Year'] = df['Year'].apply(pd.to_numeric, errors ='coerce')
    df = filter_out(df, 'Country Code', countries)
    df = filter_out(df, 'Year', years)
    return df

preprocess(emissions)
preprocess(gdp)

temperatures = pd.DataFrame(temperatures.groupby(['Country', 'Year'])['Average temperature'].mean())
temperatures = temperatures.reset_index()
temperatures = filter_out(temperatures, 'Year', years)
