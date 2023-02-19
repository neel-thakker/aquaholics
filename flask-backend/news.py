import requests
import os
import sys
from dotenv import load_dotenv

load_dotenv()

secret = os.getenv('SECRET_KEY')

def get_news(query):

    url = 'https://newsapi.org/v2/everything?'
    parameters = {
        'q': query, # query phrase
        'pageSize': 5,  # maximum is 100
        'apiKey': secret
    }

    response = requests.get(url, params = parameters)

    response_json = response.json()

    data = []
    for items in response_json['articles']:
        df = {
            'source': items['source']['name'],
            'tittle': items['title'],
            'publishedAt': items['publishedAt'],
            'content': items['content'][:-13],
            'url': items['url'],
            'urlToImg': items['urlToImage']
        }
        data.append(df)
    return data

if __name__ == "__main__":
    print(get_news(sys.argv[1]))