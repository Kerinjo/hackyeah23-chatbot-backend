import requests
import pandas as pd
from searchterm import Searchterm
from fuzzywuzzy import process


def get_url(searchterm:str):
    url = f'https://api.dane.gov.pl/resources/?title[phrase]={searchterm}&format[terms]=csv'
    return url


# api dane gov pl datasets
def get_searches(searchterm):
    url = get_url(searchterm)
    res = requests.get(url)
    json = res.json()
    data = json['data']
    return data


def choose_resource(query):
    searchterm = Searchterm(query).text
    data = get_searches(searchterm)

    titles = list(map(lambda d: d['attributes']['title'], data))
    
    match = process.extractOne(searchterm, titles)
    print(f"Match: {match[0]}, Confidence: {match[1]}")
    idx = titles.index(match[0])

    resource = data[idx]['attributes']
    df = pd.read_csv(resource['link'])
    print(df)


def choose_colums(query):
    pass


def plot_df(df):
    pass


if __name__ == '__main__':
    get_searches('Jakie są podatki?')