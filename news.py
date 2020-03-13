import requests

def get_news_info(api_key):

    payload = {'country': 'us', 'apiKey': api_key}

    url = requests.get("http://newsapi.org/v2/top-headlines", params=payload)
    open_page = url.json() 
  
    articles = open_page["articles"]
    article_list = []
      
    for article in articles:

        article_dict = {'source': article["source"],
                        'title': article["title"],
                        'description': article["description"],
                        'url': article["url"],
                        'url_img': article["urlToImage"],
                        'publication_date': article["publishedAt"]}
          
        article_list.append(article_dict)

    return article_list